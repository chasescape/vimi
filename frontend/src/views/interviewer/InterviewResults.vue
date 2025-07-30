<template>
  <div class="interview-result-page">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <h2 class="title">AI面试分析结果</h2>
      <el-button type="primary" @click="downloadReport">下载报告</el-button>
    </div>

    <!-- 主体布局：左侧候选人信息 + 右侧分析内容 -->
    <div class="main-layout">
      <!-- 左侧候选人信息栏 -->
      <aside class="candidate-info">
        <div class="avatar-box">
          <div class="avatar" :style="{ background: avatarGradient }"></div>
          <div class="name">{{ candidateInfo.name }}</div>
          <div class="position">{{ candidateInfo.position }}</div>
        </div>

        <!-- 导航标签 -->
        <el-tabs v-model="activeTab" class="tab-nav" @tab-click="handleTabChange">
          <el-tab-pane label="报告概览" name="overview"></el-tab-pane>
          <el-tab-pane label="面试录像" name="video"></el-tab-pane>
          <el-tab-pane label="能力图谱" name="ability"></el-tab-pane>
          <el-tab-pane label="情绪分析" name="emotion"></el-tab-pane>
          <el-tab-pane label="岗位匹配" name="match"></el-tab-pane>
        </el-tabs>

        <el-button type="primary" class="ai-feedback-btn">AI反馈</el-button>
      </aside>

      <!-- 右侧内容区域 -->
      <section class="content-wrapper">
        <template v-if="activeTab === 'overview'">
          <div class="analysis-title">
            <h3>3D动态面试分析报告</h3>
            <p>基于多模态AI深度分析的全面评估</p>
          </div>

          <!-- 核心数据概览 -->
          <div class="core-metrics">
            <div class="metric-item">
              <span>技术能力</span>
              <div class="score">{{ candidateInfo.scores.technical }}/100</div>
            </div>
            <div class="metric-item">
              <span>沟通表达</span>
              <div class="score">{{ candidateInfo.scores.communication }}/100</div>
            </div>
            <div class="metric-item">
              <span>综合素质</span>
              <div class="score">{{ candidateInfo.scores.comprehensive }}/100</div>
            </div>
            <div class="metric-item">
              <span>岗位匹配</span>
              <div class="score">{{ candidateInfo.scores.match }}/100</div>
            </div>
          </div>

          <!-- 双栏图表区 -->
          <div class="chart-layout">
            <!-- 能力雷达图 -->
            <div class="chart-card">
              <h4>能力雷达图</h4>
              <div id="radar-chart" style="width: 300px; height: 300px;"></div>
            </div>

            <!-- 情绪稳定性 -->
            <div class="chart-card">
              <h4>情绪稳定性</h4>
              <div id="emotion-chart" style="width: 300px; height: 300px;"></div>
            </div>
          </div>
        </template>

        <template v-else-if="activeTab === 'video'">
          <div class="video-player">
            <video
              class="interview-video"
              :src="candidateInfo.videoUrl"
              controls
              autoplay
              muted
              playsinline
            ></video>
          </div>
        </template>

        <template v-else-if="activeTab === 'ability'">
          <div class="ability-graph">
            <!-- 这里可替换为实际能力图谱组件 -->
            <p>能力图谱可视化内容（可集成ECharts或SVG）</p>
          </div>
        </template>

        <template v-else-if="activeTab === 'emotion'">
          <div class="emotion-analysis">
            <h4>情绪分析详情</h4>
            <div class="emotion-distribution">
              <div
                class="emotion-item"
                :style="{ background: color }"
                v-for="(percent, emotion) in candidateInfo.emotionDistribution"
                :key="emotion"
              >
                {{ emotion }}: {{ percent }}%
              </div>
            </div>
          </div>
        </template>

        <template v-else-if="activeTab === 'match'">
          <div class="job-match">
            <h4>岗位匹配详情</h4>
            <ul class="match-details">
              <li v-for="(score, item) in candidateInfo.matchDetails" :key="item">
                {{ item }}: {{ score }}%
              </li>
            </ul>
          </div>
        </template>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElTabs, ElTabPane, ElButton } from 'element-plus'
import * as echarts from 'echarts' // 引入ECharts

// 模拟候选人数据（实际应从接口获取）
const candidateInfo = ref({
  name: '张小明',
  position: '高级前端开发工程师',
  videoUrl: 'https://www.w3school.com.cn/example/html5/horse.ogg', // 模拟视频地址
  scores: {
    technical: 91,
    communication: 85,
    comprehensive: 83,
    match: 89
  },
  emotionDistribution: {
    '积极情绪': 82,
    '中性情绪': 12,
    '消极情绪': 6
  },
  matchDetails: {
    '技能匹配': 90,
    '经验匹配': 85,
    '潜力匹配': 88
  }
})

