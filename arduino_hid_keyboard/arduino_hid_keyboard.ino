/*
 * Arduino Pro Micro - USB HID Keyboard Forwarder
 * Nhận command từ Python và forward như USB HID keyboard
 * Với key state tracking để prevent duplicate presses
 */

#include <Keyboard.h>

// Serial buffer
String inputString = "";
boolean stringComplete = false;

// Watchdog để auto-release nếu không nhận dữ liệu trong một khoảng thời gian
unsigned long lastReceiveMs = 0;
const unsigned long WATCHDOG_TIMEOUT_MS = 5000; // 5 giây

// Key state tracking: track các phím đang được giữ
// Sử dụng bit array để tiết kiệm memory (tối đa 128 keys)
#define MAX_KEYS 128
bool keyStates[MAX_KEYS] = {false};  // Track state của mỗi key code

// Key name to HID keycode mapping
struct KeyMapping {
  const char* name;
  uint8_t keyCode;
};

KeyMapping keyMap[] = {
  {"a", 'a'}, {"b", 'b'}, {"c", 'c'}, {"d", 'd'},
  {"e", 'e'}, {"f", 'f'}, {"g", 'g'}, {"h", 'h'},
  {"i", 'i'}, {"j", 'j'}, {"k", 'k'}, {"l", 'l'},
  {"m", 'm'}, {"n", 'n'}, {"o", 'o'}, {"p", 'p'},
  {"q", 'q'}, {"r", 'r'}, {"s", 's'}, {"t", 't'},
  {"u", 'u'}, {"v", 'v'}, {"w", 'w'}, {"x", 'x'},
  {"y", 'y'}, {"z", 'z'},
  {"0", '0'}, {"1", '1'}, {"2", '2'}, {"3", '3'},
  {"4", '4'}, {"5", '5'}, {"6", '6'}, {"7", '7'},
  {"8", '8'}, {"9", '9'},
  {"enter", KEY_RETURN}, {"esc", KEY_ESC}, {"backspace", KEY_BACKSPACE},
  {"tab", KEY_TAB}, {"space", ' '},
  {"caps", KEY_CAPS_LOCK}, {"shift", KEY_LEFT_SHIFT},
  {"ctrl", KEY_LEFT_CTRL}, {"alt", KEY_LEFT_ALT},
  {"left", KEY_LEFT_ARROW}, {"right", KEY_RIGHT_ARROW},
  {"up", KEY_UP_ARROW}, {"down", KEY_DOWN_ARROW},
  {"insert", KEY_INSERT}, {"delete", KEY_DELETE},
  {"home", KEY_HOME}, {"end", KEY_END},
  {"pgup", KEY_PAGE_UP}, {"pgdn", KEY_PAGE_DOWN},
  {"f1", KEY_F1}, {"f2", KEY_F2}, {"f3", KEY_F3}, {"f4", KEY_F4},
  {"f5", KEY_F5}, {"f6", KEY_F6}, {"f7", KEY_F7}, {"f8", KEY_F8},
  {"f9", KEY_F9}, {"f10", KEY_F10}, {"f11", KEY_F11}, {"f12", KEY_F12},
  {"semicolon", ';'}, {"equals", '='}, {"comma", ','},
  {"minus", '-'}, {"period", '.'}, {"slash", '/'},
  {"grave", '`'}, {"lbracket", '['}, {"backslash", '\\'},
  {"rbracket", ']'}, {"quote", '\''},

  // GUI / Windows keys
  {"l_gui", KEY_LEFT_GUI}, {"r_gui", KEY_RIGHT_GUI},

  // Numpad fallback (map về phím thường gần nhất)
  {"np0", '0'}, {"np1", '1'}, {"np2", '2'}, {"np3", '3'},
  {"np4", '4'}, {"np5", '5'}, {"np6", '6'}, {"np7", '7'},
  {"np8", '8'}, {"np9", '9'},
  {"np_add", '+'}, {"np_sub", '-'}, {"np_mul", '*'}, {"np_div", '/'},
  {"np_dec", '.'},

  // Keys không được Keyboard.h hỗ trợ trực tiếp → ignore (keyCode=0 sẽ bị bỏ qua)
  {"printscreen", 0}, {"scroll", 0}, {"pause", 0}, {"menu", 0}, {"numlock", 0}
};

