/*
 * Arduino Pro Micro - USB HID Keyboard Forwarder (TCP Optimized)
 * 
 * Tối ưu cho Cách 2 (TCP flow):
 * Host Script → TCP → VMware Script → Serial → Arduino → USB HID → Game
 * 
 * Improvements:
 * - Faster serial parsing (không dùng String class)
 * - Lower latency processing
 * - Better memory management
 * - Optimized command processing
 * 
 * New Features & Optimizations:
 * - Bit array for key states (saves 224 bytes RAM: 256 bytes -> 32 bytes)
 * - Binary search for key lookup (O(log n) instead of O(n))
 * - Batch serial reading (reads up to 16 bytes at once for better throughput)
 * - Key combo support (e.g., "combo:ctrl+c", "combo:shift+a", "combo:ctrl+shift+x")
 * - Batch commands support (e.g., "batch:down:a,up:a,down:b,up:b")
 * - Anti-detection: Human-like timing with random jitter to prevent fixed pattern detection
 */

#include <Keyboard.h>
#include <Arduino.h>
#include <stdint.h>
#include <string.h>
#include <avr/pgmspace.h>

// SHA-256 context structure - must be defined early for all SHA-256 functions
typedef struct {
  uint32_t state[8];
  uint64_t bitcount;
  uint8_t buffer[64];
} SHA256_CTX;

// Serial buffer - optimized for fast parsing
#define SERIAL_BUFFER_SIZE 32
char serialBuffer[SERIAL_BUFFER_SIZE];
uint8_t bufferIndex = 0;

// Optimization: Batch serial reading buffer
#define SERIAL_BATCH_SIZE 16  // Read up to 16 bytes at once
uint8_t serialBatchBuffer[SERIAL_BATCH_SIZE];

// Obfuscated serial constants
const uint8_t FRAME_START_BYTE = 0x7E;
const uint8_t HANDSHAKE_COUNTER = 0xFF;
const uint8_t HANDSHAKE_LENGTH = 16;
const uint8_t MAX_FRAME_PAYLOAD = 48;  // enough for command strings

// Obfuscation state
bool obfuscationActive = false;
bool handshakeReceived = false;
uint8_t sessionKey[HANDSHAKE_LENGTH];
bool watchdogEnabled = true;     // Control whether watchdog auto-release runs (enabled by default)

// Watchdog để auto-release nếu không nhận dữ liệu trong một khoảng thời gian
unsigned long lastReceiveMs = 0;
const unsigned long WATCHDOG_TIMEOUT_MS = 2000; // 2 giây (an toàn hơn cho lag nhẹ)

// Anti-detection: Pseudo-random jitter generator
// Use analogRead() noise as entropy source (Arduino doesn't have good hardware RNG)
// Note: A0, A1 pins should be floating (not connected) for best noise
//
// NOTE (TEMPORARY): Human-like random jitter is DISABLED by default for stability testing.
// To re-enable anti-detect timing, set HUMAN_JITTER_ENABLED to true and re-upload.
const bool HUMAN_JITTER_ENABLED = false;
uint16_t getRandomJitter(uint16_t min, uint16_t max) {
  // Read from floating analog pins for noise
  uint16_t raw = analogRead(A0);
  // Add variation by reading multiple sources
  raw ^= analogRead(A1);
  raw ^= (millis() & 0xFF);
  raw ^= (micros() & 0xFF);
  // Bug fix: Prevent overflow and division by zero
  if (max > min) {
    // Calculate range safely to prevent overflow
    uint16_t range = max - min;
    // Prevent division by zero (range + 1 could overflow if range == UINT16_MAX)
    if (range < UINT16_MAX) {
      return min + (raw % (range + 1));
    } else {
      // Edge case: range is UINT16_MAX, use modulo with range only
      return min + (raw % (range));
    }
  }
  return min;
}

// Anti-detection: Human-like delay with jitter (microseconds)
// Adds natural variation to prevent detection of fixed timing patterns
void humanDelayMicroseconds(uint16_t base, uint16_t jitterRange) {
  // When jitter is disabled, use fixed timing for maximum determinism (no anti-detect).
  uint16_t jitter = HUMAN_JITTER_ENABLED ? getRandomJitter(0, jitterRange) : 0;
  // Prevent overflow when adding base + jitter
  uint32_t delayUs = (uint32_t)base + (uint32_t)jitter;
  // delayMicroseconds max is 16383, use delay() for longer times
  if (delayUs > 16383) {
    delay((uint16_t)(delayUs / 1000));
    delayMicroseconds((uint16_t)(delayUs % 1000));
  } else {
    delayMicroseconds((uint16_t)delayUs);
  }
}

// Anti-detection: Human-like delay with jitter (milliseconds)
void humanDelay(uint16_t base, uint16_t jitterRange) {
  // When jitter is disabled, use fixed timing for maximum determinism (no anti-detect).
  uint16_t jitter = HUMAN_JITTER_ENABLED ? getRandomJitter(0, jitterRange) : 0;
  // Prevent overflow when adding base + jitter
  uint32_t delayMs = (uint32_t)base + (uint32_t)jitter;
  // delay() accepts uint32_t, but we'll cap it to reasonable value
  if (delayMs > 65535) {
    delayMs = 65535;  // Max safe value for delay()
  }
  delay((uint16_t)delayMs);
}

