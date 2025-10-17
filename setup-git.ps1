# SitePeek - Git Setup and First Push

Write-Host 'Setting up Git for SitePeek...' -ForegroundColor Cyan

# Initialize git
Write-Host '`nInitializing Git repository...' -ForegroundColor Yellow
git init

# Add all files
Write-Host '`nAdding files to Git...' -ForegroundColor Yellow
git add .

# Commit
Write-Host '`nCreating first commit...' -ForegroundColor Yellow
git commit -m "Initial commit: SitePeek - WebSource Analyzer"

Write-Host '`nGit repository initialized successfully!' -ForegroundColor Green
Write-Host '`nNext Steps:' -ForegroundColor Cyan
Write-Host '1. Create a new repository on GitHub: https://github.com/new' -ForegroundColor White
Write-Host "2. Name it 'SitePeek'" -ForegroundColor White
Write-Host '3. Do not initialize with README' -ForegroundColor White
Write-Host '4. Run these commands (replace YOUR-USERNAME):' -ForegroundColor White
Write-Host '`n   git remote add origin https://github.com/YOUR-USERNAME/SitePeek.git' -ForegroundColor Gray
Write-Host '   git branch -M main' -ForegroundColor Gray
Write-Host '   git push -u origin main' -ForegroundColor Gray
Write-Host '`n5. See DEPLOYMENT.md for full deployment guide' -ForegroundColor White
Write-Host '`nGood luck with your deployment!' -ForegroundColor Magenta
