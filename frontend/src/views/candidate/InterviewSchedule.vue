<template>
  <div class="min-h-screen p-8 bg-gray-50">
    <!-- 状态提示 -->
    <div class="mb-8" v-if="upcomingInterviews.length">
      <div class="bg-white rounded-xl shadow-md p-6 flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-blue-600 mb-2">{{ statusMessage }}</h1>
          <p class="text-gray-600">{{ statusTip }}</p>
        </div>
        <div class="w-64">
          <InterviewCard :item="nearestInterview" />
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-20">
      <h2 class="text-2xl font-bold text-gray-600 mb-4">还没有预约面试</h2>
      <el-button 
        type="primary" 
        size="large"
        @click="$router.push('/candidate/interview-search')"
      >
        去发现心仪岗位
      </el-button>
    </div>

    <!-- 时间轴 -->
    <div class="relative" v-if="groupedInterviews.size">
      <!-- 时间轴竖线 -->
      <div class="absolute left-16 top-0 bottom-0 w-1 bg-blue-200 rounded-full"></div>
      
      <div 
        v-for="(group, date, index) in groupedInterviews" 
        :key="date"
        class="relative mb-8"
      >
        <!-- 日期标题 -->
        <div class="flex items-center mb-4 ml-16">
          <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
            <span class="text-white text-sm">{{ index + 1 }}</span>
          </div>
          <h3 class="ml-4 text-xl font-bold text-gray-700">{{ formatDate(date) }}</h3>
        </div>

        <!-- 面试卡片组 -->
        <div class="flex flex-wrap ml-32 gap-4">
          <div 
            v-for="(item, i) in group" 
            :key="i"
            class="relative"
            :class="{ 'mt-6': i > 0 }"
          >
            <!-- 时间轴连接线 -->
            <div 
              v-if="i === 0"
              class="absolute -left-16 top-1/2 w-16 h-1 bg-blue-200"
            ></div>
            
            <InterviewCard :item="item" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Clock, Calendar } from '@element-plus/icons-vue'
import InterviewCard from '@/components/interview/InterviewCard.vue'

// 删除原有的InterviewCard组件定义
// 原代码中以下部分需要删除：
// const InterviewCard = defineComponent({
//   props: ['item'],
//   setup(props) {
//     return () => (
//       <div 
//         class="card-item bg-white rounded-lg shadow-md p-4 w-64 transition-all duration-300 cursor-pointer hover:bg-blue-50"
//         onClick="{() => window.open(`/candidate/interview-page?title=${props.item.title}`)}
//       >
//         <img 
//           src={props.item.cover}
//           class="w-full h-32 object-cover rounded-lg mb-4"
//           alt="面试封面"
//         />
//         <h4 class="font-medium mb-2">{props.item.title}</h4>
//         <div class="flex items-center text-sm text-gray-500">
//           <el-icon class="mr-2"><Calendar /></el-icon>
//           <span>{props.item.time.split('T')[1].slice(0,5)}</span>
//         </div>
//       </div>
//     )
//   }
// })

// 生成模拟数据（包含同一天的数据）
const generateMockData = () => {
  const baseDate = new Date()
  const commonDay = new Date(baseDate.setDate(baseDate.getDate() + 3)).toISOString().split('T')[0]
  
  return [
    ...Array.from({length: 7}, (_, i) => ({
      title: `腾讯科技-前端工程师面试 ${i+1}`,
      cover: `/src/assets/interview_${i%5+1}.jpg`,
      position: '前端工程师',
      employer: '腾讯科技',
      time: new Date(Date.now() + 86400000 * (i + 1)).toISOString()
    })),
    // 同一天的三场面试
    ...[9, 14, 16].map(hour => ({
      title: `阿里集团-技术终面 ${hour}:00`,
      cover: '/src/assets/interview_2.jpg',
      position: '全栈开发',
      employer: '阿里巴巴',
      time: `${commonDay}T${hour.toString().padStart(2, '0')}:00:00`
    }))
  ]
}

// 计算属性
const upcomingInterviews = computed(() => 
  generateMockData().filter(item => new Date(item.time) > new Date())
)

const nearestInterview = computed(() => 
  [...upcomingInterviews.value].sort((a, b) => 
    new Date(a.time) - new Date(b.time)
  )[0]
)

const groupedInterviews = computed(() => {
  const groups = new Map()
  upcomingInterviews.value.forEach(item => {
    const date = item.time.split('T')[0]
    groups.set(date, [...(groups.get(date) || []), item])
  })
  return new Map([...groups.entries()].sort())
})

// 状态提示计算
const statusMessage = computed(() => {
  if (!nearestInterview.value) return ''
  const diff = (new Date(nearestInterview.value.time) - Date.now()) / 1000
  
  if (diff < 3600) {
    return `还有${Math.ceil(diff/60)}分钟开始面试`
  } else if (diff < 86400) {
    return `还有${Math.ceil(diff/3600)}小时开始面试`
  } else if (diff < 604800) {
    return `还有${Math.ceil(diff/86400)}天开始面试`
  }
  return `还有${Math.ceil(diff/604800)}星期开始面试`
})

// 修复后的状态提示计算
const statusTip = computed(() => {
  const matchResult = statusMessage.value.match(/分钟|小时|天|星期/)
  const key = matchResult ? matchResult[0] : ''
  return {
    '分钟': '请做好准备',
    '小时': '复习一下专业知识吧',
    '天': '试试模拟面试',
    '星期': '请规划好学习时间~'
  }[key] || ''
})

// 辅助函数
const formatDate = (isoString: string) => 
  new Date(isoString).toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
</script>

<style scoped>
.card-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.1);
}
</style>