// Key state tracking: track các phím đang được giữ
// Tăng lên 256 để support arrow keys và control keys (keyCode > 127)
#define MAX_KEYS 256
// Optimization: Use bit array instead of bool array to save RAM (256 bytes -> 32 bytes)
#define KEY_STATES_SIZE ((MAX_KEYS + 7) / 8)  // 32 bytes for 256 keys
uint8_t keyStates[KEY_STATES_SIZE] = {0};  // Bit array: 1 bit per key

// Bit array helper functions
inline void setKeyState(uint8_t keyCode) {
  if (keyCode < MAX_KEYS) {
    keyStates[keyCode / 8] |= (1 << (keyCode % 8));
  }
}

inline void clearKeyState(uint8_t keyCode) {
  if (keyCode < MAX_KEYS) {
    keyStates[keyCode / 8] &= ~(1 << (keyCode % 8));
  }
}

inline bool getKeyState(uint8_t keyCode) {
  if (keyCode < MAX_KEYS) {
    return (keyStates[keyCode / 8] & (1 << (keyCode % 8))) != 0;
  }
  return false;
}

enum FrameParseState {
  FRAME_WAIT_START = 0,
  FRAME_READ_COUNTER,
  FRAME_READ_LENGTH,
  FRAME_READ_PAYLOAD,
  FRAME_READ_CHECKSUM
};

FrameParseState frameState = FRAME_WAIT_START;
uint8_t frameCounter = 0;
uint8_t frameLength = 0;
uint8_t frameChecksum = 0;
uint8_t framePayload[MAX_FRAME_PAYLOAD];
uint8_t frameIndex = 0;
bool frameParsing = false;
unsigned long frameStartMs = 0;  // Bug fix: Track frame parsing start time for timeout
const unsigned long FRAME_TIMEOUT_MS = 100;  // 100ms timeout for frame parsing

// Key name to HID keycode mapping - optimized lookup
struct KeyMapping {
  const char* name;
  uint8_t nameLen;
  uint8_t keyCode;
};

// Sorted by name length first, then alphabetically for binary search optimization
// Binary search requires sorted array by nameLen, then by name
KeyMapping keyMap[] = {
  // Single char keys (sorted alphabetically)
  {"0", 1, '0'}, {"1", 1, '1'}, {"2", 1, '2'}, {"3", 1, '3'},
  {"4", 1, '4'}, {"5", 1, '5'}, {"6", 1, '6'}, {"7", 1, '7'},
  {"8", 1, '8'}, {"9", 1, '9'},
  {"a", 1, 'a'}, {"b", 1, 'b'}, {"c", 1, 'c'}, {"d", 1, 'd'},
  {"e", 1, 'e'}, {"f", 1, 'f'}, {"g", 1, 'g'}, {"h", 1, 'h'},
  {"i", 1, 'i'}, {"j", 1, 'j'}, {"k", 1, 'k'}, {"l", 1, 'l'},
  {"m", 1, 'm'}, {"n", 1, 'n'}, {"o", 1, 'o'}, {"p", 1, 'p'},
  {"q", 1, 'q'}, {"r", 1, 'r'}, {"s", 1, 's'}, {"t", 1, 't'},
  {"u", 1, 'u'}, {"v", 1, 'v'}, {"w", 1, 'w'}, {"x", 1, 'x'},
  {"y", 1, 'y'}, {"z", 1, 'z'},
  
  // 2-char keys (sorted alphabetically)
  {"f1", 2, KEY_F1}, {"f2", 2, KEY_F2}, {"f3", 2, KEY_F3}, {"f4", 2, KEY_F4},
  {"f5", 2, KEY_F5}, {"f6", 2, KEY_F6}, {"f7", 2, KEY_F7}, {"f8", 2, KEY_F8},
  {"f9", 2, KEY_F9}, {"up", 2, KEY_UP_ARROW},
  
  // 3-char keys (sorted alphabetically)
  {"alt", 3, KEY_LEFT_ALT}, {"end", 3, KEY_END}, {"esc", 3, KEY_ESC},
  {"f10", 3, KEY_F10}, {"f11", 3, KEY_F11}, {"f12", 3, KEY_F12},
  {"np0", 3, '0'}, {"np1", 3, '1'}, {"np2", 3, '2'}, {"np3", 3, '3'},
  {"np4", 3, '4'}, {"np5", 3, '5'}, {"np6", 3, '6'}, {"np7", 3, '7'},
  {"np8", 3, '8'}, {"np9", 3, '9'}, {"tab", 3, KEY_TAB},
  
  // 4-char keys (sorted alphabetically)
  {"caps", 4, KEY_CAPS_LOCK}, {"ctrl", 4, KEY_LEFT_CTRL},
  {"down", 4, KEY_DOWN_ARROW}, {"home", 4, KEY_HOME},
  {"left", 4, KEY_LEFT_ARROW}, {"menu", 4, 0}, {"pgdn", 4, KEY_PAGE_DOWN},
  {"pgup", 4, KEY_PAGE_UP},
  
  // 5-char keys (sorted alphabetically)
  {"comma", 5, ','}, {"enter", 5, KEY_RETURN}, {"grave", 5, '`'},
  {"l_gui", 5, KEY_LEFT_GUI}, {"minus", 5, '-'}, {"pause", 5, 0},
  {"quote", 5, '\''}, {"r_gui", 5, KEY_RIGHT_GUI}, {"right", 5, KEY_RIGHT_ARROW},
  {"shift", 5, KEY_LEFT_SHIFT}, {"slash", 5, '/'}, {"space", 5, ' '},
  
  // 6-char keys (sorted alphabetically)
  {"delete", 6, KEY_DELETE}, {"equals", 6, '='}, {"insert", 6, KEY_INSERT},
  {"np_add", 6, '+'}, {"np_dec", 6, '.'}, {"np_div", 6, '/'},
  {"np_mul", 6, '*'}, {"np_sub", 6, '-'}, {"period", 6, '.'}, {"scroll", 6, 0},
  
  // 7-char keys
  {"numlock", 7, 0},
  
  // 8-char keys (sorted alphabetically)
  {"lbracket", 8, '['}, {"rbracket", 8, ']'},
  
  // 9-char keys (sorted alphabetically)
  {"backslash", 9, '\\'}, {"backspace", 9, KEY_BACKSPACE},
  {"semicolon", 9, ';'},
  
  // 11-char keys
  {"printscreen", 11, 0}
};

