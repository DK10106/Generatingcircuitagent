import os
import sys
import subprocess

def setup_environment():
    # Set up KiCad environment variables
    kicad_symbols_path = os.path.join("C:", "Program Files", "KiCad", "7.0", "share", "kicad", "symbols")
    os.environ["KICAD_SYMBOL_DIR"] = kicad_symbols_path
    os.environ["KICAD6_SYMBOL_DIR"] = kicad_symbols_path
    os.environ["KICAD7_SYMBOL_DIR"] = kicad_symbols_path
    os.environ["KICAD8_SYMBOL_DIR"] = kicad_symbols_path

    # Set up PATH to include both Machine and User paths
    try:
        import winreg
        
        # Get Machine PATH
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_READ) as key:
            machine_path = winreg.QueryValueEx(key, "Path")[0]
        
        # Get User PATH
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
            user_path = winreg.QueryValueEx(key, "Path")[0]
        
        # Combine paths
        full_path = machine_path + ";" + user_path
        os.environ["PATH"] = full_path
        
        # Verify Ollama is accessible
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("ERROR: Ollama is not accessible. Please ensure it's properly installed.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error setting up environment: {str(e)}")
        sys.exit(1)

# Set up environment before importing other modules
setup_environment()

from interface.chat_ui import main

if __name__ == "__main__":
    main() 