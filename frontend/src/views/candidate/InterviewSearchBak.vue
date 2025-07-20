<template>
  <div class="min-h-screen p-8 bg-gray-50">
    <!-- 搜索栏 -->
    <div class="flex items-center gap-4 mb-8">
      <el-input 
        v-model="searchKeyword"
        placeholder="搜索感兴趣的面试..."
        size="large"
        @keyup.enter="handleSearch"
      >
        <template #suffix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <el-button 
        type="primary" 
        size="large"
        @click="handleSearch"
      >
        <el-icon class="mr-2"><Search /></el-icon>
        搜索
      </el-button>
    </div>

    <!-- 面试列表 -->
    <el-table :data="tableData" style="width: 100%" class="mb-6">
      <el-table-column prop="title" label="面试名称" width="220" />
      <el-table-column prop="position" label="面试岗位" width="180" />
      <el-table-column prop="employer" label="面试单位" width="200" />
      <el-table-column prop="time" label="面试时间" width="180" />
      <el-table-column label="操作">
        <template #default>
          <el-button type="primary" size="small">查看详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      background
      layout="prev, pager, next"
      :total="filteredData.length"
      :page-size="pageSize"
      v-model:current-page="currentPage"
      class="justify-center"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'

// 生成模拟数据
const generateMockData = () => {
  const positions = ['前端工程师', 'Java开发', '产品经理', '数据分析师', 'UI设计师']
  const employers = ['腾讯科技', '阿里巴巴', '字节跳动', '华为技术', '百度']
  const mockData = []

  for (let i = 1; i <= 50; i++) {
    mockData.push({
      title: `2024校园招聘-${i}`,
      position: positions[Math.floor(Math.random() * positions.length)],
      employer: employers[Math.floor(Math.random() * employers.length)],
      time: generateRandomDate()
    })
  }
  return mockData
}

// 生成随机日期（过去一年内）
const generateRandomDate = () => {
  const start = new Date()
  start.setFullYear(start.getFullYear() - 1)
  const end = new Date()
  const date = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()))
  return date.toISOString().split('T')[0]
}

// 数据与状态管理
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(15)
const mockData = generateMockData()

// 计算属性
const filteredData = computed(() => {
  return mockData.filter(item => 
    Object.values(item).some(value => 
      value.toString().toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  )
})

const tableData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

// 事件处理
const handleSearch = () => {
  currentPage.value = 1
}
</script>

<style scoped>
@reference "tailwindcss";
.el-table :deep(th) {
    
  @apply bg-blue-50 text-gray-700 font-medium;
}

.el-table :deep(td) {
  @apply py-4;
}
</style>