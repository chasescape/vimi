<template>
  <div class="interview-create p-6">
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold mb-6">岗位信息总览</h2>
      
      <!-- 搜索和筛选 -->
      <div class="flex items-center gap-4 mb-6">
        <el-input
          v-model="searchQuery"
          placeholder="搜索岗位/类别"
          class="w-64"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-select v-model="cityFilter" placeholder="全部城市" clearable>
          <el-option label="北京" value="北京" />
          <el-option label="上海" value="上海" />
          <el-option label="深圳" value="深圳" />
          <el-option label="广州" value="广州" />
          <el-option label="杭州" value="杭州" />
        </el-select>

        <el-select v-model="salaryFilter" placeholder="薪资范围" clearable>
          <el-option label="10k-15k" value="10k-15k" />
          <el-option label="15k-20k" value="15k-20k" />
          <el-option label="20k-30k" value="20k-30k" />
          <el-option label="30k以上" value="30k+" />
        </el-select>

        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>筛选
        </el-button>

        <el-button type="success" @click="handleCreatePosition">
          <el-icon><Plus /></el-icon>新增岗位
        </el-button>
      </div>

      <!-- 岗位列表 -->
      <el-table :data="filteredPositions" v-loading="loading">
        <el-table-column prop="title" label="岗位名称" min-width="200">
          <template #default="{ row }">
            <div class="font-medium text-blue-600">{{ row.title }}</div>
            <div class="text-gray-500 text-sm">{{ row.department }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="city" label="工作地点" width="100" />
        <el-table-column prop="salary" label="薪资范围" width="120" />
        <el-table-column prop="candidates" label="候选人" width="100">
          <template #default="{ row }">
            {{ row.candidates }}人
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
            <el-button type="primary" link @click="handleCreateInterview(row)">
              创建面试
            </el-button>
            <el-button type="primary" link @click="handleViewDetail(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 创建面试对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="创建面试"
      width="600px"
    >
      <el-form :model="interviewForm" label-width="100px">
        <el-form-item label="面试岗位">
          <span>{{ selectedPosition?.title }}</span>
        </el-form-item>
        <el-form-item label="候选人">
          <el-select v-model="interviewForm.candidate" placeholder="请选择候选人" class="w-full">
            <el-option
              v-for="candidate in candidates"
              :key="candidate.id"
              :label="candidate.name"
              :value="candidate.id"
            >
              <div class="flex items-center">
                <span>{{ candidate.name }}</span>
                <span class="text-gray-500 ml-2">({{ candidate.experience }}年经验)</span>
                  </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="面试时间">
          <el-date-picker
            v-model="interviewForm.time"
            type="datetime"
            placeholder="选择面试时间"
            class="w-full"
          />
        </el-form-item>
        <el-form-item label="面试形式">
          <el-radio-group v-model="interviewForm.type">
            <el-radio label="online">线上面试</el-radio>
            <el-radio label="offline">线下面试</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="面试地点" v-if="interviewForm.type === 'offline'">
          <el-input v-model="interviewForm.location" placeholder="请输入面试地点" />
        </el-form-item>
        <el-form-item label="面试链接" v-else>
          <el-input v-model="interviewForm.link" placeholder="请输入面试链接">
            <template #append>
              <el-button @click="generateMeetingLink">生成链接</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="interviewForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入面试备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitInterview">
            创建面试
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 新增岗位对话框 -->
    <el-dialog
      v-model="showPositionDialog"
      title="新增岗位"
      width="600px"
    >
      <el-form :model="positionForm" label-width="100px">
        <el-form-item label="岗位名称" required>
          <el-input v-model="positionForm.title" placeholder="请输入岗位名称" />
        </el-form-item>
        <el-form-item label="所属部门" required>
          <el-input v-model="positionForm.department" placeholder="请输入所属部门" />
        </el-form-item>
        <el-form-item label="工作地点" required>
          <el-select v-model="positionForm.city" placeholder="请选择工作地点" class="w-full">
            <el-option label="北京" value="北京" />
            <el-option label="上海" value="上海" />
            <el-option label="深圳" value="深圳" />
            <el-option label="广州" value="广州" />
            <el-option label="杭州" value="杭州" />
          </el-select>
        </el-form-item>
        <el-form-item label="薪资范围" required>
          <el-select v-model="positionForm.salary" placeholder="请选择薪资范围" class="w-full">
            <el-option label="10k-15k" value="10k-15k" />
            <el-option label="15k-20k" value="15k-20k" />
            <el-option label="20k-30k" value="20k-30k" />
            <el-option label="30k以上" value="30k+" />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位描述">
          <el-input
            v-model="positionForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入岗位描述"
          />
        </el-form-item>
        <el-form-item label="任职要求">
          <el-input
            v-model="positionForm.requirements"
            type="textarea"
            :rows="4"
            placeholder="请输入任职要求"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showPositionDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitPosition">
            确认添加
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'

// 搜索和筛选
const searchQuery = ref('')
const cityFilter = ref('')
const salaryFilter = ref('')
const loading = ref(false)

// 模拟岗位数据
const positions = ref([
  {
    id: 1,
    title: '前端开发工程师',
    department: '研发中心-前端组',
    city: '北京',
    salary: '20k-30k',
    candidates: 5,
    status: 'active'
  },
  {
    id: 2,
    title: '后端开发工程师',
    department: '研发中心-后端组',
    city: '上海',
    salary: '25k-35k',
    candidates: 8,
    status: 'active'
  },
  {
    id: 3,
    title: '产品经理',
    department: '产品部',
    city: '深圳',
    salary: '20k-30k',
    candidates: 3,
    status: 'paused'
  },
  {
    id: 4,
    title: 'UI设计师',
    department: '设计部',
    city: '广州',
    salary: '15k-25k',
    candidates: 4,
    status: 'active'
  },
  {
    id: 5,
    title: '算法工程师',
    department: '研发中心-算法组',
    city: '北京',
    salary: '30k+',
    candidates: 6,
    status: 'active'
  }
])

// 模拟候选人数据
const candidates = ref([
  { id: 1, name: '张三', experience: 3 },
  { id: 2, name: '李四', experience: 5 },
  { id: 3, name: '王五', experience: 2 },
  { id: 4, name: '赵六', experience: 4 }
])

// 筛选岗位
const filteredPositions = computed(() => {
  return positions.value.filter(position => {
    const matchQuery = !searchQuery.value || 
      position.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      position.department.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchCity = !cityFilter.value || position.city === cityFilter.value
    const matchSalary = !salaryFilter.value || position.salary === salaryFilter.value
    
    return matchQuery && matchCity && matchSalary
  })
})

// 获取状态类型
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    paused: 'info',
    closed: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    active: '招聘中',
    paused: '已暂停',
    closed: '已关闭'
  }
  return texts[status] || status
}

