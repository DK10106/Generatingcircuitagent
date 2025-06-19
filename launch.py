#!/usr/bin/env python3
"""
Launcher script for KiCad AI Circuit Generator
Allows users to choose between different interfaces
"""

import subprocess
import sys
import os

def main():
    print("⚡ KiCad AI Circuit Generator")
    print("=" * 40)
    print("Choose your interface:")
    print()
    print("1. Simple Interface (Beginner-Friendly)")
    print("   - Button-based circuit generation")
    print("   - Easy to use, no typing required")
    print("   - Perfect for getting started")
    print()
    print("2. Chat Interface (Advanced)")
    print("   - Natural language input")
    print("   - More flexible and interactive")
    print("   - Better for complex requests")
    print()
    print("3. Test Circuit Generation")
    print("   - Run tests to verify everything works")
    print("   - Check if all dependencies are installed")
    print()
    print("4. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting Simple Interface...")
                print("Opening browser at: http://localhost:8501")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
                break
                
            elif choice == "2":
                print("\n🚀 Starting Chat Interface...")
                print("Opening browser at: http://localhost:8501")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "interface/chat_ui.py"])
                break
                
            elif choice == "3":
                print("\n🧪 Running Circuit Generation Tests...")
                subprocess.run([sys.executable, "test_circuit_generation.py"])
                break
                
            elif choice == "4":
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            break

if __name__ == "__main__":
    main() 