<template>
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>用户登录</h2>
        </div>
      </template>
      <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" style="width: 100%">登录</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="goToRegister" style="width: 100%">注册新用户</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserLogin',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleLogin() {
      // 简化登录逻辑，直接发送请求
      console.log('登录请求数据:', this.loginForm)
      console.log('请求URL:', '/user/login/')
      
      // 明确使用完整路径
      axios.post('/api/user/login/', this.loginForm)
        .then(response => {
          console.log('登录响应:', response)
          if (response.data.user_id) {
            localStorage.setItem('userId', response.data.user_id)
            this.$message.success('登录成功')
            this.$router.push(`/recommendations/${response.data.user_id}`)
          }
        })
        .catch(error => {
          console.error('登录错误:', error)
          let errorMessage = '登录失败'
          if (error.response) {
            console.error('错误响应:', error.response)
            errorMessage = error.response.data.error || '登录失败'
          } else if (error.request) {
            console.error('错误请求:', error.request)
            errorMessage = '网络错误，请检查服务器连接'
          } else {
            console.error('错误信息:', error.message)
            errorMessage = '登录失败: ' + error.message
          }
          this.$message.error(errorMessage)
        })
    },
    goToRegister() {
      this.$router.push('/register')
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
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