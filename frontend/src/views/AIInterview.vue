<template>
  <div :class="['container', { 'dark-mode': isDarkMode }]">
    <!-- 模式切换按钮 -->
    <button @click="toggleDarkMode" class="mode-toggle">
      {{ isDarkMode ? '☀️ 明亮模式' : '🌙 暗黑模式' }}
    </button>

    <!-- 顶部标题 -->
    <h1 class="main-title">虚拟人面试系统</h1>

    <div class="layout-grid">
      <!-- 左上角 - 应聘者信息（动态显示三个字段） -->
  <div class="panel candidate-info">
    <h2 class="panel-title">应聘者信息</h2>
    
    <!-- 添加照片展示框 -->
    <div class="avatar-container">
    <img :src="photoPath || '/default-avatar.jpg'" alt="应聘者照片" class="avatar-image">
    <div v-if="!photoPath" class="avatar-placeholder">
      <span>暂无照片</span>
    </div>
  </div>
    <div class="info-item">
      <span class="info-label">姓名：</span>
      <span class="info-value">{{ username }}</span>
    </div>
    <div class="info-item">
      <span class="info-label">职位：</span>
      <span class="info-value">{{ jobTitle }}</span>
    </div>
    <div class="info-item">
      <span class="info-label">职位类别：</span>
      <span class="info-value">{{ jobCategory }}</span>
    </div>
</div>

      <!-- 中间 - 虚拟人区域 -->
      <div class="panel virtual-human">
        <iframe
          ref="demoIframe"
          src="http://localhost:5173"
          allow="microphone; autoplay"
          class="virtual-human-iframe"
        ></iframe>
      </div>

      <!-- 右上角 - 视频区域 -->
      <div class="panel video-panel">
        <h2 class="panel-title">面试者视频</h2>
        <div class="video-container">
          <div class="video-placeholder">
            <span>视频预览区域</span>
            <button class="video-control-btn">开启摄像头</button>
          </div>
        </div>
      </div>

      <!-- 左下角 - 语音测评 -->
      <div class="panel evaluation-panel">
        <h2 class="panel-title">
          语音测评雷达图
          <span class="data-status">
            (数据{{ hasEvaluationData ? '已加载' : '加载中或无数据' }})
          </span>
        </h2>
        <div ref="evaluationChartRef" class="chart-container"></div>
      </div>

      <!-- 右下角 - 情绪分析 -->
      <div class="panel sentiment-panel">
        <h2 class="panel-title">
          情绪占比分析
          <span class="data-status">
            (数据{{ hasSentimentData ? '已加载' : '加载中或无数据' }})
          </span>
        </h2>
        <div ref="chartRef" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

/* ===== 状态区 ===== */
const username = ref('加载中...')
const jobTitle = ref('加载中...')
const jobCategory = ref('加载中...')

const subtitle = ref('')
const sendText = ref('')
const demoIframe = ref(null)
const tempBuffer = ref('')
const mainBuffer = ref('')
const photoPath = ref('')
const chartRef = ref(null)
let chartInstance = null
const sentimentData = ref({ positive: 0, neutral: 0, negative: 0 })
const hasSentimentData = ref(false)

const evaluationChartRef = ref(null)
let evaluationChartInstance = null
const evaluationResult = ref('')
const evaluationParsed = ref(null)
const hasEvaluationData = ref(false)

const isDarkMode = ref(false)

/* ===== 常量 ===== */
const MERGE_INTERVAL = 1000
const SAVE_INTERVAL = 3000

/* ===== 定时器句柄 ===== */
let mergeTimer = null
let saveTimer = null

/* ===== 明暗模式切换 ===== */
function toggleDarkMode() {
  isDarkMode.value = !isDarkMode.value
  nextTick(() => {
    renderChart()
    renderEvaluationChart()
  })
}

/* ===== 收到字幕 ===== */
function handleMessage(event) {
  if (event.origin !== 'http://localhost:5173') return

  if (event.data.type === 'subtitle_update') {
    const text = event.data.text || ''
    subtitle.value = text
    tempBuffer.value += text.endsWith(' ') ? text : text + ' '
  } else if (event.data.type === 'audio_blob') {
    const audioBase64 = event.data.audioData
    console.log('[收到音频数据]', audioBase64)
    uploadAudio(audioBase64)
  }
}

/* ===== 合并缓存 ===== */
function mergeTempToMain() {
  if (tempBuffer.value.trim()) {
    mainBuffer.value += tempBuffer.value
    console.log('[合并] 当前主缓存 =>', mainBuffer.value)
    tempBuffer.value = ''
  }
}

