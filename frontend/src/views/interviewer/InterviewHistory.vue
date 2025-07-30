<template>
  <div class="approved-candidates-page">
    <!-- 头部 -->
    <div class="header">
      <h1>已安排面试的候选人</h1>
      <div class="stats-export">
        <div class="stat-card">
          <span class="stat-value">{{ filteredCandidates.length }}</span>
          <span class="stat-label">当前显示</span>
        </div>
        <button class="export-btn" @click="exportExcel">导出 Excel</button>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filters">
      <input
        v-model="searchKeyword"
        placeholder="搜索姓名..."
        class="filter-input"
        @input="onFilterChange"
      />
      <select v-model="selectedJob" class="filter-input" @change="onFilterChange">
        <option value="">全部岗位</option>
        <option v-for="j in jobOptions" :key="j" :value="j">{{ j }}</option>
      </select>
      <button class="refresh-btn" @click="fetchApproved">刷新</button>
    </div>

    <!-- 中部面板：两个图表 + 即将面试 -->
    <div class="middle-panel">
      <div class="charts-container">
        <section class="chart-panel">
          <h2>岗位分布</h2>
          <div ref="jobChart" class="chart-container"></div>
        </section>
        <section class="chart-panel">
          <h2>面试时间分布（小时）</h2>
          <div ref="timeChart" class="chart-container"></div>
        </section>
      </div>

      <section class="upcoming-panel">
        <h2>即将面试（3小时内）</h2>
        <ul class="upcoming-list">
          <li v-for="c in upcomingCandidates" :key="c.id" class="upcoming-item">
            <div class="upcoming-name">{{ c.name }}</div>
            <div class="upcoming-position">{{ c.position || '岗位未知' }}</div>
            <div
              class="countdown"
              :class="{ expired: getRemainingTime(c.interviewTime).expired }"
            >
              {{ getRemainingTime(c.interviewTime).text }}
            </div>
          </li>
          <li v-if="upcomingCandidates.length === 0" class="empty-upcoming">暂无即将面试候选人</li>
        </ul>
      </section>
    </div>

    <!-- 底部：候选人列表 -->
    <ul v-if="!loading && filteredCandidates.length" class="candidate-list">
      <li v-for="c in filteredCandidates" :key="c.id" class="candidate-item">
        <div class="candidate-info">
          <span class="candidate-name">{{ c.name }}</span>
          <span class="candidate-position">岗位: {{ c.position || '未填写' }}</span>
          <span class="candidate-id">申请ID: {{ c.id }}</span>
        </div>
        <div class="interview-info">
          <span class="time">面试时间: {{ formatDateTime(c.interviewTime) }}</span>
          <span
            class="countdown"
            :class="{ expired: getRemainingTime(c.interviewTime).expired }"
          >
            {{ getRemainingTime(c.interviewTime).text }}
          </span>
          <a :href="c.interviewLink" class="link" target="_blank">进入面试</a>
        </div>
      </li>
    </ul>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>正在加载数据...</p>
    </div>

    <div v-else-if="!loading && filteredCandidates.length === 0" class="empty-state">
      暂无符合条件的候选人
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import * as XLSX from 'xlsx'
import * as echarts from 'echarts'

