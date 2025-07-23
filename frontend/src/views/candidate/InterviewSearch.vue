<template>
  <div class="job-search">
    <!-- 搜索栏 -->
    <div class="search-bar bg-white p-6 rounded-lg shadow mb-6">
      <el-form :model="searchForm" inline>
        <el-form-item>
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索职位名称、公司名称"
            prefix-icon="Search"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-select v-model="searchForm.city" placeholder="城市" clearable>
            <el-option
              v-for="city in cities"
              :key="city.value"
              :label="city.label"
              :value="city.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="searchForm.experience" placeholder="工作经验" clearable>
            <el-option
              v-for="exp in experiences"
              :key="exp.value"
              :label="exp.label"
              :value="exp.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="searchForm.salary" placeholder="薪资范围" clearable>
            <el-option
              v-for="salary in salaries"
              :key="salary.value"
              :label="salary.label"
              :value="salary.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 职位列表 -->
    <div class="job-list bg-white rounded-lg shadow">
      <div class="p-6 border-b border-gray-200">
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">职位列表</h2>
          <div class="flex items-center space-x-4">
            <el-select v-model="sortBy" placeholder="排序" size="small">
              <el-option label="最新发布" value="latest" />
              <el-option label="薪资最高" value="salary" />
            </el-select>
          </div>
        </div>
      </div>

      <div v-if="loading" class="p-6 text-center">
        <el-icon class="animate-spin text-gray-400" :size="24">
          <Loading />
        </el-icon>
              </div>

      <template v-else>
        <div v-if="jobs.length === 0" class="p-6 text-center text-gray-500">
          暂无匹配的职位
            </div>

        <div v-else class="divide-y divide-gray-200">
          <div
            v-for="job in jobs"
            :key="job.id"
            class="job-item p-6 hover:bg-gray-50 transition-colors cursor-pointer"
            @click="showJobDetail(job)"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-lg font-medium text-gray-900">{{ job.title }}</h3>
                <div class="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                  <span>{{ job.company }}</span>
                  <span>{{ job.city }}</span>
                  <span>{{ job.experience }}</span>
                  <span>{{ job.education }}</span>
                </div>
                <div class="mt-2 flex items-center space-x-2">
                  <el-tag
                    v-for="tag in job.tags"
                    :key="tag"
                    size="small"
                    class="mr-2"
                  >
                    {{ tag }}
                  </el-tag>
              </div>
              </div>
              <div class="text-right">
                <div class="text-lg font-medium text-red-500">{{ job.salary }}</div>
                <div class="mt-2">
                  <el-button 
                    type="primary" 
                    size="small"
                    :disabled="job.applied"
                    @click.stop="handleApply(job)"
                  >
                    {{ job.applied ? '已投递' : '立即投递' }}
                  </el-button>
            </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="p-6 flex justify-center">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 30, 50]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
      </div>
      </template>
    </div>

    <!-- 职位详情对话框 -->
    <el-dialog
      v-model="showDetail"
      title="职位详情"
      width="800px"
      destroy-on-close
    >
      <div v-if="selectedJob" class="job-detail">
        <div class="flex justify-between items-start mb-6">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ selectedJob.title }}</h2>
            <div class="mt-2 text-gray-500">
              {{ selectedJob.company }} · {{ selectedJob.city }}
      </div>
    </div>
          <div class="text-right">
            <div class="text-xl font-bold text-red-500">{{ selectedJob.salary }}</div>
            <el-button 
              type="primary" 
              class="mt-2"
              :disabled="selectedJob.applied"
              @click="handleApply(selectedJob)"
            >
              {{ selectedJob.applied ? '已投递' : '立即投递' }}
            </el-button>
      </div>
    </div>

        <el-descriptions :column="2" border>
          <el-descriptions-item label="工作经验">
            {{ selectedJob.experience }}
          </el-descriptions-item>
          <el-descriptions-item label="学历要求">
            {{ selectedJob.education }}
          </el-descriptions-item>
          <el-descriptions-item label="职位类型">
            {{ selectedJob.type }}
          </el-descriptions-item>
          <el-descriptions-item label="发布时间">
            {{ selectedJob.publishTime }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="mt-6">
          <h3 class="text-lg font-medium mb-4">职位描述</h3>
          <div class="text-gray-600 whitespace-pre-line">{{ selectedJob.description }}</div>
        </div>

        <div class="mt-6">
          <h3 class="text-lg font-medium mb-4">职位要求</h3>
          <div class="text-gray-600 whitespace-pre-line">{{ selectedJob.requirements }}</div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Search, Loading } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 在script setup的开头添加类型定义
