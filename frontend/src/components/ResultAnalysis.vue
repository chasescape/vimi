<template>
  <div class="cyber-container">
    <!-- 背景元素 -->
    <div class="cyber-grid"></div>
    <div class="cyber-pulse"></div>
    <div class="cyber-orb" style="top: 10%; left: 10%; animation-delay: 0s;"></div>
    <div class="cyber-orb" style="top: 70%; left: 80%; animation-delay: 3s;"></div>
    <div class="cyber-orb" style="top: 30%; left: 60%; animation-delay: 6s;"></div>
    
    <!-- 头部导航 -->
    <header class="cyber-header">
      <div class="container">
        <div class="header-content">
          <div class="logo">
            <i class="fas fa-robot"></i>
            <span>AI面试分析结果</span>
          </div>
          <div class="header-actions">
            <button class="cyber-btn" @click="showDownloadModal = true">
              <i class="fas fa-download"></i> 下载报告
            </button>
            <button class="cyber-btn" @click="toggleDarkMode">
              <i class="fas" :class="darkMode ? 'fa-sun' : 'fa-moon'"></i>
            </button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- 主体内容 -->
    <main class="container main-layout">
      <!-- 侧边导航 -->
      <aside class="sidebar">
         <div class="sidebar-header">
    <div class="candidate-avatar">
      <i class="fas fa-user-tie"></i>
    </div>
    <div class="candidate-info">
      <h3>张小明</h3>
      <p>高级前端开发工程师</p>
    </div>
  </div>
        
         <nav class="sidebar-nav">
    <ul>
      <li v-for="nav in navItems" :key="nav.id" 
          :class="{active: activeNav === nav.id}"
          @click="activeNav = nav.id">
        <i :class="nav.icon"></i>
        <span>{{ nav.label }}</span>
        <div class="nav-indicator"></div>
      </li>
    </ul>
  </nav>
        
     
  <div class="sidebar-footer">
    <!-- 这里只保留百分比显示，移除球体 -->
    <div class="match-score">
    </div>
    <button class="cyber-btn feedback-btn" @click="showFeedbackModal">
      <i class="fas fa-comment-alt"></i> AI反馈
    </button>
  </div>
</aside>
      
      <!-- 主内容区域 -->
      <div class="content-area">
        <!-- 报告概览 -->
        <section class="report-overview" v-show="activeNav === 'overview'">
          <h1 class="cyber-title">3D动态面试分析报告</h1>
          <p class="cyber-subtitle">基于多模态AI深度分析的全面评估</p>
          
          <div class="overview-grid">
            <div class="overview-card">
              <div class="card-header">
                <i class="fas fa-chart-radar"></i>
                <h3>能力雷达图</h3>
              </div>
              <div class="card-body">
                <div class="radar-chart">
                  <canvas ref="radarChart"></canvas>
                </div>
                <div class="chart-legend">
                  <div class="legend-item" v-for="item in legendData" :key="item.label">
                    <span class="legend-color" :style="{backgroundColor: item.color}"></span>
                    <span class="legend-label">{{ item.label }}</span>
                    <span class="legend-value">{{ item.value }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="overview-card">
              <div class="card-header">
                <i class="fas fa-brain"></i>
                <h3>情绪稳定性</h3>
              </div>
              <div class="card-body">
                <div class="emotion-chart">
                  <canvas ref="emotionChart"></canvas>
                </div>
                <div class="emotion-stats">
                  <div class="stat-item">
                    <span class="stat-label">积极情绪</span>
                    <span class="stat-value">82%</span>
                    <div class="stat-bar">
                      <div class="stat-fill" style="width: 82%; background: #4cc9f0;"></div>
                    </div>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">中性情绪</span>
                    <span class="stat-value">12%</span>
                    <div class="stat-bar">
                      <div class="stat-fill" style="width: 12%; background: #3a86ff;"></div>
                    </div>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">消极情绪</span>
                    <span class="stat-value">6%</span>
                    <div class="stat-bar">
                      <div class="stat-fill" style="width: 6%; background: #ff006e;"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="overview-card">
              <div class="card-header">
                <i class="fas fa-atom"></i>
                <h3>岗位匹配</h3>
              </div>
              <div class="card-body">
                <div class="match-chart">
                  <div class="match-sphere">
                    <div class="sphere-surface">
                      <div class="skill-point" v-for="(point, index) in spherePoints" :key="index"
                           :style="{
                             transform: `rotateX(${point.rotateX}deg) rotateY(${point.rotateY}deg)`,
                             background: point.color
                           }">
                        <div class="point-tooltip">{{ point.skill }}: {{ point.value }}%</div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="match-items">
                  <div class="match-item" v-for="item in matchItems" :key="item.skill">
                    <div class="match-skill">
                      <span>{{ item.skill }}</span>
                      <span class="match-demand">需求: {{ item.demand }}</span>
                    </div>
                    <div class="match-comparison">
                      <div class="match-bar">
                        <div class="match-candidate" :style="{width: item.candidate + '%'}"></div>
                        <div class="match-required" :style="{width: item.required + '%'}"></div>
                      </div>
                      <span class="match-percent">{{ item.match }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="overview-card">
              <div class="card-header">
                <i class="fas fa-project-diagram"></i>
                <h3>发展建议</h3>
              </div>
              <div class="card-body">
                <div class="steps-container">
                  <div class="step-card" v-for="step in steps" :key="step.title" @click="showStepDetail(step)">
                    <div class="step-icon" :style="{background: step.color}">
                      <i :class="step.icon"></i>
                    </div>
                    <h4>{{ step.title }}</h4>
                    <div class="step-progress">
                      <div class="progress-bar">
                        <div class="progress-fill" :style="{width: step.progress + '%'}"></div>
                      </div>
                      <span>{{ step.progress }}% 完成度</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <!-- 面试视频分析 -->
        <section class="video-analysis" v-show="activeNav === 'video'">
          <div class="section-header">
            <h2><i class="fas fa-video"></i> 全息面试录像分析</h2>
          </div>
          
          <div class="video-grid">
            <div class="video-card" v-for="video in videos" :key="video.id">
              <div class="video-header">
                <h3>{{ video.title }}</h3>
                <div class="video-score">
                  <span>{{ video.score }}</span>
                  <i class="fas" :class="video.trendIcon" :style="{color: video.trendColor}"></i>
                </div>
              </div>
              
              <div class="video-container">
                <div class="video-placeholder">
                  <i class="fas fa-play-circle"></i>
                  <span>点击播放面试录像</span>
                </div>
                <div class="video-timeline">
                  <div class="timeline-marker" 
                       v-for="marker in video.markers" 
                       :key="marker.time"
                       :style="{left: marker.position + '%', backgroundColor: marker.color}"
                       :title="marker.label">
                  </div>
                </div>
                
                <div class="video-controls">
                  <button v-for="(control, idx) in videoControls" 
                          :key="idx" 
                          :title="control.title"
                          @click="handleVideoControl(control.action, video.id)">
                    <i :class="control.icon"></i>
                  </button>
                </div>
              </div>
              
              <div class="video-insights">
                <div class="insight-item" v-for="insight in video.insights" :key="insight.type">
                  <div class="insight-label">
                    <i :class="insight.icon"></i>
                    <span>{{ insight.label }}</span>
                  </div>
                  <div class="insight-value">{{ insight.value }}</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <!-- 能力分析 -->
        <section class="skills-analysis" v-show="activeNav === 'skills'">
          <div class="section-header">
            <h2><i class="fas fa-chart-network"></i> 3D能力图谱分析</h2>
          </div>
          
          <div class="skills-container">
            <div class="skills-chart">
              <div class="skills-web">
                <div class="web-layer" v-for="(layer, lIdx) in skillLayers" :key="lIdx"
                     :style="{transform: `rotate(${lIdx * 45}deg)`}">
                  <div class="web-line" v-for="(line, lineIdx) in layer.lines" :key="lineIdx"
                       :style="{
                         transform: `rotate(${line.angle}deg)`,
                         '--hue': line.hue
                       }">
                    <div class="web-node" v-for="(node, nIdx) in line.nodes" :key="nIdx"
                         :style="{
                           left: `${node.position}%`,
                           '--hue': line.hue,
                           '--alpha': node.alpha
                         }">
                      <div class="node-tooltip">{{ node.skill }}: {{ node.value }}%</div>
                    </div>
                  </div>
                </div>
                <div class="web-center"></div>
              </div>
            </div>
            
            <div class="skills-details">
              <div class="skill-category" v-for="skill in skills" :key="skill.category">
                <div class="category-header">
                  <h3>{{ skill.category }}</h3>
                  <div class="category-score">
                    <span>{{ skill.score }}/100</span>
                    <div class="score-bar">
                      <div class="score-fill" :style="{width: skill.score + '%', background: skill.color}"></div>
                    </div>
                  </div>
                </div>
                
                <div class="skill-items">
                  <div class="skill-item" v-for="item in skill.items" :key="item.name">
                    <div class="skill-info">
                      <span class="skill-name">{{ item.name }}</span>
                      <span class="skill-value">{{ item.value }}%</span>
                    </div>
                    <div class="skill-bar">
                      <div class="skill-fill" :style="{width: item.value + '%', background: skill.color}"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <!-- 情绪分析 -->
        <section class="emotion-analysis" v-show="activeNav === 'emotion'">
          <div class="section-header">
            <h2><i class="fas fa-brain"></i> 动态情绪图谱分析</h2>
          </div>
          
          <div class="emotion-grid">
            <div class="emotion-card">
              <div class="card-header">
                <h3>情绪波动曲线</h3>
                <span class="card-score">稳定性: 88%</span>
              </div>
              <div class="card-body">
                <div class="emotion-chart">
                  <canvas ref="emotionWaveChart"></canvas>
                </div>
                <div class="emotion-keyframes">
                  <div class="keyframe" v-for="point in emotionPoints" :key="point.time">
                    <div class="keyframe-time">{{ point.time }}</div>
                    <div class="keyframe-emotion" :style="{backgroundColor: point.color}">
                      <i :class="point.icon"></i>
                    </div>
                    <div class="keyframe-label">{{ point.label }}</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="emotion-card">
              <div class="card-header">
                <h3>情绪热点分布</h3>
                <span class="card-score">积极情绪: 82%</span>
              </div>
              <div class="card-body">
                <div class="heatmap-chart">
                  <div class="heatmap-grid">
                    <div class="heatmap-row" v-for="(row, rowIdx) in heatmapData" :key="rowIdx">
                      <div class="heatmap-cell" v-for="(cell, cellIdx) in row" :key="cellIdx"
                           :style="{
                             '--intensity': cell.intensity,
                             '--hue': cell.hue
                           }">
                        <div class="heatmap-tooltip">
                          {{ cell.time }}<br>
                          情绪强度: {{ cell.intensity * 100 }}%<br>
                          {{ cell.emotion }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="emotion-stats">
                  <div class="stat-item" v-for="stat in emotionStats" :key="stat.type">
                    <div class="stat-info">
                      <span class="stat-label">{{ stat.label }}</span>
                      <span class="stat-value">{{ stat.value }}</span>
                    </div>
                    <div class="stat-bar">
                      <div class="stat-fill" :style="{width: stat.percent + '%', background: stat.color}"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <!-- 岗位匹配分析 -->
<!-- 岗位匹配分析部分 - 添加球体 -->
<section class="match-analysis" v-show="activeNav === 'match'">
  <div class="section-header">
    <h2><i class="fas fa-atom"></i> 3D岗位匹配分析</h2>
  </div>
  
  <div class="match-container">
    <div class="match-visual">
      <!-- 球体移到这里 -->
      <div class="match-sphere">
        <div class="sphere-surface">
          <div class="skill-point" v-for="(point, index) in spherePoints" :key="index"
               :style="{
                 transform: `rotateX(${point.rotateX}deg) rotateY(${point.rotateY}deg)`,
                 background: point.color
               }">
            <div class="point-tooltip">{{ point.skill }}: {{ point.value }}%</div>
          </div>
        </div>
      </div>
      <div class="match-score">
        <span>89%</span>
        <p>匹配度</p>
      </div>
    </div>
    
    <div class="match-details">
      <!-- 匹配详情保持不变 -->
      <div class="match-item" v-for="item in matchItems" :key="item.skill">
        <div class="match-skill">
          <span>{{ item.skill }}</span>
          <span class="match-demand">需求: {{ item.demand }}</span>
        </div>
        <div class="match-comparison">
          <div class="match-bar">
            <div class="match-candidate" :style="{width: item.candidate + '%'}"></div>
            <div class="match-required" :style="{width: item.required + '%'}"></div>
          </div>
          <span class="match-percent">{{ item.match }}%</span>
        </div>
      </div>
      
      <div class="match-summary">
        <h4>AI匹配总结</h4>
        <p>候选人在技术能力方面与岗位要求高度匹配，特别是在JavaScript和React方面表现突出。沟通能力和团队协作达到岗位要求，在系统设计经验方面还有提升空间。</p>
      </div>
    </div>
  </div>
