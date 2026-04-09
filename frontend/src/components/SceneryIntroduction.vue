<template>
  <div class="scenery-container" v-loading="loading">
    <div class="page-header">
      <h2>🏞️ 风景名胜介绍</h2>
      <p>探索祖国大好河山，感受自然之美</p>
    </div>

    <div class="category-tabs">
      <el-radio-group v-model="activeCategory" @change="filterScenery">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="自然风光">自然风光</el-radio-button>
        <el-radio-button label="历史古迹">历史古迹</el-radio-button>
        <el-radio-button label="现代都市">现代都市</el-radio-button>
        <el-radio-button label="民族风情">民族风情</el-radio-button>
      </el-radio-group>
    </div>

    <div class="scenery-grid">
      <el-card v-for="scenery in filteredScenery" :key="scenery.id" class="scenery-card" shadow="hover">
        <div class="scenery-image">
          <img :src="scenery.image" :alt="scenery.name" @error="handleImageError">
          <div class="scenery-overlay">
            <h3>{{ scenery.name }}</h3>
            <p class="scenery-location">📍 {{ scenery.location }}</p>
          </div>
        </div>
        <div class="scenery-content">
          <div class="scenery-meta">
            <el-tag :type="getCategoryType(scenery.category)">{{ scenery.category }}</el-tag>
            <el-rate v-model="scenery.rating" disabled text-color="#ff9900" size="small" />
          </div>
          <p class="scenery-desc">{{ scenery.description }}</p>
          <div class="scenery-features">
            <div class="feature-item">
              <span class="feature-label">最佳季节：</span>
              <span class="feature-value">{{ scenery.bestSeason }}</span>
            </div>
            <div class="feature-item">
              <span class="feature-label">游玩时长：</span>
              <span class="feature-value">{{ scenery.duration }}</span>
            </div>
            <div class="feature-item">
              <span class="feature-label">门票价格：</span>
              <span class="feature-value">{{ scenery.price }}</span>
            </div>
          </div>
          <div class="scenery-tags">
            <el-tag v-for="tag in scenery.tags" :key="tag" size="small" effect="plain">{{ tag }}</el-tag>
          </div>
        </div>
      </el-card>
    </div>

    <div v-if="filteredScenery.length === 0" class="empty-state">
      <el-empty description="暂无符合条件的风景"></el-empty>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'SceneryIntroduction',
  setup() {
    const activeCategory = ref('')
    const loading = ref(false)

    const sceneryList = ref([])

    const categoryMap = {
      'natural': '自然风光',
      'cultural': '历史古迹',
      'leisure': '现代都市',
      'ethnic': '民族风情'
    }

    const fetchDestinations = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/destination/list/')
        if (response.data && Array.isArray(response.data)) {
          sceneryList.value = response.data.map((dest, index) => ({
            id: dest.id,
            name: dest.name,
            location: `${dest.city}${dest.region ? '·' + dest.region : ''}`,
            category: categoryMap[dest.category] || dest.category || '自然风光',
            description: dest.description || '暂无描述',
            bestSeason: dest.popular_season || '四季皆宜',
            duration: '1-3天',
            price: dest.price_level === 'low' ? '免费' : dest.price_level === 'medium' ? '50-200元/人' : '200元以上/人',
            rating: parseFloat(dest.rating || (4.5 + Math.random() * 0.5).toFixed(1)),
            tags: dest.tags || ['热门景点'],
            image: dest.images && dest.images.length > 0 ? dest.images[0] : 'https://picsum.photos/600/400?random=' + index
          }))
        }
      } catch (error) {
        console.error('获取景点失败:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchDestinations()
    })

    const filteredScenery = computed(() => {
      if (!activeCategory.value) {
        return sceneryList.value
      }
      return sceneryList.value.filter(s => s.category === activeCategory.value)
    })

    const filterScenery = () => {
      // 过滤逻辑已在computed中实现
    }

    const getCategoryType = (category) => {
      const typeMap = {
        '自然风光': 'success',
        '历史古迹': 'warning',
        '现代都市': 'primary',
        '民族风情': 'danger'
      }
      return typeMap[category] || 'info'
    }

    const handleImageError = (e) => {
      e.target.src = 'https://via.placeholder.com/600x400?text=风景图片'
    }

    return {
      activeCategory,
      loading,
      sceneryList,
      filteredScenery,
      filterScenery,
      getCategoryType,
      handleImageError
    }
  }
}
</script>

<style scoped>
.scenery-container {
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
}

.page-header p {
  color: #666;
  font-size: 16px;
}

.category-tabs {
  margin-bottom: 30px;
  text-align: center;
}

.scenery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

@media (max-width: 1400px) {
  .scenery-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1000px) {
  .scenery-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .scenery-grid {
    grid-template-columns: 1fr;
  }
}

.scenery-card {
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s;
}

.scenery-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.scenery-image {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.scenery-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.scenery-card:hover .scenery-image img {
  transform: scale(1.1);
}

.scenery-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  padding: 15px;
  color: white;
}

.scenery-overlay h3 {
  font-size: 16px;
  margin-bottom: 3px;
}

.scenery-location {
  font-size: 12px;
  opacity: 0.9;
}

.scenery-content {
  padding: 15px;
}

.scenery-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.scenery-desc {
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
  font-size: 13px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.scenery-features {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 12px;
}

.feature-item {
  display: flex;
  justify-content: space-between;
  padding: 3px 0;
  font-size: 13px;
}

.feature-label {
  color: #888;
}

.feature-value {
  color: #333;
  font-weight: 500;
}

.scenery-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 50px;
}
</style>
