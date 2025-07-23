<template>
  <div class="home-container p-6">
    <!-- 欢迎卡片 -->
    <div class="welcome-card bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow-lg mb-6">
      <h2 class="text-2xl font-bold mb-2">欢迎回来，{{ username }}！</h2>
      <p class="text-blue-100">今天是个寻找理想工作的好日子</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div v-for="stat in statistics" :key="stat.title" 
           class="stat-card bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-700">{{ stat.title }}</h3>
          <el-icon :size="24" :class="stat.iconColor">
            <component :is="stat.icon" />
          </el-icon>
        </div>
        <div class="text-3xl font-bold text-gray-900 mb-2">{{ stat.value }}</div>
        <p class="text-sm text-gray-500">{{ stat.description }}</p>
      </div>
    </div>

    <!-- 最近面试 -->
    <div class="recent-interviews bg-white p-6 rounded-lg shadow">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-700">最近面试</h3>
        <router-link to="/candidate/history" class="text-blue-500 hover:text-blue-600">
          查看全部
        </router-link>
      </div>
      <div v-if="recentInterviews.length > 0" class="space-y-4">
        <div v-for="interview in recentInterviews" :key="interview.id" 
             class="interview-item flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
          <div class="flex items-center space-x-4">
            <el-avatar :size="40" :src="interview.companyLogo">
              {{ interview.companyName.charAt(0) }}
            </el-avatar>
            <div>
              <h4 class="font-medium text-gray-900">{{ interview.position }}</h4>
              <p class="text-sm text-gray-500">{{ interview.companyName }}</p>
            </div>
          </div>
          <div class="text-right">
            <p class="text-sm font-medium" :class="getStatusClass(interview.status)">
              {{ getStatusText(interview.status) }}
            </p>
            <p class="text-sm text-gray-500">{{ interview.time }}</p>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-8 text-gray-500">
        暂无面试记录
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  Document,
  Calendar,
  Timer
} from '@element-plus/icons-vue'

const username = ref(localStorage.getItem('username') || '求职者')

// 统计数据
const statistics = [
  {
    title: '已投递简历',
    value: '12',
    description: '本月新增 5 份',
    icon: Document,
    iconColor: 'text-blue-500'
  },
  {
    title: '待面试',
    value: '3',
    description: '最近一次 2024-02-25',
    icon: Calendar,
    iconColor: 'text-green-500'
  },
  {
    title: '面试完成',
    value: '8',
    description: '通过率 75%',
    icon: Timer,
    iconColor: 'text-purple-500'
  }
]

// 面试状态
const InterviewStatus = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
} as const

type InterviewStatus = typeof InterviewStatus[keyof typeof InterviewStatus]

interface Interview {
  id: number
  companyName: string
  companyLogo?: string
  position: string
  time: string
  status: InterviewStatus
}

// 最近面试数据
const recentInterviews = ref<Interview[]>([
  {
    id: 1,
    companyName: '字节跳动',
    position: '前端开发工程师',
    time: '2024-02-25 14:30',
    status: InterviewStatus.PENDING
  },
  {
    id: 2,
    companyName: '阿里巴巴',
    position: '全栈开发工程师',
    time: '2024-02-23 10:00',
    status: InterviewStatus.COMPLETED
  },
  {
    id: 3,
    companyName: '腾讯',
    position: 'Web前端工程师',
    time: '2024-02-20 15:00',
    status: InterviewStatus.CANCELLED
  }
])

// 获取状态样式
const getStatusClass = (status: InterviewStatus) => {
  switch (status) {
    case InterviewStatus.PENDING:
      return 'text-blue-500'
    case InterviewStatus.COMPLETED:
      return 'text-green-500'
    case InterviewStatus.CANCELLED:
      return 'text-red-500'
    default:
      return ''
  }
}

// 获取状态文本
const getStatusText = (status: InterviewStatus) => {
  switch (status) {
    case InterviewStatus.PENDING:
      return '待面试'
    case InterviewStatus.COMPLETED:
      return '已完成'
    case InterviewStatus.CANCELLED:
      return '已取消'
    default:
      return ''
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.interview-item {
  cursor: pointer;
}
</style>