</section>
      </div>
    </main>
    
    <!-- 页脚 -->
    <footer class="cyber-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <div class="logo">
              <i class="fas fa-robot"></i>
              <span>AI面试分析系统</span>
            </div>
            <p>基于人工智能的下一代招聘解决方案</p>
            <div class="social-links">
              <a href="#"><i class="fab fa-linkedin"></i></a>
              <a href="#"><i class="fab fa-github"></i></a>
              <a href="#"><i class="fab fa-twitter"></i></a>
              <a href="#"><i class="fab fa-youtube"></i></a>
            </div>
          </div>
          
          <div class="footer-links">
            <div class="link-column" v-for="column in footerColumns" :key="column.title">
              <h3>{{ column.title }}</h3>
              <ul>
                <li v-for="(link, idx) in column.links" :key="idx">
                  <a :href="link.url"><i :class="link.icon"></i> {{ link.text }}</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2023 AI面试分析系统. 保留所有权利.</p>
          <div class="footer-meta">
            <a href="#">隐私政策</a>
            <a href="#">使用条款</a>
            <a href="#">Cookie设置</a>
          </div>
        </div>
      </div>
    </footer>
    
    <!-- AI反馈模态框 -->
    <div class="cyber-modal" v-if="showFeedbackModal" @click.self="showFeedbackModal = false">
      <div class="modal-content feedback-modal">
        <button class="close-btn" @click="showFeedbackModal = false"><i class="fas fa-times"></i></button>
        <h3><i class="fas fa-comment-dots"></i> AI深度反馈</h3>
        <div class="modal-body">
          <div class="feedback-tabs">
            <button v-for="tab in feedbackTabs" 
                    :key="tab.id"
                    :class="{active: activeFeedbackTab === tab.id}"
                    @click="activeFeedbackTab = tab.id">
              <i :class="tab.icon"></i> {{ tab.label }}
            </button>
          </div>
          
          <div class="feedback-content">
            <div class="feedback-pane" v-show="activeFeedbackTab === 'strengths'">
              <h4><i class="fas fa-star"></i> 核心优势</h4>
              <div class="strength-list">
                <div class="strength-item" v-for="(strength, idx) in strengths" :key="idx">
                  <div class="strength-icon">
                    <i class="fas fa-check-circle"></i>
                  </div>
                  <div class="strength-text">
                    <h5>{{ strength.title }}</h5>
                    <p>{{ strength.description }}</p>
                    <div class="strength-evidence">
                      <span>证据点:</span>
                      <ul>
                        <li v-for="(evidence, eIdx) in strength.evidences" :key="eIdx">{{ evidence }}</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="feedback-pane" v-show="activeFeedbackTab === 'improvements'">
              <h4><i class="fas fa-rocket"></i> 改进建议</h4>
              <div class="improvement-list">
                <div class="improvement-item" v-for="(improve, idx) in improvements" :key="idx">
                  <div class="improvement-icon">
                    <i class="fas fa-bullseye"></i>
                  </div>
                  <div class="improvement-text">
                    <h5>{{ improve.area }}</h5>
                    <p>{{ improve.suggestion }}</p>
                    <div class="improvement-resources" v-if="improve.resources">
                      <span>学习资源:</span>
                      <ul>
                        <li v-for="(resource, rIdx) in improve.resources" :key="rIdx">
                          <a :href="resource.link" target="_blank">{{ resource.title }}</a>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="feedback-pane" v-show="activeFeedbackTab === 'summary'">
              <h4><i class="fas fa-file-alt"></i> 综合评估</h4>
              <div class="summary-content">
                <div class="summary-card" v-for="summary in feedbackSummary" :key="summary.category">
                  <div class="summary-header">
                    <i :class="summary.icon"></i>
                    <h5>{{ summary.category }}</h5>
                    <span class="summary-score">{{ summary.score }}/100</span>
                  </div>
                  <div class="summary-body">
                    <p>{{ summary.overview }}</p>
                    <div class="summary-highlights">
                      <div class="highlight" v-for="(highlight, hIdx) in summary.highlights" :key="hIdx">
                        <span class="highlight-label">{{ highlight.label }}:</span>
                        <span class="highlight-value">{{ highlight.value }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 发展建议详情模态框 -->
    <div class="cyber-modal" v-if="showStepModal" @click.self="showStepModal = false">
      <div class="modal-content step-modal">
        <button class="close-btn" @click="showStepModal = false"><i class="fas fa-times"></i></button>
        <h3><i :class="currentStep.icon" :style="{color: currentStep.color}"></i> {{ currentStep.title }}</h3>
        <div class="modal-body">
          <div class="step-detail">
            <p>{{ currentStep.detail }}</p>
            <div class="step-progress">
              <div class="progress-header">
                <span>完成进度</span>
                <span>{{ currentStep.progress }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{width: currentStep.progress + '%', background: currentStep.color}"></div>
              </div>
            </div>
            
            <div class="step-resources" v-if="currentStep.resources">
              <h4>推荐资源</h4>
              <ul>
                <li v-for="(resource, idx) in currentStep.resources" :key="idx">
                  <a :href="resource.link" target="_blank">{{ resource.title }}</a>
                </li>
              </ul>
            </div>
            
            <div class="step-timeline">
              <h4>时间规划</h4>
              <div class="timeline">
                <div class="timeline-item" v-for="(item, idx) in timelineItems" :key="idx">
                  <div class="timeline-dot" :style="{background: currentStep.color}"></div>
                  <div class="timeline-content">
                    <h5>{{ item.title }}</h5>
                    <p>{{ item.description }}</p>
                    <span class="timeline-date">{{ item.date }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 下载报告模态框 -->
    <div class="cyber-modal" v-if="showDownloadModal" @click.self="showDownloadModal = false">
      <div class="modal-content download-modal">
        <button class="close-btn" @click="showDownloadModal = false"><i class="fas fa-times"></i></button>
        <h3>下载完整报告</h3>
        <div class="modal-body">
          <p>请选择您要下载的报告格式：</p>
          <div class="download-options">
            <button class="download-option" @click="downloadReport('pdf')">
              <i class="fas fa-file-pdf"></i> PDF格式
            </button>
            <button class="download-option" @click="downloadReport('word')">
              <i class="fas fa-file-word"></i> Word格式
            </button>
            <button class="download-option" @click="downloadReport('html')">
              <i class="fas fa-file-code"></i> HTML格式
            </button>
          </div>
          <div class="download-customize">
            <h4>自定义报告内容</h4>
            <div class="customize-options">
              <label v-for="option in downloadOptions" :key="option.id">
                <input type="checkbox" v-model="option.checked"> {{ option.label }}
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Chart from 'chart.js/auto'

// 暗黑模式切换
const darkMode = ref(true)
const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
  document.documentElement.classList.toggle('light-mode', !darkMode.value)
}

// 导航项
const navItems = ref([
  { id: 'overview', label: '报告概览', icon: 'fas fa-chart-pie' },
  { id: 'video', label: '面试录像', icon: 'fas fa-video' },
  { id: 'skills', label: '能力图谱', icon: 'fas fa-chart-network' },
  { id: 'emotion', label: '情绪分析', icon: 'fas fa-brain' },
  { id: 'match', label: '岗位匹配', icon: 'fas fa-atom' }
])

const activeNav = ref('overview')

// 图表引用
const radarChart = ref<HTMLCanvasElement | null>(null)
const emotionChart = ref<HTMLCanvasElement | null>(null)
const emotionWaveChart = ref<HTMLCanvasElement | null>(null)

// 3D球体数据
const spherePoints = ref([
  { skill: 'JavaScript', value: 94, rotateX: 20, rotateY: 30, color: '#4cc9f0' },
  { skill: 'React', value: 89, rotateX: 40, rotateY: 60, color: '#3a86ff' },
  { skill: 'TypeScript', value: 85, rotateX: 60, rotateY: 90, color: '#8338ec' },
  { skill: '系统设计', value: 82, rotateX: 80, rotateY: 120, color: '#ff006e' },
  { skill: '算法', value: 87, rotateX: 100, rotateY: 150, color: '#ffbe0b' },
  { skill: '沟通', value: 85, rotateX: 120, rotateY: 180, color: '#38b000' }
])

// 能力图谱数据
const skillLayers = ref([
  {
    lines: [
      { angle: 0, hue: 190, nodes: [
        { skill: 'JavaScript', value: 94, position: 70, alpha: 0.9 },
        { skill: 'ES6', value: 88, position: 50, alpha: 0.8 },
        { skill: 'TypeScript', value: 85, position: 30, alpha: 0.7 }
      ]},
      { angle: 45, hue: 210, nodes: [
        { skill: 'React', value: 89, position: 80, alpha: 0.9 },
        { skill: 'Vue', value: 75, position: 60, alpha: 0.7 },
        { skill: 'Angular', value: 65, position: 40, alpha: 0.6 }
      ]},
      { angle: 90, hue: 230, nodes: [
        { skill: 'Node.js', value: 82, position: 75, alpha: 0.8 },
        { skill: 'Express', value: 78, position: 55, alpha: 0.7 },
        { skill: 'NestJS', value: 70, position: 35, alpha: 0.6 }
      ]},
      { angle: 135, hue: 250, nodes: [
        { skill: 'HTML5', value: 92, position: 85, alpha: 0.9 },
        { skill: 'CSS3', value: 88, position: 65, alpha: 0.8 },
        { skill: 'SASS', value: 80, position: 45, alpha: 0.7 }
      ]},
      { angle: 180, hue: 270, nodes: [
        { skill: 'Webpack', value: 85, position: 70, alpha: 0.8 },
        { skill: 'Vite', value: 80, position: 50, alpha: 0.7 },
        { skill: 'Rollup', value: 70, position: 30, alpha: 0.6 }
      ]},
      { angle: 225, hue: 290, nodes: [
        { skill: 'Git', value: 90, position: 80, alpha: 0.9 },
        { skill: 'CI/CD', value: 75, position: 60, alpha: 0.7 },
        { skill: 'Docker', value: 65, position: 40, alpha: 0.6 }
      ]},
      { angle: 270, hue: 310, nodes: [
        { skill: '算法', value: 87, position: 75, alpha: 0.8 },
        { skill: '数据结构', value: 85, position: 55, alpha: 0.7 },
        { skill: '设计模式', value: 80, position: 35, alpha: 0.6 }
      ]},
      { angle: 315, hue: 330, nodes: [
        { skill: '沟通', value: 85, position: 85, alpha: 0.8 },
        { skill: '团队协作', value: 80, position: 65, alpha: 0.7 },
        { skill: '领导力', value: 70, position: 45, alpha: 0.6 }
      ]}
    ]
  }
])

// 热力图数据
const heatmapData = ref(
  Array.from({ length: 10 }, (_, row) => 
    Array.from({ length: 20 }, (_, col) => ({
      time: `${Math.floor(col * 3)}:${(col * 3 % 1 * 60).toString().padStart(2, '0')}`,
      emotion: ['积极', '中性', '消极'][Math.floor(Math.random() * 3)],
      intensity: Math.random() * 0.8 + 0.2,
      hue: row < 3 ? 190 : row < 7 ? 210 : 230
    }))
  )
)

// 视频分析数据
const videos = ref([
  {
    id: 1,
    title: '候选人视频分析',
    score: '流畅度: 92%',
    trendIcon: 'fa-arrow-up',
    trendColor: '#4cc9f0',
    markers: [
      { time: '00:02:15', position: 15, color: '#4cc9f0', label: '技术问题回答开始' },
      { time: '00:05:30', position: 30, color: '#3a86ff', label: '算法问题开始' },
      { time: '00:12:45', position: 45, color: '#8338ec', label: '系统设计环节' },
      { time: '00:25:20', position: 65, color: '#ff006e', label: '行为问题回答' }
    ],
    insights: [
      { type: 'engagement', label: '参与度', value: '94%', icon: 'fas fa-fire' },
      { type: 'clarity', label: '表达清晰度', value: '89%', icon: 'fas fa-comment-alt' },
      { type: 'confidence', label: '自信度', value: '91%', icon: 'fas fa-brain' },
      { type: 'response', label: '反应速度', value: '87%', icon: 'fas fa-bolt' },
      { type: 'articulation', label: '表达流畅度', value: '90%', icon: 'fas fa-comments' },
      { type: 'bodylang', label: '肢体语言', value: '85%', icon: 'fas fa-hands' }
    ]
  },
  {
    id: 2,
    title: '面试官视频分析',
    score: '互动质量: 88%',
    trendIcon: 'fa-arrow-down',
    trendColor: '#ff006e',
    markers: [
      { time: '00:01:45', position: 10, color: '#4cc9f0', label: '自我介绍环节' },
      { time: '00:07:20', position: 35, color: '#3a86ff', label: '技术深入探讨' },
      { time: '00:15:10', position: 50, color: '#8338ec', label: '情景模拟' },
      { time: '00:30:05', position: 70, color: '#ff006e', label: '反问环节' }
    ],
    insights: [
      { type: 'questions', label: '问题质量', value: '92%', icon: 'fas fa-question-circle' },
      { type: 'feedback', label: '反馈及时性', value: '85%', icon: 'fas fa-comments' },
      { type: 'engagement', label: '互动参与度', value: '90%', icon: 'fas fa-users' },
      { type: 'clarity', label: '表达清晰度', value: '88%', icon: 'fas fa-comment-alt' },
      { type: 'professional', label: '专业度', value: '93%', icon: 'fas fa-user-tie' },
      { type: 'fairness', label: '公平性', value: '95%', icon: 'fas fa-balance-scale' }
    ]
  }
])

const videoControls = ref([
  { title: '播放/暂停', icon: 'fas fa-play', action: 'play' },
  { title: '全屏', icon: 'fas fa-expand', action: 'fullscreen' },
  { title: '3D模式', icon: 'fas fa-cube', action: '3d' },
  { title: '分析模式', icon: 'fas fa-chart-line', action: 'analyze' },
  { title: '下载', icon: 'fas fa-download', action: 'download' }
])

const handleVideoControl = (action: string, videoId: number) => {
  console.log(`执行视频控制: ${action} 视频ID: ${videoId}`)
  if (action === 'play') {
    // 播放/暂停逻辑
  } else if (action === 'fullscreen') {
    // 全屏逻辑
  }
}

// 能力分析数据
const skills = ref([
  {
    category: '技术能力',
    score: 91,
    color: '#4cc9f0',
    items: [
      { name: 'JavaScript深度', value: 94 },
      { name: 'React框架', value: 89 },
      { name: '算法与数据结构', value: 87 },
      { name: '系统设计', value: 82 },
      { name: 'TypeScript', value: 85 },
      { name: '性能优化', value: 79 }
    ]
  },
  {
    category: '沟通表达',
    score: 85,
    color: '#3a86ff',
    items: [
      { name: '语言清晰度', value: 92 },
      { name: '逻辑性', value: 88 },
      { name: '回答结构化', value: 83 },
      { name: '倾听能力', value: 77 },
      { name: '非语言表达', value: 81 },
      { name: '说服力', value: 79 }
    ]
  },
  {
    category: '综合素质',
    score: 83,
    color: '#8338ec',
    items: [
      { name: '问题解决能力', value: 89 },
      { name: '团队协作', value: 85 },
      { name: '学习能力', value: 82 },
      { name: '抗压能力', value: 76 },
      { name: '创新思维', value: 80 },
      { name: '领导潜力', value: 72 }
    ]
  }
])

// 情绪分析数据
const emotionPoints = ref([
  { time: '00:02:15', label: '技术问题', icon: 'fas fa-code', color: '#4cc9f0' },
  { time: '00:05:30', label: '算法问题', icon: 'fas fa-project-diagram', color: '#3a86ff' },
  { time: '00:12:45', label: '系统设计', icon: 'fas fa-sitemap', color: '#8338ec' },
  { time: '00:25:20', label: '行为问题', icon: 'fas fa-users', color: '#ff006e' },
  { time: '00:30:05', label: '反问环节', icon: 'fas fa-question', color: '#ffbe0b' }
])

const emotionStats = ref([
  { type: 'positive', label: '积极情绪', value: '82%', percent: 82, color: '#4cc9f0' },
  { type: 'neutral', label: '中性情绪', value: '12%', percent: 12, color: '#3a86ff' },
  { type: 'negative', label: '消极情绪', value: '6%', percent: 6, color: '#ff006e' }
])

// 岗位匹配数据
const matchItems = ref([
  { skill: 'JavaScript', candidate: 94, required: 90, demand: '高', match: 104 },
  { skill: 'React', candidate: 89, required: 85, demand: '高', match: 105 },
  { skill: 'TypeScript', candidate: 85, required: 80, demand: '中', match: 106 },
  { skill: '系统设计', candidate: 82, required: 85, demand: '高', match: 96 },
  { skill: '算法', candidate: 87, required: 80, demand: '中', match: 109 },
  { skill: '沟通能力', candidate: 85, required: 80, demand: '中', match: 106 }
])

// 反馈数据
const feedbackTabs = ref([
  { id: 'strengths', label: '核心优势', icon: 'fas fa-star' },
  { id: 'improvements', label: '改进建议', icon: 'fas fa-rocket' },
  { id: 'summary', label: '综合评估', icon: 'fas fa-file-alt' }
])

const activeFeedbackTab = ref('strengths')
const showFeedbackModal = ref(false)

const strengths = ref([
  {
    title: '扎实的JavaScript基础',
    description: '候选人对JavaScript语言特性有深入理解，能够熟练运用ES6+特性，对闭包、原型链等核心概念掌握牢固。',
    evidences: [
      '在白板编程环节展示了清晰的变量作用域理解',
      '正确回答了所有JavaScript概念性问题',
      '代码示例中使用了多种ES6+特性'
    ]
  },
  {
    title: 'React框架熟练度',
    description: '对React框架有深入理解，能够合理使用hooks，对虚拟DOM原理和性能优化有独到见解。',
    evidences: [
      '正确解释了React Fiber架构',
      '展示了自定义hook的使用',
      '提出了合理的性能优化方案'
    ]
  },
  {
    title: '问题解决能力',
    description: '面对复杂问题时能够快速分解问题，提出多种解决方案并进行比较分析。',
    evidences: [
      '在算法问题中展示了分治思想',
      '系统设计环节考虑了多种备选方案',
      '能够权衡不同方案的优缺点'
    ]
  }
])

const improvements = ref([
  {
    area: '系统设计经验',
    suggestion: '建议加强大型前端项目架构设计经验，特别是微前端领域，可以通过参与开源项目或模拟项目来积累经验。',
    resources: [
      { title: '微前端架构实战指南', link: '#' },
      { title: '大型前端项目架构案例', link: '#' },
      { title: '系统设计面试准备', link: '#' }
    ]
  },
  {
    area: '性能优化技巧',
    suggestion: '建议深入学习现代前端性能优化技巧，特别是首屏加载优化和运行时性能优化，关注Web Vitals指标。',
    resources: [
      { title: 'Web性能权威指南', link: '#' },
      { title: 'Chrome DevTools高级使用', link: '#' },
      { title: 'Lighthouse优化实践', link: '#' }
    ]
  },
  {
    area: '白板表达能力',
    suggestion: '建议练习在白板上的绘图和表达能力，可以参加模拟面试或与同事进行练习，提高在压力下的表达清晰度。',
    resources: [
      { title: '技术面试白板技巧', link: '#' },
      { title: '可视化系统设计', link: '#' },
      { title: '架构图绘制规范', link: '#' }
    ]
  }
])

const feedbackSummary = ref([
  {
    category: '技术能力',
    icon: 'fas fa-code',
    score: 91,
    overview: '候选人在技术能力方面表现优秀，特别是在JavaScript和React方面展示了深厚的功底。系统设计能力良好，能够清晰地阐述架构思路。',
    highlights: [
      { label: '核心优势', value: 'JavaScript深度, React熟练度' },
      { label: '提升空间', value: '微前端架构, 性能优化' },
      { label: '推荐学习', value: '《前端架构设计》《高性能JavaScript》' }
    ]
  },
  {
    category: '沟通表达',
    icon: 'fas fa-comments',
    score: 85,
    overview: '语言表达清晰流畅，能够有条理地组织回答。在解释复杂概念时表现优秀，但偶尔会急于回答问题。',
    highlights: [
      { label: '核心优势', value: '技术概念解释清晰' },
      { label: '提升空间', value: '回答节奏控制' },
      { label: '推荐练习', value: '结构化表达训练' }
    ]
  },
  {
    category: '综合素质',
    icon: 'fas fa-star',
    score: 83,
    overview: '展现了优秀的问题解决能力和学习能力。团队协作意识强，能够很好地理解面试官的问题意图。',
    highlights: [
      { label: '核心优势', value: '问题分解能力, 学习能力' },
      { label: '提升空间', value: '压力下的表现' },
      { label: '推荐资源', value: '《思考，快与慢》' }
    ]
  }
])

// 发展建议数据
const steps = ref([
  {
    title: '学习路径',
    icon: 'fas fa-graduation-cap',
    summary: '推荐阅读技术书籍和完成3个中型项目实践',
    detail: '详细的学习计划包括：1. 每月阅读一本技术书籍；2. 每周完成一个技术挑战；3. 参与开源项目贡献；4. 学习微前端架构原理和实践。',
    color: '#4cc9f0',
    progress: 65,
    resources: [
      { title: 'JavaScript高级程序设计', link: '#' },
      { title: 'React设计原理', link: '#' },
      { title: '微前端架构实战', link: '#' }
    ]
  },
  {
    title: '项目实践',
    icon: 'fas fa-laptop-code',
    summary: '建议主导一个微前端架构项目',
    detail: '项目实践建议：1. 从零搭建微前端架构；2. 实现模块联邦；3. 优化构建性能；4. 实施CI/CD流程。预计耗时3个月。',
    color: '#3a86ff',
    progress: 40,
    resources: [
      { title: '微前端项目模板', link: '#' },
      { title: 'Webpack模块联邦指南', link: '#' },
      { title: 'CI/CD最佳实践', link: '#' }
    ]
  },
  {
    title: '职业发展',
    icon: 'fas fa-briefcase',
    summary: '6个月内可申请技术主管岗位',
    detail: '职业发展路径：1. 6个月技术主管；2. 1年高级技术主管；3. 2年前端架构师；4. 3年技术总监。薪资增长曲线分析。',
    color: '#8338ec',
    progress: 25,
    resources: [
      { title: '技术领导力培养', link: '#' },
      { title: '职业发展规划', link: '#' },
      { title: '薪资谈判技巧', link: '#' }
    ]
  },
  {
    title: '面试结果',
    icon: 'fas fa-handshake',
    summary: '已进入最终候选名单',
    detail: '面试结果分析：1. 技术评分优秀；2. 沟通表达良好；3. 综合素质达标；4. 团队匹配度高。预计薪资范围25-35k。',
    color: '#ff006e',
    progress: 90,
    resources: [
      { title: '薪资水平报告', link: '#' },
      { title: '公司文化分析', link: '#' },
      { title: '福利待遇指南', link: '#' }
    ]
  }
])

const timelineItems = ref([
  {
    title: '第一阶段',
    description: '基础知识巩固与小型项目实践',
    date: '1-2个月'
  },
  {
    title: '第二阶段',
    description: '中型项目开发与架构设计',
    date: '3-4个月'
  },
  {
    title: '第三阶段',
    description: '复杂系统设计与团队协作',
    date: '5-6个月'
  },
  {
    title: '第四阶段',
    description: '技术领导力培养与职业发展',
    date: '6个月以上'
  }
])

const currentStep = ref(steps.value[0])
const showStepModal = ref(false)

const showStepDetail = (step: any) => {
  currentStep.value = step
  showStepModal.value = true
}

// 页脚数据
const footerColumns = ref([
  {
    title: '关于AI分析',
    links: [
      { icon: 'fas fa-robot', text: '分析算法说明', url: '#' },
      { icon: 'fas fa-chart-line', text: '数据采集方式', url: '#' },
      { icon: 'fas fa-shield-alt', text: '隐私保护政策', url: '#' },
      { icon: 'fas fa-question-circle', text: '常见问题', url: '#' }
    ]
  },
  {
    title: '候选人服务',
    links: [
      { icon: 'fas fa-user-tie', text: '职业咨询', url: '#' },
      { icon: 'fas fa-book-open', text: '学习资源', url: '#' },
      { icon: 'fas fa-project-diagram', text: '项目实践', url: '#' },
      { icon: 'fas fa-file-alt', text: '简历优化', url: '#' }
    ]
  },
  {
    title: '企业服务',
    links: [
      { icon: 'fas fa-bullhorn', text: '发布职位', url: '#' },
      { icon: 'fas fa-search', text: '人才搜索', url: '#' },
      { icon: 'fas fa-chart-pie', text: '分析报告', url: '#' },
      { icon: 'fas fa-cogs', text: '企业解决方案', url: '#' }
    ]
  },
  {
    title: '联系我们',
    links: [
      { icon: 'fas fa-envelope', text: 'contact@airesume.com', url: 'mailto:contact@airesume.com' },
      { icon: 'fas fa-phone', text: '400-888-9999', url: 'tel:4008889999' },
      { icon: 'fas fa-map-marker-alt', text: '北京市海淀区科技园路88号', url: '#' }
    ]
  }
])

// 下载选项
const downloadOptions = ref([
  { id: 'video', label: '包含面试视频', checked: true },
  { id: 'charts', label: '包含分析图表', checked: true },
  { id: 'feedback', label: '包含AI反馈', checked: true },
  { id: 'suggestions', label: '包含发展建议', checked: true }
])

const showDownloadModal = ref(false)

// 计算属性
const legendData = computed(() => {
  return [
    { label: '技术能力', value: '91/100', color: '#4cc9f0' },
    { label: '沟通表达', value: '85/100', color: '#3a86ff' },
    { label: '综合素质', value: '83/100', color: '#8338ec' },
    { label: '岗位匹配', value: '89%', color: '#ff006e' }
  ]
})

const downloadReport = (format: string) => {
  alert(`开始下载${format.toUpperCase()}格式报告`)
  showDownloadModal.value = false
}

// 初始化图表
onMounted(() => {
  if (radarChart.value) {
    new Chart(radarChart.value, {
      type: 'radar',
      data: {
        labels: ['JavaScript', 'React', '算法', '系统设计', '沟通', '团队协作', '学习能力'],
        datasets: [
          {
            label: '候选人能力',
            data: [94, 89, 87, 82, 85, 85, 82],
            backgroundColor: 'rgba(76, 201, 240, 0.2)',
            borderColor: '#4cc9f0',
            borderWidth: 2,
            pointBackgroundColor: '#4cc9f0',
            pointRadius: 4
          },
          {
            label: '岗位要求',
            data: [90, 85, 80, 85, 80, 80, 75],
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            borderColor: 'rgba(255, 255, 255, 0.5)',
            borderWidth: 1,
            pointBackgroundColor: 'rgba(255, 255, 255, 0.5)',
            pointRadius: 3
          }
        ]
      },
      options: {
        scales: {
          r: {
            angleLines: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            pointLabels: {
              color: 'rgba(255, 255, 255, 0.8)'
            },
            ticks: {
              backdropColor: 'transparent',
              color: 'rgba(255, 255, 255, 0.5)'
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: 'rgba(255, 255, 255, 0.8)'
            }
          }
        }
      }
    })
  }

  if (emotionChart.value) {
    new Chart(emotionChart.value, {
      type: 'doughnut',
      data: {
        labels: ['积极情绪', '中性情绪', '消极情绪'],
        datasets: [{
          data: [82, 12, 6],
          backgroundColor: ['#4cc9f0', '#3a86ff', '#ff006e'],
          borderWidth: 0
        }]
      },
      options: {
        cutout: '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: 'rgba(255, 255, 255, 0.8)',
              padding: 20
            }
          }
        }
      }
    })
  }

  if (emotionWaveChart.value) {
    new Chart(emotionWaveChart.value, {
      type: 'line',
      data: {
        labels: Array.from({ length: 20 }, (_, i) => `${i * 3}:00`),
        datasets: [
          {
            label: '情绪波动',
            data: [0.2, 0.4, 0.6, 0.8, 0.7, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.6, 0.8, 0.9, 0.7, 0.5, 0.3, 0.4, 0.6, 0.8],
            borderColor: '#4cc9f0',
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            backgroundColor: 'rgba(76, 201, 240, 0.1)'
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.7)'
            }
          },
          y: {
            min: 0,
            max: 1,
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.7)'
            }
          }
        },
        plugins: {
          legend: {
            display: false
          }
        }
      }
    })
  }
})
</script>

