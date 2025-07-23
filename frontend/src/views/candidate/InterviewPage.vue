<template>
  <div class="interview-page">
    <div class="header">
      <h1>面试准备</h1>
    </div>

    <div class="main-content">
      <!-- 左侧：面试信息和准备材料 -->
      <div class="left-panel">
        <el-card class="interview-info">
          <template #header>
            <div class="card-header">
              <h3>即将开始的面试</h3>
            </div>
          </template>
          <div v-if="upcomingInterview" class="upcoming-interview">
            <p class="company">{{ upcomingInterview.company }}</p>
            <p class="position">{{ upcomingInterview.position }}</p>
            <div class="interview-time">
              <i class="el-icon-time"></i>
              <span>{{ upcomingInterview.time }}</span>
            </div>
            <div class="countdown" v-if="countdown">
              距离面试还有：{{ countdown }}
            </div>
            <el-button type="primary" @click="startInterview" :disabled="!canStartInterview">
              进入面试
            </el-button>
          </div>
          <div v-else class="no-interview">
            暂无即将开始的面试
          </div>
        </el-card>

        <el-card class="preparation-materials">
          <template #header>
            <div class="card-header">
              <h3>面试准备材料</h3>
            </div>
          </template>
          <el-collapse v-model="activeMaterials">
            <el-collapse-item title="公司信息" name="company">
              <div class="company-info">
                <h4>{{ upcomingInterview?.company }}</h4>
                <p>{{ companyInfo.description }}</p>
                <div class="company-details">
                  <p><strong>行业：</strong>{{ companyInfo.industry }}</p>
                  <p><strong>规模：</strong>{{ companyInfo.size }}</p>
                  <p><strong>融资阶段：</strong>{{ companyInfo.funding }}</p>
                </div>
              </div>
            </el-collapse-item>

            <el-collapse-item title="岗位要求" name="requirements">
              <div class="job-requirements">
                <h4>岗位职责</h4>
                <ul>
                  <li v-for="(duty, index) in jobInfo.duties" :key="'duty'+index">
                    {{ duty }}
                  </li>
                </ul>
                <h4>任职要求</h4>
                <ul>
                  <li v-for="(req, index) in jobInfo.requirements" :key="'req'+index">
                    {{ req }}
                  </li>
                </ul>
              </div>
            </el-collapse-item>

            <el-collapse-item title="面试技巧" name="tips">
              <div class="interview-tips">
                <div v-for="(tip, index) in interviewTips" :key="index" class="tip-item">
                  <h4>{{ tip.title }}</h4>
                  <p>{{ tip.content }}</p>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </div>

      <!-- 右侧：模拟练习 -->
      <div class="right-panel">
        <el-card class="practice-section">
          <template #header>
            <div class="card-header">
              <h3>模拟练习</h3>
            </div>
          </template>
          
          <!-- 练习模式选择 -->
          <div class="practice-modes">
            <el-radio-group v-model="practiceMode">
              <el-radio-button label="qa">问答练习</el-radio-button>
              <el-radio-button label="scenario">情景模拟</el-radio-button>
              <el-radio-button label="technical">技术面试</el-radio-button>
            </el-radio-group>
          </div>

          <!-- 练习内容 -->
          <div class="practice-content">
            <!-- 问答练习模式 -->
            <div v-if="practiceMode === 'qa'" class="qa-practice">
              <div class="question-list">
                <div v-for="(qa, index) in practiceQuestions" :key="index" class="question-item">
                  <div class="question" @click="selectQuestion(qa)">
                    <span class="question-number">Q{{ index + 1 }}</span>
                    <span class="question-text">{{ qa.question }}</span>
                    <span class="difficulty" :class="qa.difficulty">
                      {{ qa.difficulty }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 情景模拟模式 -->
            <div v-if="practiceMode === 'scenario'" class="scenario-practice">
              <div class="scenario-list">
                <div v-for="(scenario, index) in scenarios" :key="index" class="scenario-item">
                  <h4>{{ scenario.title }}</h4>
                  <p>{{ scenario.description }}</p>
                  <el-button @click="startScenario(scenario)">开始模拟</el-button>
                </div>
              </div>
            </div>

            <!-- 技术面试模式 -->
            <div v-if="practiceMode === 'technical'" class="technical-practice">
              <div class="topic-list">
                <el-tree
                  :data="technicalTopics"
                  :props="defaultProps"
                  @node-click="handleTopicClick"
                >
                </el-tree>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 练习反馈 -->
        <el-card class="feedback-section" v-if="showFeedback">
          <template #header>
            <div class="card-header">
              <h3>练习反馈</h3>
            </div>
          </template>
          <div class="feedback-content">
            <div class="score-section">
              <div class="score-item">
                <span class="label">整体表现</span>
                <el-rate v-model="feedback.overallScore" disabled></el-rate>
              </div>
              <div class="score-item">
                <span class="label">回答完整性</span>
                <el-progress :percentage="feedback.completeness"></el-progress>
              </div>
              <div class="score-item">
                <span class="label">语言表达</span>
                <el-progress :percentage="feedback.expression"></el-progress>
              </div>
            </div>
            <div class="feedback-details">
              <h4>详细点评</h4>
              <p>{{ feedback.comments }}</p>
            </div>
            <div class="improvement-suggestions">
              <h4>改进建议</h4>
              <ul>
                <li v-for="(suggestion, index) in feedback.suggestions" :key="index">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 模拟面试对话框 -->
    <el-dialog
      title="模拟面试"
      :visible.sync="showPracticeDialog"
      width="70%"
      :before-close="handlePracticeClose"
    >
      <div class="practice-dialog-content">
        <div class="video-section" v-if="showVideo">
          <video ref="localVideo" autoplay muted></video>
        </div>
        <div class="qa-section">
          <div class="current-question">
            <h3>{{ currentQuestion?.question }}</h3>
            <p class="question-tips" v-if="currentQuestion?.tips">
              提示：{{ currentQuestion.tips }}
            </p>
          </div>
          <div class="answer-section">
            <el-input
              type="textarea"
              v-model="currentAnswer"
              :rows="4"
              placeholder="在这里输入你的答案..."
            ></el-input>
          </div>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handlePracticeClose">结束练习</el-button>
        <el-button type="primary" @click="submitAnswer">提交答案</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'InterviewPage',
  setup() {
    // 面试信息
    const upcomingInterview = ref(null)
    const countdown = ref('')
    const canStartInterview = ref(false)
    const activeMaterials = ref(['company'])

    // 练习相关
    const practiceMode = ref('qa')
    const showPracticeDialog = ref(false)
    const showVideo = ref(false)
    const currentQuestion = ref(null)
    const currentAnswer = ref('')
    const showFeedback = ref(false)

    // 公司信息
    const companyInfo = reactive({
      description: '这是一家领先的科技公司...',
      industry: '互联网/人工智能',
      size: '1000-5000人',
      funding: 'D轮'
    })

    // 岗位信息
    const jobInfo = reactive({
      duties: [
        '负责核心业务系统的设计和开发',
        '参与技术方案的讨论和评审',
        '解决系统运行中的技术问题'
      ],
      requirements: [
        '本科及以上学历，计算机相关专业',
        '3年以上相关开发经验',
        '精通Java、Spring Boot等技术栈'
      ]
    })

    // 面试技巧
    const interviewTips = ref([
      {
        title: 'STAR法则',
        content: '使用情境(Situation)、任务(Task)、行动(Action)和结果(Result)来组织你的回答。'
      },
      {
        title: '准备问题',
        content: '准备一些关于公司和职位的问题，展现你的求知欲和热情。'
      }
    ])

    // 练习题目
    const practiceQuestions = ref([
      {
        question: '请介绍一下你自己',
        difficulty: 'easy',
        tips: '可以从教育背景、工作经验、技能特长等方面展开。'
      },
      {
        question: '你为什么选择我们公司？',
        difficulty: 'medium',
        tips: '研究公司背景，结合个人职业发展来回答。'
      }
    ])

    // 情景模拟
    const scenarios = ref([
      {
        title: '处理紧急项目',
        description: '你正在负责一个项目，突然接到一个更紧急的任务，如何处理？'
      },
      {
        title: '团队协作',
        description: '与团队成员意见不一致时，你会如何处理？'
      }
    ])

    // 技术主题
    const technicalTopics = ref([
      {
        label: '编程语言',
        children: [
          { label: 'Java基础' },
          { label: 'Python基础' }
        ]
      },
      {
        label: '数据结构',
        children: [
          { label: '数组和链表' },
          { label: '树和图' }
        ]
      }
    ])

    const defaultProps = {
      children: 'children',
      label: 'label'
    }

    // 反馈数据
    const feedback = reactive({
      overallScore: 4,
      completeness: 85,
      expression: 90,
      comments: '回答结构清晰，论述有理有据。',
      suggestions: [
        '可以多举一些具体的例子',
        '建议控制答题时间在2-3分钟内'
      ]
    })

    // 方法定义
    const startInterview = () => {
      if (!canStartInterview.value) {
        ElMessage.warning('还未到面试时间')
        return
      }
      // 实现进入面试房间的逻辑
    }

    const selectQuestion = (question) => {
      currentQuestion.value = question
      showPracticeDialog.value = true
      if (practiceMode.value === 'qa') {
        initializeVideo()
      }
    }

    const startScenario = (scenario) => {
      currentQuestion.value = {
        question: scenario.description,
        tips: '请详细描述你的处理方案'
      }
      showPracticeDialog.value = true
      initializeVideo()
    }

    const handleTopicClick = (data) => {
      if (!data.children) {
        currentQuestion.value = {
          question: `请详细讲解${data.label}的主要概念和应用`,
          tips: '可以结合实际项目经验来说明'
        }
        showPracticeDialog.value = true
      }
    }

    const initializeVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        showVideo.value = true
        nextTick(() => {
          const video = document.querySelector('video')
          video.srcObject = stream
        })
      } catch (err) {
        console.error('无法访问摄像头:', err)
        ElMessage.error('无法访问摄像头，请检查权限设置')
      }
    }

    const submitAnswer = () => {
      if (!currentAnswer.value) {
        ElMessage.warning('请输入你的答案')
        return
      }
      // 这里可以添加答案分析的逻辑
      showFeedback.value = true
      showPracticeDialog.value = false
      currentAnswer.value = ''
    }

    const handlePracticeClose = () => {
      showPracticeDialog.value = false
      showVideo.value = false
      const video = document.querySelector('video')
      if (video && video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop())
      }
      currentAnswer.value = ''
    }

    // 生命周期钩子
    onMounted(() => {
      // 获取面试信息
      fetchUpcomingInterview()
      // 启动倒计时
      startCountdown()
    })

    onUnmounted(() => {
      // 清理资源
      handlePracticeClose()
    })

    const fetchUpcomingInterview = async () => {
      try {
        const response = await fetch('/api/interview/upcoming')
        if (response.ok) {
          upcomingInterview.value = await response.json()
        }
      } catch (error) {
        console.error('获取面试信息失败:', error)
      }
    }

    const startCountdown = () => {
      // 实现倒计时逻辑
    }

    return {
      upcomingInterview,
      countdown,
      canStartInterview,
      activeMaterials,
      companyInfo,
      jobInfo,
      interviewTips,
      practiceMode,
      practiceQuestions,
      scenarios,
      technicalTopics,
      defaultProps,
      showPracticeDialog,
      showVideo,
      currentQuestion,
      currentAnswer,
      showFeedback,
      feedback,
      startInterview,
      selectQuestion,
      startScenario,
      handleTopicClick,
      submitAnswer,
      handlePracticeClose
    }
  }
}
</script>

