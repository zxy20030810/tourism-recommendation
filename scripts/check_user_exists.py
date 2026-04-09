#!/usr/bin/env python3
"""
检查用户是否存在并验证密码
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

import django
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourism_recommendation.settings')

# 初始化Django
django.setup()

from tourism_recommendation.apps.user.models import User

# 检查用户
def check_user(username, password):
    print(f"检查用户: {username}")
    
    try:
        # 尝试获取用户
        user = User.objects.get(username=username)
        print(f"用户存在: {user.username}")
        print(f"  用户ID: {user.id}")
        print(f"  邮箱: {user.email}")
        
        # 验证密码
        is_valid = check_password(password, user.password)
        print(f"  密码验证: {'正确' if is_valid else '错误'}")
        
        # 使用authenticate验证
        auth_user = authenticate(username=username, password=password)
        print(f"  authenticate结果: {'成功' if auth_user else '失败'}")
        
        return True
        
    except User.DoesNotExist:
        print(f"用户不存在: {username}")
        return False
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

# 列出所有用户
def list_users():
    print("\n所有用户:")
    try:
        users = User.objects.all()
        if users:
            for user in users:
                print(f"- {user.username} (ID: {user.id}, 邮箱: {user.email})")
        else:
            print("  没有用户")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    print("=== 用户检查工具 ===")
    print()
    
    # 检查测试用户
    check_user('testuser', 'test123456')
    
    # 检查其他可能的用户
    print()
    check_user('admin', 'admin123')
    
    # 列出所有用户
    list_users()