<style>
/* 基础样式 */
:root {
  --primary-color: #4CC9F0;
  --secondary-color: #4361EE;
  --accent-color: #48CAE4;
  --success-color: #38b000;
  --warning-color: #ffaa00;
  --danger-color: #ef233c;
  
  --dark-bg: #0f0f1b;
  --dark-card: rgba(15, 15, 27, 0.7);
  --dark-text: rgba(255, 255, 255, 0.95);
  --dark-text-secondary: rgba(255, 255, 255, 0.8);
  --dark-text-tertiary: rgba(255, 255, 255, 0.6);
  
  --light-bg: #f8f9fa;
  --light-card: rgba(255, 255, 255, 0.9);
  --light-text: #212529;
  --light-text-secondary: #495057;
  --light-text-tertiary: #6c757d;
  
  --bg-color: var(--dark-bg);
  --card-bg: var(--dark-card);
  --text-primary: var(--dark-text);
  --text-secondary: var(--dark-text-secondary);
  --text-tertiary: var(--dark-text-tertiary);
  --border-color: rgba(76, 201, 240, 0.2);
}

.light-mode {
  --bg-color: var(--light-bg);
  --card-bg: var(--light-card);
  --text-primary: var(--light-text);
  --text-secondary: var(--light-text-secondary);
  --text-tertiary: var(--light-text-tertiary);
  --border-color: rgba(0, 0, 0, 0.1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', 'Microsoft YaHei', sans-serif;
}

body {
  background-color: var(--bg-color);
  color: var(--text-primary);
  line-height: 1.6;
}

a {
  color: var(--primary-color);
  text-decoration: none;
  transition: all 0.3s;
}

a:hover {
  color: var(--accent-color);
}

img {
  max-width: 100%;
  height: auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 背景元素 */
.cyber-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(76, 201, 240, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(76, 201, 240, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  z-index: 0;
  animation: gridMove 20s linear infinite;
}

.cyber-pulse {
  position: fixed;
  width: 300vw;
  height: 300vh;
  left: -100vw;
  top: -100vh;
  background: radial-gradient(circle, rgba(67, 97, 238, 0.05) 0%, transparent 70%);
  animation: pulse 15s ease infinite;
  z-index: 0;
}

.cyber-orb {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(76, 201, 240, 0.1) 0%, transparent 70%);
  filter: blur(30px);
  animation: floatOrb 15s infinite ease-in-out;
  z-index: 0;
}

/* 头部样式 */
.cyber-header {
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(15, 15, 27, 0.7);
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(to right, var(--accent-color), var(--primary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: flex;
  align-items: center;
  text-shadow: 0 0 10px rgba(76, 201, 240, 0.5);
  letter-spacing: 1px;
}

.logo i {
  margin-right: 10px;
  font-size: 28px;
  animation: float 3s ease-in-out infinite;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.cyber-btn {
  background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
  display: flex;
  align-items: center;
  font-size: 14px;
}

.cyber-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(67, 97, 238, 0.6);
}

.cyber-btn i {
  margin-right: 8px;
}

/* 主布局 */
.main-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 30px;
  margin: 30px 0;
}

/* 侧边栏 */
.sidebar {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  height: fit-content;
  position: sticky;
  top: 100px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.candidate-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: white;
}

.candidate-info h3 {
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.candidate-info p {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.sidebar-nav ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.sidebar-nav li {
  padding: 12px 15px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  position: relative;
  transition: all 0.3s;
}

.sidebar-nav li:hover {
  background: rgba(76, 201, 240, 0.1);
}

.sidebar-nav li.active {
  background: rgba(76, 201, 240, 0.2);
  color: var(--accent-color);
}

.sidebar-nav li.active .nav-indicator {
  opacity: 1;
}

.sidebar-nav li i {
  font-size: 1rem;
  margin-right: 12px;
  width: 20px;
  text-align: center;
}

.sidebar-nav li span {
  flex: 1;
}

.nav-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-color);
  opacity: 0;
  transition: all 0.3s;
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.match-score {
  margin-bottom: 20px;
}
/* 侧边栏样式调整 */
.sidebar-footer .match-score {
  text-align: center;
  margin-bottom: 15px;
}

.sidebar-footer .match-score span {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--accent-color);
  display: block;
  line-height: 1;
}

.sidebar-footer .match-score p {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

/* 岗位匹配部分的球体样式 */
.match-sphere {
  position: relative;
  width: 100%;
  height: 300px;
  perspective: 1000px;
}

.sphere-surface {
  position: absolute;
  width: 200px;
  height: 200px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: rgba(76, 201, 240, 0.1);
  box-shadow: 0 0 30px rgba(76, 201, 240, 0.2);
  animation: rotateSphere 20s infinite linear;
}

.skill-point {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  left: 50%;
  top: 50%;
  margin-left: -6px;
  margin-top: -6px;
  transform-origin: center;
  transition: all 0.3s;
}

.skill-point:hover {
  transform: scale(1.5) !important;
  z-index: 10;
}

.point-tooltip {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.skill-point:hover .point-tooltip {
  opacity: 1;
}

@keyframes rotateSphere {
  0% { transform: translate(-50%, -50%) rotateX(0) rotateY(0); }
  100% { transform: translate(-50%, -50%) rotateX(360deg) rotateY(360deg); }
}
.score-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  position: relative;
}

.score-circle::before {
  content: '';
  position: absolute;
  inset: 5px;
  border-radius: 50%;
  border: 2px dashed rgba(255, 255, 255, 0.3);
}

.score-circle span {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.sidebar-footer p {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.feedback-btn {
  width: 100%;
  justify-content: center;
  margin-top: 15px;
}

/* 内容区域 */
.content-area {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 25px;
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
}

.cyber-title {
  font-size: 2rem;
  margin-bottom: 10px;
  background: linear-gradient(120deg, #48CAE4, #4361EE, #48CAE4);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s linear infinite;
}

.cyber-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 20px;
}

.section-header {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.section-header h2 {
  font-size: 1.4rem;
  display: flex;
  align-items: center;
}

.section-header h2 i {
  margin-right: 12px;
  color: var(--accent-color);
}

/* 报告概览 */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.overview-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  overflow: hidden;
  transition: all 0.3s;
}

.overview-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.card-header {
  padding: 15px;
  background: rgba(76, 201, 240, 0.1);
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
}

.card-header i {
  font-size: 1.2rem;
  color: var(--accent-color);
  margin-right: 10px;
}

.card-header h3 {
  font-size: 1rem;
}

.card-body {
  padding: 15px;
}

.radar-chart,
.emotion-chart,
.emotion-chart canvas,
.heatmap-chart {
  width: 100% !important;
  height: auto !important;
  aspect-ratio: 1 / 1;
  margin-bottom: 15px;
}

.match-chart {
  position: relative;
  width: 100%;
  height: 300px;
  margin-bottom: 15px;
}

.match-sphere {
  position: relative;
  width: 100%;
  height: 100%;
  perspective: 1000px;
}

.sphere-surface {
  position: absolute;
  width: 200px;
  height: 200px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: rgba(76, 201, 240, 0.1);
  box-shadow: 0 0 30px rgba(76, 201, 240, 0.2);
  animation: rotateSphere 20s infinite linear;
}

.skill-point {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  left: 50%;
  top: 50%;
  margin-left: -6px;
  margin-top: -6px;
  transform-origin: center;
  transition: all 0.3s;
}

.skill-point:hover {
  transform: scale(1.5) !important;
  z-index: 10;
}

.point-tooltip {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.skill-point:hover .point-tooltip {
  opacity: 1;
}

.chart-legend {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
}

.legend-label {
  flex: 1;
  color: var(--text-secondary);
}

.legend-value {
  font-weight: 600;
  color: var(--accent-color);
}

.emotion-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-label {
  flex: 1;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 0.85rem;
  font-weight: 600;
  min-width: 40px;
  text-align: right;
  margin-right: 10px;
}

.stat-bar {
  width: 80px;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 3px;
}

.match-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.match-item {
  margin-bottom: 10px;
}

.match-skill {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.85rem;
}

.match-demand {
  color: var(--text-secondary);
}

.match-comparison {
  display: flex;
  align-items: center;
  gap: 10px;
}

.match-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  display: flex;
  position: relative;
}

.match-candidate {
  height: 100%;
  background: var(--primary-color);
  border-radius: 4px 0 0 4px;
  position: relative;
  z-index: 1;
}

.match-required {
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 0 4px 4px 0;
  position: absolute;
  left: 0;
}

.match-percent {
  font-weight: 600;
  color: var(--accent-color);
  min-width: 40px;
  text-align: right;
  font-size: 0.85rem;
}

.steps-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
}

.step-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 15px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: all 0.3s;
}

.step-card:hover {
  background: rgba(76, 201, 240, 0.1);
  transform: translateY(-3px);
}

.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
  margin-bottom: 10px;
}

.step-card h4 {
  font-size: 0.85rem;
  margin-bottom: 10px;
}

.step-progress {
  width: 100%;
}

.step-progress .progress-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  margin-bottom: 5px;
  overflow: hidden;
}

.step-progress .progress-fill {
  height: 100%;
  border-radius: 2px;
  background: linear-gradient(to right, var(--primary-color), var(--accent-color));
}

.step-progress span {
  font-size: 0.7rem;
  color: var(--text-secondary);
}

/* 视频分析 */
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
}

.video-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border-color);
  transition: all 0.3s;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.video-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.video-header h3 {
  font-size: 1.1rem;
}

