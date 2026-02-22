<template>
  <div class="recommendation-container">
    <h2>为您推荐的旅游目的地</h2>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="loading-icon"><Loading /></el-icon>
      <span>加载中...</span>
    </div>
    
    <!-- 推荐列表 -->
    <div v-else-if="recommendations.length > 0" class="recommendation-list">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" v-for="item in recommendations" :key="item.destination_id">
          <el-card class="destination-card" @click="goToDetail(item.destination_id)">
            <template #header>
              <div class="card-header">
                <h3>{{ item.destination_name }}</h3>
                <div class="card-header-actions">
                  <el-icon 
                    :class="{ 'favorite-icon': isFavorite(item.destination_id) }"
                    @click.stop="toggleFavorite(item.destination_id)"
                    style="cursor: pointer; margin-right: 10px;"
                  >
                    <StarFilled v-if="isFavorite(item.destination_id)" />
                    <Star v-else />
                  </el-icon>
                  <el-rate v-model="item.rating" disabled :max="5" :precision="1"></el-rate>
                </div>
              </div>
            </template>
            <div class="card-body">
              <div class="destination-info">
                <el-icon><Location /></el-icon>
                <span>{{ item.city }} · {{ item.region }}</span>
              </div>
              <div class="destination-category">
                <el-tag size="small">{{ item.category }}</el-tag>
              </div>
              <div class="recommendation-score">
                <span>推荐指数: {{ item.score }}</span>
              </div>
            </div>
            <div class="card-footer">
              <el-button type="primary" size="small">查看详情</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 无推荐结果 -->
    <div v-else class="empty-container">
      <el-icon class="empty-icon"><InfoFilled /></el-icon>
      <p>暂无推荐结果</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { Loading, Location, InfoFilled, Star, StarFilled } from '@element-plus/icons-vue'

export default {
  name: 'RecommendationList',
  props: {
    userId: {
      type: String,
      required: true
    }
  },
  components: {
    Loading,
    Location,
    InfoFilled,
    Star,
    StarFilled
  },
  data() {
    return {
      recommendations: [],
      loading: false
    }
  },
  mounted() {
    this.getRecommendations()
  },
  methods: {
    async getRecommendations() {
      this.loading = true
      try {
        const response = await axios.get(`/recommendation/user/${this.userId}/`)
        this.recommendations = response.data
      } catch (error) {
        this.$message.error('获取推荐失败')
        console.error('Error fetching recommendations:', error)
      } finally {
        this.loading = false
      }
    },
    goToDetail(destinationId) {
      this.$router.push(`/destination/${destinationId}`)
    },
    
    // 检查是否收藏
    isFavorite(destinationId) {
      const favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      return favorites.includes(destinationId)
    },
    
    // 切换收藏状态
    toggleFavorite(destinationId) {
      let favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      
      if (favorites.includes(destinationId)) {
        // 取消收藏
        favorites = favorites.filter(id => id !== destinationId)
        this.$message.success('已取消收藏')
      } else {
        // 添加收藏
        favorites.push(destinationId)
        this.$message.success('收藏成功')
      }
      
      localStorage.setItem('favorites', JSON.stringify(favorites))
    }
  }
}
</script>

<style scoped>
.recommendation-container {
  padding: 20px;
}

.recommendation-container h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  flex-direction: column;
}

.loading-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 20px;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.recommendation-list {
  margin-top: 20px;
}

.destination-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.destination-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.card-header-actions {
  display: flex;
  align-items: center;
}

.favorite-icon {
  color: #f56c6c;
  font-size: 18px;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.card-body {
  margin: 15px 0;
}

.destination-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  color: #666;
}

.destination-info .el-icon {
  margin-right: 5px;
}

.destination-category {
  margin-bottom: 10px;
}

.recommendation-score {
  font-size: 14px;
  color: #409eff;
  font-weight: bold;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  flex-direction: column;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
}
</style>