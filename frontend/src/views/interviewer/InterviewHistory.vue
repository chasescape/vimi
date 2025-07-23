<template>
  <div class="interview-history p-6">
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">面试历史</h2>
        <div class="flex gap-4">
          <!-- 搜索和筛选 -->
          <el-input
            v-model="searchQuery"
            placeholder="搜索候选人/职位"
            class="w-64"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>

          <el-select v-model="timeFilter" placeholder="时间范围" clearable>
            <el-option label="最近一周" value="week" />
            <el-option label="最近一月" value="month" />
            <el-option label="最近三月" value="quarter" />
          </el-select>

          <el-select v-model="resultFilter" placeholder="面试结果" clearable>
            <el-option label="通过" value="pass" />
            <el-option label="未通过" value="fail" />
            <el-option label="待定" value="pending" />
          </el-select>

          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>筛选
          </el-button>
        </div>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-4 gap-6 mb-6">
        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon class="text-blue-500 text-3xl mr-4"><Timer /></el-icon>
            <div>
              <h3 class="text-lg font-medium text-gray-700">总面试场次</h3>
              <p class="text-2xl font-bold text-blue-600">{{ stats.total }}</p>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon class="text-green-500 text-3xl mr-4"><CircleCheck /></el-icon>
            <div>
              <h3 class="text-lg font-medium text-gray-700">通过人数</h3>
              <p class="text-2xl font-bold text-green-600">{{ stats.passed }}</p>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon class="text-red-500 text-3xl mr-4"><CircleClose /></el-icon>
            <div>
              <h3 class="text-lg font-medium text-gray-700">未通过人数</h3>
              <p class="text-2xl font-bold text-red-600">{{ stats.failed }}</p>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon class="text-yellow-500 text-3xl mr-4"><Loading /></el-icon>
            <div>
              <h3 class="text-lg font-medium text-gray-700">待定人数</h3>
              <p class="text-2xl font-bold text-yellow-600">{{ stats.pending }}</p>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 面试记录表格 -->
      <el-table :data="filteredHistory" v-loading="loading" class="w-full">
        <el-table-column prop="date" label="面试日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.date) }}
          </template>
        </el-table-column>
        <el-table-column prop="time" label="时间" width="100">
          <template #default="{ row }">
            {{ formatTime(row.date) }}
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
        <el-table-column prop="position" label="面试职位" min-width="150" />
        <el-table-column prop="duration" label="时长" width="100">
          <template #default="{ row }">
            {{ row.duration }}分钟
          </template>
        </el-table-column>
        <el-table-column prop="type" label="面试形式" width="100">
          <template #default="{ row }">
            <el-tag :type="row.type === 'online' ? 'success' : 'warning'" size="small">
              {{ row.type === 'online' ? '线上' : '线下' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="result" label="面试结果" width="100">
          <template #default="{ row }">
            <el-tag :type="getResultType(row.result)" size="small">
              {{ getResultText(row.result) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="score" label="评分" width="100">
          <template #default="{ row }">
            <el-rate
              v-model="row.score"
              disabled
              text-color="#ff9900"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetail(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Search, 
  Timer, 
  CircleCheck, 
  CircleClose,
  Loading
} from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const searchQuery = ref('')
const timeFilter = ref('')
const resultFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

// 统计数据
const stats = ref({
  total: 86,
  passed: 45,
  failed: 28,
  pending: 13
})

// 模拟面试历史数据
const historyData = ref([
  {
    id: 1,
    date: new Date('2024-01-15 10:00:00'),
    candidate: '张三',
    position: '前端开发工程师',
    duration: 60,
    type: 'online',
    result: 'pass',
    score: 4.5,
    notes: '技术基础扎实，沟通能力良好'
  },
  {
    id: 2,
    date: new Date('2024-01-14 14:30:00'),
    candidate: '李四',
    position: '后端开发工程师',
    duration: 90,
    type: 'offline',
    result: 'fail',
    score: 2.5,
    notes: '基础概念不清晰，项目经验较少'
  },
  {
    id: 3,
    date: new Date('2024-01-13 16:00:00'),
    candidate: '王五',
    position: '产品经理',
    duration: 75,
    type: 'online',
    result: 'pending',
    score: 3.5,
    notes: '产品思维不错，需要进一步评估'
  },
  {
    id: 4,
    date: new Date('2024-01-12 11:00:00'),
    candidate: '赵六',
    position: 'UI设计师',
    duration: 60,
    type: 'online',
    result: 'pass',
    score: 5,
    notes: '设计能力出色，作品集优秀'
  },
  {
    id: 5,
    date: new Date('2024-01-11 15:30:00'),
    candidate: '钱七',
    position: '算法工程师',
    duration: 120,
    type: 'offline',
    result: 'pass',
    score: 4,
    notes: '算法理解深入，解题思路清晰'
  }
])

// 筛选面试记录
const filteredHistory = computed(() => {
  return historyData.value.filter(record => {
    const matchQuery = !searchQuery.value || 
      record.candidate.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      record.position.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchResult = !resultFilter.value || record.result === resultFilter.value
    
    // 时间筛选
    let matchTime = true
    if (timeFilter.value) {
      const now = new Date()
      const recordDate = new Date(record.date)
      const diffDays = Math.floor((now.getTime() - recordDate.getTime()) / (1000 * 60 * 60 * 24))
      
      switch (timeFilter.value) {
        case 'week':
          matchTime = diffDays <= 7
          break
        case 'month':
          matchTime = diffDays <= 30
          break
        case 'quarter':
          matchTime = diffDays <= 90
          break
      }
    }
    
    return matchQuery && matchResult && matchTime
  })
})

// 格式化日期
const formatDate = (date: Date) => {
  return date.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  })
}

// 格式化时间
const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取结果类型
const getResultType = (result: string) => {
  const types: Record<string, string> = {
    pass: 'success',
    fail: 'danger',
    pending: 'warning'
  }
  return types[result] || 'info'
}

// 获取结果文本
const getResultText = (result: string) => {
  const texts: Record<string, string> = {
    pass: '通过',
    fail: '未通过',
    pending: '待定'
  }
  return texts[result] || result
}

// 搜索
const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 查看详情
const viewDetail = (record: any) => {
  router.push(`/interviewer/interview/${record.id}`)
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  // TODO: 重新加载数据
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  // TODO: 重新加载数据
}
</script>

<style scoped>
.interview-history {
  min-height: calc(100vh - 64px);
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-pagination) {
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