.video-score {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.video-score span {
  color: var(--accent-color);
}

.video-container {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  aspect-ratio: 16/9;
  background: #000;
  margin-bottom: 15px;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(15, 15, 27, 0.8), rgba(67, 97, 238, 0.5));
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.video-placeholder:hover {
  background: linear-gradient(135deg, rgba(15, 15, 27, 0.9), rgba(67, 97, 238, 0.6));
}

.video-placeholder i {
  font-size: 3rem;
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 0.8);
}

.video-placeholder span {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
}

.video-timeline {
  position: absolute;
  bottom: 50px;
  left: 0;
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
}

.timeline-marker {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  top: -2px;
  transform: translateX(-50%);
  cursor: pointer;
  transition: all 0.3s;
}

.timeline-marker:hover {
  transform: translateX(-50%) scale(1.5);
}

.video-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  padding: 12px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

.video-controls button {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-controls button:hover {
  background: var(--accent-color);
  transform: scale(1.1);
}

.video-insights {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
}

.insight-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 10px;
  text-align: center;
}

.insight-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 5px;
}

.insight-value {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--accent-color);
}

/* 能力分析 */
.skills-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.skills-chart {
  position: relative;
  width: 100%;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
}

.skills-web {
  position: relative;
  width: 100%;
  height: 100%;
}

