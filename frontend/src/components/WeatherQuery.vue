<template>
  <div class="weather-container">
    <div class="page-header">
      <h2>🌤️ 天气查询</h2>
      <p>查询目的地天气，合理安排行程</p>
    </div>

    <div class="search-section">
      <el-input
        v-model="searchCity"
        placeholder="输入城市名称查询天气"
        prefix-icon="Search"
        clearable
        @keyup.enter="searchWeather"
        style="max-width: 400px;"
      />
      <el-button type="primary" @click="searchWeather" style="margin-left: 10px;">查询</el-button>
    </div>

    <div class="hot-cities">
      <span class="label">热门城市：</span>
      <el-tag
        v-for="city in hotCities"
        :key="city"
        @click="quickSearch(city)"
        style="cursor: pointer; margin-right: 8px;"
      >
        {{ city }}
      </el-tag>
    </div>

    <div v-if="weatherData" class="weather-result">
      <el-card class="current-weather">
        <div class="weather-main">
          <div class="weather-icon">{{ getWeatherIcon(weatherData.weather) }}</div>
          <div class="weather-info">
            <h2>{{ weatherData.city }}</h2>
            <div class="temperature">{{ weatherData.temperature }}°C</div>
            <div class="weather-desc">{{ weatherData.weather }}</div>
          </div>
        </div>
        <div class="weather-details">
          <div class="detail-item">
            <span class="label">体感温度</span>
            <span class="value">{{ weatherData.feelsLike }}°C</span>
          </div>
          <div class="detail-item">
            <span class="label">湿度</span>
            <span class="value">{{ weatherData.humidity }}%</span>
          </div>
          <div class="detail-item">
            <span class="label">风速</span>
            <span class="value">{{ weatherData.windSpeed }} m/s</span>
          </div>
          <div class="detail-item">
            <span class="label">空气质量</span>
            <span class="value">{{ weatherData.aqi }}</span>
          </div>
        </div>
        <div class="travel-suggestion">
          <el-alert
            :title="weatherData.suggestion"
            type="info"
            :closable="false"
            show-icon
          />
        </div>
      </el-card>

      <div class="forecast-section">
        <h3>未来7天天气预报</h3>
        <div class="forecast-grid">
          <el-card v-for="day in forecast" :key="day.date" class="forecast-card" shadow="hover">
            <div class="forecast-date">{{ day.date }}</div>
            <div class="forecast-icon">{{ getWeatherIcon(day.weather) }}</div>
            <div class="forecast-temp">
              <span class="high">{{ day.high }}°</span>
              <span class="low">/ {{ day.low }}°</span>
            </div>
            <div class="forecast-weather">{{ day.weather }}</div>
          </el-card>
        </div>
      </div>

      <div class="travel-tips">
        <h3>旅游小贴士</h3>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="tip-card">
              <div class="tip-icon">👔</div>
              <h4>穿衣建议</h4>
              <p>{{ weatherData.clothingTip }}</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="tip-card">
              <div class="tip-icon">☂️</div>
              <h4>出行建议</h4>
              <p>{{ weatherData.travelTip }}</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="tip-card">
              <div class="tip-icon">🏃</div>
              <h4>运动建议</h4>
              <p>{{ weatherData.sportTip }}</p>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

    <div v-else class="empty-state">
      <el-empty description="请输入城市名称查询天气"></el-empty>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'WeatherQuery',
  setup() {
    const searchCity = ref('')
    const weatherData = ref(null)
    
    const hotCities = ['北京', '上海', '广州', '深圳', '成都', '杭州', '西安', '南京']

    const forecast = ref([
      { date: '今天', weather: '晴', high: 25, low: 15 },
      { date: '明天', weather: '多云', high: 24, low: 14 },
      { date: '后天', weather: '小雨', high: 22, low: 13 },
      { date: '第4天', weather: '晴', high: 26, low: 16 },
      { date: '第5天', weather: '晴', high: 27, low: 17 },
      { date: '第6天', weather: '多云', high: 25, low: 16 },
      { date: '第7天', weather: '晴', high: 26, low: 15 }
    ])

    const mockWeatherData = {
      '北京': {
        city: '北京',
        temperature: 22,
        feelsLike: 20,
        humidity: 45,
        windSpeed: 3.5,
        weather: '晴',
        aqi: '优',
        suggestion: '天气晴朗，适合户外活动和旅游出行',
        clothingTip: '建议穿着长袖衬衫、薄外套等春秋装',
        travelTip: '天气较好，适宜外出游玩，注意防晒',
        sportTip: '天气不错，适合进行户外运动'
      },
      '上海': {
        city: '上海',
        temperature: 24,
        feelsLike: 23,
        humidity: 65,
        windSpeed: 4.2,
        weather: '多云',
        aqi: '良',
        suggestion: '多云天气，温度适宜，适合出行',
        clothingTip: '建议穿着薄款外套或长袖T恤',
        travelTip: '天气舒适，可以安排户外活动',
        sportTip: '适合进行中等强度的户外运动'
      },
      '成都': {
        city: '成都',
        temperature: 20,
        feelsLike: 19,
        humidity: 70,
        windSpeed: 2.1,
        weather: '阴',
        aqi: '良',
        suggestion: '阴天，温度适中，适合室内外活动',
        clothingTip: '建议穿着长袖衣物，可备一件薄外套',
        travelTip: '天气阴沉，建议携带雨具以备不时之需',
        sportTip: '可以进行轻度户外运动'
      },
      '广州': {
        city: '广州',
        temperature: 28,
        feelsLike: 30,
        humidity: 75,
        windSpeed: 2.8,
        weather: '晴',
        aqi: '良',
        suggestion: '天气炎热，注意防暑降温',
        clothingTip: '建议穿着短袖、短裤等夏季服装',
        travelTip: '天气炎热，建议早晚出行，避开正午高温',
        sportTip: '建议选择室内运动或早晚户外运动'
      }
    }

    const searchWeather = () => {
      if (!searchCity.value) {
        ElMessage.warning('请输入城市名称')
        return
      }

      const city = searchCity.value.trim()
      
      if (mockWeatherData[city]) {
        weatherData.value = mockWeatherData[city]
        ElMessage.success(`已查询 ${city} 的天气`)
      } else {
        const randomWeather = {
          city: city,
          temperature: Math.floor(Math.random() * 15) + 15,
          feelsLike: Math.floor(Math.random() * 15) + 14,
          humidity: Math.floor(Math.random() * 30) + 50,
          windSpeed: (Math.random() * 5 + 1).toFixed(1),
          weather: ['晴', '多云', '阴', '小雨'][Math.floor(Math.random() * 4)],
          aqi: ['优', '良', '轻度污染'][Math.floor(Math.random() * 3)],
          suggestion: '天气一般，建议根据实际情况安排出行',
          clothingTip: '建议根据温度选择合适的衣物',
          travelTip: '出行前请关注天气变化',
          sportTip: '根据天气情况选择合适的运动方式'
        }
        weatherData.value = randomWeather
        ElMessage.success(`已查询 ${city} 的天气（模拟数据）`)
      }
    }

    const quickSearch = (city) => {
      searchCity.value = city
      searchWeather()
    }

    const getWeatherIcon = (weather) => {
      const iconMap = {
        '晴': '☀️',
        '多云': '⛅',
        '阴': '☁️',
        '小雨': '🌧️',
        '中雨': '🌧️',
        '大雨': '⛈️',
        '雪': '❄️'
      }
      return iconMap[weather] || '🌤️'
    }

    return {
      searchCity,
      weatherData,
      hotCities,
      forecast,
      searchWeather,
      quickSearch,
      getWeatherIcon
    }
  }
}
</script>