// Phase 5: Device Fingerprinting Bypass - Random timing seed
// Use analog noise để tạo random seed (không có randomSeed() trong setup)
unsigned long randomSeedValue = 0;

void setup() {
  // Phase 5: Initialize random seed từ analog noise (device fingerprinting bypass)
  // Read analog pin 0 (unconnected) để tạo random seed từ electrical noise
  randomSeedValue = analogRead(0);
  for (int i = 0; i < 10; i++) {
    randomSeedValue = (randomSeedValue << 1) ^ analogRead(0);
    delayMicroseconds(100);
  }
  randomSeed(randomSeedValue);
  
  // Initialize serial communication (115200 để giảm độ trễ)
  Serial.begin(115200);
  
  // Initialize Keyboard library
  Keyboard.begin();
  
  // Reserve space for input string
  inputString.reserve(64);
  
  // Initialize key states (all released)
  for (int i = 0; i < MAX_KEYS; i++) {
    keyStates[i] = false;
  }

  // Initialize watchdog timer
  lastReceiveMs = millis();
  
  // Wait for serial connection (optional, for debugging)
  // while (!Serial) {
  //   ; // wait for serial port to connect
  // }
}

void releaseAllKeys() {
  // Emergency: release all keys (cleanup)
  for (int i = 0; i < MAX_KEYS; i++) {
    if (keyStates[i]) {
      Keyboard.release(i);
      keyStates[i] = false;
    }
  }
}

void loop() {
  // Read serial data
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    lastReceiveMs = millis(); // cập nhật watchdog khi nhận dữ liệu
    
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
  
  // Process complete command
  if (stringComplete) {
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }

  // Watchdog: nếu quá timeout mà vẫn còn key đang giữ, auto release
  if ((millis() - lastReceiveMs) > WATCHDOG_TIMEOUT_MS) {
    // Kiểm tra xem có phím nào đang giữ không
    bool anyHeld = false;
    for (int i = 0; i < MAX_KEYS; i++) {
      if (keyStates[i]) { anyHeld = true; break; }
    }
    if (anyHeld) {
      releaseAllKeys();
    }
    // reset mốc thời gian để không spam releaseAllKeys
    lastReceiveMs = millis();
  }
}

void processCommand(String command) {
  command.trim(); // Remove whitespace
  
  // Special command: all_up => release all keys
  if (command.equalsIgnoreCase("all_up")) {
    releaseAllKeys();
    return;
  }

  // Parse command: "action:key"
  int colonIndex = command.indexOf(':');
  if (colonIndex == -1) {
    return; // Invalid format
  }
  
  String action = command.substring(0, colonIndex);
  String keyName = command.substring(colonIndex + 1);
  
  // Find key code
  uint8_t keyCode = getKeyCode(keyName);
  if (keyCode == 0 && keyName.length() > 1) {
    // Not found in map, skip
    return;
  }
  
  // Phase 5: Device Fingerprinting Bypass - Add random timing variation
  // Add small random delay (1-5ms) để tránh fingerprinting patterns
  unsigned long randomDelay = random(1000, 5000);  // 1-5ms in microseconds
  delayMicroseconds(randomDelay);
  
  // Execute action với key repeat support
  if (action == "down") {
    // Support key repeat: if key is already held, release and press again to generate new key event
    if (keyCode < MAX_KEYS) {
      if (keyStates[keyCode]) {
        // Key already held - release and press again for key repeat
        Keyboard.release(keyCode);
        delay(1);  // Small delay to ensure release is processed
        Keyboard.press(keyCode);
        // Key remains pressed (keyStates[keyCode] = true)
      } else {
        // Key not held - press it
        Keyboard.press(keyCode);
        keyStates[keyCode] = true;  // Mark as pressed
      }
    }
  } else if (action == "up") {
    // Release key nếu đang được giữ
    if (keyCode < MAX_KEYS && keyStates[keyCode]) {
      Keyboard.release(keyCode);
      keyStates[keyCode] = false;  // Mark as released
    }
    // Nếu key không được giữ, ignore duplicate up
  }
}

uint8_t getKeyCode(String keyName) {
  // Convert to lowercase
  keyName.toLowerCase();
  
  // Search in key map
  int mapSize = sizeof(keyMap) / sizeof(KeyMapping);
  for (int i = 0; i < mapSize; i++) {
    if (keyName == keyMap[i].name) {
      return keyMap[i].keyCode;
    }
  }
  
  // Not found
  return 0;
}

