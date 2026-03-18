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

    <div class="guide-list">
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
            <el-button size="small" @click="collectGuide(guide)">
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
import { ref, computed } from 'vue'
import { Star, CollectionTag } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'TravelGuide',
  components: {
    Star,
    CollectionTag
  },
  setup() {
    const searchKeyword = ref('')
    const activeTab = ref('')

    const guides = ref([
      {
        id: 1,
        title: '第一次去北京必看！故宫游览全攻略',
        category: '行程规划',
        author: '旅游达人小王',
        date: '2026-03-15',
        views: 12580,
        likes: 892,
        summary: '详细介绍故宫游览路线、门票预约、最佳游览时间等信息，让你轻松玩转故宫！',
        content: `<h4>🎫 门票预约</h4>
          <p>故宫实行实名制预约购票，建议提前10天在官网预约。旺季门票60元，淡季40元。</p>
          <h4>⏰ 开放时间</h4>
          <p>旺季（4月1日-10月31日）8:30-17:00</p>
          <p>淡季（11月1日-3月31日）8:30-16:30</p>
          <h4>🚶 推荐路线</h4>
          <p>午门→太和殿→中和殿→保和殿→乾清宫→交泰殿→坤宁宫→御花园→神武门</p>`,
        tags: ['北京', '故宫', '必看攻略']
      },
      {
        id: 2,
        title: '旅行必备物品清单，再也不怕忘带东西',
        category: '出行准备',
        author: '背包客小李',
        date: '2026-03-10',
        views: 8920,
        likes: 654,
        summary: '超详细的旅行物品清单，涵盖证件、衣物、电子设备、药品等各个方面，打印出来对照打包！',
        content: `<h4>📋 证件类</h4>
          <p>身份证、护照、驾照、学生证、银行卡、现金</p>
          <h4>👕 衣物类</h4>
          <p>根据目的地天气准备，建议带一件外套、舒适的运动鞋</p>
          <h4>📱 电子设备</h4>
          <p>手机、充电宝、充电器、相机、转换插头</p>`,
        tags: ['出行准备', '必备清单', '实用攻略']
      },
      {
        id: 3,
        title: '学生党穷游攻略：如何用最少的钱玩最多的地方',
        category: '省钱攻略',
        author: '省钱小能手',
        date: '2026-03-08',
        views: 15680,
        likes: 1234,
        summary: '分享学生党穷游经验，包括交通、住宿、门票等方面的省钱技巧，让你的旅行预算减半！',
        content: `<h4>🚄 交通省钱</h4>
          <p>学生证购买火车票可享优惠，提前购票更便宜</p>
          <h4>🏨 住宿省钱</h4>
          <p>选择青旅或民宿，多人分摊更划算</p>
          <h4>🎫 门票省钱</h4>
          <p>学生证半价，关注景区优惠活动</p>`,
        tags: ['省钱攻略', '学生党', '穷游']
      },
      {
        id: 4,
        title: '高原旅行注意事项，预防高反必看',
        category: '注意事项',
        author: '户外达人老张',
        date: '2026-03-05',
        views: 9870,
        likes: 756,
        summary: '前往西藏、青海等高原地区旅行，需要注意哪些事项？如何预防和应对高原反应？',
        content: `<h4>⚠️ 高原反应预防</h4>
          <p>提前一周服用红景天，到达后不要剧烈运动</p>
          <h4>🧳 必备物品</h4>
          <p>防晒霜、墨镜、帽子、保温杯、氧气瓶</p>
          <h4>🚫 禁忌事项</h4>
          <p>不要饮酒、不要暴饮暴食、不要剧烈运动</p>`,
        tags: ['高原旅行', '注意事项', '安全攻略']
      },
      {
        id: 5,
        title: '成都3天2夜完美行程规划',
        category: '行程规划',
        author: '成都本地人',
        date: '2026-03-01',
        views: 11230,
        likes: 876,
        summary: '本地人推荐的成都经典路线，涵盖大熊猫基地、宽窄巷子、锦里、春熙路等热门景点！',
        content: `<h4>Day 1</h4>
          <p>上午：大熊猫基地 → 下午：宽窄巷子 → 晚上：锦里古街</p>
          <h4>Day 2</h4>
          <p>上午：杜甫草堂 → 下午：武侯祠 → 晚上：春熙路</p>
          <h4>Day 3</h4>
          <p>上午：人民公园喝茶 → 下午：太古里 → 晚上：火锅</p>`,
        tags: ['成都', '行程规划', '3天2夜']
      },
      {
        id: 6,
        title: '自驾游必备：车辆检查与安全驾驶指南',
        category: '出行准备',
        author: '老司机阿强',
        date: '2026-02-28',
        views: 7650,
        likes: 543,
        summary: '自驾游出发前，这些车辆检查项目一定要做！还有安全驾驶技巧分享。',
        content: `<h4>🔧 车辆检查项目</h4>
          <p>轮胎、刹车、机油、防冻液、电瓶、灯光</p>
          <h4>🚗 随车工具</h4>
          <p>备胎、千斤顶、三角警示牌、灭火器、急救包</p>
          <h4>⚠️ 安全驾驶</h4>
          <p>遵守交规、不疲劳驾驶、保持车距</p>`,
        tags: ['自驾游', '安全驾驶', '出行准备']
      }
    ])

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
      // 过滤逻辑已在computed中实现
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

    const likeGuide = (guide) => {
      guide.likes++
      ElMessage.success('点赞成功！')
    }

    const collectGuide = () => {
      ElMessage.success('收藏成功！')
    }

    return {
      searchKeyword,
      activeTab,
      guides,
      filteredGuides,
      filterGuides,
      getCategoryType,
      likeGuide,
      collectGuide
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