.web-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  transform-origin: center;
}

.web-line {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  transform-origin: center;
}

.web-line::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 70%;
  height: 1px;
  background: hsla(var(--hue), 80%, 60%, 0.3);
  transform: translate(-50%, -50%) rotate(0deg);
}

.web-node {
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background: hsla(var(--hue), 80%, 60%, var(--alpha));
  cursor: pointer;
  transition: all 0.3s;
}

.web-node:hover {
  transform: translate(-50%, -50%) scale(1.5);
  box-shadow: 0 0 10px hsla(var(--hue), 80%, 60%, 0.8);
}

.node-tooltip {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.web-node:hover .node-tooltip {
  opacity: 1;
}

.web-center {
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--primary-color);
  box-shadow: 0 0 15px rgba(76, 201, 240, 0.5);
}

.skills-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.skill-category {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 15px;
  border: 1px solid var(--border-color);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.category-header h3 {
  font-size: 1.1rem;
}

.category-score {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-score span {
  font-weight: 600;
  color: var(--accent-color);
}

.score-bar {
  width: 80px;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 3px;
}

.skill-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skill-item {
  margin-bottom: 10px;
}

.skill-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.skill-name {
  color: var(--text-secondary);
}

.skill-value {
  font-weight: 600;
  color: var(--accent-color);
}

.skill-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.skill-fill {
  height: 100%;
  border-radius: 3px;
  position: relative;
}

.skill-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: progressShine 2s infinite;
}

/* 情绪分析 */
.emotion-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.emotion-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border-color);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-header h3 {
  font-size: 1.1rem;
}

