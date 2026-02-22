# 前后端集成测试指南

## 系统状态
✅ 前端服务器运行中：http://localhost:3002/
✅ 后端服务器运行中：http://127.0.0.1:8000/
✅ 数据库连接正常：MySQL 8.0
✅ 测试数据已创建：1个用户，10个目的地

## 测试步骤

### 1. 访问前端应用
在浏览器中打开：http://localhost:3002/

### 2. 测试用户登录
- 用户名：testuser
- 密码：testpass123

### 3. 测试功能流程
1. **登录** → 输入testuser/testpass123
2. **查看推荐** → 登录后自动跳转到推荐页面
3. **查看目的地详情** → 点击"查看详情"按钮
4. **修改偏好** → 点击"修改偏好"按钮

### 4. 测试新用户注册
1. 点击"注册新用户"或"注册"按钮
2. 填写注册信息：
   - 用户名：newuser
   - 密码：newpass123
   - 邮箱：newuser@example.com
   - 性别：选择一个
   - 年龄：输入数字
   - 旅游类型：选择一个
   - 消费水平：选择一个
3. 点击"注册"按钮
4. 注册成功后使用新账号登录

## API端点测试

### 用户相关
- POST /api/user/register/ - 用户注册
- POST /api/user/login/ - 用户登录
- GET /api/user/info/{user_id}/ - 获取用户信息
- PUT /api/user/preference/{user_id}/ - 更新用户偏好

### 目的地相关
- GET /api/destination/list/ - 获取目的地列表
- GET /api/destination/detail/{destination_id}/ - 获取目的地详情

### 推荐相关
- GET /api/recommendation/user/{user_id}/ - 获取用户推荐

## 常见问题

### Q: 前端无法连接后端
A: 检查：
1. 后端服务器是否正常运行
2. Vite代理配置是否正确
3. 浏览器控制台是否有CORS错误

### Q: 登录失败
A: 检查：
1. 用户名和密码是否正确
2. 数据库中是否存在该用户
3. 后端API是否正常响应

### Q: 推荐列表为空
A: 检查：
1. 数据库中是否有目的地数据
2. 推荐API是否正常工作
3. 浏览器控制台是否有错误信息

## 下一步建议

1. **功能完善**
   - 实现用户登出功能
   - 添加用户个人中心
   - 完善错误处理和用户提示

2. **算法优化**
   - 集成训练好的深度学习模型
   - 实现实时推荐算法
   - 添加推荐解释功能

3. **性能优化**
   - 添加数据缓存
   - 优化数据库查询
   - 实现分页功能

4. **部署准备**
   - 配置生产环境
   - 优化前端打包
   - 准备部署文档

## 技术栈总结

### 后端
- Django 6.0.2
- Django REST Framework
- MySQL 8.0
- TensorFlow 2.x

### 前端
- Vue.js 3
- Vue Router
- Element Plus
- Vite
- Axios

### 深度学习模型
- Wide&Deep
- DeepFM