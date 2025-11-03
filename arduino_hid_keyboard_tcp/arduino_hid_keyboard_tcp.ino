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

// Serial buffer - optimized for fast parsing
#define SERIAL_BUFFER_SIZE 32
char serialBuffer[SERIAL_BUFFER_SIZE];
uint8_t bufferIndex = 0;

// Watchdog để auto-release nếu không nhận dữ liệu trong một khoảng thời gian
unsigned long lastReceiveMs = 0;
const unsigned long WATCHDOG_TIMEOUT_MS = 3000; // 3 giây (reduced từ 5s để faster response)

// Key state tracking: track các phím đang được giữ
// Sử dụng bit array để tiết kiệm memory (tối đa 128 keys)
#define MAX_KEYS 128
bool keyStates[MAX_KEYS] = {false};  // Track state của mỗi key code

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
  {"up", 2, KEY_UP_ARROW}, {"down", 4, KEY_DOWN_ARROW},
  {"left", 4, KEY_LEFT_ARROW}, {"right", 5, KEY_RIGHT_ARROW},
  
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

void setup() {
  // Initialize serial communication - 115200 for low latency
  Serial.begin(115200);
  
  // Initialize Keyboard library
  Keyboard.begin();
  
  // Initialize key states (all released)
  memset(keyStates, false, MAX_KEYS);
  
  // Initialize watchdog timer
  lastReceiveMs = millis();
  
  // Optional: wait for serial connection (for debugging only)
  // while (!Serial) {
  //   ; // wait for serial port to connect
  // }
}

void releaseAllKeys() {
  // Emergency: release all keys (cleanup)
  for (uint8_t i = 0; i < MAX_KEYS; i++) {
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
    // Not found in map, skip
    return;
  }
  
  // Execute action - optimized for low latency
  if (actionLen == 4 && strEq(action, "down", 4)) {
    // Key down
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
    // Key up
    if (keyCode < MAX_KEYS && keyStates[keyCode]) {
      Keyboard.release(keyCode);
      keyStates[keyCode] = false;
    }
  }
}

void loop() {
  // Fast serial reading - no String class overhead
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    lastReceiveMs = millis(); // Update watchdog
    
    if (inChar == '\n' || bufferIndex >= SERIAL_BUFFER_SIZE - 1) {
      // Command complete or buffer full
      if (bufferIndex > 0) {
        serialBuffer[bufferIndex] = '\0'; // Null terminate
        processCommand(serialBuffer, bufferIndex);
        bufferIndex = 0; // Reset buffer
      }
    } else if (inChar != '\r') {
      // Ignore carriage return, add other chars
      serialBuffer[bufferIndex++] = inChar;
    }
  }
  
  // Watchdog: auto-release nếu quá timeout
  unsigned long currentMs = millis();
  if ((currentMs - lastReceiveMs) > WATCHDOG_TIMEOUT_MS) {
    // Check if any keys are held
    bool anyHeld = false;
    for (uint8_t i = 0; i < MAX_KEYS; i++) {
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

