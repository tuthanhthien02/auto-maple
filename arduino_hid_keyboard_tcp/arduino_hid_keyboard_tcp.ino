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
 */

#include <Keyboard.h>
#include <Arduino.h>
#include <stdint.h>
#include <string.h>
#include <avr/pgmspace.h>

// Serial buffer - optimized for fast parsing
#define SERIAL_BUFFER_SIZE 32
char serialBuffer[SERIAL_BUFFER_SIZE];
uint8_t bufferIndex = 0;

// Obfuscated serial constants
const uint8_t FRAME_START_BYTE = 0x7E;
const uint8_t HANDSHAKE_COUNTER = 0xFF;
const uint8_t HANDSHAKE_LENGTH = 16;
const uint8_t MAX_FRAME_PAYLOAD = 48;  // enough for command strings

// Obfuscation state
bool obfuscationActive = false;
bool handshakeReceived = false;
uint8_t sessionKey[HANDSHAKE_LENGTH];

// Watchdog để auto-release nếu không nhận dữ liệu trong một khoảng thời gian
unsigned long lastReceiveMs = 0;
const unsigned long WATCHDOG_TIMEOUT_MS = 3000; // 3 giây (reduced từ 5s để faster response)

// Key state tracking: track các phím đang được giữ
// Tăng lên 256 để support arrow keys và control keys (keyCode > 127)
#define MAX_KEYS 256
bool keyStates[MAX_KEYS] = {false};  // Track state của mỗi key code

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

// Key name to HID keycode mapping - optimized lookup
struct KeyMapping {
  const char* name;
  uint8_t nameLen;
  uint8_t keyCode;
};

// Sorted by name length và alphabetically để faster lookup
KeyMapping keyMap[] = {
  // Single char keys (fastest lookup)
  {"a", 1, 'a'}, {"b", 1, 'b'}, {"c", 1, 'c'}, {"d", 1, 'd'},
  {"e", 1, 'e'}, {"f", 1, 'f'}, {"g", 1, 'g'}, {"h", 1, 'h'},
  {"i", 1, 'i'}, {"j", 1, 'j'}, {"k", 1, 'k'}, {"l", 1, 'l'},
  {"m", 1, 'm'}, {"n", 1, 'n'}, {"o", 1, 'o'}, {"p", 1, 'p'},
  {"q", 1, 'q'}, {"r", 1, 'r'}, {"s", 1, 's'}, {"t", 1, 't'},
  {"u", 1, 'u'}, {"v", 1, 'v'}, {"w", 1, 'w'}, {"x", 1, 'x'},
  {"y", 1, 'y'}, {"z", 1, 'z'},
  {"0", 1, '0'}, {"1", 1, '1'}, {"2", 1, '2'}, {"3", 1, '3'},
  {"4", 1, '4'}, {"5", 1, '5'}, {"6", 1, '6'}, {"7", 1, '7'},
  {"8", 1, '8'}, {"9", 1, '9'},
  
  // 2-char keys
  {"up", 2, KEY_UP_ARROW},
  // 3-char keys  
  // 4-char keys
  {"down", 4, KEY_DOWN_ARROW}, {"left", 4, KEY_LEFT_ARROW},
  // 5-char keys
  {"right", 5, KEY_RIGHT_ARROW},
  
  // Common keys (3-4 chars)
  {"esc", 3, KEY_ESC}, {"tab", 3, KEY_TAB}, {"alt", 3, KEY_LEFT_ALT},
  {"f1", 2, KEY_F1}, {"f2", 2, KEY_F2}, {"f3", 2, KEY_F3}, {"f4", 2, KEY_F4},
  {"f5", 2, KEY_F5}, {"f6", 2, KEY_F6}, {"f7", 2, KEY_F7}, {"f8", 2, KEY_F8},
  {"f9", 2, KEY_F9}, {"f10", 3, KEY_F10}, {"f11", 3, KEY_F11}, {"f12", 3, KEY_F12},
  {"end", 3, KEY_END}, {"pgup", 4, KEY_PAGE_UP}, {"pgdn", 4, KEY_PAGE_DOWN},
  {"home", 4, KEY_HOME}, {"delete", 6, KEY_DELETE}, {"insert", 6, KEY_INSERT},
  
  // 4+ char keys
  {"space", 5, ' '}, {"enter", 5, KEY_RETURN}, {"shift", 5, KEY_LEFT_SHIFT},
  {"ctrl", 4, KEY_LEFT_CTRL}, {"caps", 4, KEY_CAPS_LOCK},
  {"backspace", 9, KEY_BACKSPACE},
  
  // Special chars
  {"semicolon", 9, ';'}, {"equals", 6, '='}, {"comma", 5, ','},
  {"minus", 5, '-'}, {"period", 6, '.'}, {"slash", 5, '/'},
  {"grave", 5, '`'}, {"lbracket", 8, '['}, {"backslash", 9, '\\'},
  {"rbracket", 8, ']'}, {"quote", 5, '\''},
  
  // GUI / Windows keys
  {"l_gui", 5, KEY_LEFT_GUI}, {"r_gui", 5, KEY_RIGHT_GUI},
  
  // Numpad fallback
  {"np0", 3, '0'}, {"np1", 3, '1'}, {"np2", 3, '2'}, {"np3", 3, '3'},
  {"np4", 3, '4'}, {"np5", 3, '5'}, {"np6", 3, '6'}, {"np7", 3, '7'},
  {"np8", 3, '8'}, {"np9", 3, '9'},
  {"np_add", 6, '+'}, {"np_sub", 6, '-'}, {"np_mul", 6, '*'}, {"np_div", 6, '/'},
  {"np_dec", 6, '.'},
  
  // Unsupported keys (keyCode = 0)
  {"printscreen", 11, 0}, {"scroll", 6, 0}, {"pause", 5, 0}, 
  {"menu", 4, 0}, {"numlock", 7, 0}
};

