<template>
  <div class="app-container">
    <el-container>
      <el-header height="60px" class="app-header">
        <div class="header-content">
          <h1 class="app-title">旅游目的地智能推荐系统</h1>
          <div class="header-nav">
            <el-button type="primary" @click="goToLogin">登录</el-button>
            <el-button @click="goToRegister">注册</el-button>
          </div>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view></router-view>
      </el-main>
      <el-footer height="60px" class="app-footer">
        <p>© 2026 旅游目的地智能推荐系统 | 基于深度学习技术</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { Star, Cpu, Location } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    Star,
    Cpu,
    Location
  },
  methods: {
    goToLogin() {
      this.$router.push('/login')
    },
    goToRegister() {
      this.$router.push('/register')
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f7fa;
}

.app-container {
  min-height: 100vh;
}

.app-header {
  background-color: #409eff;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.app-title {
  font-size: 20px;
  font-weight: bold;
}

.header-nav {
  display: flex;
  gap: 10px;
}

.app-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  margin-bottom: 40px;
}

.hero-section h2 {
  font-size: 36px;
  margin-bottom: 20px;
}

.hero-section p {
  font-size: 18px;
  margin-bottom: 30px;
  opacity: 0.9;
}

.features-section {
  margin-top: 40px;
}

.features-section h3 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #333;
}

.feature-card {
  height: 100%;
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.feature-icon {
  font-size: 24px;
  color: #409eff;
}

.app-footer {
  background-color: #333;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 10px 20px;
  }
  
  .app-title {
    margin-bottom: 10px;
  }
  
  .hero-section h2 {
    font-size: 24px;
  }
  
  .hero-section p {
    font-size: 14px;
  }
  
  .el-col {
    flex: 100%;
    max-width: 100%;
  }
}
</style>