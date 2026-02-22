"""
DeepFM模型实现
"""
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Embedding, concatenate, Flatten, Add
from tensorflow.keras.models import Model

def build_deepfm_model(feature_columns, embedding_dim=32, hidden_units=[256, 128, 64]):
    """
    构建DeepFM模型
    
    Args:
        feature_columns: 所有特征列
        embedding_dim: 嵌入维度
        hidden_units: 隐藏层单元数
        
    Returns:
        DeepFM模型
    """
    # 输入层
    inputs = {name: Input(shape=(1,), name=name) for name, _ in feature_columns}
    
    # FM部分 - 线性部分
    linear_outputs = []
    for name, vocab_size in feature_columns:
        linear_embedding = Embedding(input_dim=vocab_size, output_dim=1, input_length=1)(inputs[name])
        linear_outputs.append(Flatten()(linear_embedding))
    linear_part = Add()(linear_outputs)
    
    # FM部分 - 交互部分
    embeddings = []
    for name, vocab_size in feature_columns:
        embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=1)(inputs[name])
        embeddings.append(Flatten()(embedding))
    
    # 二阶交互
    square_sum = tf.square(Add()(embeddings))
    sum_square = Add()([tf.square(emb) for emb in embeddings])
    interaction_part = 0.5 * tf.reduce_sum(square_sum - sum_square, axis=1, keepdims=True)
    
    # Deep部分
    deep_inputs = concatenate(embeddings, axis=1)
    x = deep_inputs
    for units in hidden_units:
        x = Dense(units, activation='relu')(x)
    deep_part = Dense(1, activation='relu')(x)
    
    # 组合所有部分
    output = Add()([linear_part, interaction_part, deep_part])
    output = Dense(1, activation='sigmoid')(output)
    
    model = Model(inputs=list(inputs.values()), outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    return model