import requests
import json

# 测试登录API
def test_login():
    url = "http://localhost:8000/api/user/login/"
    
    # 测试数据
    test_data = {
        "username": "testuser10",
        "password": "password10"
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✓ 登录成功！")
        else:
            print("✗ 登录失败！")
            
    except Exception as e:
        print(f"Error: {e}")

# 测试注册API
def test_register():
    url = "http://localhost:8000/api/user/register/"
    
    # 测试数据
    test_data = {
        "username": "testuser10",
        "password": "password10",
        "email": "testuser10@example.com",
        "gender": "male",
        "age": 25
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✓ 注册成功！")
        else:
            print("✗ 注册失败！")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== 测试登录API ===")
    test_login()
    print("\n=== 测试注册API ===")
    test_register()
