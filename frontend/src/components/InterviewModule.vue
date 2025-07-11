<template>
  <div class="interview-module">
    <div class="tech-background">
      <div class="tech-circle circle-1"></div>
      <div class="tech-circle circle-2"></div>
      <div class="tech-circle circle-3"></div>
    </div>
    
    <h2 class="tech-title">
      <span class="title-text">面试中心</span>
      <span class="title-glow"></span>
    </h2>
    
    <div class="interview-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
        class="tech-tab"
      >
        <span class="tab-icon" :class="tab.icon"></span>
        <span class="tab-label">{{ tab.label }}</span>
        <span class="tab-glow"></span>
      </button>
    </div>
    
    <!-- 即将面试 -->
    <transition name="fade-slide" mode="out-in">
      <div class="upcoming-interviews tech-panel" v-if="activeTab === 'upcoming'">
        <div class="panel-header">
          <h3>即将开始的面试</h3>
          <div class="panel-actions">
            <button class="tech-button small" @click="syncCalendar">
              <i class="fas fa-sync-alt"></i> 同步日历
            </button>
          </div>
        </div>
        
        <div class="interview-list">
          <div 
            class="interview-item tech-card" 
            v-for="interview in upcomingInterviews" 
            :key="interview.id"
            :style="{'--card-accent': interview.cardColor}"
          >
            <div class="card-decoration"></div>
            <div class="interview-info">
              <div class="info-header">
                <h3>{{ interview.position }}</h3>
                <div class="company-badge">
                  <i class="fas fa-building"></i>
                  <span>{{ interview.company }}</span>
                </div>
              </div>
              
              <div class="info-details">
                <div class="detail-item">
                  <i class="fas fa-calendar-alt"></i>
                  <span>{{ interview.date }} {{ interview.time }}</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-clock"></i>
                  <span>{{ interview.duration }}分钟</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-user-tie"></i>
                  <span>{{ interview.interviewer || '待确认' }}</span>
                </div>
              </div>
              
              <div class="info-status">
                <div class="status-badge" :class="interview.status">
                  <span>{{ interview.status === 'scheduled' ? '已确认' : '待确认' }}</span>
                </div>
                <div class="countdown" v-if="interview.status === 'scheduled'">
                  <i class="fas fa-hourglass-half"></i>
                  <span>倒计时: {{ interview.countdown }}</span>
                </div>
              </div>
            </div>
            
            <div class="interview-actions">
              <div class="action-buttons">
                <button class="tech-button primary" @click="joinInterview(interview.id)">
                  <i class="fas fa-video"></i> 进入面试
                </button>
                <button class="tech-button secondary" @click="showInterviewPrep(interview.id)">
                  <i class="fas fa-clipboard-list"></i> 准备清单
                </button>
              </div>
              <div class="action-buttons">
                <button class="tech-button warning" @click="rescheduleInterview(interview.id)">
                  <i class="fas fa-calendar-plus"></i> 改期
                </button>
                <button class="tech-button danger" @click="cancelInterview(interview.id)">
                  <i class="fas fa-times"></i> 取消
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="empty-state" v-if="upcomingInterviews.length === 0">
          <div class="empty-icon">
            <i class="fas fa-calendar-times"></i>
          </div>
          <h4>暂无即将开始的面试</h4>
          <p>准备好寻找新的机会了吗？</p>
          <button class="tech-button primary" @click="$emit('change-tab', 'jobs')">
            <i class="fas fa-search"></i> 浏览职位
          </button>
        </div>
      </div>
    </transition>
    
    <!-- 已完成面试 -->
    <transition name="fade-slide" mode="out-in">
      <div class="completed-interviews tech-panel" v-if="activeTab === 'completed'">
        <div class="panel-header">
          <h3>面试记录</h3>
          <div class="panel-actions">
            <div class="tech-select">
              <select v-model="completedFilter">
                <option value="all">全部</option>
                <option value="passed">通过</option>
                <option value="failed">未通过</option>
                <option value="pending">待定</option>
              </select>
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>
        </div>
        
        <div class="interview-list">
          <div 
            class="interview-item tech-card" 
            v-for="interview in filteredCompletedInterviews" 
            :key="interview.id"
            :style="{'--card-accent': interview.cardColor}"
          >
            <div class="card-decoration"></div>
            <div class="interview-info">
              <div class="info-header">
                <h3>{{ interview.position }}</h3>
                <div class="company-badge">
                  <i class="fas fa-building"></i>
                  <span>{{ interview.company }}</span>
                </div>
              </div>
              
              <div class="info-details">
                <div class="detail-item">
                  <i class="fas fa-calendar-alt"></i>
                  <span>{{ interview.date }} {{ interview.time }}</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-clock"></i>
                  <span>{{ interview.duration }}分钟</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-user-tie"></i>
                  <span>{{ interview.interviewer }}</span>
                </div>
              </div>
              
              <div class="info-result">
                <div class="result-score">
                  <div class="score-circle" :style="{'--score': interview.score/100}">
                    <span>{{ interview.score }}</span>
                  </div>
                  <div class="score-label">
                    <span>综合评分</span>
                    <span class="result-status" :class="interview.result">
                      {{ getResultText(interview.result) }}
                    </span>
                  </div>
                </div>
                <div class="result-tags">
                  <span class="tech-tag" v-for="tag in interview.tags" :key="tag">{{ tag }}</span>
                </div>
              </div>
            </div>
            
            <div class="interview-actions">
              <button class="tech-button primary" @click="reviewInterview(interview.id)">
                <i class="fas fa-play-circle"></i> 回放
              </button>
              <button class="tech-button secondary" @click="showAnalysis(interview.id)">
                <i class="fas fa-chart-line"></i> 分析
              </button>
              <button class="tech-button" @click="viewFeedback(interview.id)">
                <i class="fas fa-comment-dots"></i> 反馈
              </button>
              <button class="tech-button" @click="downloadReport(interview.id)">
                <i class="fas fa-download"></i> 报告
              </button>
            </div>
          </div>
        </div>
        
        <div class="empty-state" v-if="filteredCompletedInterviews.length === 0">
          <div class="empty-icon">
            <i class="fas fa-history"></i>
          </div>
          <h4>暂无面试记录</h4>
          <p>完成面试后，您可以在这里查看详细记录和分析</p>
        </div>
      </div>
    </transition>
    
    <!-- AI模拟练习 -->
    <transition name="fade-slide" mode="out-in">
      <div class="ai-practice tech-panel" v-if="activeTab === 'practice'">
        <div class="practice-header">
          <h3>AI模拟面试训练</h3>
          <p>通过AI模拟真实面试场景，提前练习面试技巧，提高正式面试成功率</p>
        </div>
        
        <div class="practice-stats">
          <div class="stat-card">
            <div class="stat-value">{{ practiceStats.totalSessions }}</div>
            <div class="stat-label">总练习次数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ practiceStats.avgScore }}</div>
            <div class="stat-label">平均得分</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ practiceStats.improvement }}%</div>
            <div class="stat-label">进步率</div>
          </div>
        </div>
        
        <div class="practice-options">
          <div 
            class="option-card tech-card" 
            v-for="option in practiceOptions" 
            :key="option.id"
            :style="{'--card-accent': option.color}"
            @click="startPractice(option.id)"
          >
            <div class="card-decoration"></div>
            <div class="option-icon">
              <i :class="option.icon"></i>
            </div>
            <h4>{{ option.title }}</h4>
            <p>{{ option.description }}</p>
            <div class="option-progress">
              <div class="progress-bar" :style="{width: `${option.progress}%`}"></div>
              <span>完成度: {{ option.progress }}%</span>
            </div>
            <button class="tech-button primary">
              开始练习 <i class="fas fa-arrow-right"></i>
            </button>
          </div>
        </div>
        
        <div class="practice-history">
          <h4>最近练习记录</h4>
          <div class="history-list">
            <div class="history-item" v-for="item in practiceHistory" :key="item.id">
              <div class="history-type">{{ item.type }}</div>
              <div class="history-date">{{ item.date }}</div>
              <div class="history-score" :class="getScoreClass(item.score)">
                {{ item.score }}分
              </div>
              <button class="tech-button small" @click="reviewPractice(item.id)">
                <i class="fas fa-eye"></i> 查看
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
    
    <!-- 面试准备清单模态框 -->
    <transition name="modal">
      <div class="tech-modal" v-if="showPrepModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>面试准备清单</h3>
            <button class="modal-close" @click="showPrepModal = false">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="prep-checklist">
              <div class="checklist-header">
                <h4>{{ currentInterview.position }} @ {{ currentInterview.company }}</h4>
                <div class="interview-time">
                  <i class="fas fa-calendar-alt"></i>
                  <span>{{ currentInterview.date }} {{ currentInterview.time }}</span>
                </div>
              </div>
              
              <div class="checklist-section">
                <h5><i class="fas fa-laptop"></i> 技术准备</h5>
                <div class="checklist-items">
                  <label class="check-item" v-for="item in techPrepItems" :key="item.id">
                    <input type="checkbox" v-model="item.checked">
                    <span class="checkmark"></span>
                    <span class="check-text">{{ item.text }}</span>
                  </label>
                </div>
              </div>
              
              <div class="checklist-section">
                <h5><i class="fas fa-comments"></i> 问题准备</h5>
                <div class="checklist-items">
                  <label class="check-item" v-for="item in questionPrepItems" :key="item.id">
                    <input type="checkbox" v-model="item.checked">
                    <span class="checkmark"></span>
                    <span class="check-text">{{ item.text }}</span>
                  </label>
                </div>
                <button class="tech-button small" @click="addCustomQuestion">
                  <i class="fas fa-plus"></i> 添加自定义问题
                </button>
              </div>
              
              <div class="checklist-section">
                <h5><i class="fas fa-check-circle"></i> 其他准备</h5>
                <div class="checklist-items">
                  <label class="check-item" v-for="item in otherPrepItems" :key="item.id">
                    <input type="checkbox" v-model="item.checked">
                    <span class="checkmark"></span>
                    <span class="check-text">{{ item.text }}</span>
                  </label>
                </div>
              </div>
              
              <div class="checklist-progress">
                <div class="progress-bar" :style="{width: `${prepProgress}%`}"></div>
                <div class="progress-text">准备完成度: {{ prepProgress }}%</div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="tech-button" @click="showPrepModal = false">
              关闭
            </button>
            <button class="tech-button primary" @click="savePrepList">
              <i class="fas fa-save"></i> 保存
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    <!-- 面试分析模态框 -->
    <transition name="modal">
      <div class="tech-modal" v-if="showAnalysisModal">
        <div class="modal-content large">
          <div class="modal-header">
            <h3>面试分析报告</h3>
            <div class="modal-subtitle">
              {{ currentInterview.position }} @ {{ currentInterview.company }}
            </div>
            <button class="modal-close" @click="showAnalysisModal = false">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="analysis-tabs">
              <button 
                v-for="tab in analysisTabs" 
                :key="tab.id"
                :class="{ active: activeAnalysisTab === tab.id }"
                @click="activeAnalysisTab = tab.id"
                class="tech-tab"
              >
                <span class="tab-icon" :class="tab.icon"></span>
                <span class="tab-label">{{ tab.label }}</span>
              </button>
            </div>
            
            <transition name="fade-slide" mode="out-in">
              <div class="analysis-content" v-if="activeAnalysisTab === 'metrics'">
                <div class="metrics-overview">
                  <div class="overview-card">
                    <div class="overview-score">
                      <div class="score-circle large" :style="{'--score': currentInterview.score/100}">
                        <span>{{ currentInterview.score }}</span>
                      </div>
                      <div class="score-label">
                        <div class="label-main">综合评分</div>
                        <div class="label-sub">满分100分</div>
                      </div>
                    </div>
                    <div class="overview-comment">
                      <div class="comment-title">AI评价</div>
                      <div class="comment-text">{{ analysisData.overallComment }}</div>
                    </div>
                  </div>
                  
                  <div class="metrics-grid">
                    <div class="metric-card" v-for="metric in analysisData.metrics" :key="metric.id">
                      <div class="metric-value">{{ metric.value }}</div>
                      <div class="metric-label">{{ metric.label }}</div>
                      <div class="metric-bar">
                        <div class="bar-fill" :style="{width: `${metric.value}%`}"></div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="radar-chart-container">
                  <div class="chart-container">
                    <canvas ref="radarChart"></canvas>
                  </div>
                  <div class="chart-legend">
                    <div class="legend-item" v-for="item in radarData.labels" :key="item">
                      <span class="legend-color" :style="{backgroundColor: radarData.colors[radarData.labels.indexOf(item)]}"></span>
                      <span class="legend-text">{{ item }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
            
            <transition name="fade-slide" mode="out-in">
              <div class="analysis-content" v-if="activeAnalysisTab === 'emotion'">
                <div class="emotion-overview">
                  <div class="emotion-stats">
                    <div class="stat-card" v-for="stat in emotionStats" :key="stat.type">
                      <div class="stat-value">{{ stat.value }}%</div>
                      <div class="stat-label">{{ stat.label }}</div>
                      <div class="stat-bar">
                        <div class="bar-fill" :style="{width: `${stat.value}%`, backgroundColor: stat.color}"></div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="emotion-timeline">
                    <div class="timeline-chart">
                      <canvas ref="emotionChart"></canvas>
                    </div>
                    <div class="timeline-keymoments">
                      <div class="keymoment" v-for="moment in keyMoments" :key="moment.time">
                        <div class="moment-time">{{ moment.time }}</div>
                        <div class="moment-text">{{ moment.text }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="emotion-comments">
                  <div class="comment-card">
                    <div class="comment-title">
                      <i class="fas fa-smile" style="color: #4CAF50;"></i>
                      <span>最佳表现时刻</span>
                    </div>
                    <div class="comment-text">{{ analysisData.bestMoment }}</div>
                  </div>
                  <div class="comment-card">
                    <div class="comment-title">
                      <i class="fas fa-frown" style="color: #F44336;"></i>
                      <span>有待改进时刻</span>
                    </div>
                    <div class="comment-text">{{ analysisData.improveMoment }}</div>
                  </div>
                </div>
              </div>
            </transition>
            
            <transition name="fade-slide" mode="out-in">
              <div class="analysis-content" v-if="activeAnalysisTab === 'feedback'">
                <div class="feedback-strengths">
                  <div class="feedback-header">
                    <i class="fas fa-check-circle"></i>
                    <h4>优势表现</h4>
                  </div>
                  <ul class="feedback-list">
                    <li v-for="(item, index) in analysisData.strengths" :key="index">
                      <i class="fas fa-thumbs-up"></i>
                      <span>{{ item }}</span>
                    </li>
                  </ul>
                </div>
                
                <div class="feedback-improvements">
                  <div class="feedback-header">
                    <i class="fas fa-exclamation-circle"></i>
                    <h4>改进建议</h4>
                  </div>
                  <ul class="feedback-list">
                    <li v-for="(item, index) in analysisData.improvements" :key="index">
                      <i class="fas fa-lightbulb"></i>
                      <span>{{ item }}</span>
                    </li>
                  </ul>
                </div>
                
                <div class="feedback-questions">
                  <div class="feedback-header">
                    <i class="fas fa-question-circle"></i>
                    <h4>问题回答分析</h4>
                  </div>
                  <div class="question-list">
                    <div class="question-item" v-for="question in analysisData.questions" :key="question.id">
                      <div class="question-text">
                        <span class="question-label">问题:</span>
                        <span>{{ question.text }}</span>
                      </div>
                      <div class="question-rating">
                        <div class="rating-stars">
                          <i 
                            class="fas fa-star" 
                            v-for="n in 5" 
                            :key="n" 
                            :class="{filled: n <= question.rating}"
                          ></i>
                        </div>
                        <span class="rating-label">{{ getRatingText(question.rating) }}</span>
                      </div>
                      <div class="question-feedback">
                        <span class="feedback-label">反馈:</span>
                        <span>{{ question.feedback }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
            
            <transition name="fade-slide" mode="out-in">
              <div class="analysis-content" v-if="activeAnalysisTab === 'resources'">
                <div class="resources-header">
                  <h4>基于您的面试表现推荐的学习资源</h4>
                  <p>这些资源将帮助您改进面试中发现的薄弱环节</p>
                </div>
                
                <div class="resources-list">
                  <div class="resource-card" v-for="resource in analysisData.resources" :key="resource.id">
                    <div class="resource-type" :class="resource.type">
                      <i :class="resource.icon"></i>
                      <span>{{ resource.typeText }}</span>
                    </div>
                    <div class="resource-content">
                      <h5>{{ resource.title }}</h5>
                      <p>{{ resource.description }}</p>
                      <div class="resource-meta">
                        <span class="meta-item">
                          <i class="fas fa-clock"></i>
                          <span>{{ resource.duration }}</span>
                        </span>
                        <span class="meta-item">
                          <i class="fas fa-tag"></i>
                          <span>{{ resource.tags.join(', ') }}</span>
                        </span>
                      </div>
                    </div>
                    <button class="tech-button small">
                      <i class="fas fa-external-link-alt"></i> 查看
                    </button>
                  </div>
                </div>
              </div>
            </transition>
          </div>
          <div class="modal-footer">
            <button class="tech-button" @click="showAnalysisModal = false">
              关闭
            </button>
            <button class="tech-button primary" @click="downloadReport(currentInterview.id)">
              <i class="fas fa-download"></i> 下载完整报告
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

const activeTab = ref('upcoming')
const showPrepModal = ref(false)
const showAnalysisModal = ref(false)
const activeAnalysisTab = ref('metrics')
const completedFilter = ref('all')
const radarChart = ref(null)
const emotionChart = ref(null)

const tabs = [
  { id: 'upcoming', label: '即将面试', icon: 'fas fa-calendar-check' },
  { id: 'completed', label: '面试记录', icon: 'fas fa-history' },
  { id: 'practice', label: 'AI模拟', icon: 'fas fa-robot' }
]

const analysisTabs = [
  { id: 'metrics', label: '综合指标', icon: 'fas fa-chart-bar' },
  { id: 'emotion', label: '情绪分析', icon: 'fas fa-smile' },
  { id: 'feedback', label: '反馈建议', icon: 'fas fa-comment-alt' },
  { id: 'resources', label: '学习资源', icon: 'fas fa-book-open' }
]

const upcomingInterviews = ref([
  {
    id: 1,
    position: '高级前端开发工程师',
    company: 'ABC科技有限公司',
    date: '2023-11-15',
    time: '14:30',
    duration: 60,
    status: 'scheduled',
    countdown: '2天3小时',
    interviewer: '张经理 (技术主管)',
    cardColor: '#6366f1',
    preparation: {
      techChecked: [1, 2, 4],
      questionChecked: [1, 3],
      otherChecked: [1, 2]
    }
  },
  {
    id: 2,
    position: 'UI/UX设计师',
    company: 'XYZ设计公司',
    date: '2023-11-18',
    time: '10:00',
    duration: 45,
    status: 'pending',
    countdown: '5天1小时',
    interviewer: '',
    cardColor: '#ec4899',
    preparation: {
      techChecked: [],
      questionChecked: [],
      otherChecked: []
    }
  }
])

const completedInterviews = ref([
  {
    id: 3,
    position: '产品经理',
    company: 'DEF互联网',
    date: '2023-10-28',
    time: '09:30',
    duration: 90,
    score: 85,
    result: 'passed',
    interviewer: '李总监 (产品部)',
    cardColor: '#14b8a6',
    tags: ['沟通能力强', '产品思维好', '需加强技术理解'],
    analysis: {
      overallComment: '整体表现优秀，产品思维清晰，沟通表达能力强，对技术实现有一定理解但可以更深入。'
    }
  },
  {
    id: 4,
    position: '全栈工程师',
    company: 'GHI科技',
    date: '2023-10-15',
    time: '15:00',
    duration: 120,
    score: 72,
    result: 'pending',
    interviewer: '王CTO',
    cardColor: '#f97316',
    tags: ['技术扎实', '架构思维好', '表达需提升'],
    analysis: {
      overallComment: '技术能力扎实，系统设计能力强，但在表达复杂技术概念时不够清晰，需要提高沟通效率。'
    }
  },
  {
    id: 5,
    position: '数据分析师',
    company: 'JKL数据',
    date: '2023-09-20',
    time: '13:30',
    duration: 60,
    score: 68,
    result: 'failed',
    interviewer: '赵经理 (数据分析部)',
    cardColor: '#8b5cf6',
    tags: ['统计基础好', '业务理解不足', '可视化能力一般'],
    analysis: {
      overallComment: '统计学基础扎实，但对业务场景理解不够深入，数据可视化表达能力有待提高。'
    }
  }
])

const filteredCompletedInterviews = computed(() => {
  if (completedFilter.value === 'all') return completedInterviews.value
  return completedInterviews.value.filter(i => i.result === completedFilter.value)
})

const practiceOptions = [
  {
    id: 1,
    title: '技术岗位模拟',
    description: '针对技术岗位的常见问题和技术考察',
    icon: 'fas fa-code',
    color: '#6366f1',
    progress: 65
  },
  {
    id: 2,
    title: '行为面试模拟',
    description: '考察沟通能力、团队协作等软技能',
    icon: 'fas fa-users',
    color: '#ec4899',
    progress: 40
  },
  {
    id: 3,
    title: '压力面试模拟',
    description: '模拟高压环境下的表现和应变能力',
    icon: 'fas fa-fire',
    color: '#f97316',
    progress: 25
  },
  {
    id: 4,
    title: '高管面试模拟',
    description: '针对高级职位的战略思维和领导力考察',
    icon: 'fas fa-user-tie',
    color: '#14b8a6',
    progress: 10
  }
]

const practiceStats = {
  totalSessions: 12,
  avgScore: 76,
  improvement: 22
}

const practiceHistory = [
  { id: 1, type: '技术模拟', date: '2023-11-10', score: 82 },
  { id: 2, type: '行为模拟', date: '2023-11-08', score: 75 },
  { id: 3, type: '压力模拟', date: '2023-11-05', score: 68 },
  { id: 4, type: '技术模拟', date: '2023-11-02', score: 79 }
]

const techPrepItems = [
  { id: 1, text: '复习岗位要求的技术栈', checked: false },
  { id: 2, text: '准备项目经验介绍', checked: false },
  { id: 3, text: '练习编码题/设计题', checked: false },
  { id: 4, text: '了解公司技术栈和产品', checked: false },
  { id: 5, text: '准备技术问题提问', checked: false }
]

const questionPrepItems = [
  { id: 1, text: '自我介绍(1-2分钟版本)', checked: false },
  { id: 2, text: '职业规划和发展目标', checked: false },
  { id: 3, text: '项目经验中的挑战和解决方案', checked: false },
  { id: 4, text: '离职原因/求职动机', checked: false },
  { id: 5, text: '薪资期望和考虑因素', checked: false }
]

const otherPrepItems = [
  { id: 1, text: '测试面试设备和网络', checked: false },
  { id: 2, text: '准备安静、整洁的面试环境', checked: false },
  { id: 3, text: '准备纸笔做记录', checked: false },
  { id: 4, text: '提前10分钟进入面试间', checked: false },
  { id: 5, text: '穿着得体(即使是线上面试)', checked: false }
]

const prepProgress = computed(() => {
  const totalItems = [...techPrepItems, ...questionPrepItems, ...otherPrepItems].length
  const checkedItems = [
    ...techPrepItems.filter(i => i.checked),
    ...questionPrepItems.filter(i => i.checked),
    ...otherPrepItems.filter(i => i.checked)
  ].length
  return Math.round((checkedItems / totalItems) * 100)
})

const currentInterview = ref({})
const analysisData = ref({})
const radarData = ref({})
const emotionStats = ref([])
const keyMoments = ref([])

onMounted(() => {
  initAnalysisData()
})

const initAnalysisData = () => {
  analysisData.value = {
    overallComment: '整体表现良好，技术能力扎实，沟通表达清晰，但在某些复杂问题的深入探讨上可以更详细。',
    metrics: [
      { id: 1, label: '技术能力', value: 92 },
      { id: 2, label: '沟通表达', value: 78 },
      { id: 3, label: '问题解决', value: 85 },
      { id: 4, label: '岗位匹配', value: 89 },
      { id: 5, label: '文化契合', value: 76 }
    ],
    strengths: [
      '技术问题回答准确率高',
      '表达清晰有条理',
      '对行业有深入理解',
      '项目经验与岗位匹配度高',
      '问题思考全面'
    ],
    improvements: [
      '可以更详细地阐述项目经验',
      '注意控制语速，避免过快',
      '可以多提一些有深度的问题',
      '技术细节可以更深入',
      '展示更多主动性'
    ],
    questions: [
      {
        id: 1,
        text: '请介绍您最复杂的项目经验以及遇到的挑战',
        rating: 4,
        feedback: '回答全面，项目复杂度展示充分，但可以更详细说明具体的技术挑战和解决方案。'
      },
      {
        id: 2,
        text: '如何处理与团队成员的技术分歧?',
        rating: 3,
        feedback: '回答体现了团队合作精神，但可以补充具体案例和最终达成的技术决策。'
      },
      {
        id: 3,
        text: '您如何看待我们产品的技术架构?',
        rating: 5,
        feedback: '回答展现了深入的技术理解和独特的见解，非常出色。'
      }
    ],
    resources: [
      {
        id: 1,
        type: 'course',
        typeText: '在线课程',
        icon: 'fas fa-video',
        title: '高级系统设计面试指南',
        description: '深入讲解大型系统设计面试的要点和常见问题解决方案',
        duration: '4小时',
        tags: ['系统设计', '面试', '架构']
      },
      {
        id: 2,
        type: 'article',
        typeText: '技术文章',
        icon: 'fas fa-book',
        title: '如何清晰表达复杂技术概念',
        description: '工程师沟通技巧：如何向非技术人员解释技术问题',
        duration: '15分钟阅读',
        tags: ['沟通', '技术表达']
      },
      {
        id: 3,
        type: 'book',
        typeText: '电子书',
        icon: 'fas fa-book-open',
        title: '技术面试完整指南2023',
        description: '涵盖最新技术面试趋势和准备策略的全面指南',
        duration: '300页',
        tags: ['面试', '准备', '技术']
      }
    ],
    bestMoment: '在讨论项目架构时展现了清晰的思维和深入的技术理解，表达流畅自信。',
    improveMoment: '回答行为问题时稍显紧张，语速加快，可以更从容地组织语言。'
  }

  radarData.value = {
    labels: ['技术能力', '沟通表达', '问题解决', '岗位匹配', '文化契合', '学习能力'],
    datasets: [{
      data: [92, 78, 85, 89, 76, 88],
      backgroundColor: 'rgba(99, 102, 241, 0.2)',
      borderColor: 'rgba(99, 102, 241, 1)',
      pointBackgroundColor: 'rgba(99, 102, 241, 1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(99, 102, 241, 1)'
    }],
    colors: ['#6366f1', '#ec4899', '#f97316', '#14b8a6', '#8b5cf6', '#10b981']
  }

  emotionStats.value = [
    { type: 'positive', label: '积极情绪', value: 72, color: '#4CAF50' },
    { type: 'neutral', label: '中性情绪', value: 18, color: '#2196F3' },
    { type: 'negative', label: '消极情绪', value: 10, color: '#F44336' }
  ]

  keyMoments.value = [
    { time: '00:05:23', text: '自我介绍时表现自信，语气积极' },
    { time: '00:12:45', text: '讨论技术问题时专注且专业' },
    { time: '00:25:30', text: '遇到难题时稍显紧张，语速加快' },
    { time: '00:38:12', text: '分享项目经验时热情高涨' },
    { time: '00:52:40', text: '提问环节表现主动且有见地' }
  ]
}

watch(showAnalysisModal, (val) => {
  if (val) {
    nextTick(() => {
      createRadarChart()
      createEmotionChart()
    })
  }
})

const createRadarChart = () => {
  if (radarChart.value) {
    const ctx = radarChart.value.getContext('2d')
    new Chart(ctx, {
      type: 'radar',
      data: {
        labels: radarData.value.labels,
        datasets: radarData.value.datasets
      },
      options: {
        responsive: true,
        scales: {
          r: {
            angleLines: {
              display: true,
              color: 'rgba(255, 255, 255, 0.1)'
            },
            suggestedMin: 0,
            suggestedMax: 100,
            ticks: {
              backdropColor: 'transparent',
              color: '#fff',
              font: {
                family: "'Inter', sans-serif"
              }
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            pointLabels: {
              color: '#fff',
              font: {
                family: "'Inter', sans-serif",
                size: 12
              }
            }
          }
        },
        plugins: {
          legend: {
            display: false
          }
        },
        elements: {
          line: {
            borderWidth: 2
          }
        }
      }
    })
  }
}

const createEmotionChart = () => {
  if (emotionChart.value) {
    const ctx = emotionChart.value.getContext('2d')
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30', '00:35', '00:40', '00:45', '00:50', '00:55'],
        datasets: [
          {
            label: '情绪指数',
            data: [65, 59, 80, 81, 56, 55, 70, 75, 82, 78, 85, 90],
            fill: true,
            backgroundColor: 'rgba(99, 102, 241, 0.2)',
            borderColor: 'rgba(99, 102, 241, 1)',
            tension: 0.4,
            pointBackgroundColor: 'rgba(99, 102, 241, 1)',
            pointBorderColor: '#fff',
            pointRadius: 5,
            pointHoverRadius: 7
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              color: '#fff'
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          },
          x: {
            ticks: {
              color: '#fff'
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#fff',
            bodyColor: '#fff',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1
          }
        }
      }
    })
  }
}

const joinInterview = (id) => {
  console.log('加入面试:', id)
}

const cancelInterview = (id) => {
  console.log('取消面试:', id)
}

const rescheduleInterview = (id) => {
  console.log('改期面试:', id)
}

const reviewInterview = (id) => {
  console.log('回放面试:', id)
}

const showInterviewPrep = (id) => {
  currentInterview.value = upcomingInterviews.value.find(i => i.id === id)
  // 加载已保存的准备清单状态
  techPrepItems.forEach(item => {
    item.checked = currentInterview.value.preparation.techChecked.includes(item.id)
  })
  questionPrepItems.forEach(item => {
    item.checked = currentInterview.value.preparation.questionChecked.includes(item.id)
  })
  otherPrepItems.forEach(item => {
    item.checked = currentInterview.value.preparation.otherChecked.includes(item.id)
  })
  showPrepModal.value = true
}

const savePrepList = () => {
  // 保存准备清单状态
  currentInterview.value.preparation.techChecked = techPrepItems.filter(i => i.checked).map(i => i.id)
  currentInterview.value.preparation.questionChecked = questionPrepItems.filter(i => i.checked).map(i => i.id)
  currentInterview.value.preparation.otherChecked = otherPrepItems.filter(i => i.checked).map(i => i.id)
  showPrepModal.value = false
}

const addCustomQuestion = () => {
  const newId = Math.max(...questionPrepItems.map(i => i.id)) + 1
  questionPrepItems.push({
    id: newId,
    text: '自定义问题 (点击编辑)',
    checked: false
  })
}

const showAnalysis = (id) => {
  currentInterview.value = completedInterviews.value.find(i => i.id === id)
  showAnalysisModal.value = true
  activeAnalysisTab.value = 'metrics'
}

const viewFeedback = (id) => {
  currentInterview.value = completedInterviews.value.find(i => i.id === id)
  showAnalysisModal.value = true
  activeAnalysisTab.value = 'feedback'
}

const downloadReport = (id) => {
  console.log('下载报告:', id)
}

const startPractice = (id) => {
  console.log('开始练习:', id)
}

const reviewPractice = (id) => {
  console.log('回放练习:', id)
}

const syncCalendar = () => {
  console.log('同步日历')
}

const getResultText = (result) => {
  return result === 'passed' ? '通过' : result === 'pending' ? '待定' : '未通过'
}

const getScoreClass = (score) => {
  if (score >= 85) return 'excellent'
  if (score >= 70) return 'good'
  if (score >= 60) return 'average'
  return 'poor'
}

const getRatingText = (rating) => {
  const texts = ['需改进', '一般', '良好', '优秀', '非常出色']
  return texts[rating - 1] || ''
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.interview-module {
  position: relative;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
  color: #fff;
  overflow: hidden;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}
.tech-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  background: 
    /* 网格背景 */
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 30px 30px;
}

/* 网格背景叠加 */
.tech-background::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: 0;
}
.tech-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.15;
}
.circle-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(45deg, #4ade80, #60a5fa);
  top: -100px;
  left: -100px;
}

