#!/usr/bin/env python3
"""
Test script to verify the improvements to the KiCad circuit generator
"""

import os
import sys
from datetime import datetime

def test_environment_setup():
    """Test KiCad environment setup"""
    print("🔧 Testing KiCad environment setup...")
    
    try:
        from generate_circuit import setup_kicad_env
        
        result = setup_kicad_env()
        if result:
            print("✅ KiCad environment setup successful")
            return True
        else:
            print("❌ KiCad environment setup failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in environment setup: {e}")
        return False

def test_circuit_generation():
    """Test circuit generation functions"""
    print("\n🔌 Testing circuit generation...")
    
    try:
        from generate_circuit import CircuitGenerator
        
        # Initialize generator
        generator = CircuitGenerator()
        print("✅ CircuitGenerator initialized")
        
        # Test voltage divider
        print("Testing voltage divider...")
        result = generator.generate_voltage_divider(5.0, 3.3)
        if 'error' not in result:
            print(f"✅ Voltage divider generated: {result['name']}")
            print(f"   Files: {len(result['generated_files'])}")
        else:
            print(f"❌ Voltage divider failed: {result['error']}")
            return False
        
        # Test RC filter
        print("Testing RC filter...")
        result = generator.generate_rc_filter(1000.0)
        if 'error' not in result:
            print(f"✅ RC filter generated: {result['name']}")
            print(f"   Files: {len(result['generated_files'])}")
        else:
            print(f"❌ RC filter failed: {result['error']}")
            return False
        
        # Test LED circuit
        print("Testing LED circuit...")
        result = generator.generate_led_circuit(5.0)
        if 'error' not in result:
            print(f"✅ LED circuit generated: {result['name']}")
            print(f"   Files: {len(result['generated_files'])}")
        else:
            print(f"❌ LED circuit failed: {result['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error in circuit generation: {e}")
        return False

def test_llm_integration():
    """Test LLM integration"""
    print("\n🤖 Testing LLM integration...")
    
    try:
        from llm_engine import LLMEngine
        
        # Initialize LLM engine
        llm_engine = LLMEngine()
        print("✅ LLMEngine initialized")
        
        # Test simple circuit generation
        test_request = "Create a simple voltage divider that converts 12V to 5V"
        print(f"Testing LLM with request: {test_request}")
        
        result = llm_engine.generate_and_execute_circuit(test_request)
        if result and 'error' not in result:
            print(f"✅ LLM circuit generated: {result['name']}")
            print(f"   Files: {len(result['generated_files'])}")
            return True
        else:
            print(f"❌ LLM circuit failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error in LLM integration: {e}")
        return False

def test_file_generation():
    """Test that files are actually created"""
    print("\n📁 Testing file generation...")
    
    try:
        # Check output directories
        output_dirs = [
            "kicad_output/voltage_divider",
            "kicad_output/rc_low_pass_filter", 
            "kicad_output/led_circuit"
        ]
        
        total_files = 0
        for output_dir in output_dirs:
            if os.path.exists(output_dir):
                files = os.listdir(output_dir)
                print(f"✅ {output_dir}: {len(files)} files")
                total_files += len(files)
                
                # Check for specific file types
                netlist_files = [f for f in files if f.endswith('.net')]
                project_files = [f for f in files if f.endswith('.kicad_pro')]
                
                print(f"   Netlist files: {len(netlist_files)}")
                print(f"   Project files: {len(project_files)}")
            else:
                print(f"❌ Directory not found: {output_dir}")
        
        print(f"Total files generated: {total_files}")
        return total_files > 0
        
    except Exception as e:
        print(f"❌ Error checking files: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting KiCad Circuit Generator Tests")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Circuit Generation", test_circuit_generation),
        ("LLM Integration", test_llm_integration),
        ("File Generation", test_file_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The improvements are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 