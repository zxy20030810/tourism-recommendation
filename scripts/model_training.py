"""
模型训练脚本
"""
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

# 本地构建模型函数
def build_wide_deep_model(input_dim):
    """
    构建Wide&Deep模型
    
    Args:
        input_dim: 输入维度
        
    Returns:
        Wide&Deep模型
    """
    # 输入层
    inputs = Input(shape=(input_dim,))
    
    # Wide部分（线性模型）
    wide_output = Dense(1)(inputs)
    
    # Deep部分（神经网络）
    deep = Dense(64, activation='relu')(inputs)
    deep = Dropout(0.2)(deep)
    deep = Dense(32, activation='relu')(deep)
    deep = Dropout(0.2)(deep)
    deep_output = Dense(1)(deep)
    
    # 合并Wide和Deep部分
    output = tf.keras.layers.Add()([wide_output, deep_output])
    output = Dense(1, activation='sigmoid')(output)
    
    # 构建模型
    model = Model(inputs=inputs, outputs=output)
    
    # 编译模型
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC()]
    )
    
    return model

def build_deepfm_model(input_dim):
    """
    构建DeepFM模型
    
    Args:
        input_dim: 输入维度
        
    Returns:
        DeepFM模型
    """
    # 输入层
    inputs = Input(shape=(input_dim,))
    
    # FM部分（二阶特征交互）
    fm = Dense(64)(inputs)
    fm = Dense(32)(fm)
    fm_output = Dense(1)(fm)
    
    # Deep部分（高阶特征交互）
    deep = Dense(64, activation='relu')(inputs)
    deep = Dropout(0.2)(deep)
    deep = Dense(32, activation='relu')(deep)
    deep = Dropout(0.2)(deep)
    deep_output = Dense(1)(deep)
    
    # 合并FM和Deep部分
    output = tf.keras.layers.Add()([fm_output, deep_output])
    output = Dense(1, activation='sigmoid')(output)
    
    # 构建模型
    model = Model(inputs=inputs, outputs=output)
    
    # 编译模型
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC()]
    )
    
    return model

def load_processed_data(data_path):
    """
    加载处理后的数据
    
    Args:
        data_path: 数据路径
        
    Returns:
        训练数据和标签
    """
    X = pd.read_csv(os.path.join(data_path, 'X_train.csv'))
    y = pd.read_csv(os.path.join(data_path, 'y_train.csv')).values.ravel()
    
    return X, y

def prepare_model_inputs(X):
    """
    准备模型输入
    
    Args:
        X: 特征数据
        
    Returns:
        模型输入格式
    """
    # 简单的输入格式 - 直接返回numpy数组
    return X.values

def train_wide_deep(X_train, y_train, X_val, y_val, model_save_path):
    """
    训练Wide&Deep模型
    
    Args:
        X_train: 训练特征
        y_train: 训练标签
        X_val: 验证特征
        y_val: 验证标签
        model_save_path: 模型保存路径
        
    Returns:
        训练好的模型
    """
    # 准备模型输入
    train_inputs = prepare_model_inputs(X_train)
    val_inputs = prepare_model_inputs(X_val)
    
    # 构建模型
    input_dim = train_inputs.shape[1]
    model = build_wide_deep_model(input_dim)
    
    # 回调函数
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ModelCheckpoint(
            filepath=os.path.join(model_save_path, 'wide_deep_best.h5'),
            monitor='val_loss',
            save_best_only=True
        ),
        TensorBoard(log_dir=os.path.join(model_save_path, 'logs', 'wide_deep'))
    ]
    
    # 训练模型
    history = model.fit(
        train_inputs,
        y_train,
        validation_data=(val_inputs, y_val),
        epochs=50,
        batch_size=32,
        callbacks=callbacks
    )
    
    # 保存模型
    model.save(os.path.join(model_save_path, 'wide_deep_model.h5'))
    
    return model, history

