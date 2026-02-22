import requests

# 测试注册功能
def test_register():
    url = 'http://localhost:8000/api/user/register/'
    data = {
        'username': 'testuser12',
        'password': 'password12',
        'email': 'testuser12@example.com',
        'gender': '男',
        'age': 25
    }
    
    print('=== 测试注册功能 ===')
    print(f'请求数据: {data}')
    
    try:
        response = requests.post(url, json=data)
        print(f'状态码: {response.status_code}')
        print(f'响应: {response.json()}')
        
        if response.status_code == 201:
            print('✓ 注册成功！')
        else:
            print('✗ 注册失败')
    except Exception as e:
        print(f'请求异常: {str(e)}')

if __name__ == '__main__':
    test_register()
