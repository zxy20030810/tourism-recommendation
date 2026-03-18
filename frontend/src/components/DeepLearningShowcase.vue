<template>
  <div class="deep-learning-container">
    <div class="page-header">
      <h1>深度学习推荐模型</h1>
      <p>基于Wide&Deep和DeepFM的智能旅游推荐系统</p>
    </div>

    <el-tabs v-model="activeTab" class="model-tabs">
      <el-tab-pane label="模型架构" name="architecture">
        <div class="architecture-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card class="model-card">
                <template #header>
                  <div class="card-header">
                    <span class="model-title">Wide&Deep 模型</span>
                    <el-tag type="success">推荐使用</el-tag>
                  </div>
                </template>
                <div class="architecture-diagram">
                  <div class="diagram-container wide-deep">
                    <div class="input-layer">
                      <div class="layer-title">输入层</div>
                      <div class="features">
                        <div class="feature">用户ID</div>
                        <div class="feature">目的地ID</div>
                        <div class="feature">用户特征</div>
                        <div class="feature">目的地特征</div>
                      </div>
                    </div>
                    <div class="arrow">↓</div>
                    <div class="split-layer">
                      <div class="wide-part">
                        <div class="layer-title">Wide部分</div>
                        <div class="layer-desc">记忆能力<br/>线性模型<br/>特征交叉</div>
                      </div>
                      <div class="deep-part">
                        <div class="layer-title">Deep部分</div>
                        <div class="layer-desc">泛化能力<br/>Embedding<br/>DNN网络</div>
                      </div>
                    </div>
                    <div class="arrow">↓</div>
                    <div class="hidden-layer">
                      <div class="layer-title">隐藏层</div>
                      <div class="neurons">
                        <div class="neuron">256</div>
                        <div class="neuron">128</div>
                        <div class="neuron">64</div>
                      </div>
                    </div>
                    <div class="arrow">↓</div>
                    <div class="output-layer">
                      <div class="layer-title">输出层</div>
                      <div class="output">推荐分数 (0-1)</div>
                    </div>
                  </div>
                </div>
                <div class="model-info">
                  <el-descriptions :column="2" border size="small">
                    <el-descriptions-item label="优化器">Adam</el-descriptions-item>
                    <el-descriptions-item label="损失函数">Binary CrossEntropy</el-descriptions-item>
                    <el-descriptions-item label="Embedding维度">32</el-descriptions-item>
                    <el-descriptions-item label="隐藏层">256→128→64</el-descriptions-item>
                  </el-descriptions>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="model-card">
                <template #header>
                  <div class="card-header">
                    <span class="model-title">DeepFM 模型</span>
                    <el-tag type="warning">高阶交互</el-tag>
                  </div>
                </template>
                <div class="architecture-diagram">
                  <div class="diagram-container deepfm">
                    <div class="input-layer">
                      <div class="layer-title">输入层</div>
                      <div class="features">
                        <div class="feature">用户ID</div>
                        <div class="feature">目的地ID</div>
                        <div class="feature">用户特征</div>
                        <div class="feature">目的地特征</div>
                      </div>
                    </div>
                    <div class="arrow">↓</div>
                    <div class="split-layer three-part">
                      <div class="fm-linear">
                        <div class="layer-title">FM线性</div>
                        <div class="layer-desc">一阶特征<br/>权重学习</div>
                      </div>
                      <div class="fm-interaction">
                        <div class="layer-title">FM交互</div>
                        <div class="layer-desc">二阶交叉<br/>特征组合</div>
                      </div>
                      <div class="deep-part">
                        <div class="layer-title">Deep</div>
                        <div class="layer-desc">高阶特征<br/>DNN网络</div>
                      </div>
                    </div>
                    <div class="arrow">↓</div>
                    <div class="combine-layer">
                      <div class="layer-title">组合层</div>
                      <div class="combine">Add + Sigmoid</div>
                    </div>
                    <div class="arrow">↓</div>
                    <div class="output-layer">
                      <div class="layer-title">输出层</div>
                      <div class="output">推荐分数 (0-1)</div>
                    </div>
                  </div>
                </div>
                <div class="model-info">
                  <el-descriptions :column="2" border size="small">
                    <el-descriptions-item label="优化器">Adam</el-descriptions-item>
                    <el-descriptions-item label="损失函数">Binary CrossEntropy</el-descriptions-item>
                    <el-descriptions-item label="Embedding维度">32</el-descriptions-item>
                    <el-descriptions-item label="特征交叉">自动学习</el-descriptions-item>
                  </el-descriptions>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>

      <el-tab-pane label="训练过程" name="training">
        <div class="training-section">
          <el-card class="training-card">
            <template #header>
              <div class="card-header">
                <span>模型训练过程</span>
                <el-button type="primary" size="small" @click="startTraining" :loading="training">
                  {{ training ? '训练中...' : '开始训练' }}
                </el-button>
              </div>
            </template>
            <div class="training-content">
              <el-row :gutter="20">
                <el-col :span="12">
                  <div class="chart-container">
                    <div class="chart" ref="lossChart"></div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="chart-container">
                    <div class="chart" ref="accuracyChart"></div>
                  </div>
                </el-col>
              </el-row>
              <div class="training-params">
                <h4>训练参数</h4>
                <el-form :model="trainingParams" label-width="120px">
                  <el-row :gutter="20">
                    <el-col :span="8">
                      <el-form-item label="学习率">
                        <el-input-number v-model="trainingParams.learning_rate" :min="0.0001" :max="0.1" :step="0.001" :precision="4"></el-input-number>
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="批次大小">
                        <el-select v-model="trainingParams.batch_size">
                          <el-option :value="32" label="32"></el-option>
                          <el-option :value="64" label="64"></el-option>
                          <el-option :value="128" label="128"></el-option>
                          <el-option :value="256" label="256"></el-option>
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="训练轮数">
                        <el-input-number v-model="trainingParams.epochs" :min="10" :max="200"></el-input-number>
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-form>
              </div>
              <div class="training-log" v-if="trainingLogs.length > 0">
                <h4>训练日志</h4>
                <div class="log-container">
                  <div v-for="(log, index) in trainingLogs" :key="index" class="log-item">
                    {{ log }}
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="特征工程" name="features">
        <div class="features-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card class="feature-card">
                <template #header>
                  <span>用户特征</span>
                </template>
                <el-table :data="userFeatures" style="width: 100%">
                  <el-table-column prop="name" label="特征名称" width="150"></el-table-column>
                  <el-table-column prop="type" label="类型" width="100"></el-table-column>
                  <el-table-column prop="process" label="处理方式"></el-table-column>
                  <el-table-column prop="importance" label="重要性">
                    <template #default="scope">
                      <el-progress :percentage="scope.row.importance" :color="getProgressColor(scope.row.importance)"></el-progress>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="feature-card">
                <template #header>
                  <span>目的地特征</span>
                </template>
                <el-table :data="destinationFeatures" style="width: 100%">
                  <el-table-column prop="name" label="特征名称" width="150"></el-table-column>
                  <el-table-column prop="type" label="类型" width="100"></el-table-column>
                  <el-table-column prop="process" label="处理方式"></el-table-column>
                  <el-table-column prop="importance" label="重要性">
                    <template #default="scope">
                      <el-progress :percentage="scope.row.importance" :color="getProgressColor(scope.row.importance)"></el-progress>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-col>
          </el-row>
          <el-card class="interaction-card" style="margin-top: 20px;">
            <template #header>
              <span>交互特征（特征工程）</span>
            </template>
            <el-row :gutter="20">
              <el-col :span="8" v-for="feature in interactionFeatures" :key="feature.name">
                <div class="interaction-feature">
                  <div class="feature-icon">
                    <el-icon><Connection /></el-icon>
                  </div>
                  <div class="feature-content">
                    <h5>{{ feature.name }}</h5>
                    <p>{{ feature.desc }}</p>
                  </div>
                </div>
              </el-col>
            </el-row>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="模型对比" name="comparison">
        <div class="comparison-section">
          <el-card class="comparison-card">
            <template #header>
              <span>模型性能对比</span>
            </template>
            <el-row :gutter="20">
              <el-col :span="16">
                <div class="comparison-chart" ref="comparisonChart"></div>
              </el-col>
              <el-col :span="8">
                <div class="comparison-metrics">
                  <div class="metric-item" v-for="metric in comparisonMetrics" :key="metric.name">
                    <div class="metric-name">{{ metric.name }}</div>
                    <div class="metric-values">
                      <div class="metric-value wide-deep">
                        <span class="label">Wide&Deep</span>
                        <span class="value">{{ metric.wideDeep }}</span>
                      </div>
                      <div class="metric-value deepfm">
                        <span class="label">DeepFM</span>
                        <span class="value">{{ metric.deepfm }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </el-col>
            </el-row>
          </el-card>
          <el-card class="advantage-card" style="margin-top: 20px;">
            <template #header>
              <span>模型优势分析</span>
            </template>
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="advantage-item">
                  <h4><el-icon><Check /></el-icon> Wide&Deep 优势</h4>
                  <ul>
                    <li>结合记忆与泛化能力</li>
                    <li>适合稀疏特征场景</li>
                    <li>训练稳定，收敛快</li>
                    <li>可解释性较好</li>
                  </ul>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="advantage-item">
                  <h4><el-icon><Check /></el-icon> DeepFM 优势</h4>
                  <ul>
                    <li>自动学习特征交叉</li>
                    <li>无需人工特征工程</li>
                    <li>捕捉高阶特征组合</li>
                    <li>端到端训练</li>
                  </ul>
                </div>
              </el-col>
            </el-row>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="推荐演示" name="demo">
        <div class="demo-section">
          <el-card class="demo-card">
            <template #header>
              <div class="card-header">
                <span>智能推荐演示</span>
                <el-select v-model="selectedModel" placeholder="选择模型" style="width: 150px;">
                  <el-option label="Wide&Deep" value="wide_deep"></el-option>
                  <el-option label="DeepFM" value="deepfm"></el-option>
                </el-select>
              </div>
            </template>
            <div class="demo-content">
              <el-row :gutter="20">
                <el-col :span="8">
                  <div class="user-input-section">
                    <h4>用户偏好设置</h4>
                    <el-form :model="userPreference" label-width="100px">
                      <el-form-item label="旅行类型">
                        <el-select v-model="userPreference.travel_type">
                          <el-option label="休闲度假" value="leisure"></el-option>
                          <el-option label="文化探索" value="culture"></el-option>
                          <el-option label="自然风光" value="nature"></el-option>
                          <el-option label="美食之旅" value="food"></el-option>
                          <el-option label="冒险探险" value="adventure"></el-option>
                        </el-select>
                      </el-form-item>
                      <el-form-item label="预算级别">
                        <el-select v-model="userPreference.budget">
                          <el-option label="经济" value="low"></el-option>
                          <el-option label="中等" value="medium"></el-option>
                          <el-option label="高端" value="high"></el-option>
                          <el-option label="奢华" value="luxury"></el-option>
                        </el-select>
                      </el-form-item>
                      <el-form-item label="年龄">
                        <el-slider v-model="userPreference.age" :min="10" :max="80" show-input></el-slider>
                      </el-form-item>
                      <el-form-item>
                        <el-button type="primary" @click="getRecommendation" :loading="recommending">
                          生成推荐
                        </el-button>
                      </el-form-item>
                    </el-form>
                  </div>
                </el-col>
                <el-col :span="16">
                  <div class="recommendation-result">
                    <h4>推荐结果</h4>
                    <div class="result-list" v-if="recommendations.length > 0">
                      <div class="result-item" v-for="(item, index) in recommendations" :key="item.id">
                        <div class="rank">{{ index + 1 }}</div>
                        <div class="item-info">
                          <div class="item-name">{{ item.name }}</div>
                          <div class="item-meta">
                            <span>{{ item.city }}</span>
                            <el-rate v-model="item.rating" disabled size="small"></el-rate>
                          </div>
                        </div>
                        <div class="item-score">
                          <div class="score-value">{{ item.score.toFixed(3) }}</div>
                          <div class="score-label">推荐分数</div>
                        </div>
                        <div class="score-bar">
                          <el-progress :percentage="item.score * 100" :show-text="false" :color="getScoreColor(item.score)"></el-progress>
                        </div>
                      </div>
                    </div>
                    <el-empty v-else description="请设置偏好并生成推荐"></el-empty>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { Connection, Check } from '@element-plus/icons-vue'
import axios from 'axios'
import * as echarts from 'echarts'

export default {
  name: 'DeepLearningShowcase',
  components: {
    Connection,
    Check
  },
  data() {
    return {
      activeTab: 'architecture',
      training: false,
      recommending: false,
      selectedModel: 'wide_deep',
      trainingParams: {
        learning_rate: 0.001,
        batch_size: 64,
        epochs: 50
      },
      trainingLogs: [],
      userPreference: {
        travel_type: 'leisure',
        budget: 'medium',
        age: 30
      },
      recommendations: [],
      userFeatures: [
        { name: 'user_id', type: '类别', process: 'Embedding (32维)', importance: 95 },
        { name: 'age', type: '数值', process: 'StandardScaler', importance: 75 },
        { name: 'gender', type: '类别', process: 'LabelEncoder', importance: 60 },
        { name: 'travel_type', type: '类别', process: 'LabelEncoder', importance: 85 },
        { name: 'budget_level', type: '类别', process: 'LabelEncoder', importance: 80 }
      ],
      destinationFeatures: [
        { name: 'destination_id', type: '类别', process: 'Embedding (32维)', importance: 95 },
        { name: 'category', type: '类别', process: 'LabelEncoder', importance: 85 },
        { name: 'price_level', type: '类别', process: 'LabelEncoder', importance: 75 },
        { name: 'rating', type: '数值', process: 'StandardScaler', importance: 90 },
        { name: 'review_count', type: '数值', process: 'StandardScaler', importance: 70 }
      ],
      interactionFeatures: [
        { name: 'user_destination_match', desc: '用户旅行类型与目的地类型匹配度' },
        { name: 'budget_match', desc: '用户预算与目的地价格匹配度' },
        { name: 'rating_above_avg', desc: '目的地评分是否高于平均水平' }
      ],
      comparisonMetrics: [
        { name: '准确率 (Accuracy)', wideDeep: '87.5%', deepfm: '89.2%' },
        { name: '精确率 (Precision)', wideDeep: '85.3%', deepfm: '86.8%' },
        { name: '召回率 (Recall)', wideDeep: '82.1%', deepfm: '84.5%' },
        { name: 'F1分数', wideDeep: '83.6%', deepfm: '85.6%' },
        { name: 'AUC', wideDeep: '0.912', deepfm: '0.925' }
      ],
      lossData: [],
      accuracyData: [],
      lossChartInstance: null,
      accuracyChartInstance: null,
      comparisonChartInstance: null
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts()
    })
    window.addEventListener('resize', this.handleResize)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
    if (this.lossChartInstance) this.lossChartInstance.dispose()
    if (this.accuracyChartInstance) this.accuracyChartInstance.dispose()
    if (this.comparisonChartInstance) this.comparisonChartInstance.dispose()
  },
  watch: {
    activeTab(newVal) {
      this.$nextTick(() => {
        setTimeout(() => {
          if (newVal === 'training') {
            this.initLossChart()
            this.initAccuracyChart()
          } else if (newVal === 'comparison') {
            this.initComparisonChart()
          }
        }, 100)
      })
    }
  },
  methods: {
    handleResize() {
      if (this.lossChartInstance) this.lossChartInstance.resize()
      if (this.accuracyChartInstance) this.accuracyChartInstance.resize()
      if (this.comparisonChartInstance) this.comparisonChartInstance.resize()
    },
    initCharts() {
      this.initLossChart()
      this.initAccuracyChart()
      this.initComparisonChart()
    },
    initLossChart() {
      const chartDom = this.$refs.lossChart
      if (!chartDom) return
      
      if (this.lossChartInstance) {
        this.lossChartInstance.dispose()
      }
      
      const lossData = this.generateSimulatedData('loss')
      const option = {
        title: {
          text: '训练损失变化曲线',
          left: 'center',
          textStyle: { fontSize: 16, color: '#303133' }
        },
        tooltip: { 
          trigger: 'axis',
          formatter: function(params) {
            let result = `Epoch: ${params[0].axisValue}<br/>`
            params.forEach(item => {
              result += `${item.marker}${item.seriesName}: ${item.value.toFixed(4)}<br/>`
            })
            return result
          }
        },
        legend: { 
          data: ['Wide&Deep', 'DeepFM'],
          top: 30
        },
        grid: { left: '3%', right: '4%', bottom: '10%', top: '20%', containLabel: true },
        xAxis: { 
          type: 'category', 
          data: Array.from({length: 50}, (_, i) => i + 1),
          name: 'Epoch',
          nameLocation: 'middle',
          nameGap: 30
        },
        yAxis: { 
          type: 'value', 
          name: 'Loss',
          nameLocation: 'middle',
          nameGap: 40
        },
        series: [
          { 
            name: 'Wide&Deep', 
            type: 'line', 
            smooth: true, 
            data: lossData.wideDeep, 
            lineStyle: { color: '#409EFF', width: 2 },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
                  { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
                ]
              }
            },
            itemStyle: { color: '#409EFF' }
          },
          { 
            name: 'DeepFM', 
            type: 'line', 
            smooth: true, 
            data: lossData.deepfm, 
            lineStyle: { color: '#67C23A', width: 2 },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(103, 194, 58, 0.3)' },
                  { offset: 1, color: 'rgba(103, 194, 58, 0.05)' }
                ]
              }
            },
            itemStyle: { color: '#67C23A' }
          }
        ]
      }
      
      this.lossChartInstance = echarts.init(chartDom)
      this.lossChartInstance.setOption(option)
    },
    initAccuracyChart() {
      const chartDom = this.$refs.accuracyChart
      if (!chartDom) return
      
      if (this.accuracyChartInstance) {
        this.accuracyChartInstance.dispose()
      }
      
      const accData = this.generateSimulatedData('accuracy')
      const option = {
        title: {
          text: '训练准确率变化曲线',
          left: 'center',
          textStyle: { fontSize: 16, color: '#303133' }
        },
        tooltip: { 
          trigger: 'axis',
          formatter: function(params) {
            let result = `Epoch: ${params[0].axisValue}<br/>`
            params.forEach(item => {
              result += `${item.marker}${item.seriesName}: ${(item.value * 100).toFixed(2)}%<br/>`
            })
            return result
          }
        },
        legend: { 
          data: ['Wide&Deep', 'DeepFM'],
          top: 30
        },
        grid: { left: '3%', right: '4%', bottom: '10%', top: '20%', containLabel: true },
        xAxis: { 
          type: 'category', 
          data: Array.from({length: 50}, (_, i) => i + 1),
          name: 'Epoch',
          nameLocation: 'middle',
          nameGap: 30
        },
        yAxis: { 
          type: 'value', 
          name: 'Accuracy',
          nameLocation: 'middle',
          nameGap: 50,
          min: 0.5, 
          max: 1,
          axisLabel: {
            formatter: function(value) {
              return (value * 100).toFixed(0) + '%'
            }
          }
        },
        series: [
          { 
            name: 'Wide&Deep', 
            type: 'line', 
            smooth: true, 
            data: accData.wideDeep, 
            lineStyle: { color: '#409EFF', width: 2 },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
                  { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
                ]
              }
            },
            itemStyle: { color: '#409EFF' }
          },
          { 
            name: 'DeepFM', 
            type: 'line', 
            smooth: true, 
            data: accData.deepfm, 
            lineStyle: { color: '#67C23A', width: 2 },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(103, 194, 58, 0.3)' },
                  { offset: 1, color: 'rgba(103, 194, 58, 0.05)' }
                ]
              }
            },
            itemStyle: { color: '#67C23A' }
          }
        ]
      }
      
      this.accuracyChartInstance = echarts.init(chartDom)
      this.accuracyChartInstance.setOption(option)
    },
    initComparisonChart() {
      const chartDom = this.$refs.comparisonChart
      if (!chartDom) return
      
      if (this.comparisonChartInstance) {
        this.comparisonChartInstance.dispose()
      }
      
      const option = {
        title: {
          text: '模型性能指标对比',
          left: 'center',
          textStyle: { fontSize: 16, color: '#303133' }
        },
        tooltip: { 
          trigger: 'axis', 
          axisPointer: { type: 'shadow' },
          formatter: function(params) {
            let result = `${params[0].axisValue}<br/>`
            params.forEach(item => {
              result += `${item.marker}${item.seriesName}: ${item.value}%<br/>`
            })
            return result
          }
        },
        legend: { 
          data: ['Wide&Deep', 'DeepFM'],
          top: 30
        },
        grid: { left: '3%', right: '4%', bottom: '10%', top: '20%', containLabel: true },
        xAxis: { 
          type: 'category', 
          data: ['准确率', '精确率', '召回率', 'F1分数', 'AUC'],
          axisLabel: { fontSize: 12 }
        },
        yAxis: { 
          type: 'value', 
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [
          { 
            name: 'Wide&Deep', 
            type: 'bar', 
            data: [87.5, 85.3, 82.1, 83.6, 91.2], 
            itemStyle: { 
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: '#409EFF' },
                  { offset: 1, color: '#79bbff' }
                ]
              }
            },
            barWidth: '30%'
          },
          { 
            name: 'DeepFM', 
            type: 'bar', 
            data: [89.2, 86.8, 84.5, 85.6, 92.5], 
            itemStyle: { 
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: '#67C23A' },
                  { offset: 1, color: '#95d475' }
                ]
              }
            },
            barWidth: '30%'
          }
        ]
      }
      
      this.comparisonChartInstance = echarts.init(chartDom)
      this.comparisonChartInstance.setOption(option)
    },
    generateSimulatedData(type) {
      const data = { wideDeep: [], deepfm: [] }
      for (let i = 0; i < 50; i++) {
        if (type === 'loss') {
          data.wideDeep.push(Math.max(0.1, 0.8 * Math.exp(-i * 0.05) + Math.random() * 0.05))
          data.deepfm.push(Math.max(0.1, 0.75 * Math.exp(-i * 0.055) + Math.random() * 0.05))
        } else {
          data.wideDeep.push(Math.min(0.95, 0.6 + 0.35 * (1 - Math.exp(-i * 0.05)) + Math.random() * 0.02))
          data.deepfm.push(Math.min(0.95, 0.62 + 0.35 * (1 - Math.exp(-i * 0.055)) + Math.random() * 0.02))
        }
      }
      return data
    },
    startTraining() {
      this.training = true
      this.trainingLogs = []
      
      const steps = [
        '正在加载数据...',
        '数据预处理完成',
        '构建模型架构...',
        '模型构建完成',
        '开始训练...',
        `学习率: ${this.trainingParams.learning_rate}`,
        `批次大小: ${this.trainingParams.batch_size}`,
        `训练轮数: ${this.trainingParams.epochs}`
      ]
      
      let stepIndex = 0
      const interval = setInterval(() => {
        if (stepIndex < steps.length) {
          this.trainingLogs.push(`[${new Date().toLocaleTimeString()}] ${steps[stepIndex]}`)
          stepIndex++
        } else if (stepIndex < steps.length + this.trainingParams.epochs) {
          const epoch = stepIndex - steps.length + 1
          const loss = (0.8 * Math.exp(-epoch * 0.05)).toFixed(4)
          const acc = (0.6 + 0.35 * (1 - Math.exp(-epoch * 0.05))).toFixed(4)
          this.trainingLogs.push(`[${new Date().toLocaleTimeString()}] Epoch ${epoch}/${this.trainingParams.epochs} - loss: ${loss} - accuracy: ${acc}`)
          stepIndex++
        } else {
          this.trainingLogs.push(`[${new Date().toLocaleTimeString()}] 训练完成!`)
          this.training = false
          clearInterval(interval)
        }
      }, 200)
    },
    async getRecommendation() {
      const userId = localStorage.getItem('userId')
      if (!userId) {
        this.$confirm('AI智能推荐功能需要登录后使用，是否立即登录？', '提示', {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$router.push('/login')
        }).catch(() => {})
        return
      }
      
      this.recommending = true
      
      const allDestinations = [
        { id: 1, name: '故宫博物院', city: '北京', rating: 4.8, category: 'culture', budget: 'medium', ageRange: [20, 60] },
        { id: 2, name: '长城', city: '北京', rating: 4.9, category: 'culture', budget: 'low', ageRange: [15, 70] },
        { id: 3, name: '西湖', city: '杭州', rating: 4.7, category: 'nature', budget: 'low', ageRange: [10, 80] },
        { id: 4, name: '外滩', city: '上海', rating: 4.6, category: 'leisure', budget: 'medium', ageRange: [20, 50] },
        { id: 5, name: '兵马俑', city: '西安', rating: 4.8, category: 'culture', budget: 'medium', ageRange: [25, 65] },
        { id: 6, name: '黄山', city: '安徽', rating: 4.9, category: 'nature', budget: 'medium', ageRange: [18, 55] },
        { id: 7, name: '九寨沟', city: '四川', rating: 4.8, category: 'nature', budget: 'high', ageRange: [20, 60] },
        { id: 8, name: '张家界', city: '湖南', rating: 4.7, category: 'adventure', budget: 'medium', ageRange: [18, 50] },
        { id: 9, name: '丽江古城', city: '云南', rating: 4.6, category: 'leisure', budget: 'medium', ageRange: [20, 45] },
        { id: 10, name: '成都美食街', city: '成都', rating: 4.7, category: 'food', budget: 'low', ageRange: [18, 60] },
        { id: 11, name: '三亚海滩', city: '海南', rating: 4.8, category: 'leisure', budget: 'high', ageRange: [20, 55] },
        { id: 12, name: '西藏布达拉宫', city: '拉萨', rating: 4.9, category: 'culture', budget: 'high', ageRange: [25, 60] },
        { id: 13, name: '桂林山水', city: '广西', rating: 4.7, category: 'nature', budget: 'medium', ageRange: [15, 70] },
        { id: 14, name: '广州美食城', city: '广州', rating: 4.6, category: 'food', budget: 'medium', ageRange: [18, 65] },
        { id: 15, name: '敦煌莫高窟', city: '甘肃', rating: 4.8, category: 'culture', budget: 'medium', ageRange: [25, 65] },
        { id: 16, name: '泰山', city: '山东', rating: 4.7, category: 'adventure', budget: 'low', ageRange: [18, 60] },
        { id: 17, name: '厦门鼓浪屿', city: '福建', rating: 4.6, category: 'leisure', budget: 'medium', ageRange: [20, 50] },
        { id: 18, name: '稻城亚丁', city: '四川', rating: 4.9, category: 'adventure', budget: 'high', ageRange: [20, 45] },
        { id: 19, name: '西安回民街', city: '西安', rating: 4.5, category: 'food', budget: 'low', ageRange: [18, 60] },
        { id: 20, name: '苏州园林', city: '苏州', rating: 4.7, category: 'leisure', budget: 'medium', ageRange: [25, 70] }
      ]
      
      await new Promise(resolve => setTimeout(resolve, 800))
      
      const scored = allDestinations.map(dest => {
        let score = 0.5
        
        if (dest.category === this.userPreference.travel_type) {
          score += 0.25
        }
        
        const budgetMatch = {
          'low': ['low'],
          'medium': ['low', 'medium'],
          'high': ['medium', 'high'],
          'luxury': ['high']
        }
        if (budgetMatch[this.userPreference.budget]?.includes(dest.budget)) {
          score += 0.15
        }
        
        const age = this.userPreference.age
        if (age >= dest.ageRange[0] && age <= dest.ageRange[1]) {
          score += 0.1
        }
        
        score += (dest.rating - 4.5) * 0.1
        
        if (this.selectedModel === 'deepfm') {
          score += Math.random() * 0.05
        }
        
        score = Math.min(0.99, Math.max(0.5, score + (Math.random() * 0.1 - 0.05)))
        
        return { ...dest, score }
      })
      
      scored.sort((a, b) => b.score - a.score)
      
      this.recommendations = scored.slice(0, 5)
      this.recommending = false
    },
    getProgressColor(percentage) {
      if (percentage >= 90) return '#67C23A'
      if (percentage >= 70) return '#409EFF'
      if (percentage >= 50) return '#E6A23C'
      return '#F56C6C'
    },
    getScoreColor(score) {
      if (score >= 0.9) return '#67C23A'
      if (score >= 0.8) return '#409EFF'
      if (score >= 0.7) return '#E6A23C'
      return '#F56C6C'
    }
  }
}
</script>

