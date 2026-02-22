import os
import django
import sys

# 添加项目路径
sys.path.append('d:/bishe/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourism_recommendation.settings')
django.setup()

from django.contrib.auth import get_user_model
from tourism_recommendation.apps.destination.models import Destination, DestinationFeature

# 获取用户模型
User = get_user_model()

# 创建测试用户
print("Creating test users...")
try:
    user1 = User.objects.create_user(
        username="testuser",
        password="testpass123",
        email="test@example.com",
        first_name="male",
        last_name="25"
    )
    print(f"Created user: {user1.username}")
except Exception as e:
    print(f"Error creating user: {e}")

# 检查是否已有目的地数据
if Destination.objects.count() == 0:
    print("\nCreating test destinations...")
    destinations_data = [
        {
            "name": "故宫博物院",
            "city": "北京",
            "region": "华北",
            "description": "中国明清两代的皇家宫殿，旧称为紫禁城，位于北京中轴线的中心。",
            "category": "cultural",
            "rating": 4.8,
            "review_count": 15000,
            "price_level": "medium",
            "popular_season": "春秋两季",
            "visitor_volume": 16000000,
            "facilities": ["停车场", "餐厅", "纪念品商店", "无障碍设施"],
            "tags": ["文化遗产", "历史建筑", "博物馆"],
            "coordinates": {"lat": 39.9163, "lng": 116.3972},
            "images": ["https://example.com/forbidden_city1.jpg", "https://example.com/forbidden_city2.jpg"]
        },
        {
            "name": "长城",
            "city": "北京",
            "region": "华北",
            "description": "中国古代的军事防御工程，世界文化遗产，被誉为世界七大奇迹之一。",
            "category": "natural",
            "rating": 4.9,
            "review_count": 20000,
            "price_level": "low",
            "popular_season": "春秋两季",
            "visitor_volume": 10000000,
            "facilities": ["停车场", "餐厅", "索道", "无障碍设施"],
            "tags": ["世界遗产", "历史建筑", "户外"],
            "coordinates": {"lat": 40.4319, "lng": 116.5704},
            "images": ["https://example.com/great_wall1.jpg", "https://example.com/great_wall2.jpg"]
        },
        {
            "name": "西湖",
            "city": "杭州",
            "region": "华东",
            "description": "中国著名的风景名胜区，以其秀丽的湖光山色和众多的名胜古迹闻名于世。",
            "category": "natural",
            "rating": 4.7,
            "review_count": 18000,
            "price_level": "low",
            "popular_season": "春季",
            "visitor_volume": 12000000,
            "facilities": ["游船", "餐厅", "纪念品商店", "自行车租赁"],
            "tags": ["自然景观", "湖泊", "文化遗产"],
            "coordinates": {"lat": 30.2437, "lng": 120.1695},
            "images": ["https://example.com/west_lake1.jpg", "https://example.com/west_lake2.jpg"]
        },
        {
            "name": "黄山",
            "city": "黄山",
            "region": "华东",
            "description": "中国著名的风景名胜区，以奇松、怪石、云海、温泉、冬雪著称。",
            "category": "natural",
            "rating": 4.8,
            "review_count": 12000,
            "price_level": "medium",
            "popular_season": "秋季",
            "visitor_volume": 8000000,
            "facilities": ["缆车", "酒店", "餐厅", "纪念品商店"],
            "tags": ["自然景观", "山岳", "户外"],
            "coordinates": {"lat": 30.1319, "lng": 118.1667},
            "images": ["https://example.com/huangshan1.jpg", "https://example.com/huangshan2.jpg"]
        },
        {
            "name": "外滩",
            "city": "上海",
            "region": "华东",
            "description": "上海著名的滨江大道，是上海的城市地标和旅游胜地。",
            "category": "leisure",
            "rating": 4.6,
            "review_count": 25000,
            "price_level": "low",
            "popular_season": "全年",
            "visitor_volume": 20000000,
            "facilities": ["餐厅", "酒吧", "纪念品商店", "观光巴士"],
            "tags": ["城市景观", "夜景", "历史建筑"],
            "coordinates": {"lat": 31.2397, "lng": 121.4944},
            "images": ["https://example.com/bund1.jpg", "https://example.com/bund2.jpg"]
        }
    ]

    for dest_data in destinations_data:
        try:
            destination = Destination.objects.create(**dest_data)
            print(f"Created destination: {destination.name}")
            
            # 创建目的地特征
            features = [
                {"feature_name": "文化价值", "feature_value": 0.8},
                {"feature_name": "自然风光", "feature_value": 0.7},
                {"feature_name": "交通便利", "feature_value": 0.9},
                {"feature_name": "价格合理", "feature_value": 0.6},
                {"feature_name": "游客满意度", "feature_value": 0.85}
            ]
            
            for feature_data in features:
                DestinationFeature.objects.create(
                    destination=destination,
                    **feature_data
                )
            print(f"Created features for: {destination.name}")
            
        except Exception as e:
            print(f"Error creating destination {dest_data['name']}: {e}")
else:
    print(f"Destinations already exist: {Destination.objects.count()}")

print("\nTest data creation completed!")
print(f"Total users: {User.objects.count()}")
print(f"Total destinations: {Destination.objects.count()}")
print(f"Total features: {DestinationFeature.objects.count()}")