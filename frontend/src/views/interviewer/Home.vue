<template>
  <div class="interviewer-home">
    <!-- 背景装饰 -->
    <div class="bg-decoration top-left"></div>
    <div class="bg-decoration bottom-right"></div>

    <!-- 欢迎区域 -->
    <div class="welcome-section bg-white p-6 rounded-xl shadow-sm mb-6 transform transition-all duration-300 hover:shadow-md">
      <h1 class="text-2xl font-bold text-gray-800 mb-3 flex items-center">
        <el-icon class="mr-2 text-primary"><User /></el-icon>
        欢迎回来，{{ userInfo.username || '面试官' }}
      </h1>
      <p class="text-gray-600 flex items-center">
        <el-icon class="mr-2 text-gray-400"><Calendar /></el-icon>
        今天是 {{ currentDate }}，您有 <span class="text-primary font-semibold">{{ todayInterviews }}</span> 场面试待进行
      </p>
    </div>

    <!-- 数据统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <el-card class="stat-card group overflow-hidden" :shadow="false">
        <div class="card-inner">
          <div class="flex items-center">
            <div class="stat-icon blue">
              <Calendar class="icon" />
            </div>
            <div class="stat-content ml-4">
              <h3 class="text-sm font-medium text-gray-500">今日面试</h3>
              <p class="text-3xl font-bold text-gray-800 mt-1">{{ todayInterviews }}</p>
            </div>
          </div>
          <div class="stat-hover"></div>
        </div>
      </el-card>

      <el-card class="stat-card group overflow-hidden" :shadow="false">
        <div class="card-inner">
          <div class="flex items-center">
            <div class="stat-icon green">
              <Finished class="icon" />
            </div>
            <div class="stat-content ml-4">
              <h3 class="text-sm font-medium text-gray-500">已完成面试</h3>
              <p class="text-3xl font-bold text-gray-800 mt-1">{{ completedInterviews }}</p>
            </div>
          </div>
          <div class="stat-hover"></div>
        </div>
      </el-card>

      <el-card class="stat-card group overflow-hidden" :shadow="false">
        <div class="card-inner">
          <div class="flex items-center">
            <div class="stat-icon purple">
              <User class="icon" />
            </div>
            <div class="stat-content ml-4">
              <h3 class="text-sm font-medium text-gray-500">候选人总数</h3>
              <p class="text-3xl font-bold text-gray-800 mt-1">{{ totalCandidates }}</p>
            </div>
          </div>
          <div class="stat-hover"></div>
        </div>
      </el-card>
    </div>

    <!-- 今日面试列表 -->
    <el-card class="mb-6 overflow-hidden" :shadow="false" border>
      <template #header>
        <div class="flex justify-between items-center">
          <span class="text-lg font-medium text-gray-800">今日面试安排</span>
          <el-button 
            type="primary" 
            @click="$router.push('/interviewer/history')"
            size="default"
            class="view-all-btn"
          >
            查看全部
          </el-button>
        </div>
      </template>
      
      <el-table 
        :data="todayInterviewList" 
        v-loading="loading" 
        style="width: 100%"
        :header-cell-style="headerCellStyle"
        :row-style="rowStyle"
        border
        :highlight-current-row="true"
      >
        <el-table-column prop="time" label="时间" width="150">
          <template #default="{ row }">
            {{ formatTime(row.time) }}
          </template>
        </el-table-column>
        <el-table-column prop="candidateName" label="候选人" width="120" />
        <el-table-column prop="position" label="面试职位" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" class="status-tag">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              @click="startInterview(row)"
              :disabled="!canStart(row)"
              size="small"
              class="start-btn"
            >
              开始面试
            </el-button>
         
          </template>
        </el-table-column>
      </el-table>

      <div v-if="todayInterviewList.length === 0" class="empty-state">
        <div class="empty-icon">
          <Calendar class="icon" />
        </div>
        <p class="empty-text">今日暂无面试安排</p>
      </div>
    </el-card>

    <!-- 快捷操作 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <el-card :shadow="false" border class="action-card overflow-hidden">
        <template #header>
          <div class="flex justify-between items-center">
            <span class="text-lg font-medium text-gray-800">快捷操作</span>
          </div>
        </template>
        
        <div class="action-buttons">
          <el-button 
            type="primary" 
            @click="$router.push('/interviewer/schedule')"
            size="default"
            class="action-btn primary"
          >
            <el-icon class="icon"><Plus /></el-icon>创建面试
          </el-button>
          <el-button 
            type="success" 
            @click="$router.push('/interviewer/history')"
            size="default"
            class="action-btn success"
          >
            <el-icon class="icon"><Calendar /></el-icon>面试日程
          </el-button>
          <el-button 
            type="info" 
            @click="$router.push('/interviewer/history')"
            size="default"
            class="action-btn info"
          >
            <el-icon class="icon"><List /></el-icon>历史记录
          </el-button>
        </div>
      </el-card>

      <el-card :shadow="false" border class="stats-card overflow-hidden">
        <template #header>
          <div class="flex justify-between items-center">
            <span class="text-lg font-medium text-gray-800">面试评估统计</span>
          </div>
        </template>
        
        <div class="stats-container">
          <div class="stat-item pass-rate">
            <div class="stat-item-value">{{ passRate }}%</div>
            <div class="stat-item-label">通过率</div>
          </div>
          <div class="stat-item avg-score">
            <div class="stat-item-value">{{ avgScore }}</div>
            <div class="stat-item-label">平均分</div>
          </div>
          <div class="stat-item total-eval">
            <div class="stat-item-value">{{ totalEvaluations }}</div>
            <div class="stat-item-label">总评估数</div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
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
const todayInterviewList = ref([])

