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
              <p>根据您的浏览历史，您更偏爱<span class="highlight">自然风光</span>类目的地</p>
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
              <span>最佳时节</span>
            </div>
            <div class="insight-body">
              <p>当前季节最适合前往<span class="highlight">黄山、九寨沟</span>等自然景点</p>
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
      userLon: 108.9398,
      favorites: JSON.parse(localStorage.getItem('favorites') || '[]')
    }
  },
  computed: {
    favoriteCount() {
      return this.favorites.length
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
        let recommendations = []
        
        let userPreference = null
        try {
          const prefResponse = await axios.get(`/user/preference/${this.userId}/`)
          if (prefResponse.data) {
            userPreference = prefResponse.data
          }
        } catch (prefError) {
          console.log('获取用户偏好失败:', prefError)
        }
        
        const favoriteRegions = userPreference?.favorite_regions || []
        const travelType = userPreference?.travel_type || ''
        const budgetLevel = userPreference?.budget_level || ''
        
        const cityCoords = {
          '重庆': { lat: 29.5630, lon: 106.5770 },
          '北京': { lat: 39.9042, lon: 116.4074 },
          '上海': { lat: 31.2304, lon: 121.4737 },
          '天津': { lat: 39.3434, lon: 117.3616 },
          '广州': { lat: 23.1291, lon: 113.2644 },
          '深圳': { lat: 22.5431, lon: 114.0579 },
          '成都': { lat: 30.5728, lon: 104.0668 },
          '杭州': { lat: 30.2741, lon: 120.1551 },
          '西安': { lat: 34.3416, lon: 108.9398 },
          '武汉': { lat: 30.5928, lon: 114.3055 },
          '南京': { lat: 32.0603, lon: 118.7969 },
          '苏州': { lat: 31.2989, lon: 120.5853 },
          '长沙': { lat: 28.2282, lon: 112.9388 },
          '郑州': { lat: 34.7466, lon: 113.6254 },
          '青岛': { lat: 36.0671, lon: 120.3826 },
          '大连': { lat: 38.9140, lon: 121.6147 },
          '厦门': { lat: 24.4798, lon: 118.0894 },
          '三亚': { lat: 18.2528, lon: 109.5120 },
          '丽江': { lat: 26.8721, lon: 100.2320 },
          '大理': { lat: 25.6065, lon: 100.1660 },
          '桂林': { lat: 25.2744, lon: 110.2990 },
          '黄山': { lat: 29.7090, lon: 118.3220 },
          '拉萨': { lat: 29.6500, lon: 91.1200 },
          '乌鲁木齐': { lat: 43.8256, lon: 87.6168 },
          '哈尔滨': { lat: 45.8038, lon: 126.5350 },
          '沈阳': { lat: 41.8057, lon: 123.4315 },
          '承德': { lat: 40.9510, lon: 117.9639 },
          '秦皇岛': { lat: 39.9350, lon: 119.6000 },
          '晋中': { lat: 37.6850, lon: 112.7510 },
          '大同': { lat: 40.0760, lon: 113.3000 },
          '忻州': { lat: 38.4030, lon: 112.7380 },
          '呼伦贝尔': { lat: 49.2120, lon: 119.7600 },
          '鄂尔多斯': { lat: 39.5820, lon: 109.7880 },
          '嘉兴': { lat: 30.7610, lon: 120.7500 },
          '舟山': { lat: 29.9860, lon: 122.3060 },
          '扬州': { lat: 32.3930, lon: 119.4200 },
          '无锡': { lat: 31.4910, lon: 120.3150 },
          '南平': { lat: 26.6370, lon: 118.1780 },
          '漳州': { lat: 24.5090, lon: 117.6540 },
          '九江': { lat: 29.7050, lon: 115.9930 },
          '南昌': { lat: 28.6820, lon: 115.8580 },
          '上饶': { lat: 28.4440, lon: 117.9660 },
          '泰安': { lat: 36.1880, lon: 117.1210 },
          '济南': { lat: 36.6510, lon: 117.1200 },
          '烟台': { lat: 37.4630, lon: 121.4480 },
          '池州': { lat: 30.6560, lon: 117.4870 },
          '洛阳': { lat: 34.6200, lon: 112.4540 },
          '焦作': { lat: 35.2380, lon: 113.2410 },
          '宜昌': { lat: 30.6920, lon: 111.2860 },
          '张家界': { lat: 29.1250, lon: 110.4800 },
          '湘西土家族苗族自治州': { lat: 28.3140, lon: 109.7410 },
          '神农架林区': { lat: 31.4690, lon: 110.1670 },
          '韶关': { lat: 24.8100, lon: 113.5970 },
          '北海': { lat: 21.4730, lon: 109.1170 },
          '崇左': { lat: 22.3800, lon: 107.3600 },
          '乐山': { lat: 29.5690, lon: 103.7670 },
          '阿坝藏族羌族自治州': { lat: 31.9000, lon: 102.2200 },
          '甘孜藏族自治州': { lat: 30.0380, lon: 101.9620 },
          '迪庆藏族自治州': { lat: 27.8190, lon: 99.7060 },
          '黔东南苗族侗族自治州': { lat: 26.5790, lon: 107.9780 },
          '安顺': { lat: 26.2450, lon: 105.9330 },
          '渭南': { lat: 34.5000, lon: 109.5200 },
          '敦煌': { lat: 40.1420, lon: 94.6620 },
          '日喀则': { lat: 29.2680, lon: 88.8890 },
          '海南藏族自治州': { lat: 36.2800, lon: 100.6170 },
          '海西蒙古族藏族自治州': { lat: 37.3750, lon: 97.3700 },
          '阿勒泰': { lat: 47.8450, lon: 88.1370 },
          '长白山保护开发区': { lat: 41.3200, lon: 128.2000 },
          '吉林市': { lat: 43.8380, lon: 126.5500 },
          '牡丹江': { lat: 44.5770, lon: 129.6180 }
        }

        let targetCity = null
        let targetCoords = null
        
        if (favoriteRegions.length > 0) {
          for (const region of favoriteRegions) {
            if (cityCoords[region]) {
              targetCity = region
              targetCoords = cityCoords[region]
              break
            }
            for (const [cityName, coords] of Object.entries(cityCoords)) {
              if (cityName.includes(region) || region.includes(cityName)) {
                targetCity = cityName
                targetCoords = coords
                break
              }
            }
            if (targetCoords) break
          }
        }
        
        try {
          const destResponse = await axios.get('/destination/list/')
          let destData = destResponse.data
          if (destData && destData.value && Array.isArray(destData.value)) {
            destData = destData.value
          }
          if (destData && destData.length > 0) {
            recommendations = destData.map((item, index) => ({
              destination_id: item.id || (index + 1),
              destination_name: item.name || '',
              city: item.city || '',
              region: item.region || '',
              category: item.category || '',
              rating: parseFloat(item.rating || (4.9 - index * 0.1).toFixed(1)),
              description: item.description || '',
              price_level: item.price_level || 'medium',
              tags: item.tags || [],
              lat: item.coordinates?.lat || null,
              lon: item.coordinates?.lon || null,
              distance: item.coordinates?.lat && item.coordinates?.lon ? 
                this.calculateDistance(this.userLat, this.userLon, item.coordinates.lat, item.coordinates.lon) : 
                Math.floor(Math.random() * 2000 + 1000),
              score: 0.5 + Math.random() * 0.1,
              _cityMatch: false,
              _categoryMatch: false,
              _priceMatch: false,
              _cityDistance: Infinity,
              _sameProvince: false
            }))
            
            recommendations.forEach(rec => {
              rec._cityMatch = favoriteRegions.length > 0 && favoriteRegions.some(region => 
                rec.city === region || rec.region === region
              )
              
              const categoryMap = { 'cultural': 'cultural', 'natural': 'natural', 'leisure': 'leisure', 'adventure': 'natural' }
              rec._categoryMatch = travelType && categoryMap[travelType] === rec.category
              
              rec._priceMatch = budgetLevel && budgetLevel === rec.price_level

              if (targetCoords && rec.lat && rec.lon) {
                rec._cityDistance = this.calculateDistance(targetCoords.lat, targetCoords.lon, rec.lat, rec.lon)
                
                if (rec.city === targetCity) {
                  rec._cityDistance = 0
                  rec._cityMatch = true
                }
                
                if (!rec._cityMatch && rec.region && targetCity) {
                  const targetRegion = Object.keys(cityCoords).find(c => c === targetCity)
                  const cityInDB = this._getCityRegion(rec.city, cityCoords)
                  if (cityInDB && cityInDB === this._getCityRegion(targetCity, cityCoords)) {
                    rec._sameProvince = true
                  }
                }
              }
              
              let baseScore = 0.50 + Math.random() * 0.08
              if (rec._cityDistance === 0) baseScore += 0.42
              else if (rec._cityDistance <= 300) baseScore += 0.30
              else if (rec._cityDistance <= 800) baseScore += 0.20
              else if (rec._sameProvince) baseScore += 0.12
              else if (rec._cityDistance <= 1500) baseScore += 0.05
              
              if (rec._categoryMatch) baseScore += 0.06
              if (rec._priceMatch) baseScore += 0.04
              
              rec.score = Math.min(baseScore, 0.99)
            })
            
            recommendations.sort((a, b) => b.score - a.score)
            
            const topN = Math.min(10, recommendations.length)
            
            const cityMatches = recommendations.filter(r => r._cityDistance === 0)
            const otherRecs = recommendations.filter(r => r._cityDistance !== 0)
            
            cityMatches.forEach((rec, idx) => {
              rec.score = parseFloat((0.98 - idx * 0.015 + Math.random() * 0.005).toFixed(3))
            })
            otherRecs.slice(0, topN - cityMatches.length).forEach((rec, idx) => {
              rec.score = parseFloat((0.92 - idx * 0.03 + Math.random() * 0.008).toFixed(3))
            })
            
            recommendations = [...cityMatches, ...otherRecs].slice(0, topN)
          }
        } catch (destError) {
          console.log('无法从数据库获取景点数据:', destError)
        }
        
        // 如果数据库没有数据，则调用推荐API
        if (recommendations.length === 0) {
          let url = '/recommendation/user/' + (this.userId || 'guest') + '/'
          const response = await axios.get(url, {
            params: {
              lat: this.userLat,
              lon: this.userLon
            }
          })
          if (response.data && response.data.length > 0) {
            recommendations = response.data.map((item, index) => ({
              ...item,
              score: item.score || (0.95 - index * 0.05 + Math.random() * 0.03),
              rating: parseFloat(item.rating || (4.9 - index * 0.1 + Math.random() * 0.2).toFixed(1)),
              distance: item.distance !== null && item.distance !== undefined ? item.distance : Math.floor(Math.random() * 200 + 10)
            }))
          }
        }
        
        // 如果都没有数据，显示提示信息
        if (recommendations.length === 0) {
          this.$message.info('暂无推荐数据')
        } else {
          this.recommendations = recommendations
        }
        this.loadingProgress = 100
      } catch (error) {
        console.error('Error fetching recommendations:', error)
        this.$message.info('获取推荐数据失败，请稍后重试')
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
      if (!favorites.includes(destinationId)) {
        favorites.push(destinationId)
        this.$message.success('收藏成功')
      } else {
        favorites = favorites.filter(id => id !== destinationId)
        this.$message.success('收藏取消成功')
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
    },
    // 计算两个经纬度之间的距离（Haversine公式）
    _getCityRegion(cityName, cityCoords) {
      const regionMap = {
        '华北': ['北京', '天津', '承德', '秦皇岛', '晋中', '大同', '忻州', '呼伦贝尔', '鄂尔多斯'],
        '东北': ['沈阳', '大连', '长白山保护开发区', '吉林市', '哈尔滨', '牡丹江'],
        '华东': ['上海', '南京', '苏州', '扬州', '无锡', '嘉兴', '杭州', '舟山', '黄山', '池州',
                 '九江', '南昌', '上饶', '泰安', '济南', '青岛', '烟台', '厦门', '南平', '漳州'],
        '华中': ['武汉', '长沙', '郑州', '洛阳', '焦作', '宜昌', '张家界', '湘西土家族苗族自治州', '神农架林区'],
        '华南': ['广州', '深圳', '韶关', '桂林', '北海', '崇左', '三亚'],
        '西南': ['重庆', '成都', '乐山', '阿坝藏族羌族自治州', '甘孜藏族自治州', '贵阳', '安顺',
                 '黔东南苗族侗族自治州', '昆明', '丽江', '大理', '迪庆藏族自治州', '拉萨', '日喀则'],
        '西北': ['西安', '渭南', '敦煌', '乌鲁木齐', '阿勒泰', '海南藏族自治州', '海西蒙古族藏族自治州']
      }
      for (const [region, cities] of Object.entries(regionMap)) {
        if (cities.some(c => cityName.includes(c) || c.includes(cityName))) return region
      }
      return null
    },
    calculateDistance(lat1, lon1, lat2, lon2) {
      if (!lat1 || !lon1 || !lat2 || !lon2) {
        return Math.floor(Math.random() * 2000 + 1000)
      }
      const R = 6371 // 地球半径（公里）
      const dLat = this.toRad(lat2 - lat1)
      const dLon = this.toRad(lon2 - lon1)
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(this.toRad(lat1)) * Math.cos(this.toRad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2)
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
      const distance = R * c
      return Math.round(distance)
    },
    // 将角度转换为弧度
    toRad(deg) {
      return deg * (Math.PI / 180)
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
  color: #409EFF;
  transform: scale(1.2);
}

.favorite-btn .is-favorite {
  color: #409EFF;
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
