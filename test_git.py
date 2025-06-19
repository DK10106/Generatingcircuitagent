import subprocess
import os
import sys

def test_git_installation():
    """Test if Git is accessible and show diagnostic information"""
    print("🔍 Testing Git Installation...")
    print("=" * 50)
    
    # Test 1: Basic git command
    print("Test 1: Basic git command")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git is working: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Git command failed: {result.stderr}")
    except FileNotFoundError:
        print("❌ Git command not found")
    
    # Test 2: Full path to Git
    print("\nTest 2: Full path to Git")
    git_paths = [
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe"
    ]
    
    for git_path in git_paths:
        if os.path.exists(git_path):
            print(f"✅ Found Git at: {git_path}")
            try:
                result = subprocess.run([git_path, '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Git works from full path: {result.stdout.strip()}")
                    return git_path
            except Exception as e:
                print(f"❌ Error running Git from full path: {e}")
        else:
            print(f"❌ Git not found at: {git_path}")
    
    # Test 3: Check PATH environment
    print("\nTest 3: Checking PATH environment")
    path = os.environ.get('PATH', '')
    git_in_path = any('git' in p.lower() for p in path.split(';'))
    print(f"Git in PATH: {'✅ Yes' if git_in_path else '❌ No'}")
    
    # Show PATH entries that might contain Git
    git_path_entries = [p for p in path.split(';') if 'git' in p.lower()]
    if git_path_entries:
        print("Git-related PATH entries:")
        for entry in git_path_entries:
            print(f"  - {entry}")
    else:
        print("No Git-related entries found in PATH")
    
    return False

def fix_git_path():
    """Provide instructions to fix Git PATH issue"""
    print("\n" + "=" * 50)
    print("🔧 HOW TO FIX GIT PATH ISSUE")
    print("=" * 50)
    
    print("""
1. CLOSE THIS TERMINAL WINDOW
2. Open a NEW PowerShell window
3. Navigate back to your project:
   cd "C:\\Users\\sdine\\Generatingcircuitagent\\Generatingcircuitagent"
4. Test Git:
   git --version

If that doesn't work:

5. Open System Properties:
   - Press Windows + R
   - Type: sysdm.cpl
   - Press Enter
   - Click "Environment Variables"

6. Add Git to PATH:
   - Find "Path" in System Variables
   - Click "Edit"
   - Click "New"
   - Add: C:\\Program Files\\Git\\bin
   - Click "OK" on all windows

7. Restart your computer

8. Open a new terminal and try again:
   git --version
""")

if __name__ == "__main__":
    git_working = test_git_installation()
    
    if git_working:
        print("\n✅ Git is working! You can now use git commands.")
        print("\nNext steps:")
        print("1. git add .")
        print("2. git commit -m \"Fix Streamlit interface\"")
        print("3. git push origin main")
    else:
        fix_git_path() 