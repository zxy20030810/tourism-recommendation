<template>
  <div class="collection-container" v-loading="loading">
    <div class="page-header">
      <h2>💖 我的收藏</h2>
      <p>查看您收藏的景点和旅游攻略</p>
    </div>

    <div class="collection-tabs">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="收藏的景点" name="destinations"></el-tab-pane>
        <el-tab-pane label="收藏的攻略" name="guides"></el-tab-pane>
      </el-tabs>
    </div>

    <div v-if="activeTab === 'destinations'" class="collection-list">
      <el-card v-for="destination in collectedDestinations" :key="destination.destination_id" class="collection-card" shadow="hover">
        <div class="destination-info">
          <h3 class="destination-name">{{ destination.destination_name }}</h3>
          <p class="destination-city">{{ destination.city }}</p>
          <p class="destination-description">{{ destination.description }}</p>
          <div class="destination-meta">
            <span class="rating">⭐ {{ destination.rating }}</span>
            <span class="distance">📍 {{ destination.distance }}km</span>
            <span class="price">💰 {{ getPriceLevel(destination.price_level) }}</span>
          </div>
          <div class="destination-tags">
            <el-tag v-for="tag in destination.tags" :key="tag" size="small" effect="plain">{{ tag }}</el-tag>
          </div>
          <div class="collection-actions">
            <el-button type="primary" size="small" @click="goToDetail(destination.destination_id)">
              查看详情
            </el-button>
            <el-button type="danger" size="small" @click="removeDestination(destination.destination_id)">
              取消收藏
            </el-button>
          </div>
        </div>
      </el-card>
      <div v-if="collectedDestinations.length === 0" class="empty-state">
        <el-empty description="暂无收藏的景点"></el-empty>
      </div>
    </div>

    <div v-if="activeTab === 'guides'" class="collection-list">
      <el-card v-for="guide in collectedGuides" :key="guide.id" class="collection-card" shadow="hover" @click="goToGuideDetail(guide.id)" style="cursor: pointer;">
        <div class="guide-info">
          <div class="guide-header">
            <el-tag :type="getCategoryType(guide.category)">{{ guide.category }}</el-tag>
            <span class="guide-author">{{ guide.author }}</span>
          </div>
          <h3 class="guide-title">{{ guide.title }}</h3>
          <p class="guide-summary">{{ guide.summary }}</p>
          <div class="guide-tags">
            <el-tag v-for="tag in guide.tags" :key="tag" size="small" effect="plain">{{ tag }}</el-tag>
          </div>
          <div class="guide-meta">
            <span class="guide-date">{{ guide.date }}</span>
            <span class="guide-views">{{ guide.views }} 浏览</span>
            <span class="guide-likes">{{ guide.likes }} 点赞</span>
          </div>
          <div class="collection-actions">
            <el-button type="danger" size="small" @click="removeGuide(guide.id, $event)">
              取消收藏
            </el-button>
          </div>
        </div>
      </el-card>
      <div v-if="collectedGuides.length === 0" class="empty-state">
        <el-empty description="暂无收藏的攻略"></el-empty>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'UserCollection',
  setup() {
    const router = useRouter()
    const activeTab = ref('destinations')
    
    // 从API获取景点数据
    const destinations = ref([])
    const guides = ref([])
    const loading = ref(false)

    // 获取景点数据
    const fetchDestinations = async () => {
      try {
        const response = await axios.get('/api/destination/list/')
        let destData = response.data
        if (destData && destData.value && Array.isArray(destData.value)) {
          destData = destData.value
        }
        if (destData && destData.length > 0) {
          destinations.value = destData.map(item => ({
            destination_id: item.id,
            destination_name: item.name,
            city: item.city,
            region: item.region,
            category: item.category,
            rating: item.rating,
            description: item.description,
            price_level: item.price_level,
            tags: item.tags || []
          }))
        }
      } catch (error) {
        console.error('Error fetching destinations:', error)
      }
    }

    // 获取攻略数据
    const fetchGuides = async () => {
      try {
        const response = await axios.get('/api/destination/guides/')
        if (response.data && response.data.length > 0) {
          guides.value = response.data.map(item => ({
            id: item.id,
            title: item.title,
            category: item.category,
            author: item.author,
            date: item.date,
            views: item.views,
            likes: item.likes,
            summary: item.summary,
            tags: item.tags || []
          }))
        }
      } catch (error) {
        console.error('Error fetching guides:', error)
      }
    }

    // 组件挂载时获取数据
    onMounted(() => {
      loading.value = true
      Promise.all([fetchDestinations(), fetchGuides()]).finally(() => {
        loading.value = false
      })
    })

    // 从 localStorage 加载收藏的景点
    const collectedDestinationIds = computed(() => {
      return new Set(JSON.parse(localStorage.getItem('favorites') || '[]'))
    })

    // 从 localStorage 加载收藏的攻略
    const collectedGuideIds = computed(() => {
      return new Set(JSON.parse(localStorage.getItem('collectedGuides') || '[]'))
    })

    // 过滤收藏的景点
    const collectedDestinations = computed(() => {
      return destinations.value.filter(dest => collectedDestinationIds.value.has(dest.destination_id))
    })

    // 过滤收藏的攻略
    const collectedGuides = computed(() => {
      return guides.value.filter(guide => collectedGuideIds.value.has(guide.id))
    })

    // 获取价格等级文本
    const getPriceLevel = (level) => {
      const levelMap = {
        'low': '低',
        'medium': '中',
        'high': '高'
      }
      return levelMap[level] || '中'
    }

    // 获取攻略分类样式
    const getCategoryType = (category) => {
      const typeMap = {
        '出行准备': 'primary',
        '行程规划': 'success',
        '省钱攻略': 'warning',
        '注意事项': 'danger'
      }
      return typeMap[category] || 'info'
    }

    // 跳转到景点详情
    const goToDetail = (destinationId) => {
      router.push(`/destination/${destinationId}`)
    }

    // 取消收藏景点
    const removeDestination = (destinationId) => {
      const favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      const newFavorites = favorites.filter(id => id !== destinationId)
      localStorage.setItem('favorites', JSON.stringify(newFavorites))
      ElMessage.success('取消收藏成功')
    }

    // 跳转到旅游攻略页面
    const goToGuideDetail = (guideId) => {
      // 跳转到旅游攻略页面
      router.push('/guide')
    }

    // 取消收藏攻略
    const removeGuide = (guideId, event) => {
      // 阻止事件冒泡，避免触发卡片点击
      if (event) {
        event.stopPropagation()
      }
      const collectedGuides = JSON.parse(localStorage.getItem('collectedGuides') || '[]')
      const newCollectedGuides = collectedGuides.filter(id => id !== guideId)
      localStorage.setItem('collectedGuides', JSON.stringify(newCollectedGuides))
      ElMessage.success('取消收藏成功')
    }

    return {
      activeTab,
      collectedDestinations,
      collectedGuides,
      getPriceLevel,
      getCategoryType,
      goToDetail,
      goToGuideDetail,
      removeDestination,
      removeGuide,
      loading
    }
  }
}
</script>

<style scoped>
.collection-container {
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

.collection-tabs {
  margin-bottom: 30px;
}

.collection-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.collection-card {
  border-radius: 10px;
  transition: all 0.3s;
}

.collection-card:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.destination-info {
  padding: 15px;
}

.destination-name {
  font-size: 20px;
  color: #333;
  margin-bottom: 5px;
}

.destination-city {
  color: #666;
  margin-bottom: 10px;
}

.destination-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.destination-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #888;
}

.destination-tags {
  margin-bottom: 15px;
}

.guide-info {
  padding: 15px;
}

.guide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.guide-author {
  font-size: 14px;
  color: #888;
}

.guide-title {
  font-size: 18px;
  color: #333;
  margin-bottom: 10px;
}

.guide-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.guide-tags {
  margin-bottom: 15px;
}

.guide-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #888;
}

.collection-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
}
</style>