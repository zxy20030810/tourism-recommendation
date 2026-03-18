from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import pandas as pd
import tensorflow as tf
import os
import json
import math
from tourism_recommendation.apps.destination.models import Destination, DestinationFeature
from django.contrib.auth import get_user_model

User = get_user_model()

def calculate_distance(lat1, lon1, lat2, lon2):
    """计算两点之间的距离（公里）"""
    R = 6371  # 地球半径（公里）
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return round(R * c, 1)

@api_view(['GET'])
def get_recommendations(request, user_id):
    """获取用户推荐"""
    try:
        is_guest = (user_id == 'guest' or str(user_id) == 'guest')
        
        if not is_guest:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        user_lat = float(request.query_params.get('lat', 34.3416))
        user_lon = float(request.query_params.get('lon', 108.9398))
        
        destinations = Destination.objects.all()
        
        recommendations = []
        for dest in destinations:
            features = DestinationFeature.objects.filter(destination=dest)
            feature_scores = {f.feature_name: f.feature_value for f in features}
            
            score = 0.7 + (dest.rating / 10)
            
            distance = None
            if dest.coordinates:
                try:
                    coords = dest.coordinates
                    if isinstance(coords, str):
                        coords = json.loads(coords)
                    dest_lat = coords.get('lat', 0)
                    dest_lon = coords.get('lon') or coords.get('lng', 0)
                    if dest_lat and dest_lon:
                        distance = calculate_distance(user_lat, user_lon, dest_lat, dest_lon)
                except:
                    pass
            
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
                'tags': dest.tags,
                'distance': distance
            })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return Response(recommendations[:10])
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