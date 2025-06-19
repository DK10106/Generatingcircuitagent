#!/usr/bin/env python3
"""
Test script to verify KiCad CLI is accessible
"""

import os
import subprocess
from generate_circuit import setup_kicad_env

def test_kicad_cli():
    print("Testing KiCad CLI accessibility...")
    
    # First, setup the environment
    setup_kicad_env()
    
    # Check if kicad-cli is in PATH
    print(f"PATH contains KiCad: {'KiCad' in os.environ.get('PATH', '')}")
    
    # Try to run kicad-cli
    try:
        result = subprocess.run(['kicad-cli', '--version'], 
                              capture_output=True, text=True, timeout=10)
        print(f"Exit code: {result.returncode}")
        print(f"Output: {result.stdout.strip()}")
        print(f"Error: {result.stderr.strip()}")
        
        if result.returncode == 0:
            print("✅ KiCad CLI is accessible!")
            return True
        else:
            print("❌ KiCad CLI returned error")
            return False
            
    except FileNotFoundError:
        print("❌ KiCad CLI not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Error running KiCad CLI: {e}")
        return False

if __name__ == "__main__":
    test_kicad_cli() 