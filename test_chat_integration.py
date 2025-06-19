#!/usr/bin/env python3
"""
Test script to verify chat interface integration with CircuitGenerator
"""

import os
import sys
from datetime import datetime

def test_circuit_generator_integration():
    """Test the CircuitGenerator integration"""
    print("🧪 Testing CircuitGenerator Integration")
    print("=" * 50)
    
    try:
        # Import the CircuitGenerator
        from circuit_generator import CircuitGenerator
        
        # Initialize CircuitGenerator
        print("Initializing CircuitGenerator...")
        generator = CircuitGenerator()
        print("✅ CircuitGenerator initialized")
        
        # Test 1: Voltage Divider
        print("\n1. Testing Voltage Divider...")
        voltage_divider_desc = {
            'circuit_type': 'voltage_divider',
            'parameters': {
                'name': 'voltage_divider_5v_33v',
                'values': {
                    'vin': 5.0,
                    'vout': 3.3
                }
            }
        }
        
        circuit_dir, generated_files = generator.generate_circuit_files(voltage_divider_desc)
        if circuit_dir and generated_files:
            print(f"✅ Voltage divider generated: {len(generated_files)} files")
            for file_path in generated_files:
                if os.path.exists(file_path):
                    print(f"   ✓ {os.path.basename(file_path)}")
                else:
                    print(f"   ❌ {os.path.basename(file_path)} - File not found")
        else:
            print("❌ Voltage divider generation failed")
        
        # Test 2: RC Filter
        print("\n2. Testing RC Filter...")
        rc_filter_desc = {
            'circuit_type': 'rc_filter',
            'parameters': {
                'name': 'rc_low_pass_1000hz',
                'values': {
                    'cutoff_freq': 1000
                }
            }
        }
        
        circuit_dir, generated_files = generator.generate_circuit_files(rc_filter_desc)
        if circuit_dir and generated_files:
            print(f"✅ RC filter generated: {len(generated_files)} files")
            for file_path in generated_files:
                if os.path.exists(file_path):
                    print(f"   ✓ {os.path.basename(file_path)}")
                else:
                    print(f"   ❌ {os.path.basename(file_path)} - File not found")
        else:
            print("❌ RC filter generation failed")
        
        # Test 3: LED Circuit
        print("\n3. Testing LED Circuit...")
        led_circuit_desc = {
            'circuit_type': 'led_circuit',
            'parameters': {
                'name': 'simple_led_circuit',
                'values': {
                    'v_source': 5.0,
                    'v_led': 2.0,
                    'i_led': 0.020
                }
            }
        }
        
        circuit_dir, generated_files = generator.generate_circuit_files(led_circuit_desc)
        if circuit_dir and generated_files:
            print(f"✅ LED circuit generated: {len(generated_files)} files")
            for file_path in generated_files:
                if os.path.exists(file_path):
                    print(f"   ✓ {os.path.basename(file_path)}")
                else:
                    print(f"   ❌ {os.path.basename(file_path)} - File not found")
        else:
            print("❌ LED circuit generation failed")
        
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
        
        print("\n🎉 CircuitGenerator integration test completed!")
        print("\nThe chat interface should now be able to generate downloadable KiCad files!")
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Make sure all required modules are installed:")
        print("pip install streamlit skidl")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_circuit_generator_integration() 