# API Test Script

Write-Host "Starting API tests..." -ForegroundColor Green

# Test 1: User Registration
Write-Host "`n1. Testing user registration..." -ForegroundColor Yellow
$body = @{
    username = "testuser"
    password = "testpass123"
    email = "test@example.com"
    gender = "male"
    age = 25
} | ConvertTo-Json

try {
    $registerResult = Invoke-RestMethod -Uri "http://localhost:8000/api/user/register/" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Registration successful: $registerResult" -ForegroundColor Green
} catch {
    Write-Host "Registration failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: User Login
Write-Host "`n2. Testing user login..." -ForegroundColor Yellow
$body = @{
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json

try {
    $loginResult = Invoke-RestMethod -Uri "http://localhost:8000/api/user/login/" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Login successful" -ForegroundColor Green
    $token = $loginResult.token
    Write-Host "Token: $token" -ForegroundColor Cyan
} catch {
    Write-Host "Login failed: $($_.Exception.Message)" -ForegroundColor Red
    $token = $null
}

# Test 3: Get User Profile
if ($token) {
    Write-Host "`n3. Testing get user profile..." -ForegroundColor Yellow
    $headers = @{
        "Authorization" = "Token $token"
    }

    try {
        $profileResult = Invoke-RestMethod -Uri "http://localhost:8000/api/user/info/1/" -Method Get -Headers $headers
        Write-Host "User profile retrieved successfully" -ForegroundColor Green
        Write-Host "Username: $($profileResult.username)" -ForegroundColor Cyan
    } catch {
        Write-Host "Get user profile failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 4: Get Destination List
Write-Host "`n4. Testing get destination list..." -ForegroundColor Yellow
try {
    $destinations = Invoke-RestMethod -Uri "http://localhost:8000/api/destination/list/" -Method Get
    Write-Host "Destination list retrieved successfully, total $($destinations.Count) destinations" -ForegroundColor Green
} catch {
    Write-Host "Get destination list failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Get Destination Detail
Write-Host "`n5. Testing get destination detail..." -ForegroundColor Yellow
try {
    $destinationDetail = Invoke-RestMethod -Uri "http://localhost:8000/api/destination/detail/1/" -Method Get
    Write-Host "Destination detail retrieved successfully" -ForegroundColor Green
    Write-Host "Destination name: $($destinationDetail.name)" -ForegroundColor Cyan
} catch {
    Write-Host "Get destination detail failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: Get Recommendations
if ($token) {
    Write-Host "`n6. Testing get recommendations..." -ForegroundColor Yellow
    $headers = @{
        "Authorization" = "Token $token"
    }

    try {
        $recommendations = Invoke-RestMethod -Uri "http://localhost:8000/api/recommendation/user/1/" -Method Get -Headers $headers
        Write-Host "Recommendations retrieved successfully" -ForegroundColor Green
        Write-Host "Recommendation count: $($recommendations.Count)" -ForegroundColor Cyan
    } catch {
        Write-Host "Get recommendations failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nTests completed!" -ForegroundColor Green