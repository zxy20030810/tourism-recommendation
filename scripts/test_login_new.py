import requests
import json

# 测试刚刚注册的用户登录
def test_new_user_login():
    base_url = "http://localhost:8000/api"
    
    # 使用刚刚注册的用户信息
    login_data = {
        "username": "testuser11",
        "password": "password11"
    }
    
    print("=== 测试新用户登录 ===")
    try:
        response = requests.post(f"{base_url}/user/login/", json=login_data, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        if response.status_code == 200:
            print("✓ 登录成功！")
        else:
            print("✗ 登录失败！")
            
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_new_user_login()
