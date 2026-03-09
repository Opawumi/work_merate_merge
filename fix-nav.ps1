
# Fix navigation active states across all HTML pages
# This script ensures the correct nav-link has the 'active' class on each page

$basePath = "c:\Users\USER\workmerate"

# Define which pages belong to which nav category
$servicePages = @("services.html", "erp-pos.html", "ar-reporting.html", "ar-advisory.html", "regulatory-engagement.html", "managed.html", "advanced-intelligence.html")
$modulePages = @("hr.html", "financial-management.html", "tax-management.html", "project-management.html", "productivity-management.html", "sc-management.html", "custom-modules.html")
$resourcePages = @("compliance-calculator.html", "tax-calendar.html", "learning.html", "tax-laws.html", "state-irs.html")
$pricingPages = @("pricing.html")
$agenticPages = @("agentic-ai.html")
$aboutPages = @("about.html")
$noActivePages = @("index.html", "contact-us.html", "cookie-policy.html", "privacy.html", "terms-and-condition.html")

# Get all HTML files
$htmlFiles = Get-ChildItem -Path $basePath -Filter "*.html" -File

foreach ($file in $htmlFiles) {
    $fileName = $file.Name
    $filePath = $file.FullName
    $content = Get-Content -Path $filePath -Raw -Encoding UTF8
    $modified = $false
    
    # First, remove ALL existing 'active' classes from nav-links in the desktop nav
    # Handle: class="nav-link active" and class="nav-link active "
    $newContent = $content
    
    # Remove active from all nav-links (desktop menu only - between <ul class="nav-menu" and </ul>)
    # We'll do a simpler approach: just replace all nav-link active patterns
    $newContent = $newContent -replace 'class="nav-link active"', 'class="nav-link"'
    $newContent = $newContent -replace "class=""nav-link active """, 'class="nav-link"'
    
    # Now determine which nav-link should be active for this page
    $activeTarget = $null
    
    if ($servicePages -contains $fileName) {
        # Services dropdown link: href="services.html" with aria-haspopup
        $activeTarget = "services"
    } elseif ($modulePages -contains $fileName) {
        # Modules dropdown link: href="custom-modules.html" with aria-haspopup
        $activeTarget = "modules"
    } elseif ($resourcePages -contains $fileName) {
        # Resources dropdown link: href="learning.html" with aria-haspopup
        $activeTarget = "resources"
    } elseif ($pricingPages -contains $fileName) {
        $activeTarget = "pricing"
    } elseif ($agenticPages -contains $fileName) {
        $activeTarget = "agentic"
    } elseif ($aboutPages -contains $fileName) {
        $activeTarget = "about"
    }
    
    if ($activeTarget) {
        switch ($activeTarget) {
            "services" {
                # Find the Services nav-link with aria-haspopup and add active
                $newContent = $newContent -replace '(<a href="services\.html" class="nav-link")( aria-haspopup="true")', '$1 active$2'
            }
            "modules" {
                # Find the Modules nav-link with aria-haspopup and add active
                $newContent = $newContent -replace '(<a href="custom-modules\.html" class="nav-link")( aria-haspopup="true")', '$1 active$2'
            }
            "resources" {
                # Find the Resources nav-link with aria-haspopup and add active
                $newContent = $newContent -replace '(<a href="learning\.html" class="nav-link")( aria-haspopup="true")', '$1 active$2'
            }
            "pricing" {
                $newContent = $newContent -replace '(<a href="pricing\.html" class="nav-link")(>Pricing)', '$1 active$2'
                # Also handle the case where it's inside an li without nav-item class
                $newContent = $newContent -replace '(class="nav-link")(>Pricing)', 'class="nav-link active"$2'
            }
            "agentic" {
                $newContent = $newContent -replace '(<a href="agentic-ai\.html" class="nav-link")(>Agentic AI)', '$1 active$2'
                $newContent = $newContent -replace '(class="nav-link")(>Agentic AI)', 'class="nav-link active"$2'
            }
            "about" {
                $newContent = $newContent -replace '(<a href="about\.html" class="nav-link")(>About us)', '$1 active$2'
                $newContent = $newContent -replace '(class="nav-link")(>About us)', 'class="nav-link active"$2'
            }
        }
    }
    
    if ($newContent -ne $content) {
        Set-Content -Path $filePath -Value $newContent -NoNewline -Encoding UTF8
        Write-Host "Updated: $fileName"
        $modified = $true
    } else {
        Write-Host "No changes: $fileName"
    }
}

Write-Host "`nDone! All nav active states have been updated."