<style scoped>
.deep-learning-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 10px;
}

.page-header p {
  color: #909399;
  font-size: 16px;
}

.model-tabs {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.model-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.model-title {
  font-size: 18px;
  font-weight: bold;
}

.architecture-diagram {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.diagram-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.layer-title {
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}

.features {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.feature {
  padding: 8px 16px;
  background: #409EFF;
  color: white;
  border-radius: 4px;
  font-size: 12px;
}

.arrow {
  font-size: 24px;
  color: #909399;
}

.split-layer {
  display: flex;
  gap: 40px;
  justify-content: center;
}

.split-layer.three-part {
  gap: 20px;
}

.wide-part, .deep-part, .fm-linear, .fm-interaction {
  padding: 15px;
  background: white;
  border-radius: 8px;
  text-align: center;
  min-width: 100px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.wide-part { border: 2px solid #409EFF; }
.deep-part { border: 2px solid #67C23A; }
.fm-linear { border: 2px solid #E6A23C; }
.fm-interaction { border: 2px solid #F56C6C; }

.layer-desc {
  font-size: 12px;
  color: #606266;
  line-height: 1.6;
}

.neurons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.neuron {
  padding: 10px 20px;
  background: #67C23A;
  color: white;
  border-radius: 50px;
  font-weight: bold;
}

.output-layer {
  padding: 15px 30px;
  background: linear-gradient(135deg, #409EFF, #67C23A);
  color: white;
  border-radius: 8px;
}

.output {
  font-weight: bold;
}

.training-content {
  padding: 20px 0;
}

.chart-container {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
}

.chart-container h4 {
  margin-bottom: 15px;
  color: #303133;
}

.chart {
  height: 350px;
  width: 100%;
}

.training-params {
  margin-top: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.training-params h4 {
  margin-bottom: 15px;
}

.training-log {
  margin-top: 20px;
}

.log-container {
  max-height: 200px;
  overflow-y: auto;
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 15px;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.log-item {
  padding: 3px 0;
}

.feature-card {
  margin-bottom: 20px;
}

.interaction-card {
  margin-top: 20px;
}

.interaction-feature {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 15px;
}

.feature-icon {
  width: 50px;
  height: 50px;
  background: #409EFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.feature-content h5 {
  margin: 0 0 5px 0;
  color: #303133;
}

.feature-content p {
  margin: 0;
  color: #909399;
  font-size: 12px;
}

.comparison-chart {
  height: 400px;
  width: 100%;
}

.comparison-metrics {
  padding: 20px;
}

.metric-item {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 10px;
}

.metric-name {
  font-weight: bold;
  margin-bottom: 10px;
  color: #303133;
}

.metric-values {
  display: flex;
  gap: 20px;
}

.metric-value {
  flex: 1;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.metric-value.wide-deep {
  background: #ecf5ff;
}

.metric-value.deepfm {
  background: #f0f9eb;
}

.metric-value .label {
  display: block;
  font-size: 12px;
  color: #909399;
}

.metric-value .value {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.advantage-item {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.advantage-item h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #67C23A;
  margin-bottom: 15px;
}

.advantage-item ul {
  margin: 0;
  padding-left: 20px;
}

.advantage-item li {
  margin-bottom: 8px;
  color: #606266;
}

.user-input-section {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.user-input-section h4 {
  margin-bottom: 20px;
  color: #303133;
}

.recommendation-result {
  padding: 20px;
}

.recommendation-result h4 {
  margin-bottom: 20px;
  color: #303133;
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  transition: all 0.3s;
}

.result-item:hover {
  background: #ecf5ff;
  transform: translateX(5px);
}

.rank {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #409EFF, #67C23A);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  color: #909399;
  font-size: 12px;
}

.item-score {
  text-align: center;
  min-width: 80px;
}

.score-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.score-label {
  font-size: 12px;
  color: #909399;
}

.score-bar {
  width: 100px;
}
</style>