<style scoped>
.interview-page {
  padding: 24px;
}

.header {
  margin-bottom: 24px;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.left-panel, .right-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upcoming-interview {
  text-align: center;
  padding: 20px;
}

.company {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
}

.position {
  font-size: 16px;
  color: #666;
  margin-bottom: 16px;
}

.interview-time {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 16px;
}

.countdown {
  font-size: 18px;
  color: #409EFF;
  margin-bottom: 20px;
}

.preparation-materials {
  margin-top: 24px;
}

.company-info, .job-requirements, .interview-tips {
  padding: 16px;
}

.company-details {
  margin-top: 16px;
}

.practice-modes {
  margin-bottom: 24px;
  text-align: center;
}

.question-list, .scenario-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.question-item {
  cursor: pointer;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  transition: all 0.3s;
}

.question-item:hover {
  border-color: #409EFF;
  background-color: #ecf5ff;
}

.question {
  display: flex;
  align-items: center;
  gap: 12px;
}

.question-number {
  font-weight: bold;
  color: #409EFF;
}

.difficulty {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.difficulty.easy {
  background-color: #f0f9eb;
  color: #67c23a;
}

.difficulty.medium {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.difficulty.hard {
  background-color: #fef0f0;
  color: #f56c6c;
}

.practice-dialog-content {
  display: flex;
  gap: 24px;
}

.video-section {
  width: 320px;
}

.video-section video {
  width: 100%;
  border-radius: 8px;
  background-color: #000;
}

.qa-section {
  flex: 1;
}

.current-question {
  margin-bottom: 20px;
}

.question-tips {
  color: #909399;
  font-size: 14px;
  margin-top: 8px;
}

.feedback-content {
  padding: 20px;
}

.score-section {
  margin-bottom: 24px;
}

.score-item {
  margin-bottom: 16px;
}

.score-item .label {
  display: inline-block;
  width: 100px;
  margin-right: 16px;
}

.feedback-details, .improvement-suggestions {
  margin-top: 20px;
}

.improvement-suggestions ul {
  padding-left: 20px;
}

.improvement-suggestions li {
  margin-bottom: 8px;
}
</style>