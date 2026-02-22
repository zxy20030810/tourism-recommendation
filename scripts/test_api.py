import requests
import json

# 测试API连接
def test_api_connection():
    base_url = "http://localhost:8000/api"
    
    # 测试1: 检查API是否可以访问
    print("=== 测试API连接 ===")
    try:
        response = requests.get(f"{base_url}/user/login/", timeout=5)
        print(f"GET /api/user/login/ 状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试2: 测试登录
    print("\n=== 测试登录 ===")
    login_data = {
        "username": "testuser10",
        "password": "password10"
    }
    
    try:
        # 禁用CSRF验证进行测试
        response = requests.post(f"{base_url}/user/login/", json=login_data, timeout=5)
        print(f"POST /api/user/login/ 状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试3: 测试注册
    print("\n=== 测试注册 ===")
    register_data = {
        "username": "testuser11",
        "password": "password11",
        "email": "testuser11@example.com",
        "gender": "male",
        "age": 25
    }
    
    try:
        response = requests.post(f"{base_url}/user/register/", json=register_data, timeout=5)
        print(f"POST /api/user/register/ 状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_api_connection()