def train_deepfm(X_train, y_train, X_val, y_val, model_save_path):
    """
    训练DeepFM模型
    
    Args:
        X_train: 训练特征
        y_train: 训练标签
        X_val: 验证特征
        y_val: 验证标签
        model_save_path: 模型保存路径
        
    Returns:
        训练好的模型
    """
    # 准备模型输入
    train_inputs = prepare_model_inputs(X_train)
    val_inputs = prepare_model_inputs(X_val)
    
    # 构建模型
    input_dim = train_inputs.shape[1]
    model = build_deepfm_model(input_dim)
    
    # 回调函数
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ModelCheckpoint(
            filepath=os.path.join(model_save_path, 'deepfm_best.h5'),
            monitor='val_loss',
            save_best_only=True
        ),
        TensorBoard(log_dir=os.path.join(model_save_path, 'logs', 'deepfm'))
    ]
    
    # 训练模型
    history = model.fit(
        train_inputs,
        y_train,
        validation_data=(val_inputs, y_val),
        epochs=50,
        batch_size=32,
        callbacks=callbacks
    )
    
    # 保存模型
    model.save(os.path.join(model_save_path, 'deepfm_model.h5'))
    
    return model, history

def evaluate_model(model, X_test, y_test):
    """
    评估模型性能
    
    Args:
        model: 训练好的模型
        X_test: 测试特征
        y_test: 测试标签
        
    Returns:
        评估指标
    """
    # 准备模型输入
    test_inputs = prepare_model_inputs(X_test)
    
    # 预测
    y_pred = model.predict(test_inputs)
    y_pred_binary = (y_pred > 0.5).astype(int)
    
    # 计算评估指标
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred_binary),
        'precision': precision_score(y_test, y_pred_binary),
        'recall': recall_score(y_test, y_pred_binary),
        'f1_score': f1_score(y_test, y_pred_binary),
        'auc': roc_auc_score(y_test, y_pred)
    }
    
    return metrics

def main():
    """
    主函数
    """
    print("=" * 50)
    print("开始模型训练流程")
    print("=" * 50)
    
    # 数据路径
    data_path = 'data/processed'
    model_save_path = 'models'
    
    # 创建模型目录
    os.makedirs(model_save_path, exist_ok=True)
    
    try:
        # 加载训练数据
        X, y = load_processed_data(data_path)
        
        # 划分训练集和测试集
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
        
        print(f"训练集大小: {X_train.shape[0]}")
        print(f"验证集大小: {X_val.shape[0]}")
        print(f"测试集大小: {X_test.shape[0]}")
        
        # 训练Wide&Deep模型
        print("\n=== 训练Wide&Deep模型 ===")
        wd_model, wd_history = train_wide_deep(X_train, y_train, X_val, y_val, model_save_path)
        
        # 训练DeepFM模型
        print("\n=== 训练DeepFM模型 ===")
        dfm_model, dfm_history = train_deepfm(X_train, y_train, X_val, y_val, model_save_path)
        
        # 评估模型
        print("\n=== 评估模型 ===")
        wd_metrics = evaluate_model(wd_model, X_test, y_test)
        dfm_metrics = evaluate_model(dfm_model, X_test, y_test)
        
        print("\nWide&Deep模型性能:")
        for metric, value in wd_metrics.items():
            print(f"{metric}: {value:.4f}")
        
        print("\nDeepFM模型性能:")
        for metric, value in dfm_metrics.items():
            print(f"{metric}: {value:.4f}")
        
        # 保存评估结果
        metrics_df = pd.DataFrame({
            'metric': list(wd_metrics.keys()),
            'wide_deep': list(wd_metrics.values()),
            'deepfm': list(dfm_metrics.values())
        })
        metrics_df.to_csv(os.path.join(model_save_path, 'model_evaluation.csv'), index=False)
        
        print("\n模型训练和评估完成！")
        
    except Exception as e:
        print(f"\n错误: 模型训练过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()