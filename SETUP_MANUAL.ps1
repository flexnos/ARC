# Manual Setup Script - Run this in PowerShell
# Copy and paste each line into PowerShell

Write-Host "========================================"
Write-Host "  MANUAL SETUP - STEP BY STEP"
Write-Host "========================================"
Write-Host ""

# Step 1: Check if we're in the right directory
Write-Host "Step 1: Navigate to project folder..."
Set-Location "d:\D down\bit"
Write-Host "Current location: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Step 2: Check Node.js is installed
Write-Host "Step 2: Checking Node.js..."
node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Node.js not found! Install from https://nodejs.org" -ForegroundColor Red
    pause
    exit
}
Write-Host "Node.js OK!" -ForegroundColor Green
Write-Host ""

# Step 3: Navigate to ui-react
Write-Host "Step 3: Going to ui-react folder..."
Set-Location "d:\D down\bit\ui-react"
Write-Host "Current location: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Step 4: Check if node_modules exists
Write-Host "Step 4: Checking if node_modules exists..."
if (Test-Path "node_modules") {
    Write-Host "node_modules already exists!" -ForegroundColor Yellow
    Write-Host "You can skip installation and go to Step 6" -ForegroundColor Yellow
} else {
    Write-Host "node_modules NOT found - need to install!" -ForegroundColor Red
    Write-Host ""
    
    # Step 5: Install dependencies
    Write-Host "Step 5: Installing npm packages (this takes 2-5 minutes)..."
    Write-Host "Please wait... downloading packages..." -ForegroundColor Cyan
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS! Installation complete!" -ForegroundColor Green
    } else {
        Write-Host "ERROR! Installation failed!" -ForegroundColor Red
        Write-Host "Try running as Administrator or check internet connection" -ForegroundColor Red
        pause
        exit
    }
}
Write-Host ""

# Step 6: Start backend
Write-Host "Step 6: Starting Backend Server..."
Write-Host "Opening new window for backend..." -ForegroundColor Cyan
Set-Location "d:\D down\bit"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn main:app --host 127.0.0.1 --port 8000"
Write-Host "Backend starting in new window..." -ForegroundColor Green
Write-Host ""

# Wait a bit
Start-Sleep -Seconds 3

# Step 7: Start frontend
Write-Host "Step 7: Starting Frontend UI..."
Write-Host "Opening new window for frontend..." -ForegroundColor Cyan
Set-Location "d:\D down\bit\ui-react"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"
Write-Host "Frontend starting in new window..." -ForegroundColor Green
Write-Host ""

Write-Host "========================================"
Write-Host "  BOTH SERVERS ARE STARTING!"
Write-Host "========================================"
Write-Host ""
Write-Host "Check the two new windows:"
Write-Host "  Backend:  http://localhost:8000"
Write-Host "  Frontend: http://localhost:3000"
Write-Host ""
Write-Host "Open your browser to: http://localhost:3000"
Write-Host ""
Write-Host "Press any key to open browser now..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open browser automatically
Start-Process "http://localhost:3000"