/* ===== 保存并分析 ===== */
async function saveToBackend() {
  mergeTempToMain()
  if (!mainBuffer.value.trim()) return

  try {
    const res = await axios.post('/api/voice_record/save', {
      user_id: 1,
      transcription: mainBuffer.value,
    })
    console.log('[保存成功]', res.data)

    const sentimentJson = res.data.sentiment || {}
    sentimentData.value = {
      positive: sentimentJson.positive || 0,
      neutral: sentimentJson.neutral || 0,
      negative: sentimentJson.negative || 0,
    }
    hasSentimentData.value = true

    await nextTick()
    renderChart()
  } catch (e) {
    console.error('[保存失败]', e)
  }
}

/* ===== 页面加载时获取最新情绪数据 ===== */
async function fetchLatestSentiment() {
  try {
    const res = await axios.get('/api/voice_record/latest_sentiment')
    if (res.data && res.data.sentiment) {
      sentimentData.value = {
        positive: res.data.sentiment.positive || 0,
        neutral: res.data.sentiment.neutral || 0,
        negative: res.data.sentiment.negative || 0,
      }
      hasSentimentData.value = true
    } else {
      hasSentimentData.value = false
    }
    await nextTick()
    renderChart()
  } catch (error) {
    console.error('[获取最新情绪失败]', error)
    hasSentimentData.value = false
    await nextTick()
    renderChart()
  }
}

/* ===== 上传音频到服务器 ===== */
async function uploadAudio(base64Audio) {
  try {
    const base64Data = base64Audio.split(',')[1]
    const binaryString = atob(base64Data)
    const len = binaryString.length
    const uint8Array = new Uint8Array(len)
    for (let i = 0; i < len; i++) {
      uint8Array[i] = binaryString.charCodeAt(i)
    }
    const blob = new Blob([uint8Array], { type: 'audio/webm' })

    const formData = new FormData()
    formData.append('file', blob, 'record.webm')
    formData.append('user_id', '1')
    formData.append('job_id', '3')

    const res = await axios.post('/api/apply/upload_audio', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    console.log('[音频上传成功]', res.data)
  } catch (error) {
    console.error('[音频上传失败]', error)
  }
}

/* ===== 获取语音测评结果 ===== */
async function fetchEvaluationResult() {
  try {
    const userId = 1
    const jobId = 3
    const res = await axios.get(`/api/apply/evaluation`, {
      params: { user_id: userId, job_id: jobId },
    })

    const result = res.data.evaluation_result || ''
    evaluationResult.value = result

    const parsed = JSON.parse(result)
    if (parsed && parsed.xml) {
      evaluationParsed.value = parseEvaluationXML(parsed.xml)
      hasEvaluationData.value = true
    } else {
      evaluationParsed.value = null
      hasEvaluationData.value = false
    }

    await nextTick()
    renderEvaluationChart()
  } catch (error) {
    console.error('[语音测评获取失败]', error)
    evaluationParsed.value = null
    hasEvaluationData.value = false
    await nextTick()
    renderEvaluationChart()
  }
}

/* ===== 解析语音测评XML ===== */
function parseEvaluationXML(xmlStr) {
  try {
    const parser = new DOMParser()
    const xmlDoc = parser.parseFromString(xmlStr, 'text/xml')
    const readNode = xmlDoc.querySelector('rec_paper > read_sentence')
    if (!readNode) {
      console.warn('[未找到评分节点]')
      return null
    }
    const getScore = (attr) => {
      const val = readNode.getAttribute(attr)
      return val ? parseFloat(parseFloat(val).toFixed(1)) : 0
    }
    return {
      fluency_score: getScore('fluency_score'),
      tone_score: getScore('tone_score'),
      phone_score: getScore('phone_score'),
      integrity_score: getScore('integrity_score'),
      total_score: getScore('total_score'),
    }
  } catch (err) {
    console.error('[XML解析失败]', err)
    return null
  }
}

/* ===== 渲染情绪柱状图 ===== */
function renderChart() {
  if (!chartRef.value) return
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }

  const textColor = isDarkMode.value ? '#00eaff' : '#333'
  const bgColor = isDarkMode.value ? '#0f1c2f' : '#fff'

  chartInstance.setOption({
    backgroundColor: bgColor,
    title: {
      text: '情绪分析占比',
      left: 'center',
      top: '5%',
      textStyle: {
        color: textColor,
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b} : {d}%',
      backgroundColor: isDarkMode.value ? '#1f1f1f' : '#fff',
      borderColor: isDarkMode.value ? '#00eaff' : '#ccc',
      textStyle: {
        color: textColor
      }
    },
    legend: {
      orient: 'horizontal',
      top: 'auto',
      bottom: '2%',
      textStyle: {
        color: textColor,
        fontSize: 13
      },
      itemGap: 25,
      data: ['积极情绪', '中性情绪', '消极情绪']
    },
    series: [
      {
        name: '情绪占比',
        type: 'pie',
        radius: ['45%', '65%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 8,
          borderColor: bgColor,
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{b}: {d}%',
          color: textColor
        },
        labelLine: {
          length: 15,
          length2: 10,
          lineStyle: {
            color: textColor
          }
        },
        data: [
          {
            value: sentimentData.value.positive,
            name: '积极情绪',
            itemStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 1,
                y2: 1,
                colorStops: [
                  { offset: 0, color: '#00ffaa' },
                  { offset: 1, color: '#009966' }
                ]
              }
            }
          },
          {
            value: sentimentData.value.neutral,
            name: '中性情绪',
            itemStyle: {
              color: {
                type: 'linear',
                x: 1,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: '#9be7ff' },
                  { offset: 1, color: '#1890ff' }
                ]
              }
            }
          },
          {
            value: sentimentData.value.negative,
            name: '消极情绪',
            itemStyle: {
              color: {
                type: 'linear',
                x: 1,
                y: 1,
                x2: 0,
                y2: 0,
                colorStops: [
                  { offset: 0, color: '#ff6a6a' },
                  { offset: 1, color: '#f5222d' }
                ]
              }
            }
          }
        ]
      }
    ]
  })
}