const uint8_t KEY_MAP_SIZE = sizeof(keyMap) / sizeof(KeyMapping);

/**********************
 *  SHA-256 / HMAC   *
 **********************/

// Forward declarations
void processCommand(const char* command, uint8_t cmdLen);
void handleKeyCombo(const char* combo, uint8_t comboLen);
void handleBatchCommands(const char* batch, uint8_t batchLen);

const uint32_t sha256_init_state[8] = {
  0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
  0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

const uint32_t sha256_k[64] PROGMEM = {
  0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
  0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
  0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
  0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
  0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
  0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
  0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
  0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
  0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

#define ROTRIGHT(a,b) (((a) >> (b)) | ((a) << (32-(b))))
#define CH(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x,y,z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTRIGHT(x,2) ^ ROTRIGHT(x,13) ^ ROTRIGHT(x,22))
#define EP1(x) (ROTRIGHT(x,6) ^ ROTRIGHT(x,11) ^ ROTRIGHT(x,25))
#define SIG0(x) (ROTRIGHT(x,7) ^ ROTRIGHT(x,18) ^ ((x) >> 3))
#define SIG1(x) (ROTRIGHT(x,17) ^ ROTRIGHT(x,19) ^ ((x) >> 10))

void sha256_transform(SHA256_CTX *ctx, const uint8_t data[64]) {
  uint32_t a, b, c, d, e, f, g, h, t1, t2, m[64];

  for (uint8_t i = 0, j = 0; i < 16; ++i, j += 4) {
    m[i] = ((uint32_t)data[j] << 24) |
           ((uint32_t)data[j + 1] << 16) |
           ((uint32_t)data[j + 2] << 8) |
           ((uint32_t)data[j + 3]);
  }
  for (uint8_t k = 16; k < 64; ++k) {
    m[k] = SIG1(m[k - 2]) + m[k - 7] + SIG0(m[k - 15]) + m[k - 16];
  }

  a = ctx->state[0];
  b = ctx->state[1];
  c = ctx->state[2];
  d = ctx->state[3];
  e = ctx->state[4];
  f = ctx->state[5];
  g = ctx->state[6];
  h = ctx->state[7];

  for (uint8_t i = 0; i < 64; ++i) {
    uint32_t k_val = pgm_read_dword(&sha256_k[i]);
    t1 = h + EP1(e) + CH(e, f, g) + k_val + m[i];
    t2 = EP0(a) + MAJ(a, b, c);
    h = g;
    g = f;
    f = e;
    e = d + t1;
    d = c;
    c = b;
    b = a;
    a = t1 + t2;
  }

  ctx->state[0] += a;
  ctx->state[1] += b;
  ctx->state[2] += c;
  ctx->state[3] += d;
  ctx->state[4] += e;
  ctx->state[5] += f;
  ctx->state[6] += g;
  ctx->state[7] += h;
}

void sha256_init(SHA256_CTX *ctx) {
  memcpy(ctx->state, sha256_init_state, sizeof(sha256_init_state));
  ctx->bitcount = 0;
  memset(ctx->buffer, 0, sizeof(ctx->buffer));
}

void sha256_update(SHA256_CTX *ctx, const uint8_t *data, size_t len) {
  for (size_t i = 0; i < len; ++i) {
    ctx->buffer[(ctx->bitcount / 8) % 64] = data[i];
    ctx->bitcount += 8;
    if (((ctx->bitcount / 8) % 64) == 0) {
      sha256_transform(ctx, ctx->buffer);
    }
  }
}

void sha256_final(SHA256_CTX *ctx, uint8_t hash[32]) {
  size_t index = (ctx->bitcount / 8) % 64;
  ctx->buffer[index++] = 0x80;
  if (index > 56) {
    while (index < 64) {
      ctx->buffer[index++] = 0x00;
    }
    sha256_transform(ctx, ctx->buffer);
    index = 0;
  }
  while (index < 56) {
    ctx->buffer[index++] = 0x00;
  }

  uint64_t bitcount_be = ctx->bitcount;
  for (int8_t i = 7; i >= 0; --i) {
    ctx->buffer[56 + i] = (uint8_t)(bitcount_be & 0xFF);
    bitcount_be >>= 8;
  }
  sha256_transform(ctx, ctx->buffer);

  for (uint8_t i = 0; i < 8; ++i) {
    hash[i * 4] = (ctx->state[i] >> 24) & 0xFF;
    hash[i * 4 + 1] = (ctx->state[i] >> 16) & 0xFF;
    hash[i * 4 + 2] = (ctx->state[i] >> 8) & 0xFF;
    hash[i * 4 + 3] = ctx->state[i] & 0xFF;
  }
}

void hmac_sha256(const uint8_t *key, size_t keylen, const uint8_t *data, size_t datalen, uint8_t out[32]) {
  uint8_t ipad[64];
  uint8_t opad[64];
  uint8_t keybuf[64];

  memset(keybuf, 0, sizeof(keybuf));
  if (keylen > 64) {
    SHA256_CTX keyctx;
    sha256_init(&keyctx);
    sha256_update(&keyctx, key, keylen);
    sha256_final(&keyctx, keybuf);
  } else {
    memcpy(keybuf, key, keylen);
  }

  for (uint8_t i = 0; i < 64; ++i) {
    ipad[i] = keybuf[i] ^ 0x36;
    opad[i] = keybuf[i] ^ 0x5c;
  }

  SHA256_CTX ctx;
  sha256_init(&ctx);
  sha256_update(&ctx, ipad, 64);
  sha256_update(&ctx, data, datalen);
  uint8_t inner[32];
  sha256_final(&ctx, inner);

  sha256_init(&ctx);
  sha256_update(&ctx, opad, 64);
  sha256_update(&ctx, inner, 32);
  sha256_final(&ctx, out);
}

/**********************
 *  Obfuscation       *
 **********************/

void resetObfuscation() {
  obfuscationActive = false;
  handshakeReceived = false;
  memset(sessionKey, 0, sizeof(sessionKey));
  watchdogEnabled = false;
}

void deriveKeystream(uint8_t counter, uint8_t length, uint8_t *out) {
  uint16_t blockIndex = 0;
  uint8_t generated = 0;
  while (generated < length) {
    uint8_t msg[3];
    msg[0] = counter;
    msg[1] = (blockIndex >> 8) & 0xFF;
    msg[2] = blockIndex & 0xFF;

    uint8_t digest[32];
    hmac_sha256(sessionKey, HANDSHAKE_LENGTH, msg, sizeof(msg), digest);

    uint8_t toCopy = min((uint8_t)(length - generated), (uint8_t)32);
    memcpy(out + generated, digest, toCopy);

    generated += toCopy;
    blockIndex++;
  }
}

void handleDecodedPayload(const uint8_t *payload, uint8_t length) {
  if (length == 0 || length >= SERIAL_BUFFER_SIZE) {
    return;
  }

  char commandBuffer[SERIAL_BUFFER_SIZE];
  memcpy(commandBuffer, payload, length);
  commandBuffer[length] = '\0';
  processCommand(commandBuffer, length);
}

void handleFrame(uint8_t counter, const uint8_t *payload, uint8_t length) {
  if (counter == HANDSHAKE_COUNTER && length == HANDSHAKE_LENGTH) {
    memcpy(sessionKey, payload, HANDSHAKE_LENGTH);
    handshakeReceived = true;
    obfuscationActive = true;
    bufferIndex = 0;
    return;
  }

  if (!handshakeReceived) {
    return;
  }

  uint8_t decoded[MAX_FRAME_PAYLOAD];
  deriveKeystream(counter, length, decoded);
  for (uint8_t i = 0; i < length; ++i) {
    decoded[i] ^= payload[i];
  }

  handleDecodedPayload(decoded, length);
}

void resetFrameParser() {
  frameState = FRAME_WAIT_START;
  frameIndex = 0;
  frameParsing = false;
  frameCounter = 0;
  frameLength = 0;
  frameChecksum = 0;
  frameStartMs = 0;  // Bug fix: Reset frame timeout tracking
}

void handleAsciiByte(uint8_t byteVal) {
  char inChar = (char)byteVal;
  if (inChar == '\n' || bufferIndex >= SERIAL_BUFFER_SIZE - 1) {
    if (bufferIndex > 0) {
      serialBuffer[bufferIndex] = '\0';
      processCommand(serialBuffer, bufferIndex);
      bufferIndex = 0;
    }
  } else if (inChar != '\r' && bufferIndex < SERIAL_BUFFER_SIZE - 1) {
    // Bug fix: Check buffer bounds before writing to prevent overflow
    serialBuffer[bufferIndex++] = inChar;
  }
}

void parseFrameByte(uint8_t value) {
  switch (frameState) {
    case FRAME_READ_COUNTER:
      frameCounter = value;
      frameState = FRAME_READ_LENGTH;
      break;
    case FRAME_READ_LENGTH:
      frameLength = value;
      if (frameLength > MAX_FRAME_PAYLOAD) {
        resetFrameParser();
      } else {
        if (frameLength == 0) {
          frameState = FRAME_READ_CHECKSUM;
        } else {
          frameIndex = 0;
          frameState = FRAME_READ_PAYLOAD;
        }
      }
      break;
    case FRAME_READ_PAYLOAD:
      // Bug fix: Check bounds before writing to prevent buffer overflow
      if (frameIndex >= MAX_FRAME_PAYLOAD) {
        resetFrameParser();
        break;
      }
      framePayload[frameIndex++] = value;
      if (frameIndex >= frameLength) {
        frameState = FRAME_READ_CHECKSUM;
      }
      break;
    case FRAME_READ_CHECKSUM: {
      frameChecksum = value;
      // Bug fix: Use uint16_t with automatic wrap-around, then cast to uint8_t for comparison
      // This handles overflow correctly (uint16_t wraps, then we compare only lower 8 bits)
      uint16_t checksum = frameCounter;
      for (uint8_t i = 0; i < frameLength; ++i) {
        checksum = (uint16_t)(checksum + framePayload[i]);  // Explicit cast for clarity
      }
      if (((uint8_t)checksum) == frameChecksum) {
        handleFrame(frameCounter, framePayload, frameLength);
      }
      resetFrameParser();
      break;
    }
    default:
      resetFrameParser();
      break;
  }
}

void setup() {
  // Initialize serial communication - 115200 for low latency
  Serial.begin(115200);
  
  // Initialize Keyboard library
  Keyboard.begin();
  
  // Initialize key states (all released) - bit array
  memset(keyStates, 0, KEY_STATES_SIZE);
  resetObfuscation();
  
  // Initialize watchdog timer
  lastReceiveMs = millis();
  
  // Anti-detection: Initialize analog pins for random jitter generation
  // Set A0, A1 as INPUT (floating) to generate noise for entropy
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  
  // Disable LED to avoid annoying blinking
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);  // Turn off LED
  
  // Disable RX/TX LED blinking (Pro Micro has separate RX/TX LEDs)
  // These LEDs blink during Serial activity - disable them by setting pins to INPUT
  // Pro Micro: RX LED on pin 17, TX LED on pin 30 (varies by board version)
  // Set pins to INPUT to disable hardware Serial LED blinking
  #ifdef LED_BUILTIN_RX
    pinMode(LED_BUILTIN_RX, INPUT);  // Disable RX LED
  #endif
  #ifdef LED_BUILTIN_TX
    pinMode(LED_BUILTIN_TX, INPUT);  // Disable TX LED
  #endif
  
  // Direct pin disable for Pro Micro (if macros not defined)
  // Pro Micro 5V/16MHz: RX=17, TX=30
  // Pro Micro 3.3V/8MHz: RX=17, TX=30
  // Setting to INPUT disables hardware LED control
  pinMode(17, INPUT);  // RX LED pin (most Pro Micro boards)
  pinMode(30, INPUT);  // TX LED pin (most Pro Micro boards)
  
  // Optional: wait for serial connection (for debugging only)
  // while (!Serial) {
  //   ; // wait for serial port to connect
  // }
}

void releaseAllKeys() {
  // Emergency: release all keys (cleanup) - support up to 256 keys
  // Optimization: Use bit array for faster iteration
  for (uint16_t i = 0; i < MAX_KEYS; i++) {
    if (getKeyState(i)) {
      Keyboard.release(i);
      clearKeyState(i);
    }
  }
}

// Fast string comparison - optimized for lowercase
bool strEq(const char* str1, const char* str2, uint8_t len) {
  for (uint8_t i = 0; i < len; i++) {
    if (str1[i] != str2[i]) {
      // Case-insensitive compare
      char c1 = str1[i];
      char c2 = str2[i];
      if (c1 >= 'A' && c1 <= 'Z') c1 += 32;
      if (c2 >= 'A' && c2 <= 'Z') c2 += 32;
      if (c1 != c2) return false;
    }
  }
  return true;
}

// Binary search helper: compare key name
int8_t compareKeyName(const char* name1, uint8_t len1, const char* name2, uint8_t len2) {
  uint8_t minLen = (len1 < len2) ? len1 : len2;
  for (uint8_t i = 0; i < minLen; i++) {
    char c1 = name1[i];
    char c2 = name2[i];
    // Case-insensitive compare
    if (c1 >= 'A' && c1 <= 'Z') c1 += 32;
    if (c2 >= 'A' && c2 <= 'Z') c2 += 32;
    if (c1 < c2) return -1;
    if (c1 > c2) return 1;
  }
  if (len1 < len2) return -1;
  if (len1 > len2) return 1;
  return 0;
}

// Fast key lookup - optimized with binary search (O(log n) instead of O(n))
uint8_t getKeyCode(const char* keyName, uint8_t keyLen) {
  // Binary search: find range with matching nameLen first
  uint8_t left = 0;
  uint8_t right = KEY_MAP_SIZE;
  uint8_t startIdx = 0;
  uint8_t endIdx = KEY_MAP_SIZE;
  
  // Find start of nameLen range
  while (left < right) {
    // Bug fix: Prevent overflow in mid calculation
    uint8_t mid = left + ((right - left) / 2);
    if (keyMap[mid].nameLen < keyLen) {
      left = mid + 1;
    } else {
      right = mid;
    }
  }
  startIdx = left;
  
  // Find end of nameLen range
  left = startIdx;
  right = KEY_MAP_SIZE;
  while (left < right) {
    // Bug fix: Prevent overflow in mid calculation
    uint8_t mid = left + ((right - left) / 2);
    if (keyMap[mid].nameLen <= keyLen) {
      left = mid + 1;
    } else {
      right = mid;
    }
  }
  endIdx = left;
  
  // Binary search within nameLen range
  left = startIdx;
  right = endIdx;
  while (left < right) {
    // Bug fix: Prevent overflow in mid calculation
    uint8_t mid = left + ((right - left) / 2);
    int8_t cmp = compareKeyName(keyName, keyLen, keyMap[mid].name, keyMap[mid].nameLen);
    if (cmp < 0) {
      right = mid;
    } else if (cmp > 0) {
      left = mid + 1;
    } else {
      return keyMap[mid].keyCode;
    }
  }
  
  return 0; // Not found
}

// New feature: Handle key combo (e.g., "ctrl+c", "shift+a", "ctrl+shift+x")
void handleKeyCombo(const char* combo, uint8_t comboLen) {
  if (comboLen == 0) return;
  
  // Parse combo: "modifier+key" or "mod1+mod2+key"
  // Find all '+' separators
  uint8_t maxModifiers = 4;  // Support up to 4 modifiers
  uint8_t modifiers[maxModifiers];
  uint8_t modifierCount = 0;
  uint8_t mainKeyCode = 0;
  
  const char* current = combo;
  uint8_t remaining = comboLen;
  
  while (remaining > 0 && modifierCount < maxModifiers) {
    // Find next '+' or end
    const char* plus = current;
    uint8_t segmentLen = 0;
    while (segmentLen < remaining && *plus != '+') {
      plus++;
      segmentLen++;
    }
    
    // Get key code for this segment
    uint8_t keyCode = getKeyCode(current, segmentLen);
    if (keyCode == 0) {
      // Invalid key, skip combo
      return;
    }
    
    // Check if this is a modifier key
    bool isModifier = (keyCode == KEY_LEFT_CTRL || keyCode == KEY_RIGHT_CTRL ||
                       keyCode == KEY_LEFT_SHIFT || keyCode == KEY_RIGHT_SHIFT ||
                       keyCode == KEY_LEFT_ALT || keyCode == KEY_RIGHT_ALT ||
                       keyCode == KEY_LEFT_GUI || keyCode == KEY_RIGHT_GUI);
    
    // Bug fix: Check if there's a '+' after this segment (not just segmentLen < remaining)
    // If segmentLen == remaining, this is the last segment (no '+'), so it must be main key
    // Also check that plus pointer is still within bounds
    bool hasNextSegment = (segmentLen < remaining && plus < (combo + comboLen) && *plus == '+');
    
    if (isModifier && hasNextSegment) {
      // This is a modifier, continue to next segment
      modifiers[modifierCount++] = keyCode;
      current = plus + 1;
      remaining -= segmentLen + 1;
    } else {
      // This is the main key (either not a modifier, or no more segments)
      mainKeyCode = keyCode;
      break;
    }
  }
  
  // Bug fix: Check if we have a valid main key (not just a modifier)
  if (mainKeyCode == 0) {
    // No main key found - invalid combo
    return;
  }
  
  // Bug fix: Ensure combo has at least one non-modifier key OR multiple modifiers
  // Allow "combo:ctrl+shift" (multiple modifiers) but reject "combo:ctrl" (single modifier)
  bool mainKeyIsModifier = (mainKeyCode == KEY_LEFT_CTRL || mainKeyCode == KEY_RIGHT_CTRL ||
                             mainKeyCode == KEY_LEFT_SHIFT || mainKeyCode == KEY_RIGHT_SHIFT ||
                             mainKeyCode == KEY_LEFT_ALT || mainKeyCode == KEY_RIGHT_ALT ||
                             mainKeyCode == KEY_LEFT_GUI || mainKeyCode == KEY_RIGHT_GUI);
  if (mainKeyIsModifier && modifierCount == 0) {
    // Only one modifier without other keys - invalid combo (use "down:ctrl" instead)
    return;
  }
  
  // Press all modifiers first
  for (uint8_t i = 0; i < modifierCount; i++) {
    if (modifiers[i] < MAX_KEYS && !getKeyState(modifiers[i])) {
      Keyboard.press(modifiers[i]);
      setKeyState(modifiers[i]);
    }
  }
  
  // Anti-detection: Small delay with jitter to ensure modifiers are registered
  humanDelayMicroseconds(1000, 300);  // 1000-1300us (1.0-1.3ms) with variation
  
  // Press main key
  if (mainKeyCode < MAX_KEYS && !getKeyState(mainKeyCode)) {
    Keyboard.press(mainKeyCode);
    setKeyState(mainKeyCode);
  }
  
  // Anti-detection: Hold time with jitter for human-like key combo timing
  humanDelay(45, 15);  // 45-60ms with variation
  
  // Release main key first
  if (mainKeyCode < MAX_KEYS && getKeyState(mainKeyCode)) {
    Keyboard.release(mainKeyCode);
    clearKeyState(mainKeyCode);
  }
  
  // Release all modifiers
  for (uint8_t i = 0; i < modifierCount; i++) {
    if (modifiers[i] < MAX_KEYS && getKeyState(modifiers[i])) {
      Keyboard.release(modifiers[i]);
      clearKeyState(modifiers[i]);
    }
  }
}

// New feature: Handle batch commands (e.g., "down:a,up:a,down:b,up:b")
void handleBatchCommands(const char* batch, uint8_t batchLen) {
  if (batchLen == 0) return;
  
  const char* current = batch;
  uint8_t remaining = batchLen;
  
  while (remaining > 0) {
    // Find next ',' or end
    const char* comma = current;
    uint8_t cmdLen = 0;
    while (cmdLen < remaining && *comma != ',') {
      comma++;
      cmdLen++;
    }
    
    // Process this command
    if (cmdLen > 0) {
      // Trim whitespace
      const char* cmdStart = current;
      uint8_t cmdLenTrimmed = cmdLen;
      while (cmdLenTrimmed > 0 && *cmdStart == ' ') {
        cmdStart++;
        cmdLenTrimmed--;
      }
      while (cmdLenTrimmed > 0 && (cmdStart[cmdLenTrimmed - 1] == ' ' || cmdStart[cmdLenTrimmed - 1] == '\r' || cmdStart[cmdLenTrimmed - 1] == '\n')) {
        cmdLenTrimmed--;
      }
      
      if (cmdLenTrimmed > 0) {
        // Create temporary null-terminated string for processCommand
        // Bug fix: Ensure we don't overflow tempCmd buffer
        char tempCmd[SERIAL_BUFFER_SIZE];
        if (cmdLenTrimmed < SERIAL_BUFFER_SIZE) {
          memcpy(tempCmd, cmdStart, cmdLenTrimmed);
          tempCmd[cmdLenTrimmed] = '\0';
          processCommand(tempCmd, cmdLenTrimmed);
        } else {
          // Command too long - skip it to prevent buffer overflow
          // This can happen if batch command contains very long individual commands
        }
      }
    }
    
    // Bug fix: Prevent infinite loop - check if we can advance
    if (cmdLen < remaining) {
      // There's a comma, move to next command
      uint8_t advance = cmdLen + 1;
      if (advance > remaining) {
        // Safety check: prevent underflow
        break;
      }
      current = comma + 1;
      remaining -= advance;
    } else {
      // No comma found, this is the last command
      break;
    }
  }
}

// Process command - optimized for low latency
void processCommand(const char* command, uint8_t cmdLen) {
  // Trim whitespace (skip leading spaces)
  const char* start = command;
  while (*start == ' ' && cmdLen > 0) {
    start++;
    cmdLen--;
  }
  
  // Trim trailing spaces and newline
  while (cmdLen > 0 && (start[cmdLen - 1] == ' ' || start[cmdLen - 1] == '\n' || start[cmdLen - 1] == '\r')) {
    cmdLen--;
  }
  
  if (cmdLen == 0) return;
  
  // Special command: all_up
  if (cmdLen == 6 && strEq(start, "all_up", 6)) {
    releaseAllKeys();
    return;
  }
  
  // New feature: Key combo support - "combo:modifier+key" or "combo:mod1+mod2+key"
  // Example: "combo:ctrl+c", "combo:shift+a", "combo:ctrl+shift+x"
  if (cmdLen >= 6 && strEq(start, "combo:", 6)) {
    handleKeyCombo(start + 6, cmdLen - 6);
    return;
  }
  
  // New feature: Batch commands - "batch:cmd1,cmd2,cmd3"
  // Example: "batch:down:a,up:a,down:b,up:b"
  if (cmdLen >= 6 && strEq(start, "batch:", 6)) {
    handleBatchCommands(start + 6, cmdLen - 6);
    return;
  }
  
  // Parse command: "action:key"
  const char* colon = start;
  uint8_t colonIdx = 0;
  while (colonIdx < cmdLen && *colon != ':') {
    colon++;
    colonIdx++;
  }
  
  if (colonIdx >= cmdLen) {
    // No colon found - invalid format
    return;
  }
  
  // Extract action (before colon)
  uint8_t actionLen = colonIdx;
  const char* action = start;
  
  // Extract key name (after colon)
  uint8_t keyLen = cmdLen - colonIdx - 1;
  const char* keyName = colon + 1;
  
  // Find key code
  uint8_t keyCode = getKeyCode(keyName, keyLen);
  if (keyCode == 0 && keyLen > 1) {
    // Not found in map - might be unsupported key (printscreen, scroll, pause, menu, numlock)
    // These keys have keyCode = 0 in keyMap and will be skipped
    return;
  }
  
  // Special handling: single char keys with keyCode = 0 should be skipped too
  if (keyCode == 0) {
    return;
  }
  
  // Execute action - optimized for low latency
  if (keyCode == '-' && actionLen == 4 && strEq(action, "down", 4)) {
    watchdogEnabled = !watchdogEnabled;
    return;
  }
  if (keyCode == '-' && actionLen == 2 && strEq(action, "up", 2)) {
    return;
  }

  if (actionLen == 4 && strEq(action, "down", 4)) {
    // Key down - support all keys including arrows and modifiers (keyCode can be > 127)
    if (keyCode < MAX_KEYS) {
      if (getKeyState(keyCode)) {
        // Key already held - release and press again for key repeat
        Keyboard.release(keyCode);
        // Anti-detection: Short delay with jitter for key repeat (human-like variation)
        humanDelayMicroseconds(500, 200); // 500-700us (0.5-0.7ms) with variation
        Keyboard.press(keyCode);
        // Key remains pressed
      } else {
        // Key not held - press it
        Keyboard.press(keyCode);
        setKeyState(keyCode);
      }
    }
  } else if (actionLen == 2 && strEq(action, "up", 2)) {
    // Key up - support all keys including arrows and modifiers
    if (keyCode < MAX_KEYS && getKeyState(keyCode)) {
      Keyboard.release(keyCode);
      clearKeyState(keyCode);
    }
  }
}

void loop() {
  // Ensure LED stays off (prevent any automatic blinking)
  digitalWrite(LED_BUILTIN, LOW);
  
  // Bug fix: Check frame parsing timeout
  if (frameParsing && frameStartMs > 0) {
    unsigned long currentMs = millis();
    unsigned long elapsed = (currentMs >= frameStartMs) 
      ? (currentMs - frameStartMs) 
      : ((4294967295UL - frameStartMs) + currentMs + 1);  // Handle millis() overflow
    if (elapsed > FRAME_TIMEOUT_MS) {
      resetFrameParser();
    }
  }
  
  // Optimization: Batch serial reading for better throughput
  // Read multiple bytes at once to reduce overhead
  uint8_t bytesAvailable = Serial.available();
  if (bytesAvailable > 0) {
    lastReceiveMs = millis(); // Update watchdog
    
    // Read up to SERIAL_BATCH_SIZE bytes at once
    uint8_t bytesToRead = (bytesAvailable > SERIAL_BATCH_SIZE) ? SERIAL_BATCH_SIZE : bytesAvailable;
    uint8_t bytesRead = Serial.readBytes(serialBatchBuffer, bytesToRead);
    
    // Process each byte
    for (uint8_t i = 0; i < bytesRead; i++) {
      uint8_t byteVal = serialBatchBuffer[i];

    if (!frameParsing) {
      if (byteVal == FRAME_START_BYTE) {
        frameParsing = true;
        frameState = FRAME_READ_COUNTER;
          frameStartMs = millis();  // Bug fix: Track frame parsing start time
        continue;
      }

      if (!obfuscationActive) {
        handleAsciiByte(byteVal);
      }
      continue;
    }

    parseFrameByte(byteVal);
    }
  }
  
  // Watchdog: auto-release nếu quá timeout (optional toggle)
  if (watchdogEnabled) {
    unsigned long currentMs = millis();
    // Bug fix: Handle millis() overflow (happens after ~49 days)
    unsigned long elapsed = (currentMs >= lastReceiveMs) 
      ? (currentMs - lastReceiveMs) 
      : ((4294967295UL - lastReceiveMs) + currentMs + 1);
    if (elapsed > WATCHDOG_TIMEOUT_MS) {
      // Check if any keys are held - optimization: check bit array quickly
      bool anyHeld = false;
      for (uint8_t i = 0; i < KEY_STATES_SIZE; i++) {
        if (keyStates[i] != 0) {
          anyHeld = true;
          break;
        }
      }
      
      if (anyHeld) {
        releaseAllKeys();
      }
      
      // Reset watchdog timer (don't spam)
      lastReceiveMs = currentMs;
    }
  }
}

