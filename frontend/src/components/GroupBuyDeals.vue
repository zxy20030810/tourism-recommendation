<template>
  <div class="groupbuy-container">
    <div class="page-header">
      <h2>🎫 团购优惠</h2>
      <p>精选旅游团购，超值优惠等你来</p>
    </div>

    <div class="filter-section">
      <el-select v-model="selectedCity" placeholder="选择城市" @change="filterDeals">
        <el-option label="全部" value=""></el-option>
        <el-option label="北京" value="北京"></el-option>
        <el-option label="上海" value="上海"></el-option>
        <el-option label="成都" value="成都"></el-option>
        <el-option label="杭州" value="杭州"></el-option>
        <el-option label="西安" value="西安"></el-option>
      </el-select>

      <el-select v-model="selectedType" placeholder="优惠类型" @change="filterDeals" style="margin-left: 15px;">
        <el-option label="全部" value=""></el-option>
        <el-option label="景点门票" value="景点门票"></el-option>
        <el-option label="酒店住宿" value="酒店住宿"></el-option>
        <el-option label="美食套餐" value="美食套餐"></el-option>
        <el-option label="旅游线路" value="旅游线路"></el-option>
      </el-select>

      <el-select v-model="sortBy" placeholder="排序方式" @change="filterDeals" style="margin-left: 15px;">
        <el-option label="默认排序" value="default"></el-option>
        <el-option label="价格从低到高" value="price_asc"></el-option>
        <el-option label="折扣力度" value="discount"></el-option>
        <el-option label="销量最高" value="sales"></el-option>
      </el-select>
    </div>

    <div class="hot-deals">
      <h3>🔥 今日特惠</h3>
      <el-carousel :interval="5000" type="card" height="200px">
        <el-carousel-item v-for="deal in hotDeals" :key="deal.id">
          <div class="hot-deal-card" :style="{ backgroundImage: `url(${deal.image})` }">
            <div class="hot-deal-overlay">
              <h4>{{ deal.title }}</h4>
              <div class="hot-deal-price">
                <span class="current">¥{{ deal.price }}</span>
                <span class="original">¥{{ deal.originalPrice }}</span>
                <span class="discount">{{ deal.discount }}折</span>
              </div>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <div class="deals-grid">
      <el-card v-for="deal in filteredDeals" :key="deal.id" class="deal-card" shadow="hover">
        <div class="deal-image">
          <img :src="deal.image" :alt="deal.title" @error="handleImageError">
          <div class="deal-badge" v-if="deal.badge">{{ deal.badge }}</div>
          <div class="deal-discount">{{ deal.discount }}折</div>
        </div>
        <div class="deal-content">
          <h3 class="deal-title">{{ deal.title }}</h3>
          <p class="deal-desc">{{ deal.description }}</p>
          <div class="deal-meta">
            <span class="location">📍 {{ deal.city }}</span>
            <span class="sales">已售 {{ deal.sales }}+</span>
          </div>
          <div class="deal-tags">
            <el-tag v-for="tag in deal.tags" :key="tag" size="small" type="danger">{{ tag }}</el-tag>
          </div>
          <div class="deal-price">
            <div class="price-info">
              <span class="current-price">¥{{ deal.price }}</span>
              <span class="original-price">¥{{ deal.originalPrice }}</span>
            </div>
            <el-button type="primary" size="small" @click="buyDeal(deal)">立即购买</el-button>
          </div>
          <div class="deal-timer" v-if="deal.endTime">
            <span>距结束：</span>
            <el-countdown :value="deal.endTime" format="HH:mm:ss" />
          </div>
        </div>
      </el-card>
    </div>

    <div v-if="filteredDeals.length === 0" class="empty-state">
      <el-empty description="暂无符合条件的优惠"></el-empty>
    </div>

    <div class="platform-tips">
      <el-alert
        title="温馨提示"
        type="info"
        :closable="false"
      >
        <template #default>
          本页面展示的团购信息仅供参考，实际购买请前往美团、大众点评等平台。如需接入真实API，请联系平台申请开发者权限。
        </template>
      </el-alert>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'GroupBuyDeals',
  setup() {
    const selectedCity = ref('')
    const selectedType = ref('')
    const sortBy = ref('default')

    const hotDeals = ref([
      {
        id: 1,
        title: '故宫门票+讲解服务',
        price: 88,
        originalPrice: 120,
        discount: 7.3,
        image: 'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800'
      },
      {
        id: 2,
        title: '上海迪士尼双人套票',
        price: 799,
        originalPrice: 1198,
        discount: 6.7,
        image: 'https://images.unsplash.com/photo-1533282960533-51328aa49826?w=800'
      },
      {
        id: 3,
        title: '成都火锅双人套餐',
        price: 168,
        originalPrice: 288,
        discount: 5.8,
        image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800'
      }
    ])

    const deals = ref([
      {
        id: 1,
        title: '故宫博物院门票+电子讲解',
        description: '含故宫门票+电子讲解服务，免排队快速入园',
        city: '北京',
        type: '景点门票',
        price: 68,
        originalPrice: 85,
        discount: 8.0,
        sales: 12580,
        badge: '爆款',
        tags: ['免排队', '电子讲解', '随时退'],
        image: 'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=400',
        endTime: new Date(Date.now() + 24 * 60 * 60 * 1000)
      },
      {
        id: 2,
        title: '上海迪士尼乐园成人票',
        description: '上海迪士尼乐园单日门票，畅玩所有项目',
        city: '上海',
        type: '景点门票',
        price: 399,
        originalPrice: 475,
        discount: 8.4,
        sales: 8920,
        badge: '热门',
        tags: ['周末可用', '快速入园', '官方直营'],
        image: 'https://images.unsplash.com/photo-1533282960533-51328aa49826?w=400',
        endTime: new Date(Date.now() + 12 * 60 * 60 * 1000)
      },
      {
        id: 3,
        title: '成都五星级酒店1晚',
        description: '豪华大床房含双早，免费停车+健身房',
        city: '成都',
        type: '酒店住宿',
        price: 388,
        originalPrice: 688,
        discount: 5.6,
        sales: 3250,
        badge: '超值',
        tags: ['含早餐', '免费停车', '延迟退房'],
        image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',
        endTime: null
      },
      {
        id: 4,
        title: '成都火锅双人套餐',
        description: '正宗成都火锅，含锅底+荤素菜品+饮品',
        city: '成都',
        type: '美食套餐',
        price: 158,
        originalPrice: 268,
        discount: 5.9,
        sales: 5680,
        badge: '必吃',
        tags: ['正宗川味', '双人套餐', '周末通用'],
        image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400',
        endTime: new Date(Date.now() + 6 * 60 * 60 * 1000)
      },
      {
        id: 5,
        title: '西湖游船+雷峰塔联票',
        description: '西湖游船往返票+雷峰塔门票，赏西湖美景',
        city: '杭州',
        type: '景点门票',
        price: 88,
        originalPrice: 120,
        discount: 7.3,
        sales: 6890,
        badge: '经典',
        tags: ['联票优惠', '随时退', '风景绝美'],
        image: 'https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=400',
        endTime: null
      },
      {
        id: 6,
        title: '西安兵马俑+华清宫一日游',
        description: '含往返交通+门票+导游讲解，品质纯玩',
        city: '西安',
        type: '旅游线路',
        price: 298,
        originalPrice: 398,
        discount: 7.5,
        sales: 4120,
        badge: '精选',
        tags: ['纯玩无购物', '含午餐', '专业导游'],
        image: 'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=400',
        endTime: new Date(Date.now() + 48 * 60 * 60 * 1000)
      },
      {
        id: 7,
        title: '北京环球影城双人票',
        description: '北京环球影城双人门票，畅玩哈利波特等主题区',
        city: '北京',
        type: '景点门票',
        price: 798,
        originalPrice: 956,
        discount: 8.3,
        sales: 7890,
        badge: '热门',
        tags: ['双人优惠', '快速通行', '热门项目'],
        image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400',
        endTime: new Date(Date.now() + 36 * 60 * 60 * 1000)
      },
      {
        id: 8,
        title: '杭州特色民宿2晚',
        description: '西湖边特色民宿，含早餐+下午茶',
        city: '杭州',
        type: '酒店住宿',
        price: 568,
        originalPrice: 898,
        discount: 6.3,
        sales: 1890,
        badge: '文艺',
        tags: ['西湖边', '含下午茶', '文艺清新'],
        image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400',
        endTime: null
      }
    ])

    const filteredDeals = computed(() => {
      let result = deals.value

      if (selectedCity.value) {
        result = result.filter(d => d.city === selectedCity.value)
      }

      if (selectedType.value) {
        result = result.filter(d => d.type === selectedType.value)
      }

      if (sortBy.value === 'price_asc') {
        result = [...result].sort((a, b) => a.price - b.price)
      } else if (sortBy.value === 'discount') {
        result = [...result].sort((a, b) => a.discount - b.discount)
      } else if (sortBy.value === 'sales') {
        result = [...result].sort((a, b) => b.sales - a.sales)
      }

      return result
    })

    const filterDeals = () => {
      // 过滤逻辑已在computed中实现
    }

    const handleImageError = (e) => {
      e.target.src = 'https://via.placeholder.com/400x300?text=团购图片'
    }

    const buyDeal = (deal) => {
      ElMessage.success(`已加入购物车：${deal.title}`)
    }

    return {
      selectedCity,
      selectedType,
      sortBy,
      hotDeals,
      deals,
      filteredDeals,
      filterDeals,
      handleImageError,
      buyDeal
    }
  }
}
</script>

