# 基于深度学习的旅游目的地智能推荐系统

## 项目简介

本项目是一个基于深度学习的旅游目的地智能推荐系统，旨在为用户提供个性化的旅游目的地推荐。系统采用前后端分离架构，后端使用Django框架和深度学习模型（Wide&Deep和DeepFM），前端使用Vue.js框架。

## 技术栈

### 后端
- Django 4.2+
- Django REST Framework
- MySQL 8.0
- TensorFlow 2.10+ / Keras
- Pandas / NumPy
- Scikit-learn

### 前端
- Vue.js 3.3+
- Vue Router 4.2+
- Element Plus
- Vite 4.4+
- Axios

## 项目结构

```
├── backend/                  # 后端代码
│   ├── tourism_recommendation/  # Django项目主目录
│   │   ├── apps/              # 应用目录
│   │   │   ├── user/          # 用户应用
│   │   │   ├── destination/   # 目的地应用
│   │   │   └── recommendation/ # 推荐应用
│   │   ├── settings.py        # 项目配置
│   │   └── urls.py            # URL配置
│   └── manage.py              # Django管理脚本
├── frontend/                 # 前端代码
│   ├── src/                   # 源代码
│   │   ├── components/        # Vue组件
│   │   ├── router/            # 路由配置
│   │   ├── App.vue            # 主应用组件
│   │   └── main.js            # 入口文件
│   ├── vite.config.js         # Vite配置
│   └── package.json           # 前端依赖
├── data/                     # 数据目录
│   ├── raw/                  # 原始数据
│   └── processed/            # 处理后的数据
├── scripts/                  # 脚本目录
│   ├── data_preprocessing.py # 数据预处理脚本
│   └── model_training.py     # 模型训练脚本
├── models/                   # 模型目录
├── requirements.txt          # 后端依赖
└── README.md                 # 项目说明
```

## 快速开始

### 1. 环境准备

#### 后端环境
1. 安装Python 3.8+
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 安装MySQL 8.0并创建数据库：
   ```sql
   CREATE DATABASE tourism_recommendation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
4. 修改`backend/tourism_recommendation/settings.py`中的数据库配置：
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'tourism_recommendation',
           'USER': 'root',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

#### 前端环境
1. 安装Node.js 16+
2. 安装依赖：
   ```bash
   cd frontend
   npm install
   ```

### 2. 数据准备

1. 在`data/raw/`目录下创建以下CSV文件：
   - `users.csv`：用户数据
   - `destinations.csv`：目的地数据
   - `interactions.csv`：用户-目的地交互数据

2. 运行数据预处理脚本：
   ```bash
   python scripts/data_preprocessing.py
   ```

### 3. 模型训练

运行模型训练脚本：
```bash
python scripts/model_training.py
```

### 4. 数据库迁移

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 5. 启动服务

#### 后端服务
```bash
cd backend
python manage.py runserver
```

#### 前端服务
```bash
cd frontend
npm run dev
```

### 6. 访问系统

打开浏览器访问：`http://localhost:3000`

## 系统功能

1. **用户管理**：注册、登录、个人信息管理
2. **偏好设置**：用户可以设置旅游类型、消费水平、喜欢的地区和景点类型
3. **智能推荐**：基于Wide&Deep和DeepFM模型的个性化推荐
4. **目的地浏览**：查看目的地列表和详情
5. **目的地搜索**：根据类别、地区、评分等条件搜索目的地

## 模型说明

### Wide&Deep模型
- **Wide部分**：线性模型，处理高阶特征交叉
- **Deep部分**：深度神经网络，学习复杂的特征表示
- **优势**：同时具备记忆能力和泛化能力

### DeepFM模型
- **FM部分**：因子分解机，处理二阶特征交叉
- **Deep部分**：深度神经网络，学习高阶特征交互
- **优势**：自动特征交叉，无需人工特征工程

## 性能评估

模型训练完成后，会在`models/model_evaluation.csv`文件中生成性能评估报告，包括准确率、精确率、召回率、F1值和AUC值等指标。

## 注意事项

1. 首次运行时需要准备好数据文件并运行数据预处理和模型训练脚本
2. 确保MySQL数据库服务正常运行
3. 前端服务默认运行在3000端口，后端服务默认运行在8000端口
4. 如需修改端口号，请修改相应的配置文件

## 许可证

MIT License# 基于深度学习的旅游目的地智能推荐系统

## 项目简介

本项目是一个基于深度学习的旅游目的地智能推荐系统，旨在为用户提供个性化的旅游目的地推荐服务。系统采用了先进的深度学习模型（Wide&Deep和DeepFM），结合用户偏好和目的地特征，实现精准的旅游推荐。

## 技术栈

### 后端
- Python 3.8+
- Django 4.2+
- Django REST Framework
- TensorFlow 2.10+
- Keras
- Pandas
- NumPy
- Scikit-learn
- MySQL

### 前端
- Vue.js 3.3+
- Vue Router 4.2+
- Element Plus 2.3+
- Axios 1.4+
- Vite 4.4+

## 项目结构