const activeTab = ref('overview')
const avatarGradient = ref('linear-gradient(135deg, #667eea 0%, #764ba2 100%)')

// 初始化图表
onMounted(() => {
  nextTick(() => {
    renderRadarChart()
    renderEmotionChart()
  })
})

// 渲染能力雷达图
function renderRadarChart() {
  const radarChart = echarts.init(document.getElementById('radar-chart'))
  const option = {
    title: { text: '' },
    tooltip: { trigger: 'item' },
    legend: { show: false },
    radar: {
      indicator: [
        { name: 'JavaScript', max: 100 },
        { name: 'React', max: 100 },
        { name: '算法', max: 100 },
        { name: '系统设计', max: 100 },
        { name: '沟通', max: 100 },
        { name: '团队协作', max: 100 },
        { name: '学习能力', max: 100 }
      ]
    },
    series: [
      {
        name: '能力对比',
        type: 'radar',
        data: [
          {
            value: [90, 85, 80, 82, 88, 92, 86], // 候选人能力
            name: '候选人能力'
          },
          {
            value: [95, 90, 85, 90, 90, 95, 90], // 岗位要求
            name: '岗位要求'
          }
        ],
        label: { show: true },
        areaStyle: { opacity: 0.2 }
      }
    ]
  }
  radarChart.setOption(option)
}

// 渲染情绪环形图
function renderEmotionChart() {
  const emotionChart = echarts.init(document.getElementById('emotion-chart'))
  const option = {
    title: { text: '' },
    tooltip: { trigger: 'item' },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['积极情绪', '中性情绪', '消极情绪']
    },
    series: [
      {
        name: '情绪分布',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: { show: false, position: 'center' },
        emphasis: { label: { show: true, fontSize: '16', fontWeight: 'bold' } },
        labelLine: { show: false },
        data: [
          { value: 82, name: '积极情绪' },
          { value: 12, name: '中性情绪' },
          { value: 6, name: '消极情绪' }
        ]
      }
    ]
  }
  emotionChart.setOption(option)
}

// Tab切换处理
function handleTabChange(tab) {
  activeTab.value = tab.name
}

// 下载报告（模拟）
function downloadReport() {
  alert('已触发报告下载逻辑（可集成实际PDF生成/下载）')
}
</script>

<style scoped>
.interview-result-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 24px;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.main-layout {
  display: flex;
  gap: 24px;
}

/* 候选人信息栏 */
.candidate-info {
  width: 260px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
  box-sizing: border-box;
}

.avatar-box {
  text-align: center;
  margin-bottom: 20px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin: 0 auto 12px;
}

.name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.position {
  font-size: 14px;
  color: #666;
}

.tab-nav {
  margin: 20px 0;
}

.ai-feedback-btn {
  width: 100%;
}

/* 内容区域 */
.content-wrapper {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 24px;
  box-sizing: border-box;
}

.analysis-title {
  margin-bottom: 24px;
}

.analysis-title h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.analysis-title p {
  font-size: 14px;
  color: #666;
}

.core-metrics {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}

.metric-item {
  flex: 1;
  text-align: center;
  padding: 16px;
  background: #f9fafc;
  border-radius: 8px;
}

.metric-item span {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.score {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.chart-layout {
  display: flex;
  gap: 24px;
}

.chart-card {
  flex: 1;
  background: #f9fafc;
  border-radius: 8px;
  padding: 20px;
  box-sizing: border-box;
}

.chart-card h4 {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 16px;
}

/* 面试录像 */
.video-player {
  text-align: center;
}

.interview-video {
  width: 100%;
  max-width: 600px;
  border-radius: 8px;
}

/* 能力图谱/情绪分析/岗位匹配通用样式 */
.ability-graph,
.emotion-analysis,
.job-match {
  padding: 20px;
  background: #f9fafc;
  border-radius: 8px;
}

.emotion-distribution {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 20px;
}

.emotion-item {
  padding: 8px 16px;
  border-radius: 4px;
  color: #fff;
}

.match-details {
  list-style: none;
  padding: 0;
  margin: 0;
}

.match-details li {
  padding: 8px 0;
  border-bottom: 1px dashed #eee;
}

/* 响应式适配 */
@media (max-width: 992px) {
  .main-layout {
    flex-direction: column;
  }
  .candidate-info {
    width: 100%;
  }
  .chart-layout {
    flex-direction: column;
  }
}
</style>