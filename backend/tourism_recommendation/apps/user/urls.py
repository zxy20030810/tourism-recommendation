from django.urls import path
from .views import register, user_login, user_logout, get_user_info, update_user_preference

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('info/<int:user_id>/', get_user_info, name='get_user_info'),
    path('preference/<int:user_id>/', update_user_preference, name='update_user_preference'),
]