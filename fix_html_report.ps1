# PowerShell script to add Question, Student Answer, and Reference Answer to HTML report

$filePath = "ui-react\app\page.tsx"
$content = Get-Content $filePath -Raw

# Find the position after extractedText section
$insertAfter = '        ${result.extractedText ? `
        <div class="details-section">
            <h3>📝 Extracted Text (OCR)</h3>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; line-height: 1.8; color: #555;">
                ${result.extractedText}
            </div>
        </div>
        ` : ''}'

$newContent = '
        ${result.question || result.studentAnswer ? `
        <div class="details-section" style="background: #f8f9fa; border-top: 2px solid #e0e0e0;">
            <h3>📝 Evaluation Details</h3>
            
            ${result.question ? `
            <div style="margin-bottom: 24px;">
                <h4 style="color: #667eea; margin-bottom: 12px; font-size: 18px;">❓ Question:</h4>
                <div style="background: white; padding: 20px; border-radius: 8px; line-height: 1.8; color: #555; border-left: 4px solid #667eea;">
                    ${result.question}
                </div>
            </div>
            ` : ''}
            
            ${result.studentAnswer ? `
            <div style="margin-bottom: 24px;">
                <h4 style="color: #667eea; margin-bottom: 12px; font-size: 18px;">✍️ Student Answer:</h4>
                <div style="background: white; padding: 20px; border-radius: 8px; line-height: 1.8; color: #555; border-left: 4px solid #4CAF50;">
                    ${result.studentAnswer}
                </div>
            </div>
            ` : ''}
            
            ${result.referenceAnswer ? `
            <div style="margin-bottom: 24px;">
                <h4 style="color: #667eea; margin-bottom: 12px; font-size: 18px;">✅ Reference Answer:</h4>
                <div style="background: white; padding: 20px; border-radius: 8px; line-height: 1.8; color: #555; border-left: 4px solid #FF9800;">
                    ${result.referenceAnswer}
                </div>
            </div>
            ` : ''}
        </div>
        ` : ''}'

# Insert the new content
$updatedContent = $content.Replace($insertAfter, $insertAfter + $newContent)

# Save the file
$updatedContent | Set-Content $filePath -NoNewline

Write-Host "✅ Successfully added Question, Student Answer, and Reference Answer to HTML report!"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Refresh your browser (Ctrl+Shift+R)"
Write-Host "2. Test text evaluation"
Write-Host "3. Download HTML report - it will now show all content!"
