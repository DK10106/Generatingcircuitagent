#!/usr/bin/env python3
"""
Test script to verify LLM execution functionality
"""

import os
import sys
from datetime import datetime

def test_llm_execution():
    """Test the LLM execution functionality"""
    print("🧪 Testing LLM Execution Functionality")
    print("=" * 50)
    
    try:
        # Import the LLMEngine
        from llm_engine import LLMEngine
        
        # Initialize LLMEngine
        print("Initializing LLMEngine...")
        llm_engine = LLMEngine()
        print("✅ LLMEngine initialized")
        
        # Test 1: Simple voltage divider request
        print("\n1. Testing simple voltage divider request...")
        user_request = "Create a voltage divider that converts 5V to 3.3V"
        
        result = llm_engine.generate_and_execute_circuit(user_request)
        
        if result['success']:
            print(f"✅ Circuit generated successfully!")
            print(f"   Circuit Name: {result['circuit_name']}")
            print(f"   Files Created: {len(result['generated_files'])}")
            for file_path in result['generated_files']:
                if os.path.exists(file_path):
                    print(f"   ✓ {os.path.basename(file_path)}")
                else:
                    print(f"   ❌ {os.path.basename(file_path)} - File not found")
            
            # Show the generated code
            if result.get('code'):
                print(f"\n   Generated Code Preview:")
                code_lines = result['code'].split('\n')[:10]  # Show first 10 lines
                for line in code_lines:
                    print(f"   {line}")
                if len(result['code'].split('\n')) > 10:
                    print(f"   ... ({len(result['code'].split('\n')) - 10} more lines)")
        else:
            print(f"❌ Circuit generation failed: {result['message']}")
            if result.get('response'):
                print(f"   AI Response: {result['response'][:200]}...")
        
        # Test 2: RC filter request
        print("\n2. Testing RC filter request...")
        user_request = "Generate an RC low-pass filter with 1kHz cutoff frequency"
        
        result = llm_engine.generate_and_execute_circuit(user_request)
        
        if result['success']:
            print(f"✅ RC filter generated successfully!")
            print(f"   Circuit Name: {result['circuit_name']}")
            print(f"   Files Created: {len(result['generated_files'])}")
            for file_path in result['generated_files']:
                if os.path.exists(file_path):
                    print(f"   ✓ {os.path.basename(file_path)}")
                else:
                    print(f"   ❌ {os.path.basename(file_path)} - File not found")
        else:
            print(f"❌ RC filter generation failed: {result['message']}")
        
        # Test 3: LED circuit request
        print("\n3. Testing LED circuit request...")
        user_request = "Design a simple LED circuit with current limiting resistor"
        
        result = llm_engine.generate_and_execute_circuit(user_request)
        
        if result['success']:
            print(f"✅ LED circuit generated successfully!")
            print(f"   Circuit Name: {result['circuit_name']}")
            print(f"   Files Created: {len(result['generated_files'])}")
            for file_path in result['generated_files']:
                if os.path.exists(file_path):
                    print(f"   ✓ {os.path.basename(file_path)}")
                else:
                    print(f"   ❌ {os.path.basename(file_path)} - File not found")
        else:
            print(f"❌ LED circuit generation failed: {result['message']}")
        
        # Check output directories
        print("\n📁 Checking output directories...")
        output_base = 'kicad_output'
        if os.path.exists(output_base):
            for circuit_dir in os.listdir(output_base):
                circuit_path = os.path.join(output_base, circuit_dir)
                if os.path.isdir(circuit_path):
                    files = os.listdir(circuit_path)
                    print(f"✅ {circuit_path}: {len(files)} files")
                    for file in files:
                        print(f"   - {file}")
        else:
            print(f"❌ {output_base}: Directory not found")
        
        print("\n🎉 LLM execution test completed!")
        print("\nThe chat interface should now be able to:")
        print("1. Generate circuit code using AI")
        print("2. Execute the code safely")
        print("3. Create downloadable KiCad files")
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Make sure all required modules are installed:")
        print("pip install streamlit skidl ollama")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_execution() 