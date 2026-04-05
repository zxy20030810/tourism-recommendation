from django.db import models


class Destination(models.Model):
    """旅游目的地模型"""
    name = models.CharField(max_length=100, verbose_name='目的地名称')
    city = models.CharField(max_length=50, verbose_name='所在城市')
    region = models.CharField(max_length=50, verbose_name='所在地区')
    description = models.TextField(verbose_name='目的地描述')
    category = models.CharField(max_length=50, choices=[
        ('natural', '自然景观'),
        ('cultural', '文化古迹'),
        ('leisure', '休闲娱乐'),
        ('adventure', '冒险体验'),
        ('shopping', '购物天堂')
    ], verbose_name='目的地类型')
    rating = models.FloatField(verbose_name='评分')
    review_count = models.IntegerField(verbose_name='评论数量')
    price_level = models.CharField(max_length=20, choices=[
        ('low', '低消费'),
        ('medium', '中等消费'),
        ('high', '高消费')
    ], verbose_name='消费水平')
    popular_season = models.CharField(max_length=100, verbose_name='最佳旅游季节')
    visitor_volume = models.IntegerField(verbose_name='年游客量')
    facilities = models.JSONField(verbose_name='设施服务')
    tags = models.JSONField(verbose_name='标签')
    coordinates = models.JSONField(verbose_name='坐标')
    images = models.JSONField(verbose_name='图片链接')
    
    class Meta:
        verbose_name = '旅游目的地'
        verbose_name_plural = '旅游目的地'
    
    def __str__(self):
        return self.name

class DestinationFeature(models.Model):
    """目的地特征模型"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name='关联目的地')
    feature_name = models.CharField(max_length=50, verbose_name='特征名称')
    feature_value = models.FloatField(verbose_name='特征值')
    
    class Meta:
        verbose_name = '目的地特征'
        verbose_name_plural = '目的地特征'


class TravelGuide(models.Model):
    """旅游攻略模型"""
    title = models.CharField(max_length=200, verbose_name='攻略标题')
    category = models.CharField(max_length=50, choices=[
        ('出行准备', '出行准备'),
        ('行程规划', '行程规划'),
        ('省钱攻略', '省钱攻略'),
        ('注意事项', '注意事项')
    ], verbose_name='攻略分类')
    author = models.CharField(max_length=100, verbose_name='作者')
    content = models.TextField(verbose_name='攻略内容')
    summary = models.TextField(verbose_name='摘要')
    views = models.IntegerField(default=0, verbose_name='浏览量')
    likes = models.IntegerField(default=0, verbose_name='点赞数')
    tags = models.JSONField(verbose_name='标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '旅游攻略'
        verbose_name_plural = '旅游攻略'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
