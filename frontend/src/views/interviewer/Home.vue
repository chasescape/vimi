<template>
  <div class="interviewer-home">
    <!-- 欢迎区域 -->
    <div class="welcome-section bg-white p-6 rounded-lg shadow-md mb-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-3">欢迎回来，{{ userInfo.username }}</h1>
      <p class="text-gray-600">今天是 {{ currentDate }}，您有 {{ todayInterviews }} 场面试待进行</p>
    </div>

    <!-- 数据统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <el-card shadow="hover" class="stat-card">
        <div class="flex items-center">
          <el-icon class="text-blue-500 text-3xl mr-4"><Calendar /></el-icon>
          <div>
            <h3 class="text-lg font-medium text-gray-700">今日面试</h3>
            <p class="text-2xl font-bold text-blue-600">{{ todayInterviews }}</p>
          </div>
        </div>
      </el-card>

      <el-card shadow="hover" class="stat-card">
        <div class="flex items-center">
          <el-icon class="text-green-500 text-3xl mr-4"><Finished /></el-icon>
          <div>
            <h3 class="text-lg font-medium text-gray-700">已完成面试</h3>
            <p class="text-2xl font-bold text-green-600">{{ completedInterviews }}</p>
          </div>
        </div>
      </el-card>

      <el-card shadow="hover" class="stat-card">
        <div class="flex items-center">
          <el-icon class="text-purple-500 text-3xl mr-4"><User /></el-icon>
          <div>
            <h3 class="text-lg font-medium text-gray-700">候选人总数</h3>
            <p class="text-2xl font-bold text-purple-600">{{ totalCandidates }}</p>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 今日面试列表 -->
    <el-card class="mb-6">
      <template #header>
        <div class="flex justify-between items-center">
          <span class="text-lg font-medium">今日面试安排</span>
          <el-button type="primary" @click="$router.push('/interviewer/schedule')">
            查看全部
          </el-button>
        </div>
      </template>
      
      <el-table :data="todayInterviewList" v-loading="loading">
        <el-table-column prop="time" label="时间" width="150">
          <template #default="{ row }">
            {{ formatTime(row.time) }}
          </template>
        </el-table-column>
        <el-table-column prop="candidateName" label="候选人" width="120" />
        <el-table-column prop="position" label="面试职位" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              link
              @click="startInterview(row)"
              :disabled="!canStart(row)"
            >
              开始面试
            </el-button>
            <el-button 
              type="primary" 
              link
              @click="viewDetail(row)"
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="todayInterviewList.length === 0" class="text-center py-8 text-gray-500">
        今日暂无面试安排
      </div>
    </el-card>

    <!-- 快捷操作 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <el-card>
        <template #header>
          <div class="flex justify-between items-center">
            <span class="text-lg font-medium">快捷操作</span>
          </div>
        </template>
        
        <div class="flex flex-wrap gap-4">
          <el-button type="primary" @click="$router.push('/interviewer/create')">
            <el-icon><Plus /></el-icon>创建面试
          </el-button>
          <el-button type="success" @click="$router.push('/interviewer/schedule')">
            <el-icon><Calendar /></el-icon>面试日程
          </el-button>
          <el-button type="info" @click="$router.push('/interviewer/history')">
            <el-icon><List /></el-icon>历史记录
          </el-button>
        </div>
      </el-card>

      <el-card>
        <template #header>
          <div class="flex justify-between items-center">
            <span class="text-lg font-medium">面试评估统计</span>
          </div>
        </template>
        
        <div class="flex items-center justify-around">
          <div class="text-center">
            <p class="text-3xl font-bold text-green-600">{{ passRate }}%</p>
            <p class="text-gray-600">通过率</p>
          </div>
          <div class="text-center">
            <p class="text-3xl font-bold text-blue-600">{{ avgScore }}</p>
            <p class="text-gray-600">平均分</p>
          </div>
          <div class="text-center">
            <p class="text-3xl font-bold text-purple-600">{{ totalEvaluations }}</p>
            <p class="text-gray-600">总评估数</p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Calendar, Finished, User, Plus, List } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { auth } from '@/utils/auth'

const router = useRouter()
const loading = ref(false)

// 用户信息
const userInfo = ref(auth.getUser() || {})

// 统计数据
const todayInterviews = ref(0)
const completedInterviews = ref(0)
const totalCandidates = ref(0)
const passRate = ref(0)
const avgScore = ref(0)
const totalEvaluations = ref(0)

// 今日面试列表
const todayInterviewList = ref([
  {
    id: 1,
    time: new Date('2024-01-20 10:00:00'),
    candidateName: '张三',
    position: '前端开发工程师',
    status: 'pending'
  },
  {
    id: 2,
    time: new Date('2024-01-20 14:00:00'),
    candidateName: '李四',
    position: '后端开发工程师',
    status: 'ready'
  }
])

// 获取当前日期
const currentDate = new Date().toLocaleDateString('zh-CN', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  weekday: 'long'
})

// 格式化时间
const formatTime = (time: Date) => {
  return time.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取状态类型
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: 'info',
    ready: 'success',
    completed: '',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待开始',
    ready: '准备中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

// 检查是否可以开始面试
const canStart = (interview: any) => {
  return interview.status === 'ready'
}

// 开始面试
const startInterview = (interview: any) => {
  router.push(`/interviewer/interview/${interview.id}`)
}

// 查看详情
const viewDetail = (interview: any) => {
  router.push(`/interviewer/history/${interview.id}`)
}

// 获取面试数据
const fetchInterviewData = async () => {
  try {
    loading.value = true
    // TODO: 调用API获取数据
    // 这里使用模拟数据
    todayInterviews.value = 2
    completedInterviews.value = 15
    totalCandidates.value = 30
    passRate.value = 85
    avgScore.value = 4.2
    totalEvaluations.value = 20
  } catch (error) {
    console.error('获取面试数据失败:', error)
    ElMessage.error('获取数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchInterviewData()
})
</script>

<style scoped>
.interviewer-home {
  padding: 24px;
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.el-card {
  border-radius: 8px;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #e8e8e8;
}

.el-icon {
  font-size: 24px;
}

.el-button {
  font-size: 14px;
}

.el-button .el-icon {
  font-size: 16px;
  margin-right: 4px;
}
</style>
