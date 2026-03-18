<template>
  <div class="scenery-container">
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
import { ref, computed } from 'vue'

export default {
  name: 'SceneryIntroduction',
  setup() {
    const activeCategory = ref('')

    const sceneryList = ref([
      {
        id: 1,
        name: '张家界国家森林公园',
        location: '湖南省张家界市',
        category: '自然风光',
        description: '以峰称奇、以谷显幽、以林见秀，三千奇峰拔地而起，八百溪流蜿蜒纵横，被誉为"扩大的盆景，缩小的仙境"。',
        bestSeason: '春秋两季',
        duration: '2-3天',
        price: '225元/人',
        rating: 4.9,
        tags: ['世界遗产', '阿凡达取景地', '玻璃栈道'],
        image: 'https://images.unsplash.com/photo-1513415756790-2ac1db1297d0?w=600'
      },
      {
        id: 2,
        name: '故宫博物院',
        location: '北京市东城区',
        category: '历史古迹',
        description: '中国明清两代的皇家宫殿，世界上现存规模最大、保存最为完整的木质结构古建筑之一。',
        bestSeason: '四季皆宜',
        duration: '1天',
        price: '60元/人',
        rating: 4.8,
        tags: ['世界遗产', '必游景点', '文化瑰宝'],
        image: 'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600'
      },
      {
        id: 3,
        name: '西湖风景区',
        location: '浙江省杭州市',
        category: '自然风光',
        description: '以秀丽的湖光山色和众多的名胜古迹闻名中外，是中国著名的旅游胜地，被誉为"人间天堂"。',
        bestSeason: '春季赏花，秋季赏月',
        duration: '1-2天',
        price: '免费',
        rating: 4.7,
        tags: ['世界遗产', '免费景区', '浪漫之地'],
        image: 'https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=600'
      },
      {
        id: 4,
        name: '外滩',
        location: '上海市黄浦区',
        category: '现代都市',
        description: '上海的标志性景观，汇集了52幢风格迥异的古典复兴大楼，素有"万国建筑博览群"之称。',
        bestSeason: '四季皆宜',
        duration: '半天',
        price: '免费',
        rating: 4.6,
        tags: ['地标建筑', '夜景绝美', '免费景点'],
        image: 'https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=600'
      },
      {
        id: 5,
        name: '九寨沟',
        location: '四川省阿坝州',
        category: '自然风光',
        description: '以翠海、叠瀑、彩林、雪峰、藏情、蓝冰"六绝"著称，被誉为"童话世界"、"人间仙境"。',
        bestSeason: '秋季',
        duration: '2天',
        price: '169元/人',
        rating: 4.9,
        tags: ['世界遗产', '童话世界', '摄影天堂'],
        image: 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600'
      },
      {
        id: 6,
        name: '兵马俑',
        location: '陕西省西安市',
        category: '历史古迹',
        description: '秦始皇陵的陪葬坑，被誉为"世界第八大奇迹"，是中国古代辉煌文明的一张金字名片。',
        bestSeason: '四季皆宜',
        duration: '半天',
        price: '120元/人',
        rating: 4.8,
        tags: ['世界遗产', '历史奇迹', '必游景点'],
        image: 'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=600'
      },
      {
        id: 7,
        name: '丽江古城',
        location: '云南省丽江市',
        category: '民族风情',
        description: '中国保存最为完好的四大古城之一，体现了中国古代城市建设的成就，是中国民居中具有鲜明特色和风格的类型之一。',
        bestSeason: '四季皆宜',
        duration: '2-3天',
        price: '50元/人',
        rating: 4.5,
        tags: ['世界遗产', '古城韵味', '纳西文化'],
        image: 'https://images.unsplash.com/photo-1528164344705-47542687000d?w=600'
      },
      {
        id: 8,
        name: '黄山',
        location: '安徽省黄山市',
        category: '自然风光',
        description: '以奇松、怪石、云海、温泉、冬雪"五绝"著称于世，素有"天下第一奇山"之称。',
        bestSeason: '四季皆宜',
        duration: '2天',
        price: '190元/人',
        rating: 4.9,
        tags: ['世界遗产', '五岳归来', '云海奇观'],
        image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600'
      }
    ])

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
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
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
  height: 250px;
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
  padding: 20px;
  color: white;
}

.scenery-overlay h3 {
  font-size: 20px;
  margin-bottom: 5px;
}

.scenery-location {
  font-size: 14px;
  opacity: 0.9;
}

.scenery-content {
  padding: 20px;
}

.scenery-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.scenery-desc {
  color: #666;
  line-height: 1.8;
  margin-bottom: 15px;
  font-size: 14px;
}

.scenery-features {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.feature-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  font-size: 14px;
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