.card-score {
  font-weight: 600;
  color: var(--accent-color);
  background: rgba(76, 201, 240, 0.1);
  padding: 4px 12px;
  border-radius: 30px;
  font-size: 0.9rem;
}

.emotion-chart,
.heatmap-chart {
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 15px;
}

.heatmap-grid {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.heatmap-row {
  display: flex;
  gap: 2px;
}

.heatmap-cell {
  flex: 1;
  aspect-ratio: 1;
  background: hsla(var(--hue), 80%, 60%, var(--intensity));
  border-radius: 2px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s;
}

.heatmap-cell:hover {
  transform: scale(1.2);
  z-index: 2;
}

.heatmap-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 5px;
  border-radius: 4px;
  font-size: 0.7rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.heatmap-cell:hover .heatmap-tooltip {
  opacity: 1;
}

.emotion-keyframes {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.keyframe {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.keyframe-time {
  font-size: 0.7rem;
  color: white;
  margin-bottom: 5px;
  background: rgba(0, 0, 0, 0.5);
  padding: 2px 6px;
  border-radius: 10px;
}

.keyframe-emotion {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  margin-bottom: 5px;
}

.keyframe-label {
  font-size: 0.7rem;
  color: white;
  background: rgba(0, 0, 0, 0.5);
  padding: 2px 6px;
  border-radius: 10px;
}

.emotion-stats {
  margin-top: 15px;
}

.stat-item {
  margin-bottom: 10px;
}

.stat-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.stat-label {
  color: var(--text-secondary);
}

.stat-value {
  font-weight: 600;
  color: var(--accent-color);
}

.stat-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 3px;
}

/* 岗位匹配分析 */
.match-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.match-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.match-sphere {
  position: relative;
  width: 100%;
  height: 100%;
  perspective: 1000px;
}

.match-score {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.match-score span {
  font-size: 3rem;
  font-weight: 700;
  color: var(--accent-color);
  display: block;
  line-height: 1;
}

.match-score p {
  font-size: 1rem;
  color: var(--text-secondary);
}

.match-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.match-item {
  margin-bottom: 15px;
}

.match-skill {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.match-demand {
  color: var(--text-secondary);
}

.match-comparison {
  display: flex;
  align-items: center;
  gap: 10px;
}

.match-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  display: flex;
  position: relative;
}

.match-candidate {
  height: 100%;
  background: var(--primary-color);
  border-radius: 4px 0 0 4px;
  position: relative;
  z-index: 1;
}

.match-required {
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 0 4px 4px 0;
  position: absolute;
  left: 0;
}

.match-percent {
  font-weight: 600;
  color: var(--accent-color);
  min-width: 40px;
  text-align: right;
}

.match-summary {
  background: rgba(76, 201, 240, 0.1);
  border-radius: 8px;
  padding: 15px;
  margin-top: 20px;
}

.match-summary h4 {
  color: var(--accent-color);
  margin-bottom: 10px;
}

.match-summary p {
  font-size: 0.9rem;
  line-height: 1.6;
}

/* 页脚 */
.cyber-footer {
  background: rgba(15, 15, 27, 0.9);
  padding: 40px 0 20px;
  border-top: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
  margin-top: 50px;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 40px;
  margin-bottom: 30px;
}

.footer-brand {
  display: flex;
  flex-direction: column;
}

.footer-brand .logo {
  margin-bottom: 15px;
}

.footer-brand p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-links a {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all 0.3s;
}

.social-links a:hover {
  background: var(--accent-color);
  color: white;
  transform: translateY(-3px);
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
}

.link-column h3 {
  font-size: 1rem;
  margin-bottom: 15px;
  padding-bottom: 8px;
  position: relative;
  color: var(--accent-color);
}

.link-column h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 30px;
  height: 2px;
  background: linear-gradient(to right, var(--accent-color), var(--primary-color));
}

.link-column ul {
  list-style: none;
}

.link-column ul li {
  margin-bottom: 10px;
}

.link-column ul li a {
  color: var(--text-secondary);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  transition: all 0.3s;
}

.link-column ul li a:hover {
  color: var(--accent-color);
  padding-left: 5px;
}

.link-column ul li a i {
  margin-right: 8px;
  font-size: 0.8rem;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 25px;
  border-top: 1px solid var(--border-color);
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.footer-meta {
  display: flex;
  gap: 15px;
}

.footer-meta a {
  color: var(--text-secondary);
  transition: all 0.3s;
}

.footer-meta a:hover {
  color: var(--accent-color);
}

/* 模态框 */
.cyber-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 25px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  border: 1px solid var(--accent-color);
  box-shadow: 0 0 25px rgba(76, 201, 240, 0.5);
}

.feedback-modal {
  max-width: 700px;
}

.step-modal {
  max-width: 600px;
}

.download-modal {
  max-width: 500px;
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.close-btn:hover {
  background: var(--danger-color);
  transform: rotate(90deg);
}

.modal-content h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.modal-content h3 i {
  margin-right: 12px;
}

.modal-body {
  margin-top: 15px;
}

/* 反馈模态框 */
.feedback-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.feedback-tabs button {
  background: none;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-secondary);
  position: relative;
  transition: all 0.3s;
}

.feedback-tabs button i {
  margin-right: 8px;
}

.feedback-tabs button.active {
  color: var(--accent-color);
  font-weight: 600;
}

.feedback-tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--accent-color);
}