.circle-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(45deg, #818cf8, #ec4899);
  bottom: -150px;
  right: -100px;
}

.circle-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(45deg, #f97316, #f43f5e);
  top: 50%;
  left: 70%;
}

.tech-title {
  position: relative;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  display: inline-block;
}

.title-text {
  position: relative;
  z-index: 1;
  background: linear-gradient(90deg, #fff 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;

  margin-left: 2rem;
  margin-top: 6rem;      /* 👈 原来是5rem，稍微再高一点 */
  font-size: 2.8rem;     /* 👈 加大字体，默认一般是1~2rem */
  font-weight: 700;      /* 👈 可选：加粗一点更有标题感 */
  line-height: 1.2;      /* 👈 避免字太挤 */
}

.title-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #6366f1 0%, #a5b4fc 100%);
  filter: blur(20px);
  opacity: 0.3;
  z-index: 0;
}

.interview-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
   margin-left: 6rem;
}

.tech-tab {
  position: relative;
  padding: 0.75rem 1.5rem;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  color: #94a3b8;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  z-index: 1;
  overflow: hidden;
}

.tech-tab::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(99, 102, 241, 0.2) 0%, rgba(99, 102, 241, 0) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tech-tab:hover {
  color: #e2e8f0;
  border-color: rgba(99, 102, 241, 0.5);
}

