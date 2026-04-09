#!/usr/bin/env python3
"""
重置用户密码
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourism_recommendation.settings')

import django
from django.contrib.auth.hashers import make_password

# 初始化Django
django.setup()

from tourism_recommendation.apps.user.models import User

def reset_password(username, new_password):
    print(f"重置用户 {username} 的密码...")
    
    try:
        user = User.objects.get(username=username)
        user.password = make_password(new_password)
        user.save()
        print(f"密码重置成功！用户 {username} 的密码已设置为: {new_password}")
        return True
        
    except User.DoesNotExist:
        print(f"用户 {username} 不存在")
        return False
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== 密码重置工具 ===")
    print()
    
    # 重置testuser的密码
    reset_password('testuser', 'test123456')
    
    print()
    print("=== 密码重置完成 ===")