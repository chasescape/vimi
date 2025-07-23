<template>
  <div class="interview-result">
    <div class="header">
      <h1>面试结果</h1>
    </div>

    <div class="main-content">
      <!-- 基本信息 -->
      <el-card class="basic-info">
        <template #header>
          <div class="card-header">
            <h3>面试基本信息</h3>
            </div>
        </template>
        <div class="info-content">
          <div class="info-item">
            <span class="label">面试岗位</span>
            <span class="value">{{ interviewInfo.position }}</span>
        </div>
                <div class="info-item">
            <span class="label">面试公司</span>
            <span class="value">{{ interviewInfo.company }}</span>
                </div>
                <div class="info-item">
            <span class="label">面试时间</span>
            <span class="value">{{ interviewInfo.time }}</span>
                </div>
                <div class="info-item">
            <span class="label">面试官</span>
            <span class="value">{{ interviewInfo.interviewer }}</span>
                </div>
                <div class="info-item">
            <span class="label">面试结果</span>
            <span class="value" :class="resultClass">{{ interviewInfo.result }}</span>
                </div>
            </div>
      </el-card>

      <!-- 评分详情 -->
      <el-card class="score-details">
        <template #header>
          <div class="card-header">
            <h3>评分详情</h3>
                        </div>
        </template>
        <div class="score-content">
          <div class="score-overview">
            <div class="total-score">
              <span class="score">{{ totalScore }}</span>
              <span class="max">/100</span>
                    </div>
            <div class="score-text">总体评分</div>
                </div>
          <div class="score-breakdown">
            <div v-for="(score, category) in scores" :key="category" class="score-item">
              <div class="score-header">
                <span class="category">{{ category }}</span>
                <span class="points">{{ score.score }}分</span>
                        </div>
              <el-progress 
                :percentage="score.score" 
                :color="score.color"
                :format="() => ''"
              ></el-progress>
              <div class="score-comments">
                <p v-for="(comment, index) in score.comments" :key="index">
                  {{ comment }}
                </p>
                    </div>
                </div>
            </div>
                            </div>
      </el-card>

      <!-- 面试反馈 -->
      <el-card class="interview-feedback">
        <template #header>
          <div class="card-header">
            <h3>面试反馈</h3>
                            </div>
        </template>
                    <div class="feedback-content">
          <!-- 优势分析 -->
          <div class="feedback-section">
            <h4>优势分析</h4>
            <ul class="strength-list">
              <li v-for="(strength, index) in feedback.strengths" :key="index">
                <i class="el-icon-check"></i>
                <span>{{ strength }}</span>
              </li>
                    </ul>
                </div>
                
          <!-- 改进建议 -->
          <div class="feedback-section">
            <h4>改进建议</h4>
            <ul class="improvement-list">
              <li v-for="(improvement, index) in feedback.improvements" :key="index">
                <i class="el-icon-warning"></i>
                <span>{{ improvement }}</span>
              </li>
                    </ul>
                </div>
                
          <!-- 面试官评语 -->
          <div class="feedback-section">
            <h4>面试官评语</h4>
            <div class="interviewer-comments">
              {{ feedback.comments }}
                </div>
                    </div>
                </div>
      </el-card>

      <!-- 下一步建议 -->
      <el-card class="next-steps">
        <template #header>
          <div class="card-header">
            <h3>下一步建议</h3>
            </div>
        </template>
        <div class="next-steps-content">
          <el-timeline>
            <el-timeline-item
              v-for="(step, index) in nextSteps"
              :key="index"
              :type="step.type"
              :color="step.color"
              :size="step.size"
            >
              <h4>{{ step.title }}</h4>
              <p>{{ step.content }}</p>
              <div v-if="step.action" class="step-action">
                <el-button type="primary" size="small" @click="handleStepAction(step)">
                  {{ step.action }}
                </el-button>
        </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'InterviewResult',
  setup() {
    // 面试基本信息
    const interviewInfo = ref({
      position: '高级前端开发工程师',
      company: '科技有限公司',
      time: '2024-03-15 14:00',
      interviewer: '张经理',
      result: '通过'
    })

    // 计算结果样式
    const resultClass = computed(() => {
      const result = interviewInfo.value.result
      return {
        'result-pass': result === '通过',
        'result-fail': result === '未通过',
        'result-pending': result === '待定'
      }
    })

    // 评分详情
    const scores = ref({
      '专业能力': {
        score: 85,
        color: '#67C23A',
        comments: [
          '技术基础扎实，对前端框架理解深入',
          '项目经验丰富，解决问题能力强'
        ]
      },
      '沟通表达': {
        score: 90,
        color: '#409EFF',
        comments: [
          '表达清晰，逻辑性强',
          '能够准确理解问题并给出合适的回答'
        ]
      },
      '学习能力': {
        score: 88,
        color: '#E6A23C',
        comments: [
          '对新技术有浓厚兴趣',
          '具备良好的自学能力'
        ]
      },
      '团队协作': {
        score: 92,
        color: '#909399',
        comments: [
          '有良好的团队合作精神',
          '能够主动承担责任'
        ]
      }
    })

    // 计算总分
    const totalScore = computed(() => {
      const scoreValues = Object.values(scores.value).map(item => item.score)
      return Math.round(scoreValues.reduce((a, b) => a + b, 0) / scoreValues.length)
    })

    // 面试反馈
    const feedback = ref({
      strengths: [
        '技术功底扎实，对前端技术栈有深入理解',
        '项目经验丰富，能够独立负责项目开发',
        '沟通表达清晰，逻辑性强',
        '具有良好的团队协作精神'
      ],
      improvements: [
        '建议深入学习性能优化相关知识',
        '可以加强算法和数据结构的学习',
        '建议多关注前端新技术的发展动态'
      ],
      comments: '候选人整体表现优秀，专业能力和沟通能力都很突出。建议在性能优化和算法方面继续提升，相信会有更好的发展。'
    })

    // 下一步建议
    const nextSteps = ref([
      {
        title: '完善个人信息',
        content: '请及时更新您的个人信息和联系方式，确保HR能够及时联系您。',
        type: 'primary',
        color: '#409EFF',
        size: 'large',
        action: '去完善'
      },
      {
        title: '等待offer',
        content: 'HR将在3个工作日内联系您，请保持手机畅通。',
        type: 'warning',
        color: '#E6A23C'
      },
      {
        title: '准备入职',
        content: '如果顺利通过，请准备好相关证件，以便办理入职手续。',
        type: 'success',
        color: '#67C23A'
      }
    ])

    // 处理步骤操作
    const handleStepAction = (step) => {
      if (step.title === '完善个人信息') {
        // 跳转到个人信息页面
      }
    }

    return {
      interviewInfo,
      resultClass,
      scores,
      totalScore,
      feedback,
      nextSteps,
      handleStepAction
    }
  }
}
</script>

