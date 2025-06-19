#!/usr/bin/env python3
"""
Test script to verify the UI fixes work correctly
"""

import sys
import os

def test_circuit_functions():
    """Test the circuit generation functions directly"""
    print("🔧 Testing circuit generation functions...")
    
    try:
        # Import the functions
        from generate_circuit import create_voltage_divider, create_rc_low_pass_filter, create_led_circuit
        
        # Test voltage divider
        print("Testing voltage divider...")
        result = create_voltage_divider(input_voltage=5.0, output_voltage=3.3)
        if 'error' not in result:
            print(f"✅ Voltage divider: {result['name']}")
            print(f"   Files: {len(result['generated_files'])}")
        else:
            print(f"❌ Voltage divider failed: {result['error']}")
            return False
        
        # Test RC filter
        print("Testing RC filter...")
        result = create_rc_low_pass_filter(1000.0)
        if 'error' not in result:
            print(f"✅ RC filter: {result['name']}")
            print(f"   Files: {len(result['generated_files'])}")
        else:
            print(f"❌ RC filter failed: {result['error']}")
            return False
        
        # Test LED circuit
        print("Testing LED circuit...")
        result = create_led_circuit(5.0)
        if 'error' not in result:
            print(f"✅ LED circuit: {result['name']}")
            print(f"   Files: {len(result['generated_files'])}")
        else:
            print(f"❌ LED circuit failed: {result['error']}")
            return False
        
        print("🎉 All circuit generation functions work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing circuit functions: {e}")
        return False

def test_circuit_generator_class():
    """Test the CircuitGenerator class"""
    print("\n🔌 Testing CircuitGenerator class...")
    
    try:
        from generate_circuit import CircuitGenerator
        
        # Create generator
        generator = CircuitGenerator()
        print("✅ CircuitGenerator created successfully")
        
        # Test custom circuit generation
        print("Testing custom circuit generation...")
        result = generator.generate_custom_circuit("Create a simple voltage divider")
        
        if result and 'error' not in result:
            print(f"✅ Custom circuit: {result['name']}")
            print(f"   Files: {len(result['generated_files'])}")
        else:
            print(f"❌ Custom circuit failed: {result.get('error', 'Unknown error')}")
            return False
        
        print("🎉 CircuitGenerator class works correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing CircuitGenerator: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing UI Fixes")
    print("=" * 40)
    
    tests = [
        ("Circuit Functions", test_circuit_functions),
        ("CircuitGenerator Class", test_circuit_generator_class)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The UI fixes are working correctly.")
        print("You can now use the UI at http://localhost:8516")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 