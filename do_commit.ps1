# Run this in PowerShell to commit the changes

cd "d:\D down\bit"

Write-Host "=== Git Commit Script ===" -ForegroundColor Green
Write-Host ""

# Stage all changes
Write-Host "Staging changes..." -ForegroundColor Yellow
git add -A

# Show what will be committed
Write-Host "`nFiles to be committed:" -ForegroundColor Yellow
git status --short

# Commit
Write-Host "`nCommitting..." -ForegroundColor Yellow
git commit -m "feat: Add batch evaluation endpoint with comprehensive UI

- Backend: Added /evaluate/batch endpoint in main.py
  * Accepts ZIP files with question.txt and student answer files
  * Auto-generates reference answers from questions  
  * Evaluates all students and returns statistics
  
- Frontend: Fixed batch upload in ui-react/app/page.tsx
  * Corrected form field name from 'zip_archive' to 'batch_file'
  * Enabled auto-reference mode for batch uploads
  * Added comprehensive batch results display
  
- Testing: Created test_batch_endpoint.py for validation

Resolves: Batch upload 0.00MB issue due to field name mismatch"

Write-Host "`n=== Commit Complete! ===" -ForegroundColor Green
Write-Host "You can now push to GitHub with: git push" -ForegroundColor Cyan
