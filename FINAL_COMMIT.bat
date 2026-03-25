@echo off
echo ======================================
echo    BATCH EVALUATION COMMIT SCRIPT
echo ======================================
echo.

cd /d "%~dp0"

echo Checking git status...
git status --short

echo.
echo Committing changes...
git commit -m "feat: batch evaluation endpoint with UI fix

- Added /evaluate/batch endpoint (main.py)
- Fixed frontend batch upload field name (ui-react/app/page.tsx)
- Created test_batch_endpoint.py for validation
- Resolves: Batch upload 0.00MB issue"

if %errorlevel% equ 0 (
    echo.
    echo ======================================
    echo    SUCCESS! Commit completed!
    echo ======================================
    echo.
    echo Next step: Run 'git push' to upload to GitHub
) else (
    echo.
    echo ======================================
    echo    No changes to commit or error occurred
    echo ======================================
)

echo.
pause