/* ===== 渲染语音测评雷达图 ===== */
function renderEvaluationChart() {
  if (!evaluationChartRef.value) return
  if (!evaluationChartInstance) {
    evaluationChartInstance = echarts.init(evaluationChartRef.value)
  }

  const data = evaluationParsed.value
    ? [
        evaluationParsed.value.fluency_score || 0,
        evaluationParsed.value.tone_score || 0,
        evaluationParsed.value.phone_score || 0,
        evaluationParsed.value.integrity_score || 0,
        evaluationParsed.value.total_score || 0,
      ]
    : [0, 0, 0, 0, 0]

  evaluationChartInstance.setOption({
    backgroundColor: isDarkMode.value ? '#2b2f38' : '#fff',
    tooltip: {
      trigger: 'item',
      textStyle: {
        color: '#fff',
        fontSize: 12,
      },
      backgroundColor: '#333',
      borderColor: '#666',
    },
    legend: {
      top: 10,
      data: ['候选人能力', '岗位要求'],
      textStyle: {
        color: '#ddd',
      },
      icon: 'rect',
    },
    radar: {
      shape: 'polygon',
      radius: '70%',
      indicator: [
        { name: '流利度', max: 100 },
        { name: '音调准确度', max: 100 },
        { name: '发音准确度', max: 100 },
        { name: '完整度', max: 100 },
        { name: '综合评分', max: 100 },
      ],
      splitNumber: 5,
      axisName: {
        color: '#ddd',
        fontSize: 13,
      },
      splitLine: {
        lineStyle: {
          color: '#444',
        },
      },
      splitArea: {
        areaStyle: {
          color: ['transparent'],
        },
      },
      axisLine: {
        lineStyle: {
          color: '#444',
        },
      },
    },
    series: [
      {
        name: '评分',
        type: 'radar',
        symbol: 'circle',
        symbolSize: 6,
        areaStyle: {
          opacity: 0,
        },
        lineStyle: {
          width: 2,
          color: '#00c0ff',
        },
        itemStyle: {
          color: '#00c0ff',
        },
        data: [
          {
            value: data,
            name: '候选人能力',
          },
          {
            value: [70, 60, 60, 80, 60], // 假设岗位要求的基准线
            name: '评分标准',
            lineStyle: {
              color: '#aaa',
              type: 'dashed',
            },
            itemStyle: {
              color: '#aaa',
            },
          },
        ],
      },
    ],
  })
}

/* ===== 监听语音测评分数变化，更新雷达图 ===== */
watch(evaluationParsed, async () => {
  await nextTick()
  renderEvaluationChart()
})

/* ===== 生命周期 ===== */
onMounted(() => {
  window.addEventListener('message', handleMessage)
  mergeTimer = setInterval(mergeTempToMain, MERGE_INTERVAL)
  saveTimer = setInterval(saveToBackend, SAVE_INTERVAL)
  fetchLatestSentiment()
  fetchEvaluationResult()
  fetchUserJobInfo()  // 新增调用
})

onBeforeUnmount(() => {
  window.removeEventListener('message', handleMessage)
  clearInterval(mergeTimer)
  clearInterval(saveTimer)
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  if (evaluationChartInstance) {
    evaluationChartInstance.dispose()
    evaluationChartInstance = null
  }
})