.feedback-content {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid var(--border-color);
}

.feedback-pane h4 {
  font-size: 1.1rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  color: var(--accent-color);
}

.feedback-pane h4 i {
  margin-right: 10px;
}

.strength-list,
.improvement-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.strength-item,
.improvement-item {
  display: flex;
  gap: 12px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.strength-item:last-child,
.improvement-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.strength-icon,
.improvement-icon {
  width: 36px;
  height: 36px;
  background: rgba(76, 201, 240, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent-color);
  flex-shrink: 0;
}

.improvement-icon {
  background: rgba(255, 0, 110, 0.1);
  color: #ff006e;
}

.strength-text h5,
.improvement-text h5 {
  font-size: 0.95rem;
  margin-bottom: 8px;
  color: var(--accent-color);
}

.improvement-text h5 {
  color: #ff006e;
}

.strength-text p,
.improvement-text p {
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 8px;
}

.strength-evidence,
.improvement-resources {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.strength-evidence span,
.improvement-resources span {
  font-weight: 600;
  color: var(--accent-color);
  display: block;
  margin-bottom: 5px;
}

.improvement-resources span {
  color: #ff006e;
}

.strength-evidence ul,
.improvement-resources ul {
  padding-left: 20px;
}

.strength-evidence li,
.improvement-resources li {
  margin-bottom: 3px;
}

.summary-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.summary-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid var(--border-color);
}

.summary-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.summary-header i {
  width: 30px;
  height: 30px;
  background: rgba(76, 201, 240, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  color: var(--accent-color);
}

.summary-header h5 {
  flex: 1;
  font-size: 0.95rem;
}

.summary-score {
  font-weight: 600;
  color: var(--accent-color);
}

.summary-body p {
  font-size: 0.85rem;
  line-height: 1.6;
  margin-bottom: 8px;
}

.summary-highlights {
  font-size: 0.8rem;
}

.highlight {
  display: flex;
  margin-bottom: 5px;
}

.highlight-label {
  font-weight: 600;
  color: var(--accent-color);
  min-width: 80px;
}

.highlight-value {
  color: var(--text-secondary);
}

/* 发展建议模态框 */
.step-detail {
  padding: 10px;
}

.step-detail p {
  font-size: 0.95rem;
  line-height: 1.7;
  margin-bottom: 20px;
}

.step-progress {
  margin-bottom: 25px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
}

.step-resources {
  margin-bottom: 25px;
}

.step-resources h4 {
  font-size: 1rem;
  color: var(--accent-color);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.step-resources h4::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 16px;
  background: var(--accent-color);
  margin-right: 8px;
}

.step-resources ul {
  padding-left: 20px;
}

.step-resources li {
  margin-bottom: 8px;
}

.step-resources a {
  color: var(--primary-color);
  font-size: 0.9rem;
}

.step-timeline {
  margin-bottom: 25px;
}

.step-timeline h4 {
  font-size: 1rem;
  color: var(--accent-color);
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.step-timeline h4::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 16px;
  background: var(--accent-color);
  margin-right: 8px;
}

.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 0;
  left: 10px;
  height: 100%;
  width: 2px;
  background: rgba(76, 201, 240, 0.3);
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
}

.timeline-dot {
  position: absolute;
  left: -30px;
  top: 5px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.timeline-content h5 {
  font-size: 0.95rem;
  margin-bottom: 5px;
}

.timeline-content p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 5px;
}

.timeline-date {
  font-size: 0.8rem;
  color: var(--accent-color);
  font-weight: 600;
}

/* 下载报告模态框 */
.download-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-top: 20px;
}

