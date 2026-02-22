# 前后端连接测试

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_backend_api():
    """测试后端API连接"""
    print("=== 测试后端API连接 ===")
    
    # 1. 测试用户登录
    print("\n1. 测试用户登录...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/user/login/", json=login_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        if response.status_code == 200:
            print("✅ 登录测试成功")
            return response.json().get('user_id')
        else:
            print("❌ 登录测试失败")
            return None
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return None

def test_destination_list():
    """测试目的地列表API"""
    print("\n2. 测试目的地列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/destination/list/")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取到 {len(data)} 个目的地")
            if data:
                print(f"第一个目的地: {data[0]['name']}")
            return True
        else:
            print("❌ 获取目的地列表失败")
            return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_recommendations(user_id):
    """测试推荐API"""
    print(f"\n3. 测试推荐API (用户ID: {user_id})...")
    try:
        response = requests.get(f"{BASE_URL}/api/recommendation/user/{user_id}/")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取到 {len(data)} 个推荐")
            if data:
                for i, rec in enumerate(data[:3], 1):
                    print(f"  {i}. {rec['destination_name']} (评分: {rec['score']})")
            return True
        else:
            print("❌ 获取推荐失败")
            return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_destination_detail():
    """测试目的地详情API"""
    print("\n4. 测试目的地详情...")
    try:
        response = requests.get(f"{BASE_URL}/api/destination/detail/1/")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取目的地详情成功")
            print(f"目的地名称: {data.get('name')}")
            print(f"城市: {data.get('city')}")
            print(f"评分: {data.get('rating')}")
            return True
        else:
            print("❌ 获取目的地详情失败")
            return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试前后端连接...\n")
    
    # 测试后端API
    user_id = test_backend_api()
    test_destination_list()
    if user_id:
        test_recommendations(user_id)
    test_destination_detail()
    
    print("\n" + "="*50)
    print("✅ 后端API测试完成！")
    print("="*50)
    print("\n💡 提示：")
    print("- 前端地址: http://localhost:3000/")
    print("- 后端地址: http://127.0.0.1:8000/")
    print("- 测试账号: testuser / testpass123")
    print("\n🎯 下一步：在浏览器中打开前端应用进行完整测试")