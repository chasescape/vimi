<template>
  <div class="interview-schedule">
    <el-card class="mb-6">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">面试日程</h2>
          <el-button type="primary" @click="refreshSchedule">
            <el-icon><Refresh /></el-icon>刷新
          </el-button>
        </div>
      </template>

      <!-- 日历视图 -->
      <el-calendar v-model="currentDate">
        <template #dateCell="{ data }">
          <div class="calendar-cell">
            <p :class="{ 'is-today': isToday(data.day) }">
              {{ data.day.split('-').slice(2).join('') }}
            </p>
            <!-- 面试事件 -->
            <div v-if="hasInterview(data.day)" class="interview-events">
              <el-tag
                v-for="interview in getInterviews(data.day)"
                :key="interview.id"
                :type="getStatusType(interview.status)"
                size="small"
                class="mb-1 cursor-pointer"
                @click="showInterviewDetail(interview)"
              >
                {{ interview.title }}
              </el-tag>
            </div>
          </div>
        </template>
      </el-calendar>
    </el-card>

    <!-- 今日面试列表 -->
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">今日面试</h2>
          <el-tag :type="getTodayInterviewCount > 0 ? 'success' : 'info'">
            {{ getTodayInterviewCount }} 场面试
          </el-tag>
        </div>
      </template>

      <el-empty v-if="getTodayInterviewCount === 0" description="今日暂无面试" />
      
      <div v-else class="today-interviews">
        <div
          v-for="interview in todayInterviews"
          :key="interview.id"
          class="interview-item p-4 border rounded-lg mb-4 hover:shadow-md transition-shadow"
        >
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-lg font-medium mb-2">{{ interview.title }}</h3>
              <p class="text-gray-600 mb-2">
                <el-icon><Timer /></el-icon>
                {{ formatTime(interview.startTime) }} - {{ formatTime(interview.endTime) }}
              </p>
              <p class="text-gray-600" v-if="interview.location">
                <el-icon><Location /></el-icon>
                {{ interview.location }}
              </p>
            </div>
            <el-tag :type="getStatusType(interview.status)">
              {{ getStatusText(interview.status) }}
            </el-tag>
          </div>
          
          <div class="mt-4 flex justify-end gap-2">
            <el-button 
              v-if="interview.meetingLink"
              type="primary" 
              link
              @click="joinMeeting(interview)"
            >
              <el-icon><VideoCamera /></el-icon>加入会议
            </el-button>
            <el-button type="primary" link @click="showInterviewDetail(interview)">
              <el-icon><Document /></el-icon>查看详情
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 面试详情对话框 -->
    <el-dialog
      v-model="showDetail"
      :title="selectedInterview?.title || '面试详情'"
      width="600px"
    >
      <div v-if="selectedInterview" class="interview-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="面试时间">
            {{ formatDateTime(selectedInterview.startTime) }}
          </el-descriptions-item>
          <el-descriptions-item label="面试时长">
            {{ selectedInterview.duration }} 分钟
          </el-descriptions-item>
          <el-descriptions-item label="面试方式">
            {{ selectedInterview.type === 'online' ? '线上面试' : '线下面试' }}
          </el-descriptions-item>
          <el-descriptions-item v-if="selectedInterview.location" label="面试地点">
            {{ selectedInterview.location }}
          </el-descriptions-item>
          <el-descriptions-item v-if="selectedInterview.meetingLink" label="会议链接">
            <el-link type="primary" @click="joinMeeting(selectedInterview)">
              点击加入会议
            </el-link>
          </el-descriptions-item>
          <el-descriptions-item label="面试官">
            {{ selectedInterview.interviewer }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(selectedInterview.status)">
              {{ getStatusText(selectedInterview.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item v-if="selectedInterview.notes" label="备注">
            {{ selectedInterview.notes }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="mt-4 flex justify-end gap-2">
          <el-button @click="showDetail = false">关闭</el-button>
          <el-button 
            v-if="canCancel(selectedInterview)"
            type="danger" 
            @click="cancelInterview(selectedInterview)"
          >
            取消面试
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Refresh,
  Timer,
  Location,
  VideoCamera,
  Document
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'

// 模拟数据
const mockInterviews = [
  {
    id: 1,
    title: '前端开发工程师面试',
    startTime: '2024-03-19 10:00:00',
    endTime: '2024-03-19 11:00:00',
    duration: 60,
    type: 'online',
    status: 'scheduled',
    meetingLink: 'https://meeting.com/123',
    interviewer: '张面试官',
    notes: '请提前5分钟进入会议室'
  },
  {
    id: 2,
    title: '技术主管面试',
    startTime: '2024-03-19 14:00:00',
    endTime: '2024-03-19 15:00:00',
    duration: 60,
    type: 'offline',
    status: 'scheduled',
    location: '北京市朝阳区xxx大厦B座12层',
    interviewer: '李主管',
    notes: '请携带简历原件'
  }
]

// 状态
const currentDate = ref(new Date())
const showDetail = ref(false)
const selectedInterview = ref(null)

// 获取今日面试
const todayInterviews = computed(() => {
  const today = dayjs().format('YYYY-MM-DD')
  return mockInterviews.filter(interview => 
    interview.startTime.startsWith(today)
  )
})

const getTodayInterviewCount = computed(() => todayInterviews.value.length)

// 检查日期是否为今天
const isToday = (date: string) => {
  return dayjs(date).isSame(dayjs(), 'day')
}

// 检查日期是否有面试
const hasInterview = (date: string) => {
  return mockInterviews.some(interview => 
    interview.startTime.startsWith(date)
  )
}

// 获取指定日期的面试
const getInterviews = (date: string) => {
  return mockInterviews.filter(interview => 
    interview.startTime.startsWith(date)
  )
}

// 获取状态类型
const getStatusType = (status: string) => {
  const types = {
    scheduled: 'primary',
    ongoing: 'success',
    completed: 'info',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts = {
    scheduled: '待面试',
    ongoing: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

// 格式化时间
const formatTime = (datetime: string) => {
  return dayjs(datetime).format('HH:mm')
}

const formatDateTime = (datetime: string) => {
  return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 显示面试详情
const showInterviewDetail = (interview: any) => {
  selectedInterview.value = interview
  showDetail.value = true
}

// 加入会议
const joinMeeting = (interview: any) => {
  if (interview.meetingLink) {
    window.open(interview.meetingLink, '_blank')
  }
}

// 检查是否可以取消面试
const canCancel = (interview: any) => {
  return interview.status === 'scheduled'
}

// 取消面试
const cancelInterview = async (interview: any) => {
  try {
    await ElMessageBox.confirm(
      '确定要取消这场面试吗？取消后无法恢复',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // TODO: 调用取消面试API
    interview.status = 'cancelled'
    ElMessage.success('面试已取消')
    showDetail.value = false
  } catch {
    // 用户取消操作
  }
}

// 刷新日程
const refreshSchedule = () => {
  // TODO: 调用获取面试列表API
  ElMessage.success('日程已更新')
}
</script>

<style scoped>
.calendar-cell {
  height: 100%;
  padding: 4px;
}

.is-today {
  color: var(--el-color-primary);
  font-weight: bold;
}

.interview-events {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 4px;
}

.interview-events .el-tag {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.today-interviews {
  max-height: 400px;
  overflow-y: auto;
}

.interview-item .el-icon {
  margin-right: 4px;
  vertical-align: middle;
}
</style>