.download-option {
  background: rgba(76, 201, 240, 0.1);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.download-option:hover {
  background: var(--accent-color);
  transform: translateY(-3px);
}

.download-option i {
  font-size: 1.8rem;
}

.download-customize {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.download-customize h4 {
  font-size: 1rem;
  margin-bottom: 15px;
  color: var(--accent-color);
}

.customize-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.customize-options label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--text-secondary);
  cursor: pointer;
}

.customize-options input {
  accent-color: var(--accent-color);
}

/* 动画 */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(-50px, -50px); }
}

@keyframes pulse {
  0%, 100% { transform: scale(0.5); opacity: 0.5; }
  50% { transform: scale(1); opacity: 0.2; }
}

@keyframes floatOrb {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.1); }
  50% { transform: translate(0, -40px) scale(0.9); }
  75% { transform: translate(-30px, -20px) scale(1.05); }
}

@keyframes progressShine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes shine {
  to { background-position: 200% center; }
}

@keyframes rotateSphere {
  0% { transform: translate(-50%, -50%) rotateX(0) rotateY(0); }
  100% { transform: translate(-50%, -50%) rotateX(360deg) rotateY(360deg); }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-layout {
    grid-template-columns: 240px 1fr;
  }
}

@media (max-width: 992px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    position: static;
    margin-bottom: 30px;
  }
  
  .skills-container,
  .match-container {
    grid-template-columns: 1fr;
  }
  
  .skills-chart,
  .match-visual {
    margin-bottom: 30px;
  }
  
  .video-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .cyber-title {
    font-size: 1.8rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .feedback-tabs {
    flex-wrap: wrap;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 576px) {
  .cyber-title {
    font-size: 1.5rem;
  }
  
  .cyber-subtitle {
    font-size: 0.95rem;
  }
  
  .section-header h2 {
    font-size: 1.2rem;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-actions button {
    width: 100%;
  }
}
</style>