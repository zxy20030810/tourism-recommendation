<template>
  <div class="destination-detail-container">
    <el-button type="primary" plain @click="goBack">返回推荐列表</el-button>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <!-- 骨架屏效果 -->
      <div class="skeleton-container">
        <div class="skeleton-header">
          <div class="skeleton-title"></div>
          <div class="skeleton-star"></div>
        </div>
        <div class="skeleton-image"></div>
        <div class="skeleton-info">
          <div class="skeleton-location"></div>
          <div class="skeleton-rating"></div>
          <div class="skeleton-tags"></div>
        </div>
        <div class="skeleton-section">
          <div class="skeleton-section-title"></div>
          <div class="skeleton-paragraph"></div>
          <div class="skeleton-paragraph"></div>
        </div>
        <div class="skeleton-section">
          <div class="skeleton-section-title"></div>
          <div class="skeleton-tags"></div>
        </div>
      </div>
    </div>
    
    <!-- 目的地详情 -->
    <div v-else-if="destination" class="destination-content">
      <div class="destination-header">
        <h1>{{ destination.name }}</h1>
        <div class="header-actions">
          <el-button 
            type="info" 
            @click="showShareDialog = true"
            icon="Share"
            size="large"
            plain
            class="share-button"
          >
            分享
          </el-button>
          <el-button 
            :type="isFavorite ? 'primary' : 'info'" 
            @click="toggleFavorite"
            :icon="isFavorite ? 'StarFilled' : 'Star'"
            circle
            size="large"
            class="favorite-button"
          ></el-button>
        </div>
      </div>
      
      <!-- 景点图片 -->
      <div class="destination-images">
        <div v-if="imageLoading" class="image-loading">
          <el-icon class="loading-icon"><Loading /></el-icon>
          <span>正在加载图片...</span>
        </div>
        <img 
          v-else
          :src="destinationImage" 
          :alt="destination.name"
          class="destination-image"
          @error="handleImageError"
        >
      </div>
      
      <div class="destination-info-header">
        <div class="destination-info">
          <div class="location-info">
            <el-icon><Location /></el-icon>
            <span>{{ destination.city }} · {{ destination.region }}</span>
          </div>
          <div class="rating-info">
            <el-rate v-model="destination.rating" disabled :max="5" :precision="1"></el-rate>
            <span>{{ destination.rating }} ({{ destination.review_count }} 条评论)</span>
          </div>
        </div>
        <div class="destination-meta">
          <el-tag size="medium">{{ destination.category }}</el-tag>
          <el-tag size="medium" type="info">{{ destination.price_level }}</el-tag>
        </div>
      </div>
      
      <div class="destination-description">
        <h2>目的地介绍</h2>
        <p>{{ destination.description }}</p>
      </div>
      
      <div class="destination-features">
        <h2>设施与服务</h2>
        <el-tag v-for="facility in destination.facilities" :key="facility" size="small" class="facility-tag">
          {{ facility }}
        </el-tag>
      </div>
      
      <div class="destination-tags">
        <h2>标签</h2>
        <el-tag v-for="tag in destination.tags" :key="tag" size="small" type="success" effect="plain">
          {{ tag }}
        </el-tag>
      </div>
      
      <div class="destination-season">
        <h2>最佳旅游季节</h2>
        <p>{{ destination.popular_season }}</p>
      </div>
    </div>
    
    <!-- 无数据状态 -->
    <div v-else class="empty-container">
      <el-icon class="empty-icon"><InfoFilled /></el-icon>
      <p>未找到目的地信息</p>
    </div>
    
    <!-- 分享对话框 -->
    <el-dialog
      v-model="showShareDialog"
      title="分享目的地"
      width="400px"
    >
      <div class="share-dialog-content">
        <div class="share-info">
          <h3>{{ destination.name }}</h3>
          <p>{{ destination.location }}</p>
        </div>
        <div class="share-platforms">
          <h4>分享到</h4>
          <div class="platform-buttons">
            <el-button 
              type="primary" 
              plain 
              @click="shareToWeChat"
              class="platform-button"
            >
              <el-icon><ChatDotRound /></el-icon>
              <span>微信</span>
            </el-button>
            <el-button 
              type="success" 
              plain 
              @click="shareToWeibo"
              class="platform-button"
            >
              <el-icon><Bell /></el-icon>
              <span>微博</span>
            </el-button>
            <el-button 
              type="warning" 
              plain 
              @click="copyLink"
              class="platform-button"
            >
              <el-icon><CopyDocument /></el-icon>
              <span>复制链接</span>
            </el-button>
          </div>
        </div>
        <div class="share-link">
          <el-input 
            v-model="shareLink" 
            readonly 
            placeholder="分享链接"
            class="link-input"
          >
            <template #append>
              <el-button @click="copyLink"><el-icon><CopyDocument /></el-icon></el-button>
            </template>
          </el-input>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { Loading, Location, InfoFilled, Picture, Star, StarFilled, Share, CopyDocument, ChatDotRound, Bell } from '@element-plus/icons-vue'

