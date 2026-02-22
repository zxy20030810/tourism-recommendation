from django.urls import path
from .views import get_recommendations, update_user_preference

urlpatterns = [
    path('user/<int:user_id>/', get_recommendations, name='get_recommendations'),
    path('update-preference/<int:user_id>/', update_user_preference, name='update_user_preference'),
]