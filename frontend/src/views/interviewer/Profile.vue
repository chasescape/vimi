<template>
  <div class="profile-page bg-gradient-to-br from-blue-50 to-purple-50 p-6 min-h-screen">
    <div class="max-w-6xl mx-auto">
      <div class="grid grid-cols-1 gap-6"> 
        <!-- 调整左右比例为3:7，右侧适度放大 -->
        <div class="grid grid-cols-1 md:grid-cols-[3fr_7fr] gap-6"> 
          <!-- 左侧用户信息卡片 -->
          <div>
            <div class="bg-white rounded-2xl shadow-xl p-6 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 border border-white/20">
              <div class="text-center mb-6">
                <div class="relative inline-block">
                  <el-avatar 
                    :size="100" 
                    :src="userInfo.avatar" 
                    class="mb-4 border-4 border-white/80 shadow-lg ring-4 ring-blue-200/50 hover:ring-blue-300/50 transition-all duration-300"
                  >
                    {{ (userInfo.name || userInfo.username)?.charAt(0)?.toUpperCase() }}
                  </el-avatar>
                  <div class="absolute bottom-2 right-2 w-4 h-4 bg-green-400 rounded-full border-2 border-white"></div>
                </div>
                <h2 class="text-2xl font-bold text-gray-800">{{ userInfo.name || userInfo.username }}</h2>
                <p class="text-gray-500 mt-2">
                  {{ userInfo.role === 'candidate' ? '应聘者' : (userInfo.role === 'interviewer' ? '面试官' : '未知角色') }}
                </p>
              </div>

              <!-- 基本信息展示 -->
              <div class="border-t border-gray-100 pt-4 space-y-3">
                <div class="flex items-center p-3 rounded-lg hover:bg-blue-50/50 transition-colors duration-200">
                  <el-icon class="text-blue-400 mr-3 text-lg"><Message /></el-icon>
                  <span class="text-gray-700">{{ userInfo.email || '未填写' }}</span>
                </div>
                <div class="flex items-center p-3 rounded-lg hover:bg-blue-50/50 transition-colors duration-200">
                  <el-icon class="text-blue-400 mr-3 text-lg"><Phone /></el-icon>
                  <span class="text-gray-700">{{ userInfo.phone || '未填写' }}</span>
                </div>
                <div class="flex items-center p-3 rounded-lg hover:bg-blue-50/50 transition-colors duration-200">
                  <el-icon class="text-blue-400 mr-3 text-lg"><Location /></el-icon>
                  <span class="text-gray-700">
                    {{ userInfo.location?.province || '' }} {{ userInfo.location?.city || '' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧编辑区（适度放大） -->
          <div>
            <div class="bg-white rounded-2xl shadow-xl p-7 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 border border-white/20">
              <div class="flex justify-between items-center mb-7">
                <h3 class="text-xl font-semibold flex items-center">
                  <el-icon class="text-blue-500 mr-2 text-xl"><Edit /></el-icon>
                  <span class="text-gray-800">编辑资料</span>
                </h3>
                <el-button 
                  type="primary" 
                  @click="saveProfile" 
                  class="shadow-md hover:shadow-lg transition-all duration-300 px-5 py-2"
                >
                  <el-icon class="mr-1"><Check /></el-icon>
                  保存修改
                </el-button>
              </div>
              
              <el-form :model="profileForm" label-width="110px">
                <el-form-item label="姓名" class="mb-7">
                  <el-input 
                    v-model="profileForm.name" 
                    placeholder="请输入姓名" 
                    class="text-base h-11 hover:shadow-md transition-all duration-300 rounded-xl"
                  />
                </el-form-item>
                <el-form-item label="邮箱" class="mb-7">
                  <el-input 
                    v-model="profileForm.email" 
                    placeholder="请输入邮箱" 
                    class="text-base h-11 hover:shadow-md transition-all duration-300 rounded-xl"
                  />
                </el-form-item>
                <el-form-item label="手机号" class="mb-7">
                  <el-input 
                    v-model="profileForm.phone" 
                    placeholder="请输入手机号" 
                    class="text-base h-11 hover:shadow-md transition-all duration-300 rounded-xl"
                  />
                </el-form-item>
                <el-form-item label="所在地" class="mb-6">
                  <div class="flex gap-5">
                    <el-input 
                      v-model="profileForm.location.province" 
                      placeholder="省份" 
                      class="text-base h-11 hover:shadow-md transition-all duration-300 rounded-xl flex-1"
                    />
                    <el-input 
                      v-model="profileForm.location.city" 
                      placeholder="城市" 
                      class="text-base h-11 hover:shadow-md transition-all duration-300 rounded-xl flex-1"
                    />
                  </div>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </div>

        <!-- 第二行：面试统计 -->
        <div class="bg-white rounded-2xl shadow-xl p-6 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 border border-white/20">
          <h3 class="text-lg font-medium mb-4 flex items-center">
            <el-icon class="text-purple-500 mr-2"><DataAnalysis /></el-icon>
            <span class="text-gray-800">面试统计</span>
          </h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"> 
            <div class="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl hover:from-blue-100 hover:to-blue-200 transition-all duration-300 transform hover:scale-105">
              <p class="text-4xl font-bold text-blue-600">{{ stats.total }}</p>
              <p class="text-gray-600 mt-2">总面试场次</p>
            </div>
            <div class="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-xl hover:from-green-100 hover:to-green-200 transition-all duration-300 transform hover:scale-105">
              <p class="text-4xl font-bold text-green-600">{{ stats.month }}</p>
              <p class="text-gray-600 mt-2">本月面试</p>
            </div>
            <div class="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl hover:from-purple-100 hover:to-purple-200 transition-all duration-300 transform hover:scale-105">
              <p class="text-4xl font-bold text-purple-600">{{ stats.avgScore }}分</p>
              <p class="text-gray-600 mt-2">平均评分</p>
            </div>
            <div class="text-center p-6 bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl hover:from-orange-100 hover:to-orange-200 transition-all duration-300 transform hover:scale-105">
              <p class="text-4xl font-bold text-orange-600">{{ stats.passRate }}%</p>
              <p class="text-gray-600 mt-2">通过率</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 脚本逻辑与之前一致，保持不变
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { 
  Message, 
  Iphone as Phone, 
  Location, 
  DataAnalysis,
  Edit,
  Check
} from '@element-plus/icons-vue'

const userInfo = ref({})
const profileForm = ref({ name: '', email: '', phone: '', location: { province: '', city: '' } })
const stats = ref({ total: 0, month: 0, avgScore: 0, passRate: 0 })

const fetchProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/auth/profile', { headers: { Authorization: `Bearer ${token}` } })
    if (res.data.success) {
      userInfo.value = res.data.user
      if (!userInfo.value.location) userInfo.value.location = { province: '', city: '' }
      profileForm.value = {
        name: userInfo.value.name || '',
        email: userInfo.value.email || '',
        phone: userInfo.value.phone || '',
        location: { ...userInfo.value.location }
      }
    }
  } catch {
    ElMessage.error('获取资料失败')
  }
}

