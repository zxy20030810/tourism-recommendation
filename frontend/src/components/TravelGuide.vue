<template>
  <div class="guide-container">
    <div class="page-header">
      <h2>📖 旅游攻略</h2>
      <p>精选旅游攻略，助你轻松出行</p>
    </div>

    <div class="search-section">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索攻略..."
        prefix-icon="Search"
        clearable
        @input="filterGuides"
        style="max-width: 500px;"
      />
    </div>

    <div class="guide-tabs">
      <el-tabs v-model="activeTab" @tab-change="filterGuides">
        <el-tab-pane label="全部攻略" name=""></el-tab-pane>
        <el-tab-pane label="出行准备" name="出行准备"></el-tab-pane>
        <el-tab-pane label="行程规划" name="行程规划"></el-tab-pane>
        <el-tab-pane label="省钱攻略" name="省钱攻略"></el-tab-pane>
        <el-tab-pane label="注意事项" name="注意事项"></el-tab-pane>
      </el-tabs>
    </div>

    <div class="guide-list" v-loading="loading">
      <el-card v-for="guide in filteredGuides" :key="guide.id" class="guide-card" shadow="hover">
        <div class="guide-header">
          <div class="guide-category">
            <el-tag :type="getCategoryType(guide.category)">{{ guide.category }}</el-tag>
          </div>
          <div class="guide-meta">
            <span class="author">👤 {{ guide.author }}</span>
            <span class="date">📅 {{ guide.date }}</span>
            <span class="views">👁 {{ guide.views }}</span>
          </div>
        </div>
        <h3 class="guide-title">{{ guide.title }}</h3>
        <p class="guide-summary">{{ guide.summary }}</p>
        <div class="guide-content" v-html="guide.content"></div>
        <div class="guide-footer">
          <div class="guide-tags">
            <el-tag v-for="tag in guide.tags" :key="tag" size="small" effect="plain">{{ tag }}</el-tag>
          </div>
          <div class="guide-actions">
            <el-button type="primary" size="small" @click="likeGuide(guide)">
              <el-icon><Star /></el-icon>
              {{ guide.likes }}
            </el-button>
            <el-button :type="collectedGuides.has(guide.id) ? 'primary' : 'info'" size="small" @click="collectGuide(guide)">
              <el-icon><CollectionTag /></el-icon>
              收藏
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <div v-if="filteredGuides.length === 0" class="empty-state">
      <el-empty description="暂无符合条件的攻略"></el-empty>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { Star, CollectionTag } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'TravelGuide',
  components: {
    Star,
    CollectionTag
  },
  setup() {
    const searchKeyword = ref('')
    const activeTab = ref('')
    
    const guides = ref([])
    const loading = ref(false)

    // 从API获取攻略数据
    const fetchGuides = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/destination/guides/', {
          params: {
            category: activeTab.value,
            keyword: searchKeyword.value
          }
        })
        if (response.data && response.data.length > 0) {
          guides.value = response.data
        }
      } catch (error) {
        console.error('Error fetching guides:', error)
        ElMessage.error('获取攻略数据失败')
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchGuides()
    })

    const filteredGuides = computed(() => {
      let result = guides.value
      
      if (activeTab.value) {
        result = result.filter(g => g.category === activeTab.value)
      }
      
      if (searchKeyword.value) {
        const keyword = searchKeyword.value.toLowerCase()
        result = result.filter(g => 
          g.title.toLowerCase().includes(keyword) ||
          g.summary.toLowerCase().includes(keyword) ||
          g.tags.some(tag => tag.toLowerCase().includes(keyword))
        )
      }
      
      return result
    })

    const filterGuides = () => {
      // 重新从API获取数据
      fetchGuides()
    }

    const getCategoryType = (category) => {
      const typeMap = {
        '出行准备': 'primary',
        '行程规划': 'success',
        '省钱攻略': 'warning',
        '注意事项': 'danger'
      }
      return typeMap[category] || 'info'
    }

    // 从 localStorage 加载收藏的攻略
    const collectedGuides = ref(new Set(JSON.parse(localStorage.getItem('collectedGuides') || '[]')))

    const likeGuide = async (guide) => {
      try {
        await axios.post(`/api/destination/guides/${guide.id}/like/`)
        guide.likes++
        ElMessage.success('点赞成功！')
      } catch (error) {
        console.error('Error liking guide:', error)
        ElMessage.error('点赞失败，请稍后重试')
      }
    }

    const collectGuide = (guide) => {
      if (!collectedGuides.value.has(guide.id)) {
        // 创建新的 Set 以触发响应式更新
        collectedGuides.value = new Set([...collectedGuides.value, guide.id])
        // 保存到 localStorage
        localStorage.setItem('collectedGuides', JSON.stringify([...collectedGuides.value]))
        ElMessage.success('收藏成功！')
      } else {
        // 创建新的 Set 以触发响应式更新
        const newSet = new Set(collectedGuides.value)
        newSet.delete(guide.id)
        collectedGuides.value = newSet
        // 保存到 localStorage
        localStorage.setItem('collectedGuides', JSON.stringify([...collectedGuides.value]))
        ElMessage.success('收藏取消成功')
      }
    }

    return {
      searchKeyword,
      activeTab,
      guides,
      filteredGuides,
      filterGuides,
      getCategoryType,
      likeGuide,
      collectGuide,
      collectedGuides,
      loading
    }
  }
}
</script>

<style scoped>
.guide-container {
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

.search-section {
  text-align: center;
  margin-bottom: 20px;
}

.guide-tabs {
  margin-bottom: 30px;
}

.guide-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.guide-card {
  border-radius: 10px;
  transition: all 0.3s;
}

.guide-card:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.guide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.guide-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #888;
}

.guide-title {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
}

.guide-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.guide-content {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  line-height: 1.8;
}

.guide-content h4 {
  color: #409eff;
  margin-bottom: 8px;
  margin-top: 10px;
}

.guide-content h4:first-child {
  margin-top: 0;
}

.guide-content p {
  color: #666;
  margin-bottom: 5px;
}

.guide-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.guide-tags {
  display: flex;
  gap: 8px;
}

.guide-actions {
  display: flex;
  gap: 10px;
}

.empty-state {
  text-align: center;
  padding: 50px;
}
</style>