// 获取当前日期
const currentDate = new Date().toLocaleDateString('zh-CN', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  weekday: 'long'
})

// 表格样式
const headerCellStyle = {
  'background-color': '#f8fafc',
  'font-weight': '600',
  'color': '#334155',
  'border-bottom': '1px solid #e2e8f0'
}

const rowStyle = ({ rowIndex }) => {
  return {
    'background-color': rowIndex % 2 === 0 ? '#fff' : '#f8fafc',
    'transition': 'background-color 0.2s'
  }
}

// 格式化时间
const formatTime = (time) => {
  return new Date(time).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'info',
    ready: 'success',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    pending: '待开始',
    ready: '准备中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

// 检查是否可以开始面试
const canStart = (interview) => {
  return interview.status === 'ready'
}

// 开始面试
const startInterview = (interview) => {
  router.push(`/interviewer/interview/${interview.id}`)
}

// 查看详情
const viewDetail = (interview) => {
  router.push(`/interviewer/history/${interview.id}`)
}

// 获取面试数据并统计
const fetchInterviewData = async () => {
  try {
    loading.value = true
    const res = await axios.get('/api/apply/all')
    const all = res.data || []

    const approved = all.filter(app =>
      app.status === '已通过' && app.interview_time && app.interview_link
    ).map(app => ({
      id: app.application_id,
      time: new Date(app.interview_time),
      candidateName: app.username,
      position: app.job_title || '',
      status: app.interview_status || 'pending',
      link: app.interview_link
    }))

    totalCandidates.value = approved.length
    completedInterviews.value = approved.filter(i => i.status === 'completed').length

    const todayStr = new Date().toISOString().slice(0, 10)
    todayInterviewList.value = approved.filter(i =>
      i.time.toISOString().slice(0, 10) === todayStr
    )
    todayInterviews.value = todayInterviewList.value.length

    // 模拟数据
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
  background-color: #f8fafc;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  border-radius: 50%;
  z-index: 0;
  opacity: 0.05;
}

.top-left {
  top: -150px;
  left: -150px;
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
}

.bottom-right {
  bottom: -200px;
  right: -200px;
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
}

/* 欢迎区域 */
.welcome-section {
  position: relative;
  z-index: 1;
  border: 1px solid #e2e8f0;
}

/* 统计卡片 */
.stat-card {
  background-color: #fff;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
}

.card-inner {
  padding: 20px;
  position: relative;
  z-index: 1;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.blue {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.stat-icon.green {
  background-color: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.stat-icon.purple {
  background-color: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.stat-icon .icon {
  font-size: 24px;
}

.stat-content {
  flex-grow: 1;
}

.stat-hover {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.02);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stat-card.group:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
}

.stat-card.group:hover .stat-hover {
  opacity: 1;
}

/* 表格样式 */
:deep(.el-table) {
  border-radius: 6px;
  overflow: hidden;
}

.status-tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.start-btn {
  margin-right: 8px;
}

.detail-btn {
  background-color: #f1f5f9;
  color: #334155;
}

.detail-btn:hover {
  background-color: #e2e8f0;
}

/* 空状态 */
.empty-state {
  padding: 40px 0;
  text-align: center;
  color: #94a3b8;
}

.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.empty-icon .icon {
  font-size: 32px;
  color: #94a3b8;
}

.empty-text {
  font-size: 16px;
  font-weight: 500;
}

/* 快捷操作卡片 */
.action-card {
  background-color: #fff;
}

.action-buttons {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.action-btn {
  padding: 12px 16px;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn .icon {
  margin-right: 8px;
}

.action-btn.primary {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

.action-btn.primary:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.action-btn.success {
  background-color: #10b981;
  border-color: #10b981;
}

.action-btn.success:hover {
  background-color: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.action-btn.info {
  background-color: #8b5cf6;
  border-color: #8b5cf6;
}

.action-btn.info:hover {
  background-color: #7c3aed;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

/* 统计卡片 */
.stats-card {
  background-color: #fff;
}

.stats-container {
  padding: 20px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  min-height: 160px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  border-radius: 8px;
  background-color: #f8fafc;
  width: 100%;
  margin: 0 8px;
  transition: transform 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
}

.stat-item-value {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
}

.pass-rate .stat-item-value {
  color: #10b981;
}

.avg-score .stat-item-value {
  color: #3b82f6;
}

.total-eval .stat-item-value {
  color: #8b5cf6;
}

.stat-item-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .stats-container {
    flex-direction: column;
    gap: 16px;
  }
  
  .stat-item {
    margin: 8px 0;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
  }
}
</style>