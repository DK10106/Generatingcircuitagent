import os
import sys
import subprocess
import winreg
from pathlib import Path

def add_git_to_path():
    """Add Git to the system PATH environment variable"""
    print("Adding Git to PATH Environment Variable...")
    print("=" * 60)
    
    # Git installation paths to check
    git_paths = [
        r"C:\Program Files\Git\bin",
        r"C:\Program Files\Git\cmd",
        r"C:\Program Files (x86)\Git\bin",
        r"C:\Program Files (x86)\Git\cmd"
    ]
    
    # Find which Git path exists
    git_path = None
    for path in git_paths:
        if os.path.exists(path):
            git_path = path
            print(f"Found Git at: {git_path}")
            break
    
    if not git_path:
        print("Git installation not found in common locations")
        print("Please install Git first from: https://git-scm.com/download/win")
        return False
    
    try:
        # Open the registry key for system environment variables
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE
        )
        
        # Get current PATH
        current_path, _ = winreg.QueryValueEx(key, "Path")
        print(f"Current PATH: {current_path[:100]}...")
        
        # Check if Git is already in PATH
        if git_path in current_path:
            print("Git is already in PATH!")
            winreg.CloseKey(key)
            return True
        
        # Add Git to PATH
        new_path = current_path + ";" + git_path
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        
        print(f"Successfully added {git_path} to PATH")
        print("\nIMPORTANT: You need to restart your terminal for changes to take effect!")
        print("Please close this terminal and open a new one.")
        
        return True
        
    except PermissionError:
        print("Permission denied. This script needs to be run as Administrator.")
        print("\nPlease run this script as Administrator:")
        print("1. Right-click on PowerShell/Command Prompt")
        print("2. Select 'Run as Administrator'")
        print("3. Navigate to your project folder")
        print("4. Run: python add_git_to_path.py")
        return False
        
    except Exception as e:
        print(f"Error adding Git to PATH: {str(e)}")
        return False

def manual_instructions():
    """Provide manual instructions for adding Git to PATH"""
    print("\n" + "=" * 60)
    print("MANUAL INSTRUCTIONS (if automated method fails)")
    print("=" * 60)
    print("""
1. Press Windows + R
2. Type: sysdm.cpl
3. Press Enter
4. Click "Environment Variables" button
5. In "System Variables" section, find "Path"
6. Click "Edit"
7. Click "New"
8. Add: C:\\Program Files\\Git\\bin
9. Click "OK" on all windows
10. Restart your terminal
11. Test with: git --version
""")

def test_git_path():
    """Test if Git is now accessible"""
    print("\nTesting Git access...")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Git is working: {result.stdout.strip()}")
            return True
        else:
            print(f"Git test failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Git command not found - PATH may not be updated yet")
        return False

if __name__ == "__main__":
    print("Git PATH Configuration Tool")
    print("=" * 60)
    
    # Try automated method
    success = add_git_to_path()
    
    if success:
        print("\nTesting Git access...")
        if test_git_path():
            print("\nSUCCESS! Git is now accessible from anywhere.")
            print("\nYou can now use git commands normally:")
            print("git add .")
            print("git commit -m \"Your message\"")
            print("git push origin main")
        else:
            print("\nGit not accessible yet. Please restart your terminal and try again.")
    else:
        manual_instructions()
    
    print("\nPress Enter to exit...")
    input() 