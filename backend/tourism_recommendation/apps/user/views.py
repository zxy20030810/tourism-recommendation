from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
@api_view(['POST'])
def register(request):
    """用户注册"""
    data = request.data
    try:
        user = User.objects.create(
            username=data.get('username'),
            password=make_password(data.get('password')),
            email=data.get('email', ''),
            gender=data.get('gender', ''),
            age=data.get('age', None),
            travel_type=data.get('travel_type', ''),
            budget_level=data.get('budget_level', '')
        )
        return Response({'message': '注册成功', 'user_id': user.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def user_login(request):
    """用户登录"""
    print(f"收到登录请求: {request.data}")
    username = request.data.get('username')
    password = request.data.get('password')
    
    print(f"用户名: {username}, 密码: {password}")
    
    if not username or not password:
        return Response({'error': '用户名和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = authenticate(request, username=username, password=password)
        print(f"认证结果: {user}")
        
        if user:
            login(request, user)
            print(f"登录成功，用户ID: {user.id}")
            return Response({'message': '登录成功', 'user_id': user.id, 'token': 'test_token_' + str(user.id)})
        else:
            print("认证失败：用户名或密码错误")
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(f"登录过程中发生错误: {str(e)}")
        return Response({'error': f'登录失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def user_logout(request):
    """用户登出"""
    logout(request)
    return Response({'message': '登出成功'})

@api_view(['GET'])
def get_user_info(request, user_id):
    """获取用户信息"""
    try:
        user = User.objects.get(id=user_id)
        return Response({
            'username': user.username,
            'email': user.email,
            'gender': user.gender,
            'age': user.age,
            'travel_type': user.travel_type,
            'budget_level': user.budget_level,
            'favorite_regions': user.favorite_regions,
            'favorite_attractions': user.favorite_attractions
        })
    except User.DoesNotExist:
        return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_user_preference(request, user_id):
    """更新用户偏好"""
    try:
        user = User.objects.get(id=user_id)
        data = request.data
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        user.gender = data.get('gender', user.gender)
        user.age = data.get('age', user.age)
        user.travel_type = data.get('travel_type', user.travel_type)
        user.budget_level = data.get('budget_level', user.budget_level)
        user.favorite_regions = data.get('favorite_regions', user.favorite_regions)
        user.favorite_attractions = data.get('favorite_attractions', user.favorite_attractions)
        user.save()
        return Response({'message': '偏好更新成功'})
    except User.DoesNotExist:
        return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)