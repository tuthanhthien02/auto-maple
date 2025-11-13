"""
Script để check bot có dùng Arduino connection không
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import config
from src.common.vkeys import _get_arduino_output
from src.common.shared_arduino_connection import SharedArduinoConnection

def check_arduino_connection():
    """Check Arduino connection status"""
    print("=" * 60)
    print("ARDUINO CONNECTION CHECK")
    print("=" * 60)
    
    # 1. Check config.use_arduino
    print("\n1. Config Settings:")
    print(f"   config.use_arduino = {getattr(config, 'use_arduino', 'NOT SET')}")
    print(f"   config.arduino_com_port = {getattr(config, 'arduino_com_port', 'NOT SET')}")
    print(f"   config.arduino_baudrate = {getattr(config, 'arduino_baudrate', 'NOT SET')}")
    
    # 2. Check SharedArduinoConnection
    print("\n2. SharedArduinoConnection:")
    try:
        shared_conn = SharedArduinoConnection.get_instance()
        print(f"   Instance created: ✅")
        print(f"   Is connected: {shared_conn.is_connected()}")
        if shared_conn.is_connected():
            print(f"   COM Port: {shared_conn.com_port}")
            print(f"   Baudrate: {shared_conn.baudrate}")
        else:
            print(f"   ⚠️  Arduino NOT connected!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Check vkeys Arduino output
    print("\n3. VKeys Arduino Output:")
    try:
        arduino_output = _get_arduino_output()
        if arduino_output:
            if hasattr(arduino_output, 'connected'):
                print(f"   Arduino output instance: ✅")
                print(f"   Is connected: {arduino_output.connected}")
                if arduino_output.connected:
                    print(f"   COM Port: {arduino_output.com_port}")
                    print(f"   Baudrate: {arduino_output.baudrate}")
                    # Check if using shared connection
                    if hasattr(arduino_output, 'shared_connection'):
                        print(f"   Using SharedArduinoConnection: ✅")
                        shared_conn_check = arduino_output.shared_connection
                        if shared_conn_check is shared_conn:
                            print(f"   Same instance as SharedArduinoConnection: ✅")
                        else:
                            print(f"   ⚠️  Different instance!")
                    else:
                        print(f"   ⚠️  NOT using SharedArduinoConnection!")
                else:
                    print(f"   ⚠️  Arduino output NOT connected!")
            else:
                print(f"   Arduino output instance: {arduino_output}")
        else:
            print(f"   Arduino output: False (not initialized or disabled)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Check VM Input Blocker (if enabled)
    print("\n4. VM Input Blocker:")
    print(f"   config.block_vm_input = {getattr(config, 'block_vm_input', 'NOT SET')}")
    print(f"   config.force_arduino_output = {getattr(config, 'force_arduino_output', 'NOT SET')}")
    if hasattr(config, 'vm_input_blocker') and config.vm_input_blocker:
        print(f"   VM Input Blocker instance: ✅")
        print(f"   Is blocking: {config.vm_input_blocker.is_blocking()}")
    else:
        print(f"   VM Input Blocker: Not initialized")
    
    # 5. Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    use_arduino = getattr(config, 'use_arduino', False)
    shared_connected = False
    vkeys_connected = False
    
    try:
        shared_conn = SharedArduinoConnection.get_instance()
        shared_connected = shared_conn.is_connected()
    except:
        pass
    
    try:
        arduino_output = _get_arduino_output()
        if arduino_output and hasattr(arduino_output, 'connected'):
            vkeys_connected = arduino_output.connected
    except:
        pass
    
    print(f"\n✅ Config use_arduino: {use_arduino}")
    print(f"{'✅' if shared_connected else '❌'} SharedArduinoConnection: {shared_connected}")
    print(f"{'✅' if vkeys_connected else '❌'} VKeys Arduino Output: {vkeys_connected}")
    
    if use_arduino and shared_connected and vkeys_connected:
        print("\n🎉 Bot IS using Arduino connection!")
        print("   - Config enabled: ✅")
        print("   - SharedArduinoConnection: ✅")
        print("   - VKeys using Arduino: ✅")
    elif use_arduino:
        print("\n⚠️  Bot configured to use Arduino but connection failed!")
    else:
        print("\n❌ Bot is NOT using Arduino (config.use_arduino = False)")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    check_arduino_connection()