export default {
  name: 'ApprovedCandidates',
  data() {
    return {
      loading: false,
      approvedCandidates: [],
      searchKeyword: '',
      selectedJob: '',
      jobOptions: [],
      now: Date.now(),
      chartInstanceJob: null,
      chartInstanceTime: null
    }
  },
  computed: {
    filteredCandidates() {
      let list = this.approvedCandidates
      if (this.searchKeyword) {
        const kw = this.searchKeyword.toLowerCase()
        list = list.filter(c =>
          (c.name && c.name.toLowerCase().includes(kw)) ||
          (c.position && c.position.toLowerCase().includes(kw))
        )
      }
      if (this.selectedJob) {
        list = list.filter(c => c.position === this.selectedJob)
      }
      return list
    },
    jobDistribution() {
      const map = {}
      this.filteredCandidates.forEach(c => {
        const pos = c.position || '未填写'
        map[pos] = (map[pos] || 0) + 1
      })
      return Object.entries(map).map(([name, value]) => ({ name, value }))
    },
    timeDistribution() {
      const counts = Array(24).fill(0)
      this.filteredCandidates.forEach(c => {
        if (!c.interviewTime) return
        const hour = new Date(c.interviewTime).getHours()
        counts[hour]++
      })
      return counts.map((count, hour) => ({ hour, count }))
    },
    upcomingCandidates() {
      const threeHours = 3 * 3600 * 1000
      return this.filteredCandidates
        .filter(c => {
          if (!c.interviewTime) return false
          const diff = new Date(c.interviewTime).getTime() - this.now
          return diff > 0 && diff <= threeHours
        })
        .sort((a, b) => new Date(a.interviewTime) - new Date(b.interviewTime))
        .slice(0, 3)
    }
  },
  watch: {
    filteredCandidates() {
      this.updateCharts()
    }
  },
  created() {
    this.fetchApproved()
    setInterval(() => {
      this.now = Date.now()
    }, 1000)
  },
  mounted() {
    this.chartInstanceJob = echarts.init(this.$refs.jobChart)
    this.chartInstanceTime = echarts.init(this.$refs.timeChart)
  },
  methods: {
    fetchApproved() {
      this.loading = true
      axios.get('/api/apply/all')
        .then(res => {
          const filtered = res.data
            .filter(app => app.status === '已通过' && app.interview_time && app.interview_link)
            .map(app => ({
              id: app.application_id,
              name: app.username,
              position: app.job_title || '',
              interviewTime: app.interview_time,
              interviewLink: app.interview_link
            }))
          this.approvedCandidates = filtered
          this.jobOptions = [...new Set(filtered.map(c => c.position).filter(Boolean))]
          this.updateCharts()
        })
        .catch(err => {
          console.error('获取候选人失败:', err)
          alert('无法获取数据，请检查接口')
        })
        .finally(() => {
          this.loading = false
        })
    },
    onFilterChange() {
      this.updateCharts()
    },
    getRemainingTime(timeStr) {
      if (!timeStr) return { text: '未知', expired: true }
      const target = new Date(timeStr).getTime()
      const diff = target - this.now
      if (diff <= 0) {
        return { text: '已开始或结束', expired: true }
      }
      const h = Math.floor(diff / 3600000)
      const m = Math.floor((diff % 3600000) / 60000)
      const s = Math.floor((diff % 60000) / 1000)
      return { text: `倒计时 ${h}小时${m}分${s}秒`, expired: false }
    },
    exportExcel() {
      const data = this.filteredCandidates.map(c => ({
        姓名: c.name,
        岗位: c.position,
        面试时间: this.formatDateTime(c.interviewTime),
        面试链接: c.interviewLink
      }))
      const ws = XLSX.utils.json_to_sheet(data)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, '候选人')
      XLSX.writeFile(wb, `候选人列表_${new Date().toISOString().slice(0,10)}.xlsx`)
    },
    formatDateTime(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      if (isNaN(date)) return dateStr
      const Y = date.getFullYear()
      const M = (date.getMonth() + 1).toString().padStart(2, '0')
      const D = date.getDate().toString().padStart(2, '0')
      const h = date.getHours().toString().padStart(2, '0')
      const m = date.getMinutes().toString().padStart(2, '0')
      return `${Y}-${M}-${D} ${h}:${m}`
    },
    updateCharts() {
      // 岗位分布饼图（去掉legend和series.name）
      if (this.chartInstanceJob) {
        this.chartInstanceJob.setOption({
          tooltip: { trigger: 'item' },
          legend: { show: false },  // 隐藏图例
          series: [{
            // name: '岗位分布',  // 删除series名字避免tooltip多余显示
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: { 
              show: true, 
              formatter: '{b}: {c} ({d}%)',
              color: '#2c3e80',
              fontWeight: '600',
              fontSize: 14,
            },
            emphasis: { label: { show: true, fontSize: '16', fontWeight: 'bold' } },
            labelLine: { show: true },
            data: this.jobDistribution
          }]
        })
      }
      // 面试时间分布柱状图
      if (this.chartInstanceTime) {
        this.chartInstanceTime.setOption({
          tooltip: {},
          xAxis: {
            type: 'category',
            data: this.timeDistribution.map(i => i.hour + ':00')
          },
          yAxis: {
            type: 'value',
            name: '面试人数'
          },
          series: [{
            data: this.timeDistribution.map(i => i.count),
            type: 'bar',
            itemStyle: { color: '#4354e8' }
          }]
        })
      }
    }
  }
}
</script>

