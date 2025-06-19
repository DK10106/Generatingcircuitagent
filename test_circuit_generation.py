#!/usr/bin/env python3
"""
Test script for circuit generation functions
"""

import os
import sys
from datetime import datetime

def test_circuit_generation():
    """Test all circuit generation functions"""
    print("🧪 Testing Circuit Generation Functions")
    print("=" * 50)
    
    try:
        # Import the circuit generation functions
        from generate_circuit import (
            setup_kicad_env,
            create_voltage_divider,
            create_rc_low_pass_filter,
            create_led_circuit
        )
        
        # Setup KiCad environment
        print("Setting up KiCad environment...")
        setup_kicad_env()
        print("✅ KiCad environment setup complete")
        
        # Test 1: Voltage Divider
        print("\n1. Testing Voltage Divider...")
        try:
            result = create_voltage_divider(input_voltage=5.0, output_voltage=3.3)
            if result and 'download_path' in result:
                download_path = result['download_path']
                if os.path.exists(download_path):
                    print(f"✅ Voltage divider created: {os.path.basename(download_path)}")
                    print(f"   Type: {result.get('type', 'unknown')}")
                    print(f"   Response: {result.get('response', 'No response')}")
                else:
                    print(f"❌ Voltage divider file not found: {download_path}")
            else:
                print("❌ Voltage divider returned invalid result")
        except Exception as e:
            print(f"❌ Voltage divider failed: {str(e)}")
        
        # Test 2: RC Low-Pass Filter
        print("\n2. Testing RC Low-Pass Filter...")
        try:
            result = create_rc_low_pass_filter(cutoff_freq=1000)
            if result and 'download_path' in result:
                download_path = result['download_path']
                if os.path.exists(download_path):
                    print(f"✅ RC filter created: {os.path.basename(download_path)}")
                    print(f"   Type: {result.get('type', 'unknown')}")
                    print(f"   Response: {result.get('response', 'No response')}")
                else:
                    print(f"❌ RC filter file not found: {download_path}")
            else:
                print("❌ RC filter returned invalid result")
        except Exception as e:
            print(f"❌ RC filter failed: {str(e)}")
        
        # Test 3: LED Circuit
        print("\n3. Testing LED Circuit...")
        try:
            result = create_led_circuit(voltage=5.0, led_voltage=2.0, led_current=0.020)
            if result and 'download_path' in result:
                download_path = result['download_path']
                if os.path.exists(download_path):
                    print(f"✅ LED circuit created: {os.path.basename(download_path)}")
                    print(f"   Type: {result.get('type', 'unknown')}")
                    print(f"   Response: {result.get('response', 'No response')}")
                else:
                    print(f"❌ LED circuit file not found: {download_path}")
            else:
                print("❌ LED circuit returned invalid result")
        except Exception as e:
            print(f"❌ LED circuit failed: {str(e)}")
        
        # Check output directories
        print("\n📁 Checking output directories...")
        output_dirs = [
            'kicad_output/voltage_divider',
            'kicad_output/rc_low_pass_filter',
            'kicad_output/led_circuit'
        ]
        
        for output_dir in output_dirs:
            if os.path.exists(output_dir):
                files = os.listdir(output_dir)
                print(f"✅ {output_dir}: {len(files)} files")
                for file in files:
                    print(f"   - {file}")
            else:
                print(f"❌ {output_dir}: Directory not found")
        
        print("\n🎉 Circuit generation test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Make sure all required modules are installed:")
        print("pip install skidl")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_circuit_generation() 