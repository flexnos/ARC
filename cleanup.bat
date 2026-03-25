@echo off
echo Cleaning up documentation and test files...

:: Delete all .md files except README.md
del /Q *.md
echo Deleted all .md files

:: Delete test files
del /Q test_*.py check_*.py quick_*.py create_*.py fix_*.py main_minimal.py
echo Deleted test Python files

:: Delete batch test files
del /Q batch_test.zip
rmdir /S /Q batch_test
echo Deleted batch test files

:: Delete other unnecessary files
del /Q ADD_REPORT_CONTENT.txt COPY_THESE_COMMANDS.bat
echo Cleanup complete!
