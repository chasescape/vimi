<template>
  <div class="interview-schedule p-6">
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">面试日程</h2>
        <div class="flex gap-4">
          <el-radio-group v-model="viewType" size="large">
            <el-radio-button label="list">列表视图</el-radio-button>
            <el-radio-button label="calendar">日历视图</el-radio-button>
          </el-radio-group>
          <el-button type="primary" @click="$router.push('/interviewer/create')">
            <el-icon><Plus /></el-icon>创建面试
          </el-button>
        </div>
      </div>

      <!-- 列表视图 -->
      <template v-if="viewType === 'list'">
        <el-tabs v-model="activeTab" class="mb-4">
          <el-tab-pane label="今日面试" name="today">
            <el-table :data="todayInterviews" v-loading="loading">
              <el-table-column prop="time" label="时间" width="150">
                <template #default="{ row }">
                  {{ formatTime(row.time) }}
                </template>
              </el-table-column>
              <el-table-column prop="candidate" label="候选人" width="120">
                <template #default="{ row }">
                  <div class="flex items-center">
                    <el-avatar :size="24" class="mr-2">
                      {{ row.candidate.charAt(0) }}
                    </el-avatar>
                    {{ row.candidate }}
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="position" label="面试职位" />
              <el-table-column prop="type" label="面试形式" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.type === 'online' ? 'success' : 'warning'">
                    {{ row.type === 'online' ? '线上' : '线下' }}
                  </el-tag>
                </template>
              </el-table-column>
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
          </el-tab-pane>

          <el-tab-pane label="本周面试" name="week">
            <el-table :data="weekInterviews" v-loading="loading">
              <el-table-column prop="date" label="日期" width="120">
                <template #default="{ row }">
                  {{ formatDate(row.time) }}
                </template>
              </el-table-column>
              <el-table-column prop="time" label="时间" width="100">
                <template #default="{ row }">
                  {{ formatTime(row.time) }}
                </template>
              </el-table-column>
              <el-table-column prop="candidate" label="候选人" width="120">
                <template #default="{ row }">
                  <div class="flex items-center">
                    <el-avatar :size="24" class="mr-2">
                      {{ row.candidate.charAt(0) }}
                    </el-avatar>
                    {{ row.candidate }}
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="position" label="面试职位" />
              <el-table-column prop="type" label="面试形式" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.type === 'online' ? 'success' : 'warning'">
                    {{ row.type === 'online' ? '线上' : '线下' }}
                  </el-tag>
                </template>
              </el-table-column>
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
          </el-tab-pane>
        </el-tabs>
      </template>

      <!-- 日历视图 -->
      <template v-else>
        <el-calendar v-model="currentDate">
          <template #dateCell="{ data }">
            <div class="calendar-cell">
              <p :class="data.isSelected ? 'is-selected' : ''">
                {{ data.day.split('-').slice(2).join('') }}
                {{ data.isSelected ? '✔️' : '' }}
              </p>
              <div class="interview-count" v-if="getInterviewCount(data.day)">
                <el-tag size="small" type="success">
                  {{ getInterviewCount(data.day) }}场面试
                </el-tag>
              </div>
            </div>
          </template>
        </el-calendar>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const viewType = ref('list')
const activeTab = ref('today')
const currentDate = ref(new Date())

// 模拟今日面试数据
const todayInterviews = ref([
  {
    id: 1,
    time: new Date('2024-01-20 10:00:00'),
    candidate: '张三',
    position: '前端开发工程师',
    type: 'online',
    status: 'pending',
    link: 'https://meeting.vimi.ai/abc123'
  },
  {
    id: 2,
    time: new Date('2024-01-20 14:00:00'),
    candidate: '李四',
    position: '后端开发工程师',
    type: 'offline',
    status: 'ready',
    location: '北京市朝阳区xx大厦'
  },
  {
    id: 3,
    time: new Date('2024-01-20 16:00:00'),
    candidate: '王五',
    position: '产品经理',
    type: 'online',
    status: 'completed',
    link: 'https://meeting.vimi.ai/def456'
  }
])

// 模拟本周面试数据
const weekInterviews = ref([
  {
    id: 4,
    time: new Date('2024-01-21 10:00:00'),
    candidate: '赵六',
    position: 'UI设计师',
    type: 'online',
    status: 'pending',
    link: 'https://meeting.vimi.ai/ghi789'
  },
  {
    id: 5,
    time: new Date('2024-01-22 11:00:00'),
    candidate: '钱七',
    position: '算法工程师',
    type: 'offline',
    status: 'pending',
    location: '北京市海淀区xx园区'
  },
  {
    id: 6,
    time: new Date('2024-01-23 15:00:00'),
    candidate: '孙八',
    position: '前端开发工程师',
    type: 'online',
    status: 'pending',
    link: 'https://meeting.vimi.ai/jkl012'
  }
])

// 格式化时间
const formatTime = (time: Date) => {
  return time.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化日期
const formatDate = (time: Date) => {
  return time.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
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
  if (interview.type === 'online') {
    window.open(interview.link, '_blank')
  } else {
    ElMessage.info(`请前往面试地点：${interview.location}`)
  }
}

// 查看详情
const viewDetail = (interview: any) => {
  router.push(`/interviewer/interview/${interview.id}`)
}

// 获取某天的面试数量
const getInterviewCount = (day: string) => {
  const date = new Date(day)
  const count = [...todayInterviews.value, ...weekInterviews.value].filter(interview => {
    return interview.time.toDateString() === date.toDateString()
  }).length
  return count || 0
}
</script>

<style scoped>
.interview-schedule {
  min-height: calc(100vh - 64px);
}

.calendar-cell {
  height: 100%;
  padding: 8px;
}

.calendar-cell .interview-count {
  margin-top: 8px;
}

.is-selected {
  color: #409eff;
  font-weight: bold;
}

:deep(.el-calendar-day) {
  height: 100px;
}

:deep(.el-calendar-table td.is-selected .calendar-cell) {
  background-color: #f0f9ff;
}
</style>