<style scoped>
.interview-result {
  padding: 24px;
}

.header {
  margin-bottom: 24px;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 1200px;
            margin: 0 auto;
}

.card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
/* 基本信息样式 */
.info-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
            display: flex;
            align-items: center;
}

.info-item .label {
  width: 100px;
  color: #909399;
}

.info-item .value {
            font-weight: 500;
        }
        
.result-pass {
  color: #67C23A;
}

.result-fail {
  color: #F56C6C;
}

.result-pending {
  color: #E6A23C;
}

/* 评分详情样式 */
.score-content {
  display: flex;
            gap: 40px;
        }
        
.score-overview {
  text-align: center;
            padding: 20px;
  border-right: 1px solid #EBEEF5;
}

.total-score {
  font-size: 48px;
  font-weight: bold;
  color: #409EFF;
}

.total-score .max {
  font-size: 24px;
  color: #909399;
}

.score-text {
  color: #606266;
  margin-top: 8px;
}

.score-breakdown {
  flex: 1;
}

.score-item {
  margin-bottom: 24px;
}

.score-header {
            display: flex;
            justify-content: space-between;
  margin-bottom: 8px;
}

.category {
  font-weight: 500;
}

.points {
  color: #409EFF;
}

.score-comments {
  margin-top: 8px;
  color: #606266;
  font-size: 14px;
}

/* 面试反馈样式 */
.feedback-section {
  margin-bottom: 24px;
}

.feedback-section h4 {
  margin-bottom: 16px;
  font-weight: 500;
}

.strength-list,
.improvement-list {
  list-style: none;
  padding: 0;
}

.strength-list li,
.improvement-list li {
            display: flex;
            align-items: flex-start;
  margin-bottom: 12px;
}

.strength-list i {
  color: #67C23A;
  margin-right: 8px;
  margin-top: 4px;
}

.improvement-list i {
  color: #E6A23C;
  margin-right: 8px;
  margin-top: 4px;
}

.interviewer-comments {
  padding: 16px;
  background: #F5F7FA;
  border-radius: 4px;
  line-height: 1.6;
}

/* 下一步建议样式 */
.next-steps-content {
            padding: 20px;
}

.step-action {
  margin-top: 12px;
}

/* 响应式调整 */
        @media (max-width: 768px) {
  .score-content {
                flex-direction: column;
  }

  .score-overview {
    border-right: none;
    border-bottom: 1px solid #EBEEF5;
            margin-bottom: 20px;
  }
        }
</style> 
 