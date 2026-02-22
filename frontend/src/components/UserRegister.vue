<template>
  <div class="register-container">
    <el-card class="register-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>用户注册</h2>
        </div>
      </template>
      <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="registerForm.gender">
            <el-radio label="male">男</el-radio>
            <el-radio label="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input v-model.number="registerForm.age" type="number" placeholder="请输入年龄"></el-input>
        </el-form-item>
        <el-form-item label="旅游类型" prop="travel_type">
          <el-select v-model="registerForm.travel_type" placeholder="请选择旅游类型">
            <el-option label="冒险型" value="adventure"></el-option>
            <el-option label="休闲型" value="leisure"></el-option>
            <el-option label="文化型" value="cultural"></el-option>
            <el-option label="自然型" value="nature"></el-option>
            <el-option label="购物型" value="shopping"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="消费水平" prop="budget_level">
          <el-select v-model="registerForm.budget_level" placeholder="请选择消费水平">
            <el-option label="低消费" value="low"></el-option>
            <el-option label="中等消费" value="medium"></el-option>
            <el-option label="高消费" value="high"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" style="width: 100%">注册</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="goToLogin" style="width: 100%">已有账号，去登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserRegister',
  data() {
    return {
      registerForm: {
        username: '',
        password: '',
        email: '',
        gender: 'male',
        age: '',
        travel_type: 'adventure',
        budget_level: 'low',
        favorite_regions: [],
        favorite_attractions: []
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' },
          { type: 'number', message: '请输入正确的年龄', trigger: 'blur' }
        ],
        travel_type: [
          { required: true, message: '请选择旅游类型', trigger: 'change' }
        ],
        budget_level: [
          { required: true, message: '请选择消费水平', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    handleRegister() {
      this.$refs.registerFormRef.validate(async (valid) => {
        if (valid) {
          try {
            console.log('发送注册请求:', this.registerForm)
            const response = await axios.post('/user/register/', this.registerForm)
            console.log('注册响应:', response)
            
            // 简化成功判断逻辑
            if (response.status === 201 || response.data.user_id) {
              console.log('注册成功，跳转到登录页面')
              this.$message.success('注册成功，请登录')
              this.$router.push('/login')
            } else {
              console.error('注册响应没有user_id:', response.data)
              this.$message.error('注册失败：响应格式错误')
            }
          } catch (error) {
            console.error('注册错误:', error)
            let errorMessage = '注册失败'
            if (error.response) {
              console.error('错误响应:', error.response.data)
              if (error.response.data && error.response.data.error) {
                errorMessage = error.response.data.error
                if (errorMessage.includes('Duplicate entry')) {
                  errorMessage = '用户名已存在，请选择其他用户名'
                }
              }
            } else if (error.request) {
              console.error('请求发送失败:', error.request)
              errorMessage = '网络错误，请检查网络连接'
            } else {
              console.error('请求配置错误:', error.message)
            }
            this.$message.error(errorMessage)
          }
        } else {
          console.error('表单验证失败')
          this.$message.error('请检查表单填写是否正确')
        }
      })
    },
    goToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.register-card {
  width: 500px;
  border-radius: 10px;
  overflow: hidden;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  color: #333;
}
</style>