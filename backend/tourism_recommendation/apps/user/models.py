from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    """用户模型"""
    # 基本信息
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], null=True, blank=True, verbose_name='性别')
    age = models.IntegerField(null=True, blank=True, verbose_name='年龄')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机号码')
    
    # 旅游偏好
    travel_type = models.CharField(max_length=50, choices=[
        ('adventure', '冒险型'),
        ('leisure', '休闲型'),
        ('cultural', '文化型'),
        ('nature', '自然型'),
        ('shopping', '购物型')
    ], null=True, blank=True, verbose_name='旅游类型偏好')
    
    budget_level = models.CharField(max_length=20, choices=[
        ('low', '低消费'),
        ('medium', '中等消费'),
        ('high', '高消费')
    ], null=True, blank=True, verbose_name='消费水平')
    
    favorite_regions = models.JSONField(null=True, blank=True, verbose_name='喜欢的地区')
    favorite_attractions = models.JSONField(null=True, blank=True, verbose_name='喜欢的景点类型')
    
    # 历史记录
    travel_history = models.JSONField(null=True, blank=True, verbose_name='旅游历史')
    
    # 为groups和user_permissions添加related_name以避免冲突
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='user',
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'