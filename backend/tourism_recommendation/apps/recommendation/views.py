from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import pandas as pd
import tensorflow as tf
import os
import json
from tourism_recommendation.apps.destination.models import Destination, DestinationFeature
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
def get_recommendations(request, user_id):
    """获取用户推荐"""
    try:
        # 获取用户信息
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 获取所有目的地
        destinations = Destination.objects.all()
        
        # 构建推荐列表
        recommendations = []
        for dest in destinations[:5]:  # 限制返回前5个推荐
            # 获取目的地特征
            features = DestinationFeature.objects.filter(destination=dest)
            feature_scores = {f.feature_name: f.feature_value for f in features}
            
            # 计算推荐分数（简化版本）
            score = 0.7 + (dest.rating / 10)  # 基础分数 + 评分权重
            
            recommendations.append({
                'destination_id': dest.id,
                'destination_name': dest.name,
                'score': round(score, 2),
                'city': dest.city,
                'region': dest.region,
                'category': dest.category,
                'rating': dest.rating,
                'description': dest.description,
                'price_level': dest.price_level,
                'tags': dest.tags
            })
        
        # 按分数排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return Response(recommendations)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_user_preference(request, user_id):
    """更新用户偏好并重新计算推荐"""
    try:
        # 获取用户信息
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 更新用户偏好（这里简化处理）
        data = request.data
        if 'gender' in data:
            user.first_name = data['gender']
        if 'age' in data:
            user.last_name = str(data['age'])
        user.save()
        
        return Response({'message': '偏好更新成功'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)