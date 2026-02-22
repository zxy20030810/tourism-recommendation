from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Destination
import json

def get_destination_list(request):
    """
    获取目的地列表
    """
    if request.method == 'GET':
        try:
            # 获取查询参数
            category = request.GET.get('category')
            region = request.GET.get('region')
            min_rating = request.GET.get('min_rating')
            
            # 构建查询
            queryset = Destination.objects.all()
            
            if category:
                queryset = queryset.filter(category=category)
            
            if region:
                queryset = queryset.filter(region=region)
            
            if min_rating:
                queryset = queryset.filter(rating__gte=float(min_rating))
            
            # 序列化结果
            destinations = []
            for dest in queryset:
                destinations.append({
                    'destination_id': dest.id,
                    'destination_name': dest.name,
                    'city': dest.city,
                    'region': dest.region,
                    'category': dest.category,
                    'price_level': dest.price_level,
                    'rating': dest.rating,
                    'review_count': dest.review_count,
                    'description': dest.description[:100] + '...' if len(dest.description) > 100 else dest.description
                })
            
            return JsonResponse({'destinations': destinations})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '方法不允许'}, status=405)

def get_destination_detail(request, destination_id):
    """
    获取目的地详情
    """
    if request.method == 'GET':
        try:
            destination = Destination.objects.get(id=destination_id)
            
            # 序列化结果
            dest_data = {
                'id': destination.id,
                'name': destination.name,
                'city': destination.city,
                'region': destination.region,
                'category': destination.category,
                'price_level': destination.price_level,
                'rating': destination.rating,
                'review_count': destination.review_count,
                'description': destination.description,
                'facilities': destination.facilities,
                'tags': destination.tags,
                'popular_season': destination.popular_season,
                'visitor_volume': destination.visitor_volume,
                'images': destination.images
            }
            
            return JsonResponse(dest_data)
        
        except Destination.DoesNotExist:
            return JsonResponse({'error': '目的地不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '方法不允许'}, status=405)

@csrf_exempt
def search_destination(request):
    """
    搜索目的地
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            keyword = data.get('keyword', '')
            
            # 搜索名称和描述
            queryset = Destination.objects.filter(
                name__icontains=keyword
            ) | Destination.objects.filter(
                description__icontains=keyword
            ) | Destination.objects.filter(
                city__icontains=keyword
            ) | Destination.objects.filter(
                region__icontains=keyword
            )
            
            # 去重
            queryset = queryset.distinct()
            
            # 序列化结果
            destinations = []
            for dest in queryset:
                destinations.append({
                    'destination_id': dest.id,
                    'destination_name': dest.name,
                    'city': dest.city,
                    'region': dest.region,
                    'category': dest.category,
                    'price_level': dest.price_level,
                    'rating': dest.rating,
                    'description': dest.description[:100] + '...' if len(dest.description) > 100 else dest.description
                })
            
            return JsonResponse({'destinations': destinations})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '方法不允许'}, status=405)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Destination

@api_view(['GET'])
def get_destinations(request):
    """获取所有目的地"""
    destinations = Destination.objects.all()
    result = []
    for dest in destinations:
        result.append({
            'id': dest.id,
            'name': dest.name,
            'city': dest.city,
            'region': dest.region,
            'category': dest.category,
            'rating': dest.rating,
            'price_level': dest.price_level,
            'popular_season': dest.popular_season
        })
    return Response(result)

@api_view(['GET'])
def get_destination_detail(request, destination_id):
    """获取目的地详情"""
    try:
        dest = Destination.objects.get(id=destination_id)
        return Response({
            'id': dest.id,
            'name': dest.name,
            'city': dest.city,
            'region': dest.region,
            'description': dest.description,
            'category': dest.category,
            'rating': dest.rating,
            'review_count': dest.review_count,
            'price_level': dest.price_level,
            'popular_season': dest.popular_season,
            'visitor_volume': dest.visitor_volume,
            'facilities': dest.facilities,
            'tags': dest.tags,
            'coordinates': dest.coordinates,
            'images': dest.images
        })
    except Destination.DoesNotExist:
        return Response({'error': '目的地不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def search_destinations(request):
    """搜索目的地"""
    keyword = request.query_params.get('keyword', '')
    category = request.query_params.get('category', '')
    region = request.query_params.get('region', '')
    
    queryset = Destination.objects.all()
    if keyword:
        queryset = queryset.filter(name__icontains=keyword) | queryset.filter(city__icontains=keyword)
    if category:
        queryset = queryset.filter(category=category)
    if region:
        queryset = queryset.filter(region=region)
    
    result = []
    for dest in queryset:
        result.append({
            'id': dest.id,
            'name': dest.name,
            'city': dest.city,
            'region': dest.region,
            'category': dest.category,
            'rating': dest.rating,
            'price_level': dest.price_level
        })
    return Response(result)