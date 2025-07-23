<template>
  <div class="interview-history">
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
      <el-card v-for="stat in statistics" :key="stat.title" class="stat-card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm mb-1">{{ stat.title }}</p>
            <h3 class="text-2xl font-bold">{{ stat.value }}</h3>
          </div>
          <el-icon :size="24" :class="stat.iconColor">
            <component :is="stat.icon" />
          </el-icon>
        </div>
      </el-card>
    </div>

    <!-- 面试列表 -->
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">面试记录</h2>
          <div class="flex gap-4">
            <el-select v-model="filterStatus" placeholder="状态筛选" clearable>
              <el-option
                v-for="item in statusOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :shortcuts="dateShortcuts"
            />
          </div>
        </div>
      </template>

      <el-table :data="filteredInterviews" style="width: 100%">
        <el-table-column prop="date" label="面试时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.startTime) }}
          </template>
        </el-table-column>
        <el-table-column prop="position" label="面试岗位" />
        <el-table-column prop="company" label="公司名称" />
        <el-table-column prop="type" label="面试方式" width="120">
          <template #default="{ row }">
            {{ row.type === 'online' ? '线上面试' : '线下面试' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button 
              v-if="row.evaluation"
              type="primary" 
              link
              @click="viewEvaluation(row)"
            >
              查看评价
            </el-button>
            <el-button 
              v-if="row.recording"
              type="primary" 
              link
              @click="viewRecording(row)"
            >
              查看录像
            </el-button>
            <el-button type="primary" link @click="viewDetail(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
        />
      </div>
    </el-card>

    <!-- 评价详情对话框 -->
    <el-dialog
      v-model="showEvaluation"
      title="面试评价"
      width="600px"
    >
      <div v-if="selectedInterview?.evaluation" class="evaluation-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="总体评分">
            <el-rate
              v-model="selectedInterview.evaluation.overall_rating"
              disabled
              show-score
            />
          </el-descriptions-item>
          <el-descriptions-item label="技术能力">
            <el-rate
              v-model="selectedInterview.evaluation.technical_rating"
              disabled
              show-score
            />
          </el-descriptions-item>
          <el-descriptions-item label="沟通能力">
            <el-rate
              v-model="selectedInterview.evaluation.communication_rating"
              disabled
              show-score
            />
          </el-descriptions-item>
          <el-descriptions-item label="优势">
            <el-tag
              v-for="strength in selectedInterview.evaluation.strengths"
              :key="strength"
              class="mr-2"
            >
              {{ strength }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="建议改进">
            <el-tag
              v-for="weakness in selectedInterview.evaluation.weaknesses"
              :key="weakness"
              type="warning"
              class="mr-2"
            >
              {{ weakness }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="详细反馈">
            {{ selectedInterview.evaluation.feedback }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  Calendar,
  VideoCamera,
  Timer,
  CircleCheck,
  CircleClose
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'

// 统计数据
const statistics = [
  {
    title: '总面试场次',
    value: 12,
    icon: Calendar,
    iconColor: 'text-blue-500'
  },
  {
    title: '已完成面试',
    value: 8,
    icon: CircleCheck,
    iconColor: 'text-green-500'
  },
  {
    title: '待面试',
    value: 3,
    icon: Timer,
    iconColor: 'text-orange-500'
  },
  {
    title: '未通过',
    value: 1,
    icon: CircleClose,
    iconColor: 'text-red-500'
  }
]

// 模拟面试数据
const mockInterviews = [
  {
    id: 1,
    startTime: '2024-03-19 10:00:00',
    endTime: '2024-03-19 11:00:00',
    position: '前端开发工程师',
    company: '腾讯科技',
    type: 'online',
    status: 'completed',
    evaluation: {
      overall_rating: 4,
      technical_rating: 4,
      communication_rating: 5,
      strengths: ['技术基础扎实', '沟通表达清晰'],
      weaknesses: ['项目经验需要积累'],
      feedback: '整体表现不错，建议多参与实际项目积累经验。'
    },
    recording: 'https://example.com/recording/1'
  },
  {
    id: 2,
    startTime: '2024-03-18 14:00:00',
    endTime: '2024-03-18 15:00:00',
    position: '全栈开发工程师',
    company: '阿里巴巴',
    type: 'offline',
    status: 'completed',
    evaluation: {
      overall_rating: 5,
      technical_rating: 5,
      communication_rating: 4,
      strengths: ['技术广度好', '学习能力强'],
      weaknesses: ['后端经验可以加强'],
      feedback: '候选人整体素质很好，建议后续加强后端相关技术的学习。'
    }
  }
]

// 状态
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(mockInterviews.length)
const filterStatus = ref('')
const dateRange = ref([])
const showEvaluation = ref(false)
const selectedInterview = ref(null)

// 状态选项
const statusOptions = [
  { label: '待面试', value: 'scheduled' },
  { label: '进行中', value: 'ongoing' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'cancelled' }
]

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  }
]

// 过滤后的面试列表
const filteredInterviews = computed(() => {
  let result = [...mockInterviews]
  
  // 状态筛选
  if (filterStatus.value) {
    result = result.filter(item => item.status === filterStatus.value)
  }
  
  // 日期筛选
  if (dateRange.value?.length === 2) {
    const start = dayjs(dateRange.value[0]).startOf('day')
    const end = dayjs(dateRange.value[1]).endOf('day')
    result = result.filter(item => {
      const time = dayjs(item.startTime)
      return time.isAfter(start) && time.isBefore(end)
    })
  }
  
  return result
})

// 获取状态类型
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    scheduled: 'primary',
    ongoing: 'success',
    completed: 'info',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    scheduled: '待面试',
    ongoing: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

// 格式化时间
const formatDateTime = (datetime: string) => {
  return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 查看评价
const viewEvaluation = (interview: any) => {
  selectedInterview.value = interview
  showEvaluation.value = true
}

// 查看录像
const viewRecording = (interview: any) => {
  if (interview.recording) {
    window.open(interview.recording, '_blank')
  }
}

// 查看详情
const viewDetail = (interview: any) => {
  // TODO: 实现查看详情逻辑
  console.log('查看详情:', interview)
}
</script>

<style scoped>
.stat-card {
  .el-icon {
    font-size: 24px;
  }
}

.evaluation-detail {
  .el-tag {
    margin-bottom: 8px;
  }
}
</style>