<style scoped>
.groupbuy-container {
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

.filter-section {
  margin-bottom: 30px;
  text-align: center;
}

.hot-deals {
  margin-bottom: 40px;
}

.hot-deals h3 {
  margin-bottom: 20px;
  color: #333;
}

.hot-deal-card {
  height: 200px;
  background-size: cover;
  background-position: center;
  border-radius: 10px;
  position: relative;
}

.hot-deal-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  padding: 20px;
  color: white;
  border-radius: 0 0 10px 10px;
}

.hot-deal-overlay h4 {
  font-size: 18px;
  margin-bottom: 10px;
}

.hot-deal-price {
  display: flex;
  align-items: center;
  gap: 10px;
}

.hot-deal-price .current {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}

.hot-deal-price .original {
  font-size: 14px;
  text-decoration: line-through;
  opacity: 0.7;
}

.hot-deal-price .discount {
  background: #f56c6c;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.deals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.deal-card {
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s;
}

.deal-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.deal-image {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.deal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.deal-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #f56c6c;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
}

.deal-discount {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 87, 51, 0.9);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: bold;
}

.deal-content {
  padding: 15px;
}

.deal-title {
  font-size: 16px;
  margin-bottom: 8px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.deal-desc {
  font-size: 13px;
  color: #888;
  margin-bottom: 10px;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.deal-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-bottom: 10px;
}

.deal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
}

.deal-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.current-price {
  font-size: 22px;
  font-weight: bold;
  color: #f56c6c;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
  margin-left: 8px;
}

.deal-timer {
  margin-top: 10px;
  padding: 8px;
  background: #fff5f5;
  border-radius: 5px;
  font-size: 13px;
  color: #f56c6c;
  display: flex;
  align-items: center;
  gap: 5px;
}

.platform-tips {
  margin-top: 30px;
}

.empty-state {
  text-align: center;
  padding: 50px;
}
</style>