/* ===== 发送给 iframe ===== */
async function fetchUserJobInfo() {
  try {
    const res = await axios.get('/api/user/job_info', {
      params: {
        user_id: 1,
        job_id: 3
      }
    });
    
    console.log('接口返回:', res.data);
    
    // 设置默认值
    const defaultValue = '未知';
    const defaultPhoto = '/default-avatar.jpg'; // 使用相对路径或完整的URL
    
    username.value = res.data.username || defaultValue;
    jobTitle.value = res.data.job_title || defaultValue;
    jobCategory.value = res.data.job_category || defaultValue;
    photoPath.value = res.data.photo_path || ''; // 更新照片路径
    
  } catch (error) {
    username.value = '请求失败';
    jobTitle.value = '-';
    jobCategory.value = '-';
    photoPath.value = '';
    console.error('获取应聘者信息失败', error);
  }
}
</script>


<style scoped>
/* 基础样式 */
.container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #333;
  transition: all 0.3s ease;
}

.container.dark-mode {
  background-color:#0d1b2a;
  color: #e0e0e0;
}

.mode-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 8px 16px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  z-index: 100;
  font-size: 14px;
}

.main-title {
  font-size: 28px;
  text-align: center;
  margin-bottom: 30px;
  color: inherit;
}

/* 布局网格 */
.layout-grid {
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  grid-template-rows: auto auto;
  gap: 20px;
  grid-template-areas:
    "candidate-info virtual-human video-panel"
    "evaluation-panel virtual-human sentiment-panel";
}

/* 面板通用样式 */
.panel {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.dark-mode .panel {
  background-color: #2c2c2c;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.panel-title {
  font-size: 18px;
  margin-bottom: 15px;
  color: inherit;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.dark-mode .panel-title {
  border-bottom-color: #444;
}

.data-status {
  font-size: 12px;
  color: #888;
}

/* 应聘者信息 */
.candidate-info {
  grid-area: candidate-info;
}

.info-item {
  margin-bottom: 12px;
  font-size: 15px;
}

.info-label {
  font-weight: 600;
  color: #666;
}

.dark-mode .info-label {
  color: #aaa;
}

.info-value {
  color: #333;
}

.dark-mode .info-value {
  color: #e0e0e0;
}

/* 虚拟人区域 */
.virtual-human {
  grid-area: virtual-human;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.virtual-human-iframe {
  width: 100%;
  height: 500px;
  border: none;
  border-radius: 6px;
  background-color: #000;
}

.control-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.control-btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.control-btn:hover {
  opacity: 0.9;
}

.start-btn {
  background-color: #52c41a;
  color: white;
}

.interrupt-btn {
  background-color: #faad14;
  color: white;
}

.end-btn {
  background-color: #f5222d;
  color: white;
}

.transcribe-btn {
  background-color: #722ed1;
  color: white;
}

.send-text-group {
  display: flex;
  flex: 1;
  min-width: 200px;
}

.send-text-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 14px;
  outline: none;
}

.dark-mode .send-text-input {
  background-color: #333;
  border-color: #444;
  color: #e0e0e0;
}

.send-btn {
  background-color: #1890ff;
  color: white;
  border-radius: 0 4px 4px 0;
}

.subtitle-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.subtitle-title {
  font-size: 16px;
  margin-bottom: 10px;
  color: inherit;
}

.subtitle-content {
  flex: 1;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
  border: 1px solid #eee;
  overflow-y: auto;
  font-size: 15px;
  line-height: 1.5;
}

.dark-mode .subtitle-content {
  background-color: #333;
  border-color: #444;
}

/* 视频区域 */
.video-panel {
  grid-area: video-panel;
}

.video-container {
  width: 100%;
  aspect-ratio: 4/3;
  background-color: #f0f0f0;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.dark-mode .video-container {
  background-color: #333;
}

.video-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  color: #888;
}

.dark-mode .video-placeholder {
  color: #aaa;
}

.video-control-btn {
  padding: 8px 16px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 图表区域 */
.chart-container {
  width: 100%;
  height: 360px;
}

.evaluation-panel {
  grid-area: evaluation-panel;
}

.sentiment-panel {
  grid-area: sentiment-panel;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .layout-grid {
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
      "candidate-info video-panel"
      "virtual-human virtual-human"
      "evaluation-panel sentiment-panel";
  }
}

@media (max-width: 768px) {
  .layout-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "candidate-info"
      "video-panel"
      "virtual-human"
      "sentiment-panel"
      "evaluation-panel";
  }
}
/* 圆形头像容器 */
.avatar-container {
  width: 120px;
  height: 120px;
  margin: 0 auto 15px;
  border-radius: 50%;
  overflow: hidden;
  position: relative;
  border: 3px solid #e0e0e0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #f8f8f8;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 头像图片 */
.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 头像占位符 */
.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #e0e0e0;
  color: #999;
  font-size: 14px;
}

/* 暗黑模式适配 */
.dark-mode .avatar-container {
  border-color: #444;
  background-color: #2a2a2a;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.dark-mode .avatar-placeholder {
  background-color: #333;
  color: #777;
}

</style>