const fetchInterviewStats = async () => {
  try {
    const res = await axios.get('/api/apply/all')
    const list = res.data || []
    const passed = list.filter(app => app.status === '已通过' && app.interview_time)
    const total = passed.length
    const now = new Date()
    
    stats.value = {
      total,
      month: passed.filter(app => {
        const d = new Date(app.interview_time)
        return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear()
      }).length,
      avgScore: passed.length ? (passed.reduce((a, b) => a + (b.score || 0), 0) / passed.length).toFixed(1) : 0,
      passRate: list.length ? ((passed.length / list.length) * 100).toFixed(1) : 0
    }
  } catch (e) {
    console.error('获取面试统计失败', e)
  }
}

const saveProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.post('/api/auth/update', profileForm.value, { headers: { Authorization: `Bearer ${token}` } })
    res.data.success ? ElMessage.success('资料更新成功') : ElMessage.error(res.data.message || '更新失败')
    fetchProfile()
  } catch {
    ElMessage.error('更新失败')
  }
}

onMounted(() => {
  fetchProfile()
  fetchInterviewStats()
})
</script>

<style scoped>
.profile-page {
  background-attachment: fixed;
}

/* 卡片玻璃效果 */
.bg-white {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.85);
}

/* 输入框样式优化 */
:deep(.el-input__wrapper) {
  height: 44px !important; /* 对应h-11 */
  font-size: 16px !important; /* 对应text-base */
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--el-input-focus-border-color), 0 0 8px 2px rgba(59, 130, 246, 0.2) !important;
}

/* 按钮样式优化 */
:deep(.el-button--primary) {
  background: linear-gradient(135deg, #3b82f6, #6366f1);
  border: none;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* 表单标签样式 */
:deep(.el-form-item__label) {
  font-size: 16px !important;
  font-weight: 500 !important;
}

/* 统计卡片悬停动画 */
.text-center:hover {
  transform: translateY(-5px);
}

/* 头像动画 */
.el-avatar:hover {
  transform: scale(1.1) rotate(5deg);
}

/* 图标动画 */
.el-icon {
  transition: all 0.3s ease;
}

.el-icon:hover {
  transform: scale(1.2);
}
</style>