const uint8_t KEY_MAP_SIZE = sizeof(keyMap) / sizeof(KeyMapping);

/**********************
 *  SHA-256 / HMAC   *
 **********************/

void processCommand(const char* command, uint8_t cmdLen);

typedef struct {
  uint32_t state[8];
  uint64_t bitcount;
  uint8_t buffer[64];
} SHA256_CTX;

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
}

void handleAsciiByte(uint8_t byteVal) {
  char inChar = (char)byteVal;
  if (inChar == '\n' || bufferIndex >= SERIAL_BUFFER_SIZE - 1) {
    if (bufferIndex > 0) {
      serialBuffer[bufferIndex] = '\0';
      processCommand(serialBuffer, bufferIndex);
      bufferIndex = 0;
    }
  } else if (inChar != '\r') {
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
      framePayload[frameIndex++] = value;
      if (frameIndex >= frameLength) {
        frameState = FRAME_READ_CHECKSUM;
      }
      break;
    case FRAME_READ_CHECKSUM: {
      frameChecksum = value;
      uint16_t checksum = frameCounter;
      for (uint8_t i = 0; i < frameLength; ++i) {
        checksum += framePayload[i];
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
  
  // Initialize key states (all released)
  memset(keyStates, false, MAX_KEYS);
  resetObfuscation();
  
  // Initialize watchdog timer
  lastReceiveMs = millis();
  
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
  for (uint16_t i = 0; i < MAX_KEYS; i++) {
    if (keyStates[i]) {
      Keyboard.release(i);
      keyStates[i] = false;
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

// Fast key lookup - optimized for performance
uint8_t getKeyCode(const char* keyName, uint8_t keyLen) {
  // Binary search could be faster, but linear search is simpler
  // and fast enough for small map size
  for (uint8_t i = 0; i < KEY_MAP_SIZE; i++) {
    if (keyMap[i].nameLen == keyLen && strEq(keyMap[i].name, keyName, keyLen)) {
      return keyMap[i].keyCode;
    }
  }
  return 0; // Not found
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
  if (actionLen == 4 && strEq(action, "down", 4)) {
    // Key down - support all keys including arrows and modifiers (keyCode can be > 127)
    if (keyCode < MAX_KEYS) {
      if (keyStates[keyCode]) {
        // Key already held - release and press again for key repeat
        Keyboard.release(keyCode);
        // Use shorter delay for faster response (1ms -> minimal)
        delayMicroseconds(500); // 0.5ms instead of 1ms
        Keyboard.press(keyCode);
        // Key remains pressed
      } else {
        // Key not held - press it
        Keyboard.press(keyCode);
        keyStates[keyCode] = true;
      }
    }
  } else if (actionLen == 2 && strEq(action, "up", 2)) {
    // Key up - support all keys including arrows and modifiers
    if (keyCode < MAX_KEYS && keyStates[keyCode]) {
      Keyboard.release(keyCode);
      keyStates[keyCode] = false;
    }
  }
}

void loop() {
  // Ensure LED stays off (prevent any automatic blinking)
  digitalWrite(LED_BUILTIN, LOW);
  
  // Fast serial reading - no String class overhead
  while (Serial.available()) {
    uint8_t byteVal = (uint8_t)Serial.read();
    lastReceiveMs = millis(); // Update watchdog

    if (!frameParsing) {
      if (byteVal == FRAME_START_BYTE) {
        frameParsing = true;
        frameState = FRAME_READ_COUNTER;
        continue;
      }

      if (!obfuscationActive) {
        handleAsciiByte(byteVal);
      }
      continue;
    }

    parseFrameByte(byteVal);
  }
  
  // Watchdog: auto-release nếu quá timeout
  unsigned long currentMs = millis();
  if ((currentMs - lastReceiveMs) > WATCHDOG_TIMEOUT_MS) {
    // Check if any keys are held - support up to 256 keys
    bool anyHeld = false;
    for (uint16_t i = 0; i < MAX_KEYS; i++) {
      if (keyStates[i]) {
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

