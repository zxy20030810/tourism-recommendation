import requests
import json

# 模拟前端登录请求
def test_frontend_login_simulation():
    # 模拟前端的请求路径
    login_url = "http://localhost:3000/user/login/"
    
    # 测试数据
    login_data = {
        "username": "testuser11",
        "password": "password11"
    }
    
    print("=== 模拟前端登录请求 ===")
    try:
        # 模拟前端的请求，使用与前端相同的URL格式
        response = requests.post(login_url, json=login_data, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        if response.status_code == 200:
            print("✓ 登录成功！")
        else:
            print("✗ 登录失败！")
            
    except Exception as e:
        print(f"错误: {e}")
        
    # 同时测试直接访问后端API
    print("\n=== 直接访问后端API ===")
    backend_url = "http://localhost:8000/api/user/login/"
    try:
        response = requests.post(backend_url, json=login_data, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        if response.status_code == 200:
            print("✓ 登录成功！")
        else:
            print("✗ 登录失败！")
            
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_frontend_login_simulation()