<style scoped>
.weather-container {
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

.hot-cities {
  text-align: center;
  margin-bottom: 30px;
}

.hot-cities .label {
  color: #888;
  margin-right: 10px;
}

.weather-result {
  max-width: 1000px;
  margin: 0 auto;
}

.current-weather {
  margin-bottom: 30px;
}

.weather-main {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 20px;
}

.weather-icon {
  font-size: 80px;
}

.weather-info h2 {
  font-size: 28px;
  margin-bottom: 10px;
}

.temperature {
  font-size: 48px;
  font-weight: bold;
  color: #409eff;
}

.weather-desc {
  font-size: 18px;
  color: #666;
  margin-top: 5px;
}

.weather-details {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 10px;
}

.detail-item {
  text-align: center;
}

.detail-item .label {
  display: block;
  color: #888;
  font-size: 14px;
  margin-bottom: 5px;
}

.detail-item .value {
  display: block;
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.travel-suggestion {
  margin-top: 20px;
}

.forecast-section {
  margin-bottom: 30px;
}

.forecast-section h3 {
  margin-bottom: 20px;
  color: #333;
}

.forecast-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 15px;
}

.forecast-card {
  text-align: center;
  padding: 15px 10px;
}

.forecast-date {
  font-size: 14px;
  color: #888;
  margin-bottom: 10px;
}

.forecast-icon {
  font-size: 36px;
  margin-bottom: 10px;
}

.forecast-temp {
  font-size: 16px;
  margin-bottom: 5px;
}

.forecast-temp .high {
  color: #f56c6c;
  font-weight: bold;
}

.forecast-temp .low {
  color: #909399;
}

.forecast-weather {
  font-size: 14px;
  color: #666;
}

.travel-tips h3 {
  margin-bottom: 20px;
  color: #333;
}

.tip-card {
  text-align: center;
  padding: 20px;
}

.tip-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.tip-card h4 {
  margin-bottom: 10px;
  color: #333;
}

.tip-card p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

.empty-state {
  text-align: center;
  padding: 50px;
}

@media (max-width: 768px) {
  .weather-details {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .forecast-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
