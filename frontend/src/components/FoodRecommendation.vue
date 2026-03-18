<template>
  <div class="food-container">
    <div class="page-header">
      <h2>🍜 当地美食推荐</h2>
      <p>探索目的地的特色美食，品尝地道风味</p>
    </div>

    <div class="filter-section">
      <el-select v-model="selectedCity" placeholder="选择城市" @change="filterFoods">
        <el-option label="全部" value=""></el-option>
        <el-option label="北京" value="北京"></el-option>
        <el-option label="上海" value="上海"></el-option>
        <el-option label="成都" value="成都"></el-option>
        <el-option label="广州" value="广州"></el-option>
        <el-option label="西安" value="西安"></el-option>
        <el-option label="杭州" value="杭州"></el-option>
      </el-select>

      <el-select v-model="selectedCategory" placeholder="美食类型" @change="filterFoods" style="margin-left: 15px;">
        <el-option label="全部" value=""></el-option>
        <el-option label="特色小吃" value="特色小吃"></el-option>
        <el-option label="地方菜系" value="地方菜系"></el-option>
        <el-option label="网红美食" value="网红美食"></el-option>
        <el-option label="传统老字号" value="传统老字号"></el-option>
      </el-select>
    </div>

    <div class="food-grid">
      <el-card v-for="food in filteredFoods" :key="food.id" class="food-card" shadow="hover">
        <div class="food-image">
          <img :src="food.image" :alt="food.name" @error="handleImageError">
          <div class="food-tag">{{ food.category }}</div>
        </div>
        <div class="food-info">
          <h3>{{ food.name }}</h3>
          <p class="food-desc">{{ food.description }}</p>
          <div class="food-meta">
            <span class="location">📍 {{ food.city }}</span>
            <span class="price">💰 {{ food.price }}</span>
          </div>
          <div class="food-rating">
            <el-rate v-model="food.rating" disabled show-score text-color="#ff9900" />
          </div>
          <div class="food-tags">
            <el-tag v-for="tag in food.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
          </div>
        </div>
      </el-card>
    </div>

    <div v-if="filteredFoods.length === 0" class="empty-state">
      <el-empty description="暂无符合条件的美食"></el-empty>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'FoodRecommendation',
  setup() {
    const selectedCity = ref('')
    const selectedCategory = ref('')

    const foods = ref([
      {
        id: 1,
        name: '北京烤鸭',
        city: '北京',
        category: '传统老字号',
        description: '色泽红艳，肉质细嫩，味道醇厚，肥而不腻，被誉为"天下美味"',
        price: '人均150-300元',
        rating: 4.8,
        tags: ['必吃榜', '百年老店', '国宴菜品'],
        image: 'https://images.unsplash.com/photo-1518492104633-130d0cc84637?w=400'
      },
      {
        id: 2,
        name: '成都火锅',
        city: '成都',
        category: '地方菜系',
        description: '麻辣鲜香，红油翻滚，是成都最具代表性的美食之一',
        price: '人均80-150元',
        rating: 4.9,
        tags: ['麻辣鲜香', '地道川味', '网红打卡'],
        image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400'
      },
      {
        id: 3,
        name: '广州早茶',
        city: '广州',
        category: '传统老字号',
        description: '虾饺、烧卖、肠粉、叉烧包，精致的粤式点心文化',
        price: '人均60-120元',
        rating: 4.7,
        tags: ['早茶文化', '精致点心', '粤菜经典'],
        image: 'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400'
      },
      {
        id: 4,
        name: '西安肉夹馍',
        city: '西安',
        category: '特色小吃',
        description: '外酥里嫩，肉香浓郁，被誉为"中式汉堡"',
        price: '人均15-30元',
        rating: 4.6,
        tags: ['街头小吃', '性价比高', '必吃美食'],
        image: 'https://images.unsplash.com/photo-1626700051615-7dab6ee1c6b5?w=400'
      },
      {
        id: 5,
        name: '杭州西湖醋鱼',
        city: '杭州',
        category: '地方菜系',
        description: '鱼肉鲜嫩，酸甜可口，是杭州的传统名菜',
        price: '人均100-200元',
        rating: 4.5,
        tags: ['杭帮菜', '西湖名菜', '清淡鲜美'],
        image: 'https://images.unsplash.com/photo-1534604973900-c43ab4c2e0ab?w=400'
      },
      {
        id: 6,
        name: '上海小笼包',
        city: '上海',
        category: '特色小吃',
        description: '皮薄馅大，汤汁鲜美，是上海的经典小吃',
        price: '人均30-60元',
        rating: 4.7,
        tags: ['南翔小笼', '百年老店', '汤汁鲜美'],
        image: 'https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=400'
      },
      {
        id: 7,
        name: '成都串串香',
        city: '成都',
        category: '网红美食',
        description: '串串种类丰富，蘸料香辣，是成都夜宵首选',
        price: '人均50-100元',
        rating: 4.8,
        tags: ['夜宵首选', '网红美食', '性价比高'],
        image: 'https://images.unsplash.com/photo-1555126634-323283e090fa?w=400'
      },
      {
        id: 8,
        name: '北京炸酱面',
        city: '北京',
        category: '特色小吃',
        description: '面条劲道，炸酱浓香，是老北京的传统面食',
        price: '人均20-40元',
        rating: 4.4,
        tags: ['老北京', '家常美食', '经济实惠'],
        image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400'
      }
    ])

    const filteredFoods = computed(() => {
      return foods.value.filter(food => {
        const cityMatch = !selectedCity.value || food.city === selectedCity.value
        const categoryMatch = !selectedCategory.value || food.category === selectedCategory.value
        return cityMatch && categoryMatch
      })
    })

    const filterFoods = () => {
      // 过滤逻辑已在computed中实现
    }

    const handleImageError = (e) => {
      e.target.src = 'https://via.placeholder.com/400x300?text=美食图片'
    }

    return {
      selectedCity,
      selectedCategory,
      foods,
      filteredFoods,
      filterFoods,
      handleImageError
    }
  }
}
</script>

<style scoped>
.food-container {
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

.food-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.food-card {
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s;
}

.food-card:hover {
  transform: translateY(-5px);
}

.food-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.food-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.food-tag {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  color: #409eff;
  font-weight: bold;
}

.food-info {
  padding: 15px;
}

.food-info h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #333;
}

.food-desc {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 10px;
}

.food-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: #888;
}

.food-rating {
  margin-bottom: 10px;
}

.food-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.empty-state {
  text-align: center;
  padding: 50px;
}
</style>
