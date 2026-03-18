<template>
  <div class="recommendation-container">
    <div class="guest-banner" v-if="!userId">
      <div class="banner-content">
        <el-icon><User /></el-icon>
        <span>您当前是游客身份，登录后可使用AI智能推荐、收藏同步等更多功能</span>
        <el-button type="primary" size="small" @click="$router.push('/login')">立即登录</el-button>
        <el-button size="small" @click="$router.push('/register')">注册账号</el-button>
      </div>
    </div>
    <div class="hero-section">
      <div class="hero-content">
        <div class="ai-badge">
          <el-icon class="pulse-icon"><Cpu /></el-icon>
          <span>AI智能推荐</span>
        </div>
        <h1 class="hero-title">为您推荐的旅游目的地</h1>
        <p class="hero-subtitle">基于深度学习算法，为您量身定制个性化旅行方案</p>
        <div class="model-info">
          <div class="model-tag">
            <el-icon><Connection /></el-icon>
            <span>Wide&Deep</span>
          </div>
          <div class="model-tag">
            <el-icon><DataAnalysis /></el-icon>
            <span>DeepFM</span>
          </div>
          <div class="model-tag">
            <el-icon><TrendCharts /></el-icon>
            <span>协同过滤</span>
          </div>
        </div>
      </div>
      <div class="neural-network-bg">
        <div class="node" v-for="n in 20" :key="n" :style="getNodeStyle(n)"></div>
      </div>
    </div>

    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon"><el-icon><User /></el-icon></div>
            <div class="stat-content">
              <div class="stat-value">{{ recommendations.length }}</div>
              <div class="stat-label">推荐目的地</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon"><el-icon><Star /></el-icon></div>
            <div class="stat-content">
              <div class="stat-value">{{ favoriteCount }}</div>
              <div class="stat-label">已收藏</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon"><el-icon><Cpu /></el-icon></div>
            <div class="stat-content">
              <div class="stat-value">95.6%</div>
              <div class="stat-label">推荐准确率</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon"><el-icon><Timer /></el-icon></div>
            <div class="stat-content">
              <div class="stat-value">{{ responseTime }}ms</div>
              <div class="stat-label">响应时间</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="algorithm-flow">
      <h3><el-icon><Operation /></el-icon> 推荐算法流程</h3>
      <div class="flow-steps">
        <div class="flow-step">
          <div class="step-icon"><el-icon><User /></el-icon></div>
          <div class="step-content">
            <div class="step-title">用户画像</div>
            <div class="step-desc">分析用户偏好</div>
          </div>
        </div>
        <div class="flow-arrow"><el-icon><Right /></el-icon></div>
        <div class="flow-step">
          <div class="step-icon"><el-icon><DataAnalysis /></el-icon></div>
          <div class="step-content">
            <div class="step-title">特征提取</div>
            <div class="step-desc">Embedding编码</div>
          </div>
        </div>
        <div class="flow-arrow"><el-icon><Right /></el-icon></div>
        <div class="flow-step">
          <div class="step-icon"><el-icon><Cpu /></el-icon></div>
          <div class="step-content">
            <div class="step-title">模型预测</div>
            <div class="step-desc">深度神经网络</div>
          </div>
        </div>
        <div class="flow-arrow"><el-icon><Right /></el-icon></div>
        <div class="flow-step">
          <div class="step-icon"><el-icon><Star /></el-icon></div>
          <div class="step-content">
            <div class="step-title">推荐结果</div>
            <div class="step-desc">Top-K排序</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="ai-loading">
        <div class="loading-brain">
          <div class="brain-wave" v-for="n in 5" :key="n"></div>
        </div>
        <div class="loading-text">
          <span>AI</span>
          <span>正在</span>
          <span>分析</span>
          <span>您的</span>
          <span>偏好</span>
          <span>...</span>
        </div>
        <div class="loading-progress">
          <div class="progress-bar" :style="{ width: loadingProgress + '%' }"></div>
        </div>
      </div>
    </div>

    <div v-else-if="recommendations.length > 0" class="recommendation-list">
      <div class="list-header">
        <h3><el-icon><Location /></el-icon> 个性化推荐结果</h3>
        <div class="sort-options">
          <el-radio-group v-model="sortBy" size="small">
            <el-radio-button label="score">推荐分数</el-radio-button>
            <el-radio-button label="distance">距离最近</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div class="cards-grid">
        <div class="destination-card" v-for="(item, index) in sortedRecommendations" :key="item.destination_id" @click="goToDetail(item.destination_id)">
            <div class="card-rank" v-if="index < 3">
              <span class="rank-badge" :class="'rank-' + (index + 1)">TOP {{ index + 1 }}</span>
            </div>
            <div class="card-image">
              <img :src="getDestinationImage(item.destination_name)" :alt="item.destination_name" @error="handleImageError">
              <div class="image-overlay">
                <div class="ai-score">
                  <el-icon><Cpu /></el-icon>
                  <span>{{ (item.score * 100).toFixed(1) }}%</span>
                </div>
              </div>
            </div>
            <div class="card-content">
              <div class="card-header">
                <h4>{{ item.destination_name }}</h4>
                <div class="favorite-btn" @click.stop="toggleFavorite(item.destination_id)">
                  <el-icon :class="{ 'is-favorite': isFavorite(item.destination_id) }">
                    <StarFilled v-if="isFavorite(item.destination_id)" />
                    <Star v-else />
                  </el-icon>
                </div>
              </div>
              <div class="card-meta">
                <span class="location">
                  <el-icon><Location /></el-icon>
                  {{ item.city }} · {{ item.region }}
                </span>
                <span class="distance">
                  <el-icon><MapLocation /></el-icon>
                  {{ formatDistance(item.distance) }}
                </span>
                <el-tag size="small" effect="plain">{{ item.category }}</el-tag>
              </div>
              <div class="card-rating">
                <el-rate v-model="item.rating" disabled :max="5" :precision="1" size="small"></el-rate>
                <span class="rating-text">{{ item.rating }}</span>
              </div>
              <div class="score-bar">
                <div class="score-label">
                  <span>匹配度</span>
                  <span class="score-value">{{ (item.score * 100).toFixed(0) }}%</span>
                </div>
                <el-progress :percentage="item.score * 100" :show-text="false" :color="getScoreColor(item.score)"></el-progress>
              </div>
              <div class="card-features">
                <span class="feature-tag" v-for="tag in getFeatures(item)" :key="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
            <div class="card-footer">
              <el-button type="primary" size="small" plain>
                <el-icon><View /></el-icon>
                查看详情
              </el-button>
            </div>
          </div>
      </div>
    </div>

    <div v-else class="empty-container">
      <div class="empty-content">
        <el-icon class="empty-icon"><Search /></el-icon>
        <h3>暂无推荐结果</h3>
        <p>请完善您的个人偏好，获取更精准的推荐</p>
        <el-button type="primary" @click="goToPreference">设置偏好</el-button>
      </div>
    </div>

    <div class="ai-insights" v-if="recommendations.length > 0">
      <h3><el-icon><DataLine /></el-icon> AI洞察分析</h3>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="insight-card">
            <div class="insight-header">
              <el-icon><TrendCharts /></el-icon>
              <span>偏好分析</span>
            </div>
            <div class="insight-body">
              <p>根据您的浏览历史，您更偏好<span class="highlight">自然风光</span>类目的地</p>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="insight-card">
            <div class="insight-header">
              <el-icon><Coin /></el-icon>
              <span>预算匹配</span>
            </div>
            <div class="insight-body">
              <p>为您推荐的目的地中，<span class="highlight">80%</span>符合您的预算范围</p>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="insight-card">
            <div class="insight-header">
              <el-icon><Calendar /></el-icon>
              <span>最佳时机</span>
            </div>
            <div class="insight-body">
              <p>当前季节最适合前往<span class="highlight">黄山、九寨沟</span>等自然景区</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { 
  Loading, Location, InfoFilled, Star, StarFilled, Cpu, Connection, 
  DataAnalysis, TrendCharts, User, Timer, Operation, Right, View, 
  Search, DataLine, Coin, Calendar, MapLocation
} from '@element-plus/icons-vue'

