<template>
  <div class="preference-container">
    <el-card class="preference-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>个人偏好设置</h2>
        </div>
      </template>
      <el-form :model="preferenceForm" :rules="preferenceRules" ref="preferenceFormRef" label-width="120px">
        <el-form-item label="旅游类型" prop="travel_type">
          <el-select v-model="preferenceForm.travel_type" placeholder="请选择旅游类型">
            <el-option label="冒险型" value="adventure"></el-option>
            <el-option label="休闲型" value="leisure"></el-option>
            <el-option label="文化型" value="cultural"></el-option>
            <el-option label="自然型" value="nature"></el-option>
            <el-option label="购物型" value="shopping"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="消费水平" prop="budget_level">
          <el-select v-model="preferenceForm.budget_level" placeholder="请选择消费水平">
            <el-option label="低消费" value="low"></el-option>
            <el-option label="中等消费" value="medium"></el-option>
            <el-option label="高消费" value="high"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="喜欢的地区" prop="favorite_regions">
          <el-select v-model="preferenceForm.favorite_regions" multiple placeholder="请选择喜欢的地区">
            <el-option label="北京" value="北京"></el-option>
            <el-option label="上海" value="上海"></el-option>
            <el-option label="广州" value="广州"></el-option>
            <el-option label="深圳" value="深圳"></el-option>
            <el-option label="杭州" value="杭州"></el-option>
            <el-option label="成都" value="成都"></el-option>
            <el-option label="西安" value="西安"></el-option>
            <el-option label="重庆" value="重庆"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="喜欢的景点类型" prop="favorite_attractions">
          <el-select v-model="preferenceForm.favorite_attractions" multiple placeholder="请选择喜欢的景点类型">
            <el-option label="自然景观" value="natural"></el-option>
            <el-option label="文化古迹" value="cultural"></el-option>
            <el-option label="休闲娱乐" value="leisure"></el-option>
            <el-option label="冒险体验" value="adventure"></el-option>
            <el-option label="购物天堂" value="shopping"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="savePreference" style="width: 100%">保存偏好</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PreferenceForm',
  props: {
    userId: {
      type: [Number, String],
      default: 1
    }
  },
  data() {
    return {
      preferenceForm: {
        travel_type: '',
        budget_level: '',
        favorite_regions: [],
        favorite_attractions: []
      },
      preferenceRules: {
        travel_type: [
          { required: true, message: '请选择旅游类型', trigger: 'change' }
        ],
        budget_level: [
          { required: true, message: '请选择消费水平', trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    this.loadUserPreference()
  },
  methods: {
    loadUserPreference() {
      axios.get(`/user/info/${this.userId}/`)
        .then(response => {
          const userInfo = response.data
          this.preferenceForm = {
            travel_type: userInfo.travel_type || '',
            budget_level: userInfo.budget_level || '',
            favorite_regions: userInfo.favorite_regions || [],
            favorite_attractions: userInfo.favorite_attractions || []
          }
        })
        .catch(error => {
          this.$message.error('加载偏好失败')
        })
    },
    savePreference() {
      this.$refs.preferenceFormRef.validate(async (valid) => {
        if (valid) {
          try {
            const response = await axios.put(`/user/preference/${this.userId}/`, this.preferenceForm)
            if (response.data && response.data.message === '偏好更新成功') {
              this.$message.success('偏好保存成功')
              this.$router.push(`/recommendations/${this.userId}`)
            } else {
              this.$message.success('偏好保存成功')
              this.$router.push(`/recommendations/${this.userId}`)
            }
          } catch (error) {
            console.error('保存偏好失败:', error)
            const errorMsg = error.response?.data?.error || error.message || '保存失败'
            this.$message.error(errorMsg)
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.preference-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  padding: 20px;
}

.preference-card {
  width: 600px;
  border-radius: 10px;
  overflow: hidden;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  color: #333;
}
</style>