.tech-tab:hover::before {
  opacity: 1;
}

.tech-tab.active {
  background: rgba(99, 102, 241, 0.2);
  color: #e2e8f0;
  border-color: rgba(99, 102, 241, 0.5);
}

.tech-tab.active .tab-icon {
  color: #818cf8;
}

.tech-tab.active::before {
  opacity: 1;
}

.tab-icon {
  font-size: 1rem;
  transition: color 0.3s ease;
}

.tab-label {
  position: relative;
}

.tab-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: rgba(99, 102, 241, 0.3);
  filter: blur(15px);
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tech-tab.active .tab-glow {
  opacity: 0.5;
}

.tech-panel {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.panel-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #e2e8f0;
}

.panel-actions {
  display: flex;
  gap: 0.75rem;
}

.interview-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tech-card {
  position: relative;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
  overflow: hidden;
}

.tech-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  border-color: rgba(99, 102, 241, 0.3);
}

.card-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--card-accent, #6366f1);
}

.interview-item {
  display: flex;
  gap: 1.5rem;
}

.interview-info {
  flex: 1;
}

.info-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #f8fafc;
}

.company-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(99, 102, 241, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  color: #a5b4fc;
}

.company-badge i {
  font-size: 0.7rem;
}

.info-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 1rem 0;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #94a3b8;
}

