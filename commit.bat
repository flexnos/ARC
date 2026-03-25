@echo off
echo Committing batch evaluation feature...
git add -A
git status
git commit -m "feat: Add batch evaluation endpoint with comprehensive UI

- Backend: Added /evaluate/batch endpoint in main.py
  * Accepts ZIP files with question.txt and student answer files
  * Auto-generates reference answers from questions  
  * Evaluates all students and returns statistics
  * Returns individual scores, average/highest/lowest metrics
  
- Frontend: Fixed batch upload and added results display
  * Corrected form field name from 'zip_archive' to 'batch_file'
  * Enabled auto-reference mode for batch uploads
  * Extended Result interface with batch-specific fields
  * Added comprehensive batch results UI component
  * Displays statistics dashboard and individual student results
  
- Testing: Created test_batch_endpoint.py for backend validation
  * Successfully tested with 5 student answers
  * Average processing time: 731ms

Resolves: Batch upload showing 0.00MB due to field name mismatch"
echo Done!
pause
