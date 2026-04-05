<template>
  <div class="profile-container" v-loading="loading">
    <div class="page-header">
      <h2>👤 个人中心</h2>
      <p>查看和管理您的账号信息</p>
    </div>

    <div class="profile-content">
      <el-row :gutter="24">
        <el-col :span="8">
          <el-card class="profile-avatar-card" shadow="hover">
            <div class="avatar-section">
              <div class="avatar-circle">
                <span class="avatar-text">{{ avatarText }}</span>
              </div>
              <h3 class="username">{{ userInfo.username || '未登录' }}</h3>
              <p class="user-id">ID: {{ userId }}</p>
            </div>
          </el-card>

          <el-card class="quick-actions" shadow="hover">
            <h4>快捷操作</h4>
            <div class="action-buttons">
              <el-button type="primary" @click="goToPreference">
                <el-icon><Setting /></el-icon>
                修改偏好
              </el-button>
              <el-button @click="goToCollection">
                <el-icon><Star /></el-icon>
                我的收藏
              </el-button>
            </div>
          </el-card>
        </el-col>

        <el-col :span="16">
          <el-card class="info-card" shadow="hover">
            <template #header>
              <div class="card-header-title">
                <el-icon><UserFilled /></el-icon>
                <span>基本信息</span>
                <el-button type="primary" size="small" style="margin-left: auto;" @click="showEditDialog = true">
                  <el-icon><Edit /></el-icon>
                  编辑信息
                </el-button>
              </div>
            </template>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="用户名">
                <el-tag>{{ userInfo.username || '-' }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="邮箱">
                {{ userInfo.email || '未设置' }}
              </el-descriptions-item>
              <el-descriptions-item label="性别">
                {{ genderText }}
              </el-descriptions-item>
              <el-descriptions-item label="年龄">
                {{ userInfo.age ? userInfo.age + '岁' : '未设置' }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>

          <el-card class="info-card" shadow="hover" style="margin-top: 20px;">
            <template #header>
              <div class="card-header-title">
                <el-icon><Flag /></el-icon>
                <span>旅游偏好</span>
              </div>
            </template>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="旅游类型">
                <el-tag :type="travelTypeTagType" v-if="userInfo.travel_type">
                  {{ travelTypeText }}
                </el-tag>
                <span v-else style="color: #999;">未设置</span>
              </el-descriptions-item>
              <el-descriptions-item label="消费水平">
                <el-tag v-if="userInfo.budget_level" :type="budgetTagType">
                  {{ budgetText }}
                </el-tag>
                <span v-else style="color: #999;">未设置</span>
              </el-descriptions-item>
              <el-descriptions-item label="喜欢的地区" :span="2">
                <div v-if="userInfo.favorite_regions && userInfo.favorite_regions.length > 0">
                  <el-tag v-for="region in userInfo.favorite_regions" :key="region"
                          style="margin-right: 6px; margin-bottom: 4px;" effect="plain">
                    📍 {{ region }}
                  </el-tag>
                </div>
                <span v-else style="color: #999;">未设置</span>
              </el-descriptions-item>
              <el-descriptions-item label="喜欢的景点类型" :span="2">
                <div v-if="userInfo.favorite_attractions && userInfo.favorite_attractions.length > 0">
                  <el-tag v-for="attr in userInfo.favorite_attractions" :key="attr"
                          style="margin-right: 6px; margin-bottom: 4px;" type="success" effect="plain">
                    {{ attractionTypeText(attr) }}
                  </el-tag>
                </div>
                <span v-else style="color: #999;">未设置</span>
              </el-descriptions-item>
            </el-descriptions>
          </el-card>

          <el-card class="info-card" shadow="hover" style="margin-top: 20px;">
            <template #header>
              <div class="card-header-title">
                <el-icon><DataAnalysis /></el-icon>
                <span>账号统计</span>
              </div>
            </template>
            <el-row :gutter="20">
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-number">{{ collectedDestinationsCount }}</div>
                  <div class="stat-label">收藏景点</div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-number">{{ collectedGuidesCount }}</div>
                  <div class="stat-label">收藏攻略</div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-number">{{ travelTypeText || '-' }}</div>
                  <div class="stat-label">旅游类型</div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-number">{{ budgetText || '-' }}</div>
                  <div class="stat-label">消费水平</div>
                </div>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-dialog v-model="showEditDialog" title="编辑个人信息" width="500px" :close-on-click-modal="false">
      <el-form :model="editForm" label-width="80px" ref="editFormRef" :rules="editRules">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="editForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" placeholder="请输入邮箱地址" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="editForm.gender">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="editForm.age" :min="1" :max="120" placeholder="请输入年龄" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveUserInfo" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { UserFilled, Setting, Star, Flag, DataAnalysis, Edit } from '@element-plus/icons-vue'
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'UserProfile',
  components: {
    UserFilled,
    Setting,
    Star,
    Flag,
    DataAnalysis,
    Edit
  },
  props: {
    userId: {
      type: [Number, String],
      default: 1
    }
  },
  setup(props) {
    const loading = ref(false)
    const saving = ref(false)
    const showEditDialog = ref(false)
    const editFormRef = ref(null)
    const userInfo = ref({})
    const collectedDestinationsCount = ref(0)
    const collectedGuidesCount = ref(0)

    const editForm = ref({
      username: '',
      email: '',
      gender: '',
      age: null
    })

    const editRules = {
      username: [
        { min: 2, max: 20, message: '用户名长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      age: [
        { type: 'number', min: 1, max: 120, message: '年龄必须在 1-120 之间', trigger: 'blur' }
      ]
    }

    const avatarText = computed(() => {
      if (userInfo.value.username) {
        return userInfo.value.username.charAt(0).toUpperCase()
      }
      return '?'
    })

    const genderText = computed(() => {
      const map = { male: '男', female: '女' }
      return map[userInfo.value.gender] || '未设置'
    })

    const travelTypeMap = {
      adventure: '冒险型',
      leisure: '休闲型',
      cultural: '文化型',
      nature: '自然型',
      shopping: '购物型'
    }

    const travelTypeText = computed(() => travelTypeMap[userInfo.value.travel_type] || '')

    const travelTypeTagType = computed(() => {
      const typeMap = {
        adventure: 'danger',
        leisure: '',
        cultural: 'warning',
        nature: 'success',
        shopping: 'info'
      }
      return typeMap[userInfo.value.travel_type] || ''
    })

    const budgetMap = { low: '低消费', medium: '中等消费', high: '高消费' }
    const budgetText = computed(() => budgetMap[userInfo.value.budget_level] || '')
    const budgetTagType = computed(() => ({ low: 'success', medium: 'warning', high: 'danger' }[userInfo.value.budget_level] || ''))

    const attractionTypeMap = {
      natural: '🏞️ 自然景观',
      cultural: '🏛️ 文化古迹',
      leisure: '🎡 休闲娱乐',
      adventure: '⛰️ 冒险体验',
      shopping: '🛍️ 购物天堂'
    }

    const attractionTypeText = (type) => attractionTypeMap[type] || type

    const fetchUserInfo = async () => {
      loading.value = true
      try {
        const response = await axios.get(`/user/info/${props.userId}/`)
        if (response.data) {
          userInfo.value = response.data
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      } finally {
        loading.value = false
      }
    }

    const openEditDialog = () => {
      editForm.value = {
        username: userInfo.value.username || '',
        email: userInfo.value.email || '',
        gender: userInfo.value.gender || '',
        age: userInfo.value.age || null
      }
      showEditDialog.value = true
    }

    const saveUserInfo = async () => {
      if (!editFormRef.value) return
      
      try {
        await editFormRef.value.validate()
      } catch (e) {
        return
      }

      saving.value = true
      try {
        const response = await axios.put(`/user/preference/${props.userId}/`, {
          username: editForm.value.username,
          email: editForm.value.email,
          gender: editForm.value.gender,
          age: editForm.value.age
        })
        
        if (response.data) {
          ElMessage.success('个人信息更新成功！')
          showEditDialog.value = false
          await fetchUserInfo()
        }
      } catch (error) {
        console.error('保存用户信息失败:', error)
        ElMessage.error(error.response?.data?.error || '保存失败，请重试')
      } finally {
        saving.value = false
      }
    }

    const loadCollectionCounts = () => {
      try {
        const destinations = JSON.parse(localStorage.getItem('collectedDestinations') || '[]')
        const guides = JSON.parse(localStorage.getItem('collectedGuides') || '[]')
        collectedDestinationsCount.value = destinations.length
        collectedGuidesCount.value = guides.length
      } catch (e) {
        collectedDestinationsCount.value = 0
        collectedGuidesCount.value = 0
      }
    }

    onMounted(() => {
      fetchUserInfo()
      loadCollectionCounts()
    })

    return {
      loading,
      saving,
      showEditDialog,
      editForm,
      editFormRef,
      editRules,
      userInfo,
      collectedDestinationsCount,
      collectedGuidesCount,
      avatarText,
      genderText,
      travelTypeText,
      travelTypeTagType,
      budgetText,
      budgetTagType,
      attractionTypeText,
      fetchUserInfo,
      openEditDialog,
      saveUserInfo
    }
  },
  methods: {
    goToPreference() {
      this.$router.push(`/preference/${this.userId}`)
    },
    goToCollection() {
      this.$router.push('/collection')
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.page-header p {
  color: #999;
  font-size: 14px;
}

.profile-content {
  padding: 0 10px;
}

.profile-avatar-card {
  text-align: center;
}

.avatar-section {
  padding: 20px 0;
}

.avatar-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.avatar-text {
  font-size: 40px;
  color: white;
  font-weight: bold;
}

.username {
  font-size: 20px;
  color: #333;
  margin-bottom: 4px;
}

.user-id {
  color: #999;
  font-size: 13px;
}

.quick-actions {
  margin-top: 16px;
}

.quick-actions h4 {
  margin-bottom: 12px;
  color: #333;
  font-size: 15px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-buttons .el-button {
  width: 100%;
}

.card-header-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: bold;
}

.info-card {
  margin-bottom: 0;
}

.stat-item {
  text-align: center;
  padding: 16px 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  border-radius: 8px;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #999;
}
</style>
