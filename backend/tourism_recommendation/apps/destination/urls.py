from django.urls import path
from .views import (
    get_destinations, get_destination_detail, search_destinations, search_destination_images,
    get_travel_guides, get_travel_guide_detail, like_travel_guide
)

urlpatterns = [
    path('list/', get_destinations, name='get_destinations'),
    path('detail/<int:destination_id>/', get_destination_detail, name='get_destination_detail'),
    path('search/', search_destinations, name='search_destinations'),
    path('images/', search_destination_images, name='search_destination_images'),
    
    # 攻略相关API
    path('guides/', get_travel_guides, name='get_travel_guides'),
    path('guides/<int:guide_id>/detail/', get_travel_guide_detail, name='get_travel_guide_detail'),
    path('guides/<int:guide_id>/like/', like_travel_guide, name='like_travel_guide'),
]