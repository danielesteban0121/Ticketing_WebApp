# Script de prueba para los endpoints de Categories

$baseUrl = "http://127.0.0.1:8001"
$token = "DANIELYKEVIN123"

Write-Host "🧪 TESTS - Categories Microservice" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
    Write-Host "✅ PASS: Health Check" -ForegroundColor Green
    Write-Host $response | ConvertTo-Json
    Write-Host ""
} catch {
    Write-Host "❌ FAIL: Health Check" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host ""
}

# Test 2: Get all categories
Write-Host "Test 2: Get all categories" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/categories" -Method GET
    Write-Host "✅ PASS: Get all categories" -ForegroundColor Green
    $response | ForEach-Object { Write-Host $_ }
    Write-Host ""
} catch {
    Write-Host "❌ FAIL: Get all categories" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host ""
}

# Test 3: Create category
Write-Host "Test 3: Create category" -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    # Usar UTF8 sin BOM
    $body = [System.Text.Encoding]::UTF8.GetBytes('{"name":"Conciertos","description":"Eventos de música"}')
    
    $response = Invoke-WebRequest -Uri "$baseUrl/categories" `
        -Method POST `
        -Headers $headers `
        -Body $body `
        -ContentType "application/json"
    
    Write-Host "✅ PASS: Create category" -ForegroundColor Green
    $content = $response.Content | ConvertFrom-Json
    Write-Host $content | ConvertTo-Json
    Write-Host ""
} catch {
    Write-Host "❌ FAIL: Create category" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host "Response: $($_.Exception.Response | ConvertFrom-Json | ConvertTo-Json)" -ForegroundColor Red
    Write-Host ""
}

# Test 4: Get category by ID
Write-Host "Test 4: Get category by ID (1)" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/categories/1" -Method GET
    Write-Host "✅ PASS: Get category by ID" -ForegroundColor Green
    Write-Host $response | ConvertTo-Json
    Write-Host ""
} catch {
    Write-Host "❌ FAIL: Get category by ID" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host ""
}

Write-Host "✅ TESTS COMPLETE" -ForegroundColor Green