<style scoped>
.approved-candidates-page {
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background: linear-gradient(135deg, #f7f9ff, #eef2ff);
  min-height: 100vh;
  padding: 24px 36px;
  color: #333;
}

/* 头部 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e80;
}
.stats-export {
  display: flex;
  align-items: center;
  gap: 20px;
}
.stat-card {
  background: linear-gradient(135deg, #4354e8, #6f82ff);
  color: #fff;
  padding: 14px 24px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 6px 16px rgba(67, 84, 232, 0.3);
}
.stat-value {
  font-size: 28px;
  font-weight: bold;
}
.stat-label {
  font-size: 14px;
}
.export-btn {
  background: #00b894;
  color: #fff;
  border: none;
  padding: 10px 26px;
  border-radius: 24px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}
.export-btn:hover {
  background: #009874;
}

/* 筛选栏 */
.filters {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}
.filter-input {
  flex: 1;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
}
.refresh-btn {
  background: #4354e8;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 24px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}
.refresh-btn:hover {
  background: #2f3bbb;
}

/* 中部面板 */
.middle-panel {
  display: flex;
  gap: 40px;          /* 加大中间间距 */
  margin-bottom: 32px;
  flex-wrap: nowrap;  /* 保证横排不换行 */
  justify-content: space-between;
}
.charts-container {
  display: flex;
  gap: 32px;          /* 图表之间间距 */
  flex: 1;
  min-width: 280px;
  height: auto;
}
.chart-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(67, 84, 232, 0.1);
  padding: 16px;
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;

}
.chart-panel h2 {
  margin-bottom: 12px;
  color: #2c3e80;
}
.chart-container {
  height: 280px;
}

/* 即将面试 */
.upcoming-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(67, 84, 232, 0.1);
  padding: 16px;
  min-width: 280px;
  max-width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}
.upcoming-panel h2 {
  margin-bottom: 12px;
  color: #2c3e80;
}
.upcoming-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.upcoming-item {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.upcoming-name {
  font-weight: 600;
  color: #4354e8;
}
.upcoming-position {
  color: #666;
  font-size: 13px;
}
.countdown {
  font-weight: bold;
  color: #ff6b6b;
  animation: pulse 1.5s infinite;
}
.countdown.expired {
  color: #aaa;
  animation: none;
}
.empty-upcoming {
  text-align: center;
  color: #999;
  padding: 20px 0;
}

/* 候选人列表 */
.candidate-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.candidate-item {
  background: #fff;
  margin-bottom: 18px;
  padding: 20px 24px;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgba(67, 84, 232, 0.12);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.candidate-item:hover {
  background: #f8faff;
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(67, 84, 232, 0.18);
}
.candidate-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.candidate-name {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e80;
}
.candidate-position {
  font-size: 15px;
  color: #555;
}
.candidate-id {
  font-size: 13px;
  color: #7b8abe;
}
.interview-info {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 15px;
  color: #2c3e80;
}
.countdown {
  color: #ff6b6b;
  font-weight: bold;
  animation: pulse 1.5s infinite;
}
.countdown.expired {
  color: #aaa;
  animation: none;
}
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
.link {
  color: #4354e8;
  font-weight: 600;
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #7b8abe;
}
.spinner {
  border: 4px solid #e6e8f8;
  border-top-color: #4354e8;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1.2s linear infinite;
  margin-bottom: 16px;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
  text-align: center;
  font-size: 18px;
  color: #999;
  padding: 60px 0;
}
</style>
