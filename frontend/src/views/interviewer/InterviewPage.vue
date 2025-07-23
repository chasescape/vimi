<template>
  <div class="interview-detail p-6">
    <!-- 基本信息卡片 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h2 class="text-2xl font-bold mb-2">{{ interview.position }}</h2>
          <div class="flex items-center text-gray-500">
            <el-icon class="mr-2"><Timer /></el-icon>
            {{ formatDate(interview.date) }} {{ formatTime(interview.date) }}
            <el-divider direction="vertical" />
            <el-tag :type="interview.type === 'online' ? 'success' : 'warning'" size="small">
              {{ interview.type === 'online' ? '线上面试' : '线下面试' }}
            </el-tag>
            <el-divider direction="vertical" />
            <span>{{ interview.duration }}分钟</span>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <el-button v-if="interview.status === 'ready'" type="primary" @click="startInterview">
            开始面试
          </el-button>
          <el-button v-else-if="interview.status === 'completed'" type="success" plain disabled>
            已完成
          </el-button>
          <el-button v-else type="info" plain disabled>
            {{ getStatusText(interview.status) }}
          </el-button>
        </div>
      </div>

      <el-descriptions :column="3" border>
        <el-descriptions-item label="候选人">
          <div class="flex items-center">
            <el-avatar :size="24" class="mr-2">
              {{ interview.candidate.charAt(0) }}
            </el-avatar>
            {{ interview.candidate }}
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ interview.phone }}
        </el-descriptions-item>
        <el-descriptions-item label="邮箱">
          {{ interview.email }}
        </el-descriptions-item>
        <el-descriptions-item label="面试形式">
          {{ interview.type === 'online' ? '线上面试' : '线下面试' }}
        </el-descriptions-item>
        <el-descriptions-item label="面试地点/链接" :span="2">
          {{ interview.type === 'online' ? interview.link : interview.location }}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <!-- 候选人信息 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 class="text-lg font-bold mb-4">候选人信息</h3>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="工作年限">
          {{ candidate.experience }}年
        </el-descriptions-item>
        <el-descriptions-item label="当前状态">
          {{ candidate.status }}
        </el-descriptions-item>
        <el-descriptions-item label="期望薪资">
          {{ candidate.expectedSalary }}
        </el-descriptions-item>
        <el-descriptions-item label="到岗时间">
          {{ candidate.availableTime }}
        </el-descriptions-item>
        <el-descriptions-item label="技能标签" :span="2">
          <el-tag 
            v-for="skill in candidate.skills" 
            :key="skill"
            size="small"
            class="mr-2"
          >
            {{ skill }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="教育背景" :span="2">
          <div v-for="edu in candidate.education" :key="edu.school" class="mb-2">
            <div class="font-medium">{{ edu.school }}</div>
            <div class="text-gray-500">
              {{ edu.major }} | {{ edu.degree }} | {{ edu.time }}
            </div>
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="工作经历" :span="2">
          <div v-for="work in candidate.workExperience" :key="work.company" class="mb-2">
            <div class="font-medium">{{ work.company }}</div>
            <div class="text-gray-500">
              {{ work.position }} | {{ work.time }}
            </div>
            <div class="text-gray-600 mt-1">{{ work.description }}</div>
          </div>
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <!-- 面试评估 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-bold">面试评估</h3>
        <el-button type="primary" @click="handleSaveEvaluation" v-if="!interview.evaluation">
          提交评估
        </el-button>
      </div>

      <template v-if="interview.evaluation">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="技术能力">
            <el-rate v-model="interview.evaluation.technicalScore" disabled />
          </el-descriptions-item>
          <el-descriptions-item label="沟通能力">
            <el-rate v-model="interview.evaluation.communicationScore" disabled />
          </el-descriptions-item>
          <el-descriptions-item label="问题解决">
            <el-rate v-model="interview.evaluation.problemSolvingScore" disabled />
          </el-descriptions-item>
          <el-descriptions-item label="团队协作">
            <el-rate v-model="interview.evaluation.teamworkScore" disabled />
          </el-descriptions-item>
          <el-descriptions-item label="综合评价" :span="2">
            <el-tag :type="getResultType(interview.evaluation.result)">
              {{ getResultText(interview.evaluation.result) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="评估详情" :span="2">
            {{ interview.evaluation.comments }}
          </el-descriptions-item>
        </el-descriptions>
      </template>

      <template v-else>
        <el-form :model="evaluationForm" label-width="100px">
          <el-form-item label="技术能力">
            <el-rate v-model="evaluationForm.technicalScore" />
          </el-form-item>
          <el-form-item label="沟通能力">
            <el-rate v-model="evaluationForm.communicationScore" />
          </el-form-item>
          <el-form-item label="问题解决">
            <el-rate v-model="evaluationForm.problemSolvingScore" />
          </el-form-item>
          <el-form-item label="团队协作">
            <el-rate v-model="evaluationForm.teamworkScore" />
          </el-form-item>
          <el-form-item label="综合评价">
            <el-select v-model="evaluationForm.result" class="w-full">
              <el-option label="通过" value="pass" />
              <el-option label="待定" value="pending" />
              <el-option label="不通过" value="fail" />
            </el-select>
          </el-form-item>
          <el-form-item label="评估详情">
            <el-input
              v-model="evaluationForm.comments"
              type="textarea"
              :rows="4"
              placeholder="请输入详细的评估意见..."
            />
          </el-form-item>
        </el-form>
      </template>
    </div>

    <!-- 面试记录 -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h3 class="text-lg font-bold mb-4">面试记录</h3>
      <el-timeline>
        <el-timeline-item
          v-for="record in interview.records"
          :key="record.time"
          :timestamp="record.time"
          :type="getRecordType(record.type)"
        >
          <div class="font-medium">{{ record.title }}</div>
          <div class="text-gray-600 mt-1">{{ record.content }}</div>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Timer } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 模拟面试数据
const interview = ref({
  id: route.params.id,
  position: '前端开发工程师',
  date: new Date('2024-01-15 10:00:00'),
  type: 'online',
  status: 'completed',
  duration: 60,
  candidate: '张三',
  phone: '138****8000',
  email: 'zhangsan@example.com',
  link: 'https://meeting.vimi.ai/abc123',
  evaluation: {
    technicalScore: 4.5,
    communicationScore: 4,
    problemSolvingScore: 4.5,
    teamworkScore: 4,
    result: 'pass',
    comments: '候选人技术基础扎实，项目经验丰富，沟通表达清晰，推荐入职。'
  },
  records: [
    {
      time: '10:00',
      type: 'info',
      title: '面试开始',
      content: '开始技术面试环节'
    },
    {
      time: '10:15',
      type: 'success',
      title: '技术考核',
      content: '完成算法题目讲解，思路清晰，代码规范'
    },
    {
      time: '10:35',
      type: 'warning',
      title: '项目经验',
      content: '讨论项目架构设计，性能优化方案'
    },
    {
      time: '10:55',
      type: 'info',
      title: '综合问答',
      content: '职业规划，团队协作等软素质考核'
    },
    {
      time: '11:00',
      type: 'success',
      title: '面试结束',
      content: '面试圆满结束，整体表现良好'
    }
  ]
})

// 模拟候选人数据
const candidate = ref({
  experience: 3,
  status: '在职，考虑机会',
  expectedSalary: '25k-30k',
  availableTime: '一个月内',
  skills: ['Vue', 'React', 'TypeScript', 'Node.js', 'Webpack'],
  education: [
    {
      school: '某某大学',
      major: '计算机科学与技术',
      degree: '本科',
      time: '2017-2021'
    }
  ],
  workExperience: [
    {
      company: '某某科技有限公司',
      position: '前端开发工程师',
      time: '2021.07 - 至今',
      description: '负责公司核心产品的前端开发，主导多个重要功能模块的设计与实现。'
    },
    {
      company: '某某网络科技公司',
      position: '前端开发实习生',
      time: '2020.07 - 2021.01',
      description: '参与公司电商项目的开发，负责页面开发和性能优化。'
    }
  ]
})

// 评估表单
const evaluationForm = ref({
  technicalScore: 0,
  communicationScore: 0,
  problemSolvingScore: 0,
  teamworkScore: 0,
  result: '',
  comments: ''
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

// 获取记录类型
const getRecordType = (type: string) => {
  const types: Record<string, string> = {
    info: 'primary',
    success: 'success',
    warning: 'warning',
    error: 'danger'
  }
  return types[type] || 'info'
}

// 开始面试
const startInterview = () => {
  if (interview.value.type === 'online') {
    window.open(interview.value.link, '_blank')
  } else {
    ElMessage.info(`请前往面试地点：${interview.value.location}`)
  }
}

// 保存评估
const handleSaveEvaluation = () => {
  interview.value.evaluation = { ...evaluationForm.value }
  ElMessage.success('评估保存成功')
}
</script>

<style scoped>
.interview-detail {
  min-height: calc(100vh - 64px);
}

:deep(.el-descriptions__label) {
  width: 120px;
  font-weight: 500;
}

:deep(.el-timeline-item__node--primary) {
  background-color: #409eff;
}

:deep(.el-timeline-item__node--success) {
  background-color: #67c23a;
}

:deep(.el-timeline-item__node--warning) {
  background-color: #e6a23c;
}

:deep(.el-timeline-item__node--danger) {
  background-color: #f56c6c;
}
</style>