```
tourism-recommendation-system/
├── backend/                    # 后端代码
│   ├── manage.py              # Django管理脚本
│   ├── tourism_recommendation/ # 项目主目录
│   │   ├── settings.py        # 项目配置
│   │   ├── urls.py            # URL配置
│   │   └── apps/              # 应用目录
│   │       ├── user/          # 用户管理应用
│   │       ├── destination/   # 目的地管理应用
│   │       └── recommendation/ # 推荐系统应用
│   │           └── models/     # 推荐模型
├── frontend/                   # 前端代码
│   ├── package.json           # 前端依赖配置
│   ├── vite.config.js         # Vite配置
│   ├── index.html             # 前端入口
│   └── src/                   # 源代码目录
│       ├── main.js            # 主入口文件
│       ├── App.vue            # 根组件
│       ├── components/        # 组件目录
│       └── router/            # 路由配置
├── data/                       # 数据目录
│   ├── raw/                   # 原始数据
│   ├── processed/             # 处理后的数据
│   └── features/              # 特征数据
├── scripts/                    # 脚本目录
│   ├── data_preprocessing.py  # 数据预处理脚本
│   ├── feature_engineering.py # 特征工程脚本
│   ├── model_training.py      # 模型训练脚本
│   └── evaluation.py          # 模型评估脚本
├── models/                     # 模型保存目录
├── requirements.txt            # 后端依赖
└── README.md                   # 项目说明
```

## 系统功能

1. **用户管理**
   - 用户注册和登录
   - 个人信息管理
   - 旅游偏好设置

2. **目的地管理**
   - 目的地信息查询
   - 目的地搜索
   - 目的地详情展示

3. **智能推荐**
   - 基于Wide&Deep模型的推荐
   - 基于DeepFM模型的推荐
   - 个性化推荐结果展示
   - 推荐模型切换

4. **数据处理**
   - 数据清洗和预处理
   - 特征工程
   - 模型训练和评估

## 快速开始

### 1. 环境搭建

#### 后端环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 前端环境
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

### 2. 数据库配置

1. 安装MySQL数据库
2. 创建数据库：`tourism_recommendation`
3. 修改`backend/tourism_recommendation/settings.py`中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tourism_recommendation',  # 数据库名称
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'password',  # 数据库密码
        'HOST': 'localhost',  # 数据库主机
        'PORT': '3306',  # 数据库端口
    }
}
```

### 3. 数据库迁移

```bash
# 进入后端目录
cd backend

# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

### 4. 数据准备

1. 在`data/raw/`目录下创建以下CSV文件：
   - `users.csv`：用户数据
   - `destinations.csv`：目的地数据
   - `interactions.csv`：用户-目的地交互数据

2. 运行数据预处理脚本：

```bash
python scripts/data_preprocessing.py
```

### 5. 模型训练

```bash
python scripts/model_training.py
```

### 6. 启动服务

#### 后端服务
```bash
# 进入后端目录
cd backend

# 启动开发服务器
python manage.py runserver
```

#### 前端服务
```bash
# 进入前端目录
cd frontend

# 启动开发服务器
npm run dev
```

### 7. 访问系统

- 前端地址：`http://localhost:3000`
- 后端API地址：`http://localhost:8000/api/`

## 模型说明

### Wide&Deep模型

Wide&Deep模型结合了线性模型的记忆能力和深度神经网络的泛化能力，适用于推荐系统场景。

- **Wide部分**：捕获特征之间的线性关系
- **Deep部分**：学习高阶特征交互

### DeepFM模型

DeepFM模型是对Wide&Deep模型的改进，通过因子分解机（FM）部分替代了Wide部分，能够更好地捕获特征之间的交互关系。

- **FM部分**：捕获二阶特征交互
- **Deep部分**：学习高阶特征交互

## API接口

### 用户相关
- `POST /api/user/register/`：用户注册
- `POST /api/user/login/`：用户登录
- `POST /api/user/logout/`：用户登出
- `GET /api/user/info/{user_id}/`：获取用户信息
- `PUT /api/user/preference/{user_id}/`：更新用户偏好

### 目的地相关
- `GET /api/destination/list/`：获取目的地列表
- `GET /api/destination/detail/{destination_id}/`：获取目的地详情
- `GET /api/destination/search/`：搜索目的地

### 推荐相关
- `GET /api/recommendation/user/{user_id}/`：获取个性化推荐
- `POST /api/recommendation/update-preference/{user_id}/`：更新偏好并获取推荐

## 项目亮点

1. **先进的深度学习模型**：采用Wide&Deep和DeepFM模型，实现精准的旅游推荐
2. **个性化推荐**：基于用户偏好和行为，提供个性化的旅游推荐
3. **完整的系统架构**：包含前端、后端、数据处理和模型训练的完整系统
4. **良好的用户体验**：直观的界面设计和流畅的交互体验
5. **可扩展性**：模块化设计，易于扩展和维护

## 未来规划

1. 集成更多数据源，丰富推荐特征
2. 引入实时推荐机制，提升推荐时效性
3. 增加用户反馈机制，持续优化推荐质量
4. 开发移动应用，提供跨平台服务
5. 探索更先进的推荐算法，提升推荐精度

## 许可证

本项目采用MIT许可证。

## 联系方式

如有问题或建议，请联系：
- 邮箱：example@example.com
- GitHub：https://github.com/example/tourism-recommendation-system