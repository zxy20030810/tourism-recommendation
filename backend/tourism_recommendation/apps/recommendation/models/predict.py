"""
模型预测模块
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pandas as pd

def load_trained_model(model_path):
    """
    加载训练好的模型
    
    Args:
        model_path: 模型路径
        
    Returns:
        加载的模型
    """
    return load_model(model_path)

def generate_recommendations(user_id, model, destination_df, user_features, top_k=10):
    """
    为用户生成推荐
    
    Args:
        user_id: 用户ID
        model: 训练好的模型
        destination_df: 目的地数据
        user_features: 用户特征
        top_k: 推荐数量
        
    Returns:
        推荐的目的地列表
    """
    # 为每个目的地准备特征
    predictions = []
    for idx, dest in destination_df.iterrows():
        # 构建特征向量
        features = {
            'user_id': np.array([user_id]),
            'destination_id': np.array([dest['id']]),
            'travel_type': np.array([user_features['travel_type']]),
            'budget_level': np.array([user_features['budget_level']]),
            'destination_category': np.array([dest['category']]),
            'destination_price_level': np.array([dest['price_level']]),
            'user_age': np.array([user_features['age']]),
            'destination_rating': np.array([dest['rating']]),
            'destination_review_count': np.array([dest['review_count']])
        }
        
        # 预测
        pred = model.predict(features)[0][0]
        predictions.append((dest['id'], dest['name'], pred))
    
    # 按预测分数排序
    predictions.sort(key=lambda x: x[2], reverse=True)
    
    # 返回前top_k个推荐
    return predictions[:top_k]

def get_personalized_recommendations(user_id, model_type='wide_deep', top_k=10):
    """
    获取个性化推荐
    
    Args:
        user_id: 用户ID
        model_type: 模型类型
        top_k: 推荐数量
        
    Returns:
        推荐列表
    """
    # 加载模型
    model_path = f'models/{model_type}_model.h5'
    model = load_trained_model(model_path)
    
    # 加载用户特征
    user_df = pd.read_csv('data/processed/user_features.csv')
    user_features = user_df[user_df['user_id'] == user_id].iloc[0].to_dict()
    
    # 加载目的地数据
    destination_df = pd.read_csv('data/processed/destination_features.csv')
    
    # 生成推荐
    recommendations = generate_recommendations(user_id, model, destination_df, user_features, top_k)
    
    return recommendations