export default {
  name: 'DestinationDetail',
  props: {
    destinationId: {
      type: String,
      required: true
    }
  },
  components: {
    Loading,
    Location,
    InfoFilled,
    Picture,
    Star,
    StarFilled,
    Share,
    CopyDocument,
    ChatDotRound,
    Bell
  },
  data() {
    return {
      destination: null,
      loading: false,
      isFavorite: false,
      showShareDialog: false,
      shareLink: '',
      destinationImage: '',
      imageLoading: false
    }
  },
  mounted() {
    this.getDestinationDetail()
    this.checkFavoriteStatus()
  },
  methods: {
    async getDestinationDetail() {
      this.loading = true
      try {
        const response = await axios.get(`/destination/detail/${this.destinationId}/`)
        console.log('目的地详情:', response.data)
        this.destination = response.data
        // 获取图片
        this.loadDestinationImage()
      } catch (error) {
        this.$message.error('获取目的地详情失败')
        console.error('Error fetching destination detail:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadDestinationImage() {
      if (!this.destination) return
      
      this.imageLoading = true
      try {
        const response = await axios.get('/destination/images/', {
          params: { keyword: this.destination.name }
        })
        
        if (response.data.images && response.data.images.length > 0) {
          this.destinationImage = response.data.images[0].url
        } else {
          this.destinationImage = `https://source.unsplash.com/1200x600/?${encodeURIComponent(this.destination.name)},travel`
        }
      } catch (error) {
        console.error('获取图片失败:', error)
        this.destinationImage = `https://source.unsplash.com/1200x600/?${encodeURIComponent(this.destination.name)},travel`
      } finally {
        this.imageLoading = false
      }
    },
    
    goBack() {
      this.$router.back()
    },
    
    // 图片加载失败处理
    handleImageError(e) {
      e.target.src = 'https://source.unsplash.com/1200x600/?travel,landscape'
    },
    
    // 检查收藏状态
    checkFavoriteStatus() {
      const favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      this.isFavorite = favorites.includes(this.destinationId)
    },
    
    // 切换收藏状态
    toggleFavorite() {
      let favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      
      if (!this.isFavorite) {
        // 添加收藏
        favorites.push(this.destinationId)
        this.$message.success('收藏成功')
        this.isFavorite = true
      } else {
        // 取消收藏
        favorites = favorites.filter(id => id !== this.destinationId)
        this.$message.success('收藏取消成功')
        this.isFavorite = false
      }
      
      localStorage.setItem('favorites', JSON.stringify(favorites))
    },
    
    // 分享到微信
    shareToWeChat() {
      // 生成分享链接
      this.generateShareLink()
      this.$message.success('请使用微信扫描二维码分享')
      // 这里可以添加二维码生成逻辑
    },
    
    // 分享到微博
    shareToWeibo() {
      // 生成分享链接
      this.generateShareLink()
      // 构建微博分享URL
      const weiboUrl = `http://service.weibo.com/share/share.php?url=${encodeURIComponent(this.shareLink)}&title=${encodeURIComponent(this.destination.name + ' - ' + this.destination.location)}&pic=`
      window.open(weiboUrl, '_blank', 'width=600,height=400')
    },
    
    // 复制链接
    copyLink() {
      // 生成分享链接
      this.generateShareLink()
      // 复制到剪贴板
      navigator.clipboard.writeText(this.shareLink).then(() => {
        this.$message.success('链接已复制到剪贴板')
      }).catch(err => {
        this.$message.error('复制失败，请手动复制')
        console.error('复制失败:', err)
      })
    },
    
    // 生成分享链接
    generateShareLink() {
      // 构建完整的分享链接
      this.shareLink = window.location.origin + '/#/destination/' + this.destinationId
    }
  }
}
</script>

<style scoped>
.destination-detail-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading-container {
  padding: 20px;
}

.skeleton-container {
  max-width: 1200px;
  margin: 0 auto;
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.skeleton-title {
  width: 300px;
  height: 32px;
  background: #f2f2f2;
  border-radius: 4px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-star {
  width: 24px;
  height: 24px;
  background: #f2f2f2;
  border-radius: 50%;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-image {
  width: 100%;
  height: 400px;
  background: #f2f2f2;
  border-radius: 8px;
  margin-bottom: 30px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-info {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eaeaea;
}

.skeleton-location {
  width: 200px;
  height: 20px;
  background: #f2f2f2;
  border-radius: 4px;
  margin-bottom: 15px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-rating {
  width: 150px;
  height: 20px;
  background: #f2f2f2;
  border-radius: 4px;
  margin-bottom: 15px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-tags {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.skeleton-tags div {
  width: 80px;
  height: 24px;
  background: #f2f2f2;
  border-radius: 4px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-section {
  margin-bottom: 30px;
}

.skeleton-section-title {
  width: 150px;
  height: 24px;
  background: #f2f2f2;
  border-radius: 4px;
  margin-bottom: 15px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-paragraph {
  width: 100%;
  height: 16px;
  background: #f2f2f2;
  border-radius: 4px;
  margin-bottom: 10px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-paragraph:nth-child(2) {
  width: 80%;
}

.skeleton-paragraph:nth-child(3) {
  width: 60%;
}

@keyframes shimmer {
  0% {
    background: linear-gradient(to right, #f2f2f2 0%, #e6e6e6 20%, #f2f2f2 40%, #f2f2f2 100%);
    background-size: 1000px 100%;
  }
  100% {
    background: linear-gradient(to right, #f2f2f2 0%, #e6e6e6 20%, #f2f2f2 40%, #f2f2f2 100%);
    background-size: 1000px 100%;
    background-position: 1000px 0;
  }
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

.destination-content {
  margin-top: 20px;
}

.destination-content h1 {
  font-size: 32px;
  color: #333;
  margin: 0;
}

.favorite-button {
  margin-left: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
}

.share-button {
  margin-right: 15px;
}

/* 分享对话框样式 */
.share-dialog-content {
  padding: 20px 0;
}

.share-info {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eaeaea;
}

.share-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.share-info p {
  margin: 0;
  color: #666;
}

.share-platforms h4 {
  margin: 0 0 20px 0;
  color: #333;
}

.platform-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 30px;
}

.platform-button {
  flex: 1;
  min-width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.share-link {
  margin-top: 20px;
}

.link-input {
  margin-top: 10px;
}

.destination-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.destination-info-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eaeaea;
}

.destination-info {
  flex: 1;
}

.location-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  color: #666;
}

.location-info .el-icon {
  margin-right: 5px;
}

.rating-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.destination-meta {
  display: flex;
  gap: 10px;
}

.destination-description {
  margin-bottom: 30px;
}

.destination-description h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
}

.destination-description p {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
}

.destination-features,
.destination-tags,
.destination-season {
  margin-bottom: 30px;
}

.destination-features h2,
.destination-tags h2,
.destination-season h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
}

.facility-tag {
  margin-right: 10px;
  margin-bottom: 10px;
}

.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  flex-direction: column;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.destination-images {
  margin: 20px 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

.image-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #666;
}

.image-loading .loading-icon {
  font-size: 48px;
  margin-bottom: 10px;
  animation: rotate 1.5s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.destination-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.image-icon {
  font-size: 64px;
  color: #999;
  margin-bottom: 16px;
}

.image-placeholder span {
  font-size: 18px;
  color: #666;
}

.image-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
  border-radius: 4px;
}
</style>