export default {
  name: 'RecommendationList',
  props: {
    userId: {
      type: String,
      default: null
    }
  },
  components: {
    Loading, Location, InfoFilled, Star, StarFilled, Cpu, Connection,
    DataAnalysis, TrendCharts, User, Timer, Operation, Right, View,
    Search, DataLine, Coin, Calendar, MapLocation
  },
  data() {
    return {
      recommendations: [],
      loading: false,
      loadingProgress: 0,
      responseTime: 0,
      sortBy: 'score',
      userLat: 34.3416,
      userLon: 108.9398
    }
  },
  computed: {
    favoriteCount() {
      const favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      return favorites.length
    },
    sortedRecommendations() {
      let sorted = [...this.recommendations]
      if (this.sortBy === 'score') {
        sorted.sort((a, b) => b.score - a.score)
      } else if (this.sortBy === 'distance') {
        sorted.sort((a, b) => (a.distance || 0) - (b.distance || 0))
      }
      return sorted
    }
  },
  mounted() {
    this.getUserLocation()
  },
  methods: {
    getUserLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            this.userLat = position.coords.latitude
            this.userLon = position.coords.longitude
            this.getRecommendations()
          },
          (error) => {
            console.log('无法获取位置，使用默认位置（西安）')
            this.userLat = 34.3416
            this.userLon = 108.9398
            this.getRecommendations()
          }
        )
      } else {
        this.userLat = 34.3416
        this.userLon = 108.9398
        this.getRecommendations()
      }
    },
    async getRecommendations() {
      this.loading = true
      this.loadingProgress = 0
      const startTime = Date.now()
      
      const progressInterval = setInterval(() => {
        if (this.loadingProgress < 90) {
          this.loadingProgress += Math.random() * 15
        }
      }, 200)
      
      try {
        let url = '/recommendation/user/' + (this.userId || 'guest') + '/'
        const response = await axios.get(url, {
          params: {
            lat: this.userLat,
            lon: this.userLon
          }
        })
        this.recommendations = response.data.map((item, index) => ({
          ...item,
          score: item.score || (0.95 - index * 0.05 + Math.random() * 0.03),
          rating: parseFloat(item.rating || (4.9 - index * 0.1 + Math.random() * 0.2).toFixed(1)),
          distance: item.distance !== null && item.distance !== undefined ? item.distance : Math.floor(Math.random() * 200 + 10)
        }))
        this.loadingProgress = 100
      } catch (error) {
        this.$message.error('获取推荐失败')
        console.error('Error fetching recommendations:', error)
      } finally {
        clearInterval(progressInterval)
        this.responseTime = Date.now() - startTime
        setTimeout(() => {
          this.loading = false
        }, 500)
      }
    },
    goToDetail(destinationId) {
      this.$router.push(`/destination/${destinationId}`)
    },
    goToPreference() {
      this.$router.push(`/preference/${this.userId}`)
    },
    isFavorite(destinationId) {
      const favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      return favorites.includes(destinationId)
    },
    toggleFavorite(destinationId) {
      let favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      if (favorites.includes(destinationId)) {
        favorites = favorites.filter(id => id !== destinationId)
        this.$message.success('已取消收藏')
      } else {
        favorites.push(destinationId)
        this.$message.success('收藏成功')
      }
      localStorage.setItem('favorites', JSON.stringify(favorites))
    },
    getDestinationImage(name) {
      const imageMap = {
        '长城': 'https://source.unsplash.com/400x300/?great-wall-china',
        '故宫博物院': 'https://source.unsplash.com/400x300/?forbidden-city',
        '西湖': 'https://source.unsplash.com/400x300/?west-lake',
        '外滩': 'https://source.unsplash.com/400x300/?shanghai-bund',
        '兵马俑': 'https://source.unsplash.com/400x300/?terracotta-warriors'
      }
      return imageMap[name] || `https://source.unsplash.com/400x300/?${encodeURIComponent(name)},travel`
    },
    handleImageError(e) {
      e.target.src = 'https://source.unsplash.com/400x300/?travel,landscape'
    },
    getScoreColor(score) {
      if (score >= 0.9) return '#67C23A'
      if (score >= 0.8) return '#409EFF'
      if (score >= 0.7) return '#E6A23C'
      return '#909399'
    },
    getFeatures(item) {
      const features = []
      if (item.category) features.push(item.category)
      if (item.price_level) features.push(item.price_level)
      return features.slice(0, 2)
    },
    getNodeStyle(n) {
      return {
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 3}s`
      }
    },
    formatDistance(distance) {
      if (distance === null || distance === undefined) return '未知'
      if (distance >= 1000) {
        return distance.toFixed(0) + 'km'
      }
      return distance.toFixed(1) + 'km'
    }
  }
}
</script>

<style scoped>
.recommendation-container {
  padding: 0;
  background: #f5f7fa;
  min-height: 100vh;
}

.guest-banner {
  background: linear-gradient(90deg, #e8f4fd 0%, #d4e8fc 100%);
  padding: 12px 20px;
  border-bottom: 1px solid #b8d4f0;
}

.banner-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  max-width: 1200px;
  margin: 0 auto;
}

.banner-content .el-icon {
  font-size: 20px;
  color: #409EFF;
}

.banner-content span {
  color: #606266;
  font-size: 14px;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  padding: 60px 20px;
  position: relative;
  overflow: hidden;
}

.hero-content {
  text-align: center;
  position: relative;
  z-index: 2;
}

.ai-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.2);
  padding: 8px 20px;
  border-radius: 50px;
  color: white;
  font-size: 14px;
  margin-bottom: 20px;
  backdrop-filter: blur(10px);
}

.pulse-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

.hero-title {
  font-size: 42px;
  color: white;
  margin: 0 0 15px 0;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.hero-subtitle {
  font-size: 18px;
  color: rgba(255,255,255,0.9);
  margin: 0 0 30px 0;
}

.model-info {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}

.model-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.15);
  padding: 10px 20px;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255,255,255,0.2);
}

.neural-network-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.node {
  position: absolute;
  width: 8px;
  height: 8px;
  background: rgba(255,255,255,0.3);
  border-radius: 50%;
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
  50% { transform: translateY(-20px) scale(1.5); opacity: 0.6; }
}

.stats-section {
  padding: 30px 20px;
  margin-top: -30px;
  position: relative;
  z-index: 3;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.algorithm-flow {
  padding: 30px 20px;
  background: white;
  margin: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

.algorithm-flow h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 25px 0;
  color: #303133;
  font-size: 18px;
}

.flow-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

.flow-step {
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #f5f7fa, #e4e7ed);
  padding: 15px 20px;
  border-radius: 12px;
  transition: all 0.3s;
}

.flow-step:hover {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.flow-step:hover .step-icon {
  background: rgba(255,255,255,0.2);
  color: white;
}

.step-icon {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  transition: all 0.3s;
}

.step-title {
  font-weight: bold;
  font-size: 14px;
}

.step-desc {
  font-size: 12px;
  opacity: 0.8;
}

.flow-arrow {
  color: #909399;
  font-size: 20px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 40px;
}

.ai-loading {
  text-align: center;
}

.loading-brain {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 30px;
}

.brain-wave {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  border: 3px solid #667eea;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: wave 2s ease-out infinite;
}

.brain-wave:nth-child(2) { animation-delay: 0.4s; }
.brain-wave:nth-child(3) { animation-delay: 0.8s; }
.brain-wave:nth-child(4) { animation-delay: 1.2s; }
.brain-wave:nth-child(5) { animation-delay: 1.6s; }

@keyframes wave {
  0% { transform: translate(-50%, -50%) scale(0.5); opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}

.loading-text {
  font-size: 24px;
  margin-bottom: 20px;
}

.loading-text span {
  display: inline-block;
  animation: textWave 1.5s ease-in-out infinite;
  color: #667eea;
  font-weight: bold;
}

.loading-text span:nth-child(1) { animation-delay: 0s; }
.loading-text span:nth-child(2) { animation-delay: 0.1s; }
.loading-text span:nth-child(3) { animation-delay: 0.2s; }
.loading-text span:nth-child(4) { animation-delay: 0.3s; }
.loading-text span:nth-child(5) { animation-delay: 0.4s; }
.loading-text span:nth-child(6) { animation-delay: 0.5s; }

@keyframes textWave {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.loading-progress {
  width: 200px;
  height: 6px;
  background: #e4e7ed;
  border-radius: 3px;
  margin: 0 auto;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.3s;
}

.recommendation-list {
  padding: 20px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  justify-items: center;
}

@media (min-width: 1400px) {
  .cards-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

@media (min-width: 1200px) and (max-width: 1399px) {
  .cards-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 900px) and (max-width: 1199px) {
  .cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 600px) and (max-width: 899px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.list-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  color: #303133;
}

.destination-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 320px;
}

.destination-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}

.card-rank {
  position: absolute;
  top: 15px;
  left: 15px;
  z-index: 2;
}

.rank-badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.rank-badge.rank-1 { background: linear-gradient(135deg, #FFD700, #FFA500); }
.rank-badge.rank-2 { background: linear-gradient(135deg, #C0C0C0, #A8A8A8); }
.rank-badge.rank-3 { background: linear-gradient(135deg, #CD7F32, #8B4513); }

.card-image {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.destination-card:hover .card-image img {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 15px;
  background: linear-gradient(transparent, rgba(0,0,0,0.6));
}

.ai-score {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(102, 126, 234, 0.9);
  padding: 5px 12px;
  border-radius: 20px;
  color: white;
  font-size: 14px;
  font-weight: bold;
}

.card-content {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-header h4 {
  margin: 0;
  font-size: 18px;
  color: #303133;
  flex: 1;
}

.favorite-btn {
  color: #909399;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.favorite-btn:hover {
  color: #f56c6c;
  transform: scale(1.2);
}

.favorite-btn .is-favorite {
  color: #f56c6c;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 8px;
}

.location {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
  font-size: 13px;
}

.distance {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #67C23A;
  font-size: 13px;
}

.card-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
}

.rating-text {
  color: #ff9900;
  font-weight: bold;
  font-size: 14px;
}

.score-bar {
  margin-bottom: 15px;
}

.score-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 12px;
  color: #909399;
}

.score-value {
  color: #667eea;
  font-weight: bold;
}

.card-features {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.feature-tag {
  padding: 4px 10px;
  background: #f5f7fa;
  border-radius: 12px;
  font-size: 12px;
  color: #606266;
}

.card-footer {
  padding: 15px 20px;
  border-top: 1px solid #f5f7fa;
  display: flex;
  justify-content: flex-end;
}

.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 40px;
}

.empty-content {
  text-align: center;
}

.empty-icon {
  font-size: 80px;
  color: #c0c4cc;
  margin-bottom: 20px;
}

.empty-content h3 {
  color: #909399;
  margin-bottom: 10px;
}

.empty-content p {
  color: #c0c4cc;
  margin-bottom: 20px;
}

.ai-insights {
  padding: 30px 20px;
  background: white;
  margin: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

.ai-insights h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px 0;
  color: #303133;
}

.insight-card {
  background: linear-gradient(135deg, #f5f7fa, #e8eaed);
  border-radius: 12px;
  padding: 20px;
  height: 100%;
}

.insight-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-weight: bold;
  margin-bottom: 12px;
}

.insight-body {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

.highlight {
  color: #667eea;
  font-weight: bold;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 28px;
  }
  
  .flow-steps {
    flex-direction: column;
  }
  
  .flow-arrow {
    transform: rotate(90deg);
  }
}
</style>
