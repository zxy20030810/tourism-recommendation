from django.urls import path
from .views import get_destinations, get_destination_detail, search_destinations

urlpatterns = [
    path('list/', get_destinations, name='get_destinations'),
    path('detail/<int:destination_id>/', get_destination_detail, name='get_destination_detail'),
    path('search/', search_destinations, name='search_destinations'),
]