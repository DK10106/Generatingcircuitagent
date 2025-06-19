@echo off
echo Testing Git Installation...
echo ==================================================

echo.
echo Test 1: Basic git command
git --version
if %errorlevel% equ 0 (
    echo Git is working!
    echo.
    echo Next steps:
    echo 1. git add .
    echo 2. git commit -m "Fix Streamlit interface"
    echo 3. git push origin main
    goto :end
) else (
    echo Git command not found
)

echo.
echo Test 2: Full path to Git
if exist "C:\Program Files\Git\bin\git.exe" (
    echo Found Git at: C:\Program Files\Git\bin\git.exe
    "C:\Program Files\Git\bin\git.exe" --version
    if %errorlevel% equ 0 (
        echo Git works from full path!
        echo.
        echo You can use the full path for git commands:
        echo "C:\Program Files\Git\bin\git.exe" add .
        echo "C:\Program Files\Git\bin\git.exe" commit -m "Fix Streamlit interface"
        echo "C:\Program Files\Git\bin\git.exe" push origin main
        goto :end
    )
) else (
    echo Git not found at: C:\Program Files\Git\bin\git.exe
)

echo.
echo ==================================================
echo HOW TO FIX GIT PATH ISSUE
echo ==================================================
echo.
echo 1. CLOSE THIS TERMINAL WINDOW
echo 2. Open a NEW PowerShell window
echo 3. Navigate back to your project:
echo    cd "C:\Users\sdine\Generatingcircuitagent\Generatingcircuitagent"
echo 4. Test Git:
echo    git --version
echo.
echo If that doesn't work:
echo.
echo 5. Open System Properties:
echo    - Press Windows + R
echo    - Type: sysdm.cpl
echo    - Press Enter
echo    - Click "Environment Variables"
echo.
echo 6. Add Git to PATH:
echo    - Find "Path" in System Variables
echo    - Click "Edit"
echo    - Click "New"
echo    - Add: C:\Program Files\Git\bin
echo    - Click "OK" on all windows
echo.
echo 7. Restart your computer
echo.
echo 8. Open a new terminal and try again:
echo    git --version

:end
echo.
pause 