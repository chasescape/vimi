<template>
  <div class="result-container">
    <h1 class="page-title">面试结果</h1>
    <div class="result-card">
      <div class="score-row">
        <div class="score-label">总分</div>
        <div class="score-value">{{ totalScore }}</div>
      </div>
      <div class="main-flex-row">
        <!-- 左侧：图表区 -->
        <div class="chart-col">
          <div ref="radarRef" class="radar-chart"></div>
          <div class="emotion-section">
            <h3 class="emotion-title">情绪分析</h3>
            <div ref="emotionRef" class="emotion-pie-chart"></div>
            <div class="emotion-legend">
              <span class="legend-item positive">积极情绪</span>
              <span class="legend-item neutral">中性情绪</span>
              <span class="legend-item negative">消极情绪</span>
            </div>
          </div>
        </div>
        <!-- 右侧：能力进度条与分析 -->
        <div class="dimension-col">
          <div class="ability-bars">
            <div v-for="item in abilityList" :key="item.key" class="bar-row">
              <span class="bar-label">{{ item.label }}</span>
              <div class="bar-bg">
                <div class="bar-fg" :style="{ width: item.score + '%', background: item.color }"></div>
              </div>
              <span class="bar-score">{{ item.score }}</span>
            </div>
          </div>
          <div class="divider"></div>
          <div class="dimension-section" v-for="item in abilityList" :key="item.key">
            <div class="dimension-header">
              <span class="dimension-title-text">{{ item.label }}</span>
              <span class="dimension-score">{{ item.score }}/100</span>
            </div>
            <div class="dimension-desc">{{ item.desc }}</div>
            <div class="dimension-analysis">
              <span class="analysis-label">分析：</span>
              <span class="analysis-content">{{ item.analysis }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="divider"></div>
      <!-- 个性化反馈 -->
      <div class="feedback-section">
        <h3>个性化改进建议</h3>
        <ul>
          <li v-for="item in feedbackList" :key="item.type">
            <b>{{ item.type }}：</b>{{ item.suggestion }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const abilityList = ref<any[]>([])
const emotionData = ref<any[]>([])
const feedbackList = ref<any[]>([])
const totalScore = ref(0)
const radarRef = ref<HTMLDivElement | null>(null)
const emotionRef = ref<HTMLDivElement | null>(null)
const interviewText = ref('这里是本次面试的实际内容或转写') // 你实际获取的内容
  onMounted(async () => {
  // 正确请求后端接口，参数为messages数组

  const prompt = `
你是一个AI面试分析助手。请根据以下面试文本/音频/视频分析，输出如下结构化JSON数据：

1. abilities（数组）：请严格输出以下7项，每项包含 key、label、score（0-100）、desc、analysis
  - 专业知识（knowledge）：技术术语准确性、领域知识覆盖度、技术原理深度
  - 技能匹配（skill）：简历技能与岗位JD的重合率、项目经验相关性
  - 表达能力（expression）：逻辑连贯性、词汇丰富度、冗余词频率
  - 逻辑思维（logic）：问题拆解层次、观点论证严谨性、数据支撑有效性
  - 应变抗压（pressure）：非常规问题响应速度、压力下语速稳定性、微表情波动
  - 创新能力（innovation）：非标准答案占比、跨领域联想能力、解决方案新颖度
  - 职业素养（professionalism）：眼神接触率、肢体语言自信度、语音情感积极性

2. emotion（数组）：积极情绪/中性情绪/消极情绪的占比（百分比，和为100）
3. feedback（数组）：每项包含 type、suggestion

输出格式示例：
\`\`\`json
{
  "abilities": [
    {
      "key": "knowledge",
      "label": "专业知识",
      "score": 92,
      "desc": "技术术语准确性、领域知识覆盖度、技术原理深度。",
      "analysis": "专业术语丰富，知识面广，原理理解深入。"
    },
    {
      "key": "skill",
      "label": "技能匹配",
      "score": 85,
      "desc": "简历技能与岗位JD的重合率、项目经验相关性。",
      "analysis": "技能与岗位高度匹配，项目经验丰富。"
    },
    {
      "key": "expression",
      "label": "表达能力",
      "score": 78,
      "desc": "逻辑连贯性、词汇丰富度、冗余词频率。",
      "analysis": "表达较为流畅，偶有冗余词，建议加强逻辑性。"
    },
    {
      "key": "logic",
      "label": "逻辑思维",
      "score": 88,
      "desc": "问题拆解层次、观点论证严谨性、数据支撑有效性。",
      "analysis": "思维清晰，能分点作答，论证有力。"
    },
    {
      "key": "pressure",
      "label": "应变抗压",
      "score": 80,
      "desc": "非常规问题响应速度、压力下语速稳定性、微表情波动。",
      "analysis": "面对压力能保持冷静，语速稳定。"
    },
    {
      "key": "innovation",
      "label": "创新能力",
      "score": 75,
      "desc": "非标准答案占比、跨领域联想能力、解决方案新颖度。",
      "analysis": "有创新意识，能提出新颖方案。"
    },
    {
      "key": "professionalism",
      "label": "职业素养",
      "score": 90,
      "desc": "眼神接触率、肢体语言自信度、语音情感积极性。",
      "analysis": "职业素养高，肢体语言自信，情感积极。"
    }
  ],
  "emotion": [
    { "value": 60, "name": "积极情绪" },
    { "value": 30, "name": "中性情绪" },
    { "value": 10, "name": "消极情绪" }
  ],
  "feedback": [
    { "type": "语言表达优化", "suggestion": "..." }
    // ...
  ]
}
\`\`\`

请严格按照上述JSON格式输出，不要输出多余的解释性文字。

面试原始数据如下：
${interviewText.value}
`
  const { data } = await axios.post('/api/spark/chat', {
    messages: [
      {
        role: 'user',
        content: prompt
      }
    ]
  })
  // 解析reply字段，去除markdown代码块再JSON.parse
  let reply = data.reply
  reply = reply.replace(/^\s*```json\s*|^\s*```\s*|```$/gm, '').trim()
  let result
  try {
    result = JSON.parse(reply)
  } catch (e) {
    console.error('解析大模型返回JSON失败', reply)
    result = { abilities: [], emotion: [], feedback: [] }
  }
  abilityList.value = result.abilities
  emotionData.value = result.emotion
  feedbackList.value = result.feedback
  totalScore.value = result.abilities && result.abilities.length > 0
    ? Math.round(result.abilities.reduce((sum: number, item: any) => sum + item.score, 0) / result.abilities.length)
    : 0

  // 渲染图表
  nextTick(() => {
    if (radarRef.value) {
      const radarChart = echarts.init(radarRef.value)
      radarChart.setOption({
        tooltip: {
          show: true,
          backgroundColor: '#fff',
          borderColor: '#1890ff',
          borderWidth: 1,
          textStyle: { color: '#333', fontSize: 15 },
          formatter: (params: { name: string; value: number[] }) => {
            return params.name + '<br/>' +
              params.value.map((v: number, i: number) =>
                `${abilityList.value[i].label}: <b>${v}</b>`
              ).join('<br/>')
          }
        },
        radar: {
          indicator: abilityList.value.map((item: any) => ({ name: item.label, max: 100 })),
          radius: 110,
          splitNumber: 5,
          shape: 'polygon',
          axisName: {
            color: '#1890ff',
            fontWeight: 'bold',
            fontSize: 16,
            backgroundColor: '#fff',
            borderRadius: 3,
            padding: [2, 6]
          },
          splitLine: { lineStyle: { color: ['#e0e7ef', '#c6d3e7', '#a5b8d8', '#7fa1c7', '#4e7bbd'] } },
          splitArea: { areaStyle: { color: ['#f5faff', '#e6f7ff', '#f0f5ff', '#f9f0ff', '#fff'] } },
          axisLine: { lineStyle: { color: '#b2c7e1' } }
        },
        series: [{
          type: 'radar',
          data: [{
            value: abilityList.value.map((item: any) => item.score),
            name: '能力分布',
            areaStyle: { color: 'rgba(24, 144, 255, 0.3)' },
            lineStyle: { color: '#1890ff', width: 3 },
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: { color: '#1890ff', borderColor: '#fff', borderWidth: 2 }
          }]
        }]
      })
    }
    if (emotionRef.value) {
      const emotionChart = echarts.init(emotionRef.value)
      emotionChart.setOption({
        tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
        legend: { show: false },
        series: [{
          name: '情绪分析',
          type: 'pie',
          radius: ['60%', '85%'],
          avoidLabelOverlap: false,
          label: {
            show: true,
            position: 'center',
            formatter: () => '情绪分析',
            fontSize: 18,
            color: '#1890ff',
            fontWeight: 'bold'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 22,
              fontWeight: 'bold',
              color: '#1890ff'
            }
          },
          labelLine: { show: false },
          data: [
            { value: emotionData.value[0]?.value, name: '积极情绪', itemStyle: { color: '#52c41a' } },
            { value: emotionData.value[1]?.value, name: '中性情绪', itemStyle: { color: '#ffd666' } },
            { value: emotionData.value[2]?.value, name: '消极情绪', itemStyle: { color: '#ff4d4f' } }
          ]
        }]
      })
    }
  })
})
// // 能力数据
// const abilityList = [
//   {
//     key: 'knowledge',
//     label: '专业知识',
//     score: 92,
//     color: '#1890ff',
//     desc: '技术术语准确性、领域知识覆盖度、技术原理深度。',
//     analysis: '专业术语丰富，知识面广，原理理解深入。'
//   },
//   {
//     key: 'skill',
//     label: '技能匹配',
//     score: 85,
//     color: '#52c41a',
//     desc: '简历技能与岗位JD的重合率、项目经验相关性。',
//     analysis: '技能与岗位高度匹配，项目经验丰富。'
//   },
//   {
//     key: 'expression',
//     label: '表达能力',
//     score: 78,
//     color: '#ffd666',
//     desc: '逻辑连贯性、词汇丰富度、冗余词频率。',
//     analysis: '表达较为流畅，偶有冗余词，建议加强逻辑性。'
//   },
//   {
//     key: 'logic',
//     label: '逻辑思维',
//     score: 88,
//     color: '#13c2c2',
//     desc: '问题拆解层次、观点论证严谨性、数据支撑有效性。',
//     analysis: '思维清晰，能分点作答，论证有力。'
//   },
//   {
//     key: 'pressure',
//     label: '应变抗压',
//     score: 80,
//     color: '#faad14',
//     desc: '非常规问题响应速度、压力下语速稳定性、微表情波动。',
//     analysis: '面对压力能保持冷静，语速稳定。'
//   },
//   {
//     key: 'innovation',
//     label: '创新能力',
//     score: 75,
//     color: '#eb2f96',
//     desc: '非标准答案占比、跨领域联想能力、解决方案新颖度。',
//     analysis: '有创新意识，能提出新颖方案。'
//   },
//   {
//     key: 'professionalism',
//     label: '职业素养',
//     score: 90,
//     color: '#722ed1',
//     desc: '眼神接触率、肢体语言自信度、语音情感积极性。',
//     analysis: '职业素养高，肢体语言自信，情感积极。'
//   }
// ]
// const totalScore = Math.round(abilityList.reduce((sum, item) => sum + item.score, 0) / abilityList.length)

// 雷达图数据
// const radarRef = ref<HTMLDivElement | null>(null)
// const radarData = abilityList.map(item => item.score)

// 情绪分析数据
// const emotionRef = ref<HTMLDivElement | null>(null)
// const emotionData = [
//   { value: 60, name: '积极情绪' },
//   { value: 30, name: '中性情绪' },
//   { value: 10, name: '消极情绪' }
// ]

// 个性化反馈
// const feedbackList = [
//   { type: '语言表达优化', suggestion: '回答中“呃”出现12次，建议用5秒深呼吸替代，语速控制在160字/分钟（当前180字）。' },
//   { type: '逻辑结构建议', suggestion: '问题3未使用STAR结构（缺少Action部分），参考模板：我通过XX方法解决了XX问题…' },
//   { type: '非语言沟通指导', suggestion: '眼神接触率仅40%（建议＞60%），练习方法：面试时注视摄像头中央圆点5秒→移开2秒→循环。' },
//   { type: '抗压能力训练', suggestion: '压力测试题响应延迟4.2秒（平均2.5秒），推荐：每日模拟突发问答（系统“闪电问答”模块）。' }
// ]

// onMounted(() => {
//   nextTick(() => {
//     // 雷达图
//     if (radarRef.value) {
//       const radarChart = echarts.init(radarRef.value)
//       radarChart.setOption({
//         tooltip: {
//           show: true,
//           backgroundColor: '#fff',
//           borderColor: '#1890ff',
//           borderWidth: 1,
//           textStyle: { color: '#333', fontSize: 15 },
//           formatter: (params: { name: string; value: number[] }) => {
//             return params.name + '<br/>' +
//               params.value.map((v: number, i: number) =>
//                 `${abilityList[i].label}: <b>${v}</b>`
//               ).join('<br/>')
//           }
//         },
//         radar: {
//           indicator: abilityList.map(item => ({ name: item.label, max: 100 })),
//           radius: 110,
//           splitNumber: 5,
//           shape: 'polygon',
//           axisName: {
//             color: '#1890ff',
//             fontWeight: 'bold',
//             fontSize: 16,
//             backgroundColor: '#fff',
//             borderRadius: 3,
//             padding: [2, 6]
//           },
//           splitLine: {
//             lineStyle: {
//               color: ['#e0e7ef', '#c6d3e7', '#a5b8d8', '#7fa1c7', '#4e7bbd']
//             }
//           },
//           splitArea: {
//             areaStyle: {
//               color: ['#f5faff', '#e6f7ff', '#f0f5ff', '#f9f0ff', '#fff']
//             }
//           },
//           axisLine: {
//             lineStyle: {
//               color: '#b2c7e1'
//             }
//           }
//         },
//         series: [{
//           type: 'radar',
//           data: [
//             {
//               value: radarData,
//               name: '能力分布',
//               areaStyle: {
//                 color: 'rgba(24, 144, 255, 0.3)'
//               },
//               lineStyle: {
//                 color: '#1890ff',
//                 width: 3
//               },
//               symbol: 'circle',
//               symbolSize: 8,
//               itemStyle: {
//                 color: '#1890ff',
//                 borderColor: '#fff',
//                 borderWidth: 2
//               }
//             }
//           ]
//         }]
//       })
//     }
//     // 情绪分析环形图
//     if (emotionRef.value) {
//       const emotionChart = echarts.init(emotionRef.value)
//       emotionChart.setOption({
//         tooltip: {
//           trigger: 'item',
//           formatter: '{b}: {c} ({d}%)'
//         },
//         legend: { show: false },
//         series: [
//           {
//             name: '情绪分析',
//             type: 'pie',
//             radius: ['60%', '85%'],
//             avoidLabelOverlap: false,
//             label: {
//               show: true,
//               position: 'center',
//               formatter: () => '情绪分析',
//               fontSize: 18,
//               color: '#1890ff',
//               fontWeight: 'bold'
//             },
//             emphasis: {
//               label: {
//                 show: true,
//                 fontSize: 22,
//                 fontWeight: 'bold',
//                 color: '#1890ff'
//               }
//             },
//             labelLine: { show: false },
//             data: [
//               { value: emotionData[0].value, name: '积极情绪', itemStyle: { color: '#52c41a' } },
//               { value: emotionData[1].value, name: '中性情绪', itemStyle: { color: '#ffd666' } },
//               { value: emotionData[2].value, name: '消极情绪', itemStyle: { color: '#ff4d4f' } }
//             ]
//           }
//         ]
//       })
//     }
//   })
// })

</script>

<style scoped>
.result-container {
  max-width: 1400px;
  margin: 40px auto 0 auto;
  padding: 24px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #333;
}
.page-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #1a1a1a;
  text-align: left;
  padding-bottom: 12px;
  border-bottom: 2px solid #1890ff;
}
.result-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  padding: 40px 56px;
  margin-top: 24px;
  max-width: 1300px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}
@media (max-width: 1200px) {
  .result-card {
    max-width: 98vw;
    padding: 24px 8px;
  }
}
.score-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.score-label {
  font-size: 20px;
  font-weight: 600;
  color: #1890ff;
}
.score-value {
  font-size: 32px;
  font-weight: bold;
  color: #1890ff;
}
.divider {
  height: 1px;
  background: #f0f0f0;
  margin: 20px 0;
}
.main-flex-row {
  display: flex;
  gap: 32px;
  justify-content: center;
  align-items: flex-start;
  margin-bottom: 24px;
}
.chart-col {
  flex: 1 1 340px;
  min-width: 320px;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.dimension-col {
  flex: 1 1 340px;
  min-width: 320px;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.radar-chart {
  width: 100%;
  max-width: 480px;
  height: 380px;
  margin: 0 auto 32px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(24, 144, 255, 0.08);
  padding: 12px;
}
.ability-bars { margin: 24px 0; }
.bar-row { display: flex; align-items: center; margin-bottom: 12px; }
.bar-label { width: 100px; }
.bar-bg { flex: 1; background: #f0f0f0; border-radius: 8px; height: 16px; margin: 0 12px; }
.bar-fg { height: 100%; border-radius: 8px; transition: width 0.5s; }
.bar-score { width: 40px; text-align: right; }
.emotion-section {
  margin: 32px auto 0 auto;
  max-width: 480px;
  text-align: center;
}
.emotion-title {
  font-size: 20px;
  font-weight: 600;
  color: #1890ff;
  margin-bottom: 8px;
}
.emotion-pie-chart {
  width: 320px;
  height: 220px;
  margin: 0 auto;
}
.emotion-legend {
  margin-top: 8px;
  display: flex;
  justify-content: center;
  gap: 24px;
}
.legend-item {
  font-size: 15px;
  font-weight: 500;
  padding-left: 18px;
  position: relative;
}
.legend-item.positive::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  background: #52c41a;
  border-radius: 50%;
  position: absolute;
  left: 0;
  top: 3px;
}
.legend-item.neutral::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  background: #ffd666;
  border-radius: 50%;
  position: absolute;
  left: 0;
  top: 3px;
}
.legend-item.negative::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  background: #ff4d4f;
  border-radius: 50%;
  position: absolute;
  left: 0;
  top: 3px;
}
.dimension-section {
  background: #f8fafc;
  border-radius: 10px;
  padding: 18px 20px 14px 20px;
  margin-bottom: 18px;
  border-left: 4px solid #1890ff;
  box-shadow: 0 2px 8px rgba(24,144,255,0.04);
  transition: box-shadow 0.2s;
}
.dimension-section:hover {
  box-shadow: 0 4px 16px rgba(24,144,255,0.10);
}
.dimension-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 6px;
}
.dimension-title-text {
  color: #1890ff;
  font-weight: 600;
  font-size: 18px;
}
.dimension-score {
  font-size: 22px;
  color: #52c41a;
  font-weight: bold;
  margin-left: 12px;
}
.dimension-desc {
  color: #888;
  font-size: 14px;
  margin-bottom: 6px;
  margin-left: 2px;
}
.dimension-analysis {
  color: #444;
  font-size: 15px;
  margin-bottom: 2px;
  margin-left: 2px;
}
.analysis-label {
  color: #1890ff;
  font-weight: 500;
  margin-right: 4px;
}
.analysis-content {
  color: #444;
}
.feedback-section {
  margin: 32px 0 0 0;
}
.feedback-section h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1890ff;
  margin-bottom: 8px;
}
.feedback-section ul {
  padding-left: 18px;
}
.feedback-section li {
  margin-bottom: 6px;
  color: #444;
  font-size: 15px;
}
</style>