interface Job {
  id: number
  title: string
  company: string
  city: string
  experience: string
  education: string
  salary: string
  type: string
  tags: string[]
  publishTime: string
  applied: boolean
  description: string
  requirements: string
}

// 搜索表单
const searchForm = reactive({
  keyword: '',
  city: '',
  experience: '',
  salary: ''
})

// 城市选项
const cities = [
  { value: 'beijing', label: '北京' },
  { value: 'shanghai', label: '上海' },
  { value: 'guangzhou', label: '广州' },
  { value: 'shenzhen', label: '深圳' }
]

// 工作经验选项
const experiences = [
  { value: '0', label: '应届生' },
  { value: '1-3', label: '1-3年' },
  { value: '3-5', label: '3-5年' },
  { value: '5-10', label: '5-10年' },
  { value: '10+', label: '10年以上' }
]

// 薪资范围选项
const salaries = [
  { value: '0-10', label: '10k以下' },
  { value: '10-20', label: '10k-20k' },
  { value: '20-30', label: '20k-30k' },
  { value: '30-50', label: '30k-50k' },
  { value: '50+', label: '50k以上' }
]

// 列表数据
const loading = ref(false)
// 修改 jobs 的类型
const jobs = ref<Job[]>([
  {
    id: 1,
    title: '高级前端开发工程师',
    company: '字节跳动',
    city: '北京',
    experience: '3-5年',
    education: '本科及以上',
    salary: '25k-45k',
    type: '全职',
    tags: ['React', 'Vue', 'TypeScript'],
    publishTime: '2024-02-23',
    applied: false,
    description: '负责字节跳动核心业务的前端开发工作，包括但不限于：\n1. 参与产品需求分析和技术方案设计\n2. 负责前端架构的搭建和优化\n3. 开发高质量的前端代码，确保良好的用户体验\n4. 与后端工程师紧密配合，确保项目的顺利进行',
    requirements: '1. 本科及以上学历，计算机相关专业\n2. 3年以上前端开发经验\n3. 精通 HTML、CSS、JavaScript，熟悉 ES6+ 特性\n4. 熟练掌握 React 或 Vue 等主流框架\n5. 具备良好的代码风格和编程习惯\n6. 有大型项目开发经验者优先'
  },
  {
    id: 2,
    title: '全栈开发工程师',
    company: '阿里巴巴',
    city: '杭州',
    experience: '5-10年',
    education: '本科及以上',
    salary: '35k-70k',
    type: '全职',
    tags: ['Node.js', 'React', 'MySQL'],
    publishTime: '2024-02-22',
    applied: true,
    description: '负责阿里巴巴电商平台的全栈开发工作，包括但不限于：\n1. 负责系统架构设计和开发\n2. 开发高性能、可扩展的后端服务\n3. 开发响应式、易用的前端界面\n4. 参与技术难点攻关和性能优化',
    requirements: '1. 本科及以上学历，计算机相关专业\n2. 5年以上全栈开发经验\n3. 精通 Node.js 和主流前端框架\n4. 熟练掌握 MySQL 等数据库技术\n5. 具备良好的系统设计能力和问题解决能力\n6. 有大型分布式系统开发经验者优先'
  }
])

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

// 排序
const sortBy = ref('latest')

// 职位详情
const showDetail = ref(false)
// 修改 selectedJob 的类型
const selectedJob = ref<Job | null>(null)

// 搜索
const handleSearch = () => {
  loading.value = true
  // TODO: 调用搜索接口
  setTimeout(() => {
    loading.value = false
  }, 1000)
}

// 显示职位详情
const showJobDetail = (job: Job) => {
  selectedJob.value = job
  showDetail.value = true
}

// 投递简历
const handleApply = (job: Job) => {
  ElMessage.success('简历投递成功！')
  job.applied = true
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  handleSearch()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  handleSearch()
  }
</script>

<style scoped>
.job-search {
  max-width: 1200px;
  margin: 0 auto;
}

.job-item {
  transition: all 0.3s ease;
}

.job-detail {
  max-height: 70vh;
  overflow-y: auto;
}
</style> 