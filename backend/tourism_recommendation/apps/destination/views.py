from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Destination
import json
import requests
import re
import urllib.parse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

@api_view(['GET'])
def search_destination_images(request):
    """搜索目的地图片"""
    keyword = request.query_params.get('keyword', '')
    
    if not keyword:
        return Response({'error': '请提供搜索关键词'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        images = baidu_image_search(keyword)
        return Response({'images': images})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def baidu_image_search(keyword, count=5):
    """百度图片搜索"""
    try:
        url = "https://image.baidu.com/search/acjson"
        params = {
            'tn': 'resultjson_com',
            'logid': '12508647508751086108',
            'ipn': 'rj',
            'ct': '201326592',
            'is': '',
            'fp': 'result',
            'fr': '',
            'word': keyword,
            'queryWord': keyword,
            'cl': '2',
            'lm': '-1',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': '-1',
            'z': '',
            'ic': '0',
            'hd': '',
            'latest': '',
            'copyright': '',
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': '0',
            'istype': '2',
            'qc': '',
            'nc': '1',
            'expermode': '',
            'nojc': '',
            'isAsync': '',
            'pn': '0',
            'rn': str(count),
            'gsm': '1e'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://image.baidu.com/'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            data = response.json()
            images = []
            if 'data' in data:
                for item in data['data']:
                    if item and 'thumbURL' in item:
                        images.append({
                            'url': item.get('thumbURL', ''),
                            'title': item.get('fromPageTitleEnc', keyword),
                            'width': item.get('width', 0),
                            'height': item.get('height', 0)
                        })
            return images
        return []
    except Exception as e:
        print(f"百度图片搜索失败: {str(e)}")
        return get_fallback_images(keyword)

def get_fallback_images(keyword):
    """备用图片源"""
    encoded_keyword = urllib.parse.quote(keyword)
    return [
        {
            'url': f'https://source.unsplash.com/800x600/?{encoded_keyword},travel',
            'title': f'{keyword} 图片',
            'width': 800,
            'height': 600
        }
    ]

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