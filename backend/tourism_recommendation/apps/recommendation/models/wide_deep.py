"""
Wide&Deep模型实现
"""
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Embedding, concatenate, Flatten
from tensorflow.keras.models import Model

def build_wide_deep_model(feature_columns, wide_columns, deep_columns, hidden_units=[256, 128, 64]):
    """
    构建Wide&Deep模型
    
    Args:
        feature_columns: 所有特征列
        wide_columns: Wide部分使用的特征列
        deep_columns: Deep部分使用的特征列
        hidden_units: 隐藏层单元数
        
    Returns:
        Wide&Deep模型
    """
    # 输入层
    inputs = {name: Input(shape=(1,), name=name) for name, _ in feature_columns}
    
    # Wide部分
    wide_inputs = []
    for name in wide_columns:
        wide_inputs.append(inputs[name])
    wide_inputs = concatenate(wide_inputs, axis=1)
    wide_output = Dense(1, activation='relu')(wide_inputs)
    
    # Deep部分
    deep_embeddings = []
    for name in deep_columns:
        embedding = Embedding(input_dim=1000, output_dim=32, input_length=1)(inputs[name])
        deep_embeddings.append(Flatten()(embedding))
    deep_inputs = concatenate(deep_embeddings, axis=1)
    
    # 隐藏层
    x = deep_inputs
    for units in hidden_units:
        x = Dense(units, activation='relu')(x)
    
    deep_output = Dense(1, activation='relu')(x)
    
    # 组合Wide和Deep部分
    combined = concatenate([wide_output, deep_output], axis=1)
    output = Dense(1, activation='sigmoid')(combined)
    
    model = Model(inputs=list(inputs.values()), outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    return model