"""
数据预处理脚本
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

def load_raw_data(user_data_path, destination_data_path, interaction_data_path):
    """
    加载原始数据
    
    Args:
        user_data_path: 用户数据路径
        destination_data_path: 目的地数据路径
        interaction_data_path: 交互数据路径
        
    Returns:
        加载的数据帧
    """
    try:
        # 添加编码参数，尝试不同的编码格式
        user_df = pd.read_csv(user_data_path, encoding='utf-8-sig')
        destination_df = pd.read_csv(destination_data_path, encoding='utf-8-sig')
        interaction_df = pd.read_csv(interaction_data_path, encoding='utf-8-sig')
        
        print(f"加载数据完成:")
        print(f"  用户数据: {user_df.shape}")
        print(f"  目的地数据: {destination_df.shape}")
        print(f"  交互数据: {interaction_df.shape}")
        
        return user_df, destination_df, interaction_df
    except FileNotFoundError as e:
        print(f"错误: 找不到数据文件，请确保以下文件存在:")
        print(f"  {user_data_path}")
        print(f"  {destination_data_path}")
        print(f"  {interaction_data_path}")
        print(f"详细错误: {e}")
        raise
    except Exception as e:
        print(f"加载数据时发生错误: {e}")
        print("尝试使用其他编码格式...")
        try:
            # 尝试使用gbk编码
            user_df = pd.read_csv(user_data_path, encoding='gbk')
            destination_df = pd.read_csv(destination_data_path, encoding='gbk')
            interaction_df = pd.read_csv(interaction_data_path, encoding='gbk')
            
            print(f"加载数据完成 (使用gbk编码):")
            print(f"  用户数据: {user_df.shape}")
            print(f"  目的地数据: {destination_df.shape}")
            print(f"  交互数据: {interaction_df.shape}")
            
            return user_df, destination_df, interaction_df
        except Exception as e2:
            print(f"使用gbk编码也失败: {e2}")
            raise

def preprocess_user_data(user_df):
    """
    预处理用户数据
    
    Args:
        user_df: 用户数据帧
        
    Returns:
        预处理后的用户数据
    """
    print("开始预处理用户数据...")
    
    # 创建副本避免修改原始数据
    user_df = user_df.copy()
    
    # 填充缺失值
    if 'age' in user_df.columns:
        user_df['age'] = user_df['age'].fillna(user_df['age'].median())
    else:
        print("警告: 'age' 列不存在，跳过处理")
    
    if 'gender' in user_df.columns:
        user_df['gender'] = user_df['gender'].fillna('unknown')
    else:
        print("警告: 'gender' 列不存在，跳过处理")
    
    # 处理不同的列名
    if 'preferred_type' in user_df.columns:
        user_df['preferred_type'] = user_df['preferred_type'].fillna('Beach')
        # 标签编码
        le_preferred_type = LabelEncoder()
        user_df['preferred_type_encoded'] = le_preferred_type.fit_transform(user_df['preferred_type'])
        encoders = {'preferred_type': le_preferred_type}
    elif 'travel_type' in user_df.columns:
        user_df['travel_type'] = user_df['travel_type'].fillna('leisure')
        # 标签编码
        le_travel_type = LabelEncoder()
        user_df['travel_type_encoded'] = le_travel_type.fit_transform(user_df['travel_type'])
        encoders = {'travel_type': le_travel_type}
    else:
        print("警告: 缺少类型列，跳过处理")
        encoders = {}
    
    # 处理预算列
    if 'budget' in user_df.columns:
        user_df['budget'] = user_df['budget'].fillna(user_df['budget'].median())
        # 标准化预算
        scaler_budget = StandardScaler()
        user_df['budget_scaled'] = scaler_budget.fit_transform(user_df[['budget']])
        encoders['budget'] = scaler_budget
    elif 'budget_level' in user_df.columns:
        user_df['budget_level'] = user_df['budget_level'].fillna('medium')
        # 标签编码
        le_budget_level = LabelEncoder()
        user_df['budget_level_encoded'] = le_budget_level.fit_transform(user_df['budget_level'])
        encoders['budget_level'] = le_budget_level
    else:
        print("警告: 缺少预算列，跳过处理")
    
    # 处理性别列
    if 'gender' in user_df.columns:
        le_gender = LabelEncoder()
        user_df['gender_encoded'] = le_gender.fit_transform(user_df['gender'])
        encoders['gender'] = le_gender
    
    # 标准化年龄
    if 'age' in user_df.columns:
        scaler_age = StandardScaler()
        user_df['age_scaled'] = scaler_age.fit_transform(user_df[['age']])
        encoders['age'] = scaler_age
    
    print(f"用户数据预处理完成，最终形状: {user_df.shape}")
    return user_df, encoders

def preprocess_destination_data(destination_df):
    """
    预处理目的地数据
    
    Args:
        destination_df: 目的地数据帧
        
    Returns:
        预处理后的目的地数据
    """
    print("开始预处理目的地数据...")
    
    # 创建副本避免修改原始数据
    destination_df = destination_df.copy()
    
    # 填充缺失值
    if 'rating' in destination_df.columns:
        destination_df['rating'] = destination_df['rating'].fillna(destination_df['rating'].mean())
        # 标准化评分
        scaler_rating = StandardScaler()
        destination_df['rating_scaled'] = scaler_rating.fit_transform(destination_df[['rating']])
        encoders = {'rating': scaler_rating}
    else:
        print("警告: 'rating' 列不存在，跳过处理")
        encoders = {}
    
    # 处理不同的列名
    if 'type' in destination_df.columns:
        destination_df['type'] = destination_df['type'].fillna('Beach')
        # 标签编码
        le_type = LabelEncoder()
        destination_df['type_encoded'] = le_type.fit_transform(destination_df['type'])
        encoders['type'] = le_type
    elif 'category' in destination_df.columns:
        destination_df['category'] = destination_df['category'].fillna('natural')
        # 标签编码
        le_category = LabelEncoder()
        destination_df['category_encoded'] = le_category.fit_transform(destination_df['category'])
        encoders['category'] = le_category
    else:
        print("警告: 缺少类型列，跳过处理")
    
    # 处理价格列
    if 'price' in destination_df.columns:
        destination_df['price'] = destination_df['price'].fillna(destination_df['price'].median())
        # 标准化价格
        scaler_price = StandardScaler()
        destination_df['price_scaled'] = scaler_price.fit_transform(destination_df[['price']])
        encoders['price'] = scaler_price
    elif 'price_level' in destination_df.columns:
        destination_df['price_level'] = destination_df['price_level'].fillna('medium')
        # 标签编码
        le_price_level = LabelEncoder()
        destination_df['price_level_encoded'] = le_price_level.fit_transform(destination_df['price_level'])
        encoders['price_level'] = le_price_level
    else:
        print("警告: 缺少价格列，跳过处理")
    
    # 处理流行度列
    if 'popularity' in destination_df.columns:
        destination_df['popularity'] = destination_df['popularity'].fillna(destination_df['popularity'].median())
        # 标准化流行度
        scaler_popularity = StandardScaler()
        destination_df['popularity_scaled'] = scaler_popularity.fit_transform(destination_df[['popularity']])
        encoders['popularity'] = scaler_popularity
    elif 'review_count' in destination_df.columns:
        destination_df['review_count'] = destination_df['review_count'].fillna(0)
        # 标准化评论数
        scaler_review = StandardScaler()
        destination_df['review_count_scaled'] = scaler_review.fit_transform(destination_df[['review_count']])
        encoders['review_count'] = scaler_review
    else:
        print("警告: 缺少流行度/评论数列，跳过处理")
    
    print(f"目的地数据预处理完成，最终形状: {destination_df.shape}")
    return destination_df, encoders

def merge_data(user_df, destination_df, interaction_df):
    """
    合并数据
    
    Args:
        user_df: 用户数据帧
        destination_df: 目的地数据帧
        interaction_df: 交互数据帧
        
    Returns:
        合并后的数据
    """
    print("开始合并数据...")
    
    # 合并用户和交互数据
    merged_df = pd.merge(interaction_df, user_df, on='user_id', how='left')
    
    # 合并目的地数据
    merged_df = pd.merge(merged_df, destination_df, on='destination_id', how='left')
    
    print(f"数据合并完成，最终形状: {merged_df.shape}")
    return merged_df

def create_feature_engineering(merged_df):
    """
    特征工程
    
    Args:
        merged_df: 合并后的数据
        
    Returns:
        特征工程后的数据
    """
    print("开始特征工程...")
    
    # 创建副本避免修改原始数据
    merged_df = merged_df.copy()
    
    # 创建交互特征
    if 'preferred_type' in merged_df.columns and 'type' in merged_df.columns:
        merged_df['user_destination_match'] = merged_df.apply(
            lambda x: 1 if x['preferred_type'] == x['type'] else 0, axis=1
        )
        print("已创建 user_destination_match 特征 (使用 preferred_type 和 type 列)")
    elif 'travel_type' in merged_df.columns and 'category' in merged_df.columns:
        merged_df['user_destination_match'] = merged_df.apply(
            lambda x: 1 if x['travel_type'] == x['category'] else 0, axis=1
        )
        print("已创建 user_destination_match 特征 (使用 travel_type 和 category 列)")
    else:
        print("警告: 缺少必要的列，跳过 user_destination_match 特征创建")
        merged_df['user_destination_match'] = 0
    
    # 创建预算匹配特征
    if 'budget' in merged_df.columns and 'price' in merged_df.columns:
        merged_df['budget_match'] = merged_df.apply(
            lambda x: 1 if abs(x['budget'] - x['price']) < 1000 else 0, axis=1
        )
        print("已创建 budget_match 特征 (使用 budget 和 price 列)")
    elif 'budget_level' in merged_df.columns and 'price_level' in merged_df.columns:
        merged_df['budget_match'] = merged_df.apply(
            lambda x: 1 if x['budget_level'] == x['price_level'] else 0, axis=1
        )
        print("已创建 budget_match 特征 (使用 budget_level 和 price_level 列)")
    else:
        print("警告: 缺少必要的列，跳过 budget_match 特征创建")
        merged_df['budget_match'] = 0
    
    # 创建评分相关特征
    if 'rating' in merged_df.columns:
        rating_mean = merged_df['rating'].mean()
        merged_df['rating_above_avg'] = merged_df['rating'].apply(
            lambda x: 1 if x > rating_mean else 0
        )
        print("已创建 rating_above_avg 特征")
    else:
        print("警告: 缺少 rating 列，跳过 rating_above_avg 特征创建")
        merged_df['rating_above_avg'] = 0
    
    print(f"特征工程完成，最终形状: {merged_df.shape}")
    return merged_df

def prepare_training_data(merged_df, output_path):
    """
    准备训练数据
    
    Args:
        merged_df: 合并后的数据
        output_path: 输出路径
        
    Returns:
        训练数据
    """
    print("开始准备训练数据...")
    
    # 创建目标列
    if 'interaction_type' in merged_df.columns:
        merged_df['interaction'] = merged_df['interaction_type'].apply(
            lambda x: 1 if x == 'like' else 0
        )
        target_column = 'interaction'
    elif 'interaction' in merged_df.columns:
        target_column = 'interaction'
    else:
        print("警告: 缺少交互列，使用默认值")
        merged_df['interaction'] = 1
        target_column = 'interaction'
    
    print(f"使用目标列: {target_column}")
    
    # 选择可用的特征列
    available_columns = merged_df.columns.tolist()
    feature_columns = []
    
    # 定义期望的特征列（只保留存在的列）
    desired_features = [
        'user_id', 'destination_id', 'gender_encoded',
        'preferred_type_encoded', 'travel_type_encoded',
        'budget_scaled', 'budget_level_encoded',
        'type_encoded', 'category_encoded',
        'price_scaled', 'price_level_encoded',
        'age_scaled', 'rating_scaled',
        'popularity_scaled', 'review_count_scaled',
        'user_destination_match', 'budget_match', 'rating_above_avg'
    ]
    
    for feature in desired_features:
        if feature in available_columns:
            feature_columns.append(feature)
        else:
            print(f"警告: 特征 '{feature}' 不存在，跳过")
    
    # 确保有足够的特征
    if len(feature_columns) < 2:
        raise ValueError("可用特征太少，请检查数据预处理步骤")
    
    print(f"使用特征: {feature_columns}")
    
    # 准备训练数据
    X = merged_df[feature_columns]
    y = merged_df[target_column]
    
    # 检查数据质量
    if X.isnull().sum().sum() > 0:
        print("警告: 特征数据中存在缺失值，正在填充...")
        X = X.fillna(0)
    
    if y.isnull().sum() > 0:
        print("警告: 目标数据中存在缺失值，正在填充...")
        y = y.fillna(0)
    
    # 保存处理后的数据
    os.makedirs(output_path, exist_ok=True)
    X.to_csv(os.path.join(output_path, 'X_train.csv'), index=False)
    y.to_csv(os.path.join(output_path, 'y_train.csv'), index=False)
    
    # 保存特征列信息
    with open(os.path.join(output_path, 'feature_columns.txt'), 'w') as f:
        f.write('\n'.join(feature_columns))
    
    print(f"训练数据准备完成:")
    print(f"  特征数据形状: {X.shape}")
    print(f"  目标数据形状: {y.shape}")
    
    return X, y

def main():
    """
    主函数
    """
    print("=" * 50)
    print("开始数据预处理流程")
    print("=" * 50)
    
    # 数据路径
    data_dir = 'data/raw'
    
    # 创建原始数据目录（如果不存在）
    os.makedirs(data_dir, exist_ok=True)
    
    # 检查原始数据文件是否存在
    user_data_path = os.path.join(data_dir, 'users.csv')
    destination_data_path = os.path.join(data_dir, 'destinations.csv')
    interaction_data_path = os.path.join(data_dir, 'interactions.csv')
    
    if not os.path.exists(user_data_path):
        print(f"警告: 用户数据文件不存在: {user_data_path}")
        print("请确保在 data/raw 目录下有 users.csv 文件")
        return
    
    if not os.path.exists(destination_data_path):
        print(f"警告: 目的地数据文件不存在: {destination_data_path}")
        print("请确保在 data/raw 目录下有 destinations.csv 文件")
        return
    
    if not os.path.exists(interaction_data_path):
        print(f"警告: 交互数据文件不存在: {interaction_data_path}")
        print("请确保在 data/raw 目录下有 interactions.csv 文件")
        return
    
    try:
        # 加载数据
        user_df, destination_df, interaction_df = load_raw_data(
            user_data_path, destination_data_path, interaction_data_path
        )
        
        # 预处理数据
        user_df, user_encoders = preprocess_user_data(user_df)
        destination_df, destination_encoders = preprocess_destination_data(destination_df)
        
        # 合并数据
        merged_df = merge_data(user_df, destination_df, interaction_df)
        
        # 特征工程
        merged_df = create_feature_engineering(merged_df)
        
        # 准备训练数据
        output_path = 'data/processed'
        X, y = prepare_training_data(merged_df, output_path)
        
        print("\n" + "=" * 50)
        print("数据预处理完成！")
        print(f"训练数据已保存到 {output_path}")
        print(f"特征数量: {X.shape[1]}")
        print(f"样本数量: {X.shape[0]}")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n错误: 数据预处理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()