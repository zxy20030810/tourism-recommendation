import requests
import json

# 测试登录功能
def test_login():
    base_url = "http://localhost:8000/api"
    
    # 测试不同的用户
    test_users = [
        {"username": "testuser11", "password": "password11"},
        {"username": "testuser10", "password": "password10"},
        {"username": "admin", "password": "admin"},
    ]
    
    for user_data in test_users:
        print(f"\n=== 测试用户: {user_data['username']} ===")
        try:
            response = requests.post(f"{base_url}/user/login/", json=user_data, timeout=5)
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            
            if response.status_code == 200:
                print("✓ 登录成功！")
            else:
                print("✗ 登录失败！")
                
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    test_login()