// 创建面试相关
const showCreateDialog = ref(false)
const selectedPosition = ref<any>(null)
const interviewForm = ref({
  candidate: '',
  time: '',
  type: 'online',
  location: '',
  link: '',
  notes: ''
})

const handleCreateInterview = (position: any) => {
  selectedPosition.value = position
  showCreateDialog.value = true
}

const generateMeetingLink = () => {
  interviewForm.value.link = `https://meeting.vimi.ai/${Math.random().toString(36).substring(7)}`
}

const handleSubmitInterview = () => {
  // TODO: 提交面试信息
  ElMessage.success('面试创建成功')
  showCreateDialog.value = false
}

// 新增岗位相关
const showPositionDialog = ref(false)
const positionForm = ref({
  title: '',
  department: '',
  city: '',
  salary: '',
  description: '',
  requirements: ''
})

const handleCreatePosition = () => {
  showPositionDialog.value = true
}

const handleSubmitPosition = () => {
  // TODO: 提交岗位信息
  ElMessage.success('岗位创建成功')
  showPositionDialog.value = false
}

// 搜索
const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 查看详情
const handleViewDetail = (position: any) => {
  // TODO: 跳转到岗位详情页
  console.log('查看岗位详情:', position)
}
</script>

<style scoped>
.interview-create {
  min-height: calc(100vh - 64px);
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-dialog__body) {
  padding: 20px 40px;
}
</style>