.detail-item i {
  color: var(--card-accent, #6366f1);
}

.info-status {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.scheduled {
  background: rgba(74, 222, 128, 0.1);
  color: #4ade80;
}

.status-badge.pending {
  background: rgba(250, 204, 21, 0.1);
  color: #facc15;
}

.countdown {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #fca5a5;
}

.countdown i {
  color: #f87171;
}

.info-result {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.result-score {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.score-circle {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: conic-gradient(var(--card-accent, #6366f1) calc(var(--score, 0.85) * 360deg), rgba(30, 41, 59, 0.5));
  position: relative;
}

.score-circle::before {
  content: '';
  position: absolute;
  width: 2.6rem;
  height: 2.6rem;
  border-radius: 50%;
  background: #1e293b;
}

.score-circle span {
  position: relative;
  font-weight: 600;
  color: #fff;
}

.score-label {
  display: flex;
  flex-direction: column;
}

.score-label span {
  font-size: 0.8rem;
  color: #94a3b8;
}

.result-status {
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
}

.result-status.passed {
  background: rgba(74, 222, 128, 0.1);
  color: #4ade80;
}

.result-status.pending {
  background: rgba(250, 204, 21, 0.1);
  color: #facc15;
}

.result-status.failed {
  background: rgba(248, 113, 113, 0.1);
  color: #f87171;
}

.result-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tech-tag {
  font-size: 0.7rem;
  padding: 0.25rem 0.5rem;
  background: rgba(99, 102, 241, 0.1);
  color: #a5b4fc;
  border-radius: 0.5rem;
}

.interview-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 10rem;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.tech-button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.tech-button i {
  font-size: 0.8rem;
}

.tech-button.primary {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

.tech-button.primary:hover {
  background: #4f46e5;
  border-color: #4f46e5;
}

.tech-button.secondary {
  background: rgba(99, 102, 241, 0.1);
  color: #a5b4fc;
  border-color: rgba(99, 102, 241, 0.3);
}

.tech-button.secondary:hover {
  background: rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.5);
}

.tech-button.warning {
  background: rgba(234, 179, 8, 0.1);
  color: #facc15;
  border-color: rgba(234, 179, 8, 0.3);
}

.tech-button.warning:hover {
  background: rgba(234, 179, 8, 0.2);
  border-color: rgba(234, 179, 8, 0.5);
}

.tech-button.danger {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  border-color: rgba(239, 68, 68, 0.3);
}

.tech-button.danger:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}

.tech-button.small {
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 0.75rem;
  border: 1px dashed rgba(255, 255, 255, 0.1);
}

.empty-icon {
  font-size: 2.5rem;
  color: #6366f1;
  margin-bottom: 1rem;
}

.empty-state h4 {
  font-size: 1.1rem;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: #94a3b8;
  margin: 0 0 1.5rem 0;
  font-size: 0.9rem;
}

/* AI练习区域样式 */
.practice-header {
  margin-bottom: 2rem;
}

.practice-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
}

.practice-header p {
  color: #94a3b8;
  margin: 0;
  font-size: 0.95rem;
}

.practice-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  flex: 1;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
  background: linear-gradient(90deg, #6366f1 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  font-size: 0.85rem;
  color: #94a3b8;
}

.practice-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.option-card {
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
}

.option-icon {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
  font-size: 1.5rem;
  background: var(--card-accent, #6366f1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.option-card h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
  text-align: center;
}

.option-card p {
  color: #94a3b8;
  font-size: 0.9rem;
  text-align: center;
  margin: 0 0 1.5rem 0;
  min-height: 3.5rem;
}

.option-progress {
  margin-bottom: 1.5rem;
}

.progress-bar {
  height: 6px;
  background: var(--card-accent, #6366f1);
  border-radius: 3px;
  margin-bottom: 0.5rem;
  position: relative;
  overflow: hidden;
}

.progress-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: progressShine 2s infinite;
}

@keyframes progressShine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.option-progress span {
  font-size: 0.8rem;
  color: #94a3b8;
  display: block;
  text-align: center;
}

.practice-history h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 1rem 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
}

.history-type {
  flex: 1;
  color: #e2e8f0;
}

.history-date {
  width: 6rem;
  color: #94a3b8;
}

.history-score {
  width: 5rem;
  text-align: center;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
}

.history-score.excellent {
  background: rgba(74, 222, 128, 0.1);
  color: #4ade80;
}

.history-score.good {
  background: rgba(163, 230, 53, 0.1);
  color: #a3e635;
}

.history-score.average {
  background: rgba(250, 204, 21, 0.1);
  color: #facc15;
}

.history-score.poor {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

/* 模态框样式 */
.tech-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 1rem;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

.modal-content.large {
  max-width: 1000px;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.modal-subtitle {
  font-size: 0.9rem;
  color: #94a3b8;
  margin-top: 0.5rem;
}

.modal-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.2rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #e2e8f0;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 准备清单样式 */
.prep-checklist {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.checklist-header {
  margin-bottom: 1rem;
}

.checklist-header h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
}

.interview-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #94a3b8;
}

.checklist-section {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1.25rem;
}

.checklist-section h5 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checklist-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.check-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.check-item input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  width: 1.25rem;
  height: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.25rem;
  background: rgba(30, 41, 59, 0.5);
  position: relative;
  transition: all 0.3s ease;
}

.check-item:hover .checkmark {
  border-color: rgba(99, 102, 241, 0.5);
}

.check-item input:checked ~ .checkmark {
  background: #6366f1;
  border-color: #6366f1;
}

.checkmark::after {
  content: '';
  position: absolute;
  display: none;
  left: 0.45rem;
  top: 0.2rem;
  width: 0.3rem;
  height: 0.6rem;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.check-item input:checked ~ .checkmark::after {
  display: block;
}

.check-text {
  font-size: 0.9rem;
  color: #e2e8f0;
  flex: 1;
}

.check-item input:checked ~ .check-text {
  color: #a5b4fc;
  text-decoration: line-through;
}

.checklist-progress {
  margin-top: 1.5rem;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 0.75rem;
}

.progress-text {
  font-size: 0.85rem;
  color: #94a3b8;
  text-align: center;
  margin-top: 0.5rem;
}

/* 分析报告样式 */
.analysis-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.metrics-overview {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.overview-card {
  display: flex;
  gap: 2rem;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.overview-score {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.score-circle.large {
  width: 5rem;
  height: 5rem;
}

.score-circle.large::before {
  width: 4.4rem;
  height: 4.4rem;
}

.score-circle.large span {
  font-size: 1.5rem;
}

.score-label {
  display: flex;
  flex-direction: column;
}

.label-main {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e2e8f0;
}

.label-sub {
  font-size: 0.8rem;
  color: #94a3b8;
}

.overview-comment {
  flex: 1;
}

.comment-title {
  font-size: 0.9rem;
  font-weight: 500;
  color: #a5b4fc;
  margin-bottom: 0.5rem;
}

.comment-text {
  font-size: 0.9rem;
  color: #e2e8f0;
  line-height: 1.5;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.metric-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #a5b4fc);
}

.radar-chart-container {
  display: flex;
  gap: 2rem;
  margin-top: 1.5rem;
}

.chart-container {
  flex: 1;
  min-height: 300px;
}

.chart-legend {
  width: 150px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-text {
  font-size: 0.8rem;
  color: #e2e8f0;
}

.emotion-overview {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.emotion-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.emotion-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-chart {
  height: 250px;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
}

.timeline-keymoments {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.keymoment {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
}

.moment-time {
  width: 5rem;
  color: #a5b4fc;
  font-weight: 500;
}

.moment-text {
  flex: 1;
  color: #e2e8f0;
}

.emotion-comments {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 1.5rem;
}

.comment-card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
}

.comment-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.comment-text {
  font-size: 0.85rem;
  color: #e2e8f0;
  line-height: 1.5;
}

.feedback-strengths,
.feedback-improvements {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.feedback-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.feedback-header h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.feedback-list {
  padding-left: 1.5rem;
  margin: 0;
}

.feedback-list li {
  margin-bottom: 0.5rem;
  color: #e2e8f0;
  font-size: 0.9rem;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  line-height: 1.5;
}

.feedback-list li i {
  margin-top: 0.2rem;
  color: #a5b4fc;
}

.feedback-questions {
  margin-top: 1.5rem;
}

.question-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.question-item {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
}

.question-text {
  font-size: 0.9rem;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
  display: flex;
  gap: 0.5rem;
}

.question-label {
  font-weight: 500;
  color: #a5b4fc;
}

.question-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.rating-stars {
  display: flex;
  gap: 0.25rem;
}

.rating-stars i {
  font-size: 0.9rem;
  color: #64748b;
}

.rating-stars i.filled {
  color: #facc15;
}

.rating-label {
  font-size: 0.8rem;
  color: #94a3b8;
}

.question-feedback {
  font-size: 0.85rem;
  color: #e2e8f0;
  line-height: 1.5;
  display: flex;
  gap: 0.5rem;
}

.feedback-label {
  font-weight: 500;
  color: #a5b4fc;
}

.resources-header {
  margin-bottom: 1.5rem;
}

.resources-header h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
}

.resources-header p {
  font-size: 0.9rem;
  color: #94a3b8;
  margin: 0;
}

.resources-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.resource-card {
  display: flex;
  gap: 1rem;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
}

.resource-type {
  width: 6rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.resource-type.course {
  background: rgba(99, 102, 241, 0.1);
  color: #a5b4fc;
}

.resource-type.article {
  background: rgba(74, 222, 128, 0.1);
  color: #86efac;
}

.resource-type.book {
  background: rgba(249, 115, 22, 0.1);
  color: #fdba74;
}

.resource-type i {
  font-size: 1.2rem;
}

.resource-content {
  flex: 1;
}

.resource-content h5 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
}

.resource-content p {
  font-size: 0.85rem;
  color: #94a3b8;
  margin: 0 0 0.75rem 0;
  line-height: 1.5;
}

.resource-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #64748b;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* 过渡动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: all 0.3s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: translateY(20px);
}

/* 响应式调整 */
@media (max-width: 992px) {
  .interview-item {
    flex-direction: column;
  }
  
  .interview-actions {
    flex-direction: row;
    flex-wrap: wrap;
    min-width: auto;
  }
  
  .overview-card {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .radar-chart-container {
    flex-direction: column;
  }
  
  .chart-legend {
    width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .emotion-comments {
    grid-template-columns: 1fr;
  }
  
  .resource-card {
    flex-direction: column;
  }
  
  .resource-type {
    width: auto;
    flex-direction: row;
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .interview-tabs {
    flex-direction: column;
  }
  
  .practice-options {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    max-height: 80vh;
  }
}
</style>