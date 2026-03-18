<template>
  <div class="home-container">
    <el-card class="home-card">
      <div class="home-content">
        <el-icon class="home-icon"><HomeFilled /></el-icon>
        <h2>正在跳转到主页...</h2>
        <p>如果没有自动跳转，请点击下方按钮</p>
        <el-button type="primary" @click="goToRecommendations">前往推荐列表</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { HomeFilled } from '@element-plus/icons-vue'

export default {
  name: 'HomePage',
  components: {
    HomeFilled
  },
  mounted() {
    this.goToRecommendations()
  },
  methods: {
    goToRecommendations() {
      const userId = localStorage.getItem('userId')
      if (userId) {
        this.$router.push(`/recommendations/${userId}`)
      } else {
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.home-card {
  width: 400px;
  text-align: center;
}

.home-content {
  padding: 40px 20px;
}

.home-icon {
  font-size: 64px;
  color: #409EFF;
  margin-bottom: 20px;
}

.home-content h2 {
  margin-bottom: 10px;
  color: #303133;
}

.home-content p {
  color: #909399;
  margin-bottom: 20px;
}
</style>
