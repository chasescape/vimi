<template>
  <div class="modern-hr-dashboard">
    <!-- 新增：简历预览模态框 -->
    <div v-if="showResumeModal" class="resume-modal-overlay" @click.self="closeResumeModal">
      <div class="resume-modal">
        <div class="modal-header">
          <h3>{{ currentResume.candidateName }}的简历</h3>
          <button @click="closeResumeModal" class="modal-close-btn">
            <i class="icon-close"></i>
          </button>
        </div>
        <div class="modal-body">
          <iframe 
            v-if="currentResume.url" 
            :src="getPreviewUrl(currentResume.url)" 
            frameborder="0"
            class="resume-iframe"
          ></iframe>
          <div v-else class="no-resume">
            无法加载简历
          </div>
        </div>
        <div class="modal-footer">
          <button @click="downloadResume(currentResume.url)" class="download-btn">
            <i class="icon-download"></i> 下载简历
          </button>
        </div>
      </div>
    </div>

    <!-- 顶部导航 -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">
          <span class="title-highlight">HR</span> 人才管理中心
        </h1>
        <div class="header-actions">
          <button class="action-btn refresh-btn" @click="fetchApplications">
            <i class="icon-refresh"></i> 刷新数据
          </button>
          <div class="search-container">
            <i class="icon-search"></i>
            <input type="text" placeholder="搜索候选人..." v-model="searchQuery">
          </div>
        </div>
      </div>
    </div>

    <!-- 数据概览卡片 -->
    <div class="metrics-container">
      <div class="metric-card total-applications">
        <div class="metric-value">{{ applications.length }}</div>
        <div class="metric-label">总申请数</div>
        <div class="metric-icon">
          <i class="icon-document"></i>
        </div>
      </div>
      
      <div class="metric-card pending-review">
        <div class="metric-value">{{ pendingCount }}</div>
        <div class="metric-label">待审核</div>
        <div class="metric-icon">
          <i class="icon-clock"></i>
        </div>
      </div>
      
      <div class="metric-card approved">
        <div class="metric-value">{{ approvedCount }}</div>
        <div class="metric-label">已通过</div>
        <div class="metric-icon">
          <i class="icon-check"></i>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <div class="content-header">
        <h2 class="section-title">候选人申请列表</h2>
        <div class="section-actions">
          <button class="export-btn">
            <i class="icon-download"></i> 导出数据
          </button>
        </div>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <div class="loading-text">正在加载数据...</div>
      </div>
      
      <!-- 申请表格 -->
      <div v-else class="applications-table">
        <div class="table-responsive">
          <table class="applications-list">
            <thead>
              <tr>
                <th class="col-id">申请ID</th>
                <th class="col-candidate">候选人</th>
                <th class="col-position">目标岗位</th>
                <th class="col-status">状态</th>
                <th class="col-resume">简历</th>
                <th class="col-actions">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in filteredApplications" :key="app.application_id" class="application-row">
                <td class="application-id">
                  <span class="id-badge">#{{ app.application_id }}</span>
                </td>
                <td class="candidate-info">
                  <div class="candidate-avatar">
                    {{ app.username.charAt(0).toUpperCase() }}
                  </div>
                  <div class="candidate-details">
                    <div class="candidate-name">{{ app.username }}</div>
                    <div class="candidate-id">ID: {{ app.user_id || 'N/A' }}</div>
                  </div>
                </td>
                <td class="position-info">
                  <div class="position-title">{{ app.job_title }}</div>
                  <div class="department">{{ app.department || '未指定部门' }}</div>
                </td>
                <td class="application-status">
                  <div :class="['status-badge', getStatusClass(app.status)]">
                    {{ app.status }}
                  </div>
                </td>
                <td class="resume-link">
                  <!-- 修改：将a标签改为button，点击触发预览 -->
                  <button 
                    v-if="app.resume_path" 
                    @click="previewResume(app.resume_path, app.username)" 
                    class="resume-btn"
                  >
                    <i class="icon-eye"></i> 查看简历
                  </button>
                  <span v-else class="no-resume">未上传</span>
                </td>
                <td class="application-actions">
                  <div class="action-buttons">
                    <button @click="approve(app.application_id)" class="action-btn approve-btn">
                      <i class="icon-check"></i> 通过
                    </button>
                    <button @click="reject(app.application_id)" class="action-btn reject-btn">
                      <i class="icon-close"></i> 拒绝
                    </button>
                  </div>
                  
                  <transition name="slide-fade">
                    <div v-if="app.status === '已通过'" class="interview-schedule">
                      <div v-if="!isEditingInterview[app.application_id] && interviewTimes[app.application_id] && interviewLinks[app.application_id]" class="scheduled-info">
                        <div class="info-item">
                          <i class="icon-calendar"></i>
                          <span>{{ formatDateTime(interviewTimes[app.application_id]) }}</span>
                        </div>
                        <div class="info-item">
                          <i class="icon-link"></i>
                          <a :href="interviewLinks[app.application_id]" target="_blank">面试链接</a>
                        </div>
                        <button @click="editInterview(app.application_id)" class="edit-btn">
                          <i class="icon-edit"></i> 编辑
                        </button>
                      </div>
                      
                      <div v-else class="schedule-form">
                        <div class="form-group">
                          <label><i class="icon-clock"></i> 面试时间</label>
                          <input 
                            type="datetime-local" 
                            v-model="interviewTimes[app.application_id]"
                            class="form-input"
                          />
                        </div>
                        <div class="form-group">
                          <label><i class="icon-video"></i> 面试链接</label>
                          <input 
                            type="text" 
                            v-model="interviewLinks[app.application_id]"
                            class="form-input"
                            readonly
                          />
                        </div>
                        <button 
                          @click="setInterview(app.application_id)" 
                          class="save-btn"
                          :disabled="isSubmittingInterview[app.application_id]"
                        >
                          <i class="icon-save"></i> 保存安排
                        </button>
                      </div>
                    </div>
                  </transition>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ModernHrDashboard',
  data() {
    return {
      applications: [],
      loading: false,
      interviewTimes: {},
      interviewLinks: {},
      isEditingInterview: {},
      isSubmittingInterview: {},
      searchQuery: '',
      // 新增：简历预览相关数据
      showResumeModal: false,
      currentResume: {
        url: '',
        candidateName: ''
      }
    }
  },
  computed: {
    pendingCount() {
      return this.applications.filter(app => app.status === '待审核').length
    },
    approvedCount() {
      return this.applications.filter(app => app.status === '已通过').length
    },
    filteredApplications() {
      if (!this.searchQuery) return this.applications
      const query = this.searchQuery.toLowerCase()
      return this.applications.filter(app => 
        app.username.toLowerCase().includes(query) || 
        app.job_title.toLowerCase().includes(query) ||
        app.application_id.toString().includes(query)
    )}
  },
  created() {
    this.fetchApplications()
  },
  methods: {
    fetchApplications() {
      this.loading = true
      axios.get('/api/apply/all')
        .then(res => {
          this.applications = res.data

          this.interviewTimes = {}
          this.interviewLinks = {}
          this.isEditingInterview = {}
          this.isSubmittingInterview = {}

          res.data.forEach(app => {
            if (app.interview_time) {
              this.interviewTimes[app.application_id] = app.interview_time.slice(0,16)
            }
            if (app.interview_link) {
              this.interviewLinks[app.application_id] = app.interview_link
            }
            this.isEditingInterview[app.application_id] = false
            this.isSubmittingInterview[app.application_id] = false
          })
        })
        .catch(err => {
          console.error('数据获取失败：', err)
          this.showMessage('数据连接中断', 'error')
        })
        .finally(() => {
          this.loading = false
        })
    },
    approve(applicationId) {
      axios.post('/api/apply/admin/review', {
        application_id: applicationId,
        status: '已通过'
      }).then(() => {
        const app = this.applications.find(a => a.application_id === applicationId)
        if (app) app.status = '已通过'
        this.showMessage('申请已核准', 'success')
      }).catch(err => {
        console.error(err)
        this.showMessage('核准失败', 'error')
      })
    },
    reject(applicationId) {
      axios.post('/api/apply/admin/review', {
        application_id: applicationId,
        status: '已拒绝'
      }).then(() => {
        const app = this.applications.find(a => a.application_id === applicationId)
        if (app) app.status = '已拒绝'
        this.showMessage('申请已驳回', 'warning')
      }).catch(err => {
        console.error(err)
        this.showMessage('驳回失败', 'error')
      })
    },
    setInterview(applicationId) {
      const rawTime = this.interviewTimes[applicationId]
      if (!rawTime) {
        this.showMessage('请选择面试时间', 'error')
        return
      }
      
      const formattedTime = rawTime.slice(0, 16)
      const interviewLink = 'http://localhost:5174/#/AIInterview'

      this.isSubmittingInterview[applicationId] = true

      axios.post('/api/apply/admin/interview', {
        application_id: applicationId,
        interview_time: formattedTime,
        interview_link: interviewLink
      }).then(() => {
        this.interviewLinks[applicationId] = interviewLink
        this.isEditingInterview[applicationId] = false
        this.showMessage('面试安排已保存', 'success')
      }).catch(err => {
        console.error('面试设置失败：', err)
        this.showMessage('设置保存错误', 'error')
      }).finally(() => {
        this.isSubmittingInterview[applicationId] = false
      })
    },
    editInterview(applicationId) {
      this.isEditingInterview[applicationId] = true
    },
    formatDateTime(dtString) {
      if (!dtString) return ''
      return dtString.replace('T', ' ')
    },
    getStatusClass(status) {
      return {
        '已通过': 'status-approved',
        '已拒绝': 'status-rejected',
        '待审核': 'status-pending'
      }[status] || ''
    },
    showMessage(message, type) {
      // 实际项目中可替换为更美观的通知组件
      alert(message)
    },
    // 新增：预览简历方法
    previewResume(url, candidateName) {
      this.currentResume = {
        url: url,
        candidateName: candidateName
      }
      this.showResumeModal = true
    },
    // 新增：关闭预览方法
    closeResumeModal() {
      this.showResumeModal = false
      this.currentResume = {
        url: '',
        candidateName: ''
      }
    },
    // 新增：获取预览URL方法
    getPreviewUrl(url) {
      // 使用Google文档预览服务
      return `https://docs.google.com/gview?url=${encodeURIComponent(url)}&embedded=true`
    },
    // 新增：下载简历方法
    downloadResume(url) {
      window.open(url, '_blank')
    }
  }
}
</script>

<style scoped>
/* 现代化UI设计变量 */
.resume-preview-modal {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999;
}
.resume-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.resume-modal {
  background-color: white;
  border-radius: 8px;
  width: 80%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.modal-close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #666;
}

.modal-body {
  flex: 1;
  padding: 20px;
  overflow: auto;
}

.resume-iframe {
  width: 100%;
  height: 100%;
  min-height: 500px;
  border: none;
}

.modal-footer {
  padding: 12px 24px;
  border-top: 1px solid #e8e8e8;
  display: flex;
  justify-content: flex-end;
}

.download-btn {
  padding: 8px 16px;
  background-color: #4361ee;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.download-btn:hover {
  background-color: #3a56d4;
}

.no-resume {
  text-align: center;
  padding: 40px;
  color: #666;
}
.resume-preview-overlay {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
}
.resume-preview-content {
  width: 80vw;
  height: 90vh;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}
.modal-header {
  padding: 12px;
  font-weight: bold;
  background: #f5f5f5;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
}
.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}
.resume-iframe {
  flex: 1;
  width: 100%;
  border: none;
}
:root {
  --primary-color: #4361ee;
  --primary-light: #e6e9ff;
  --success-color: #4cc9f0;
  --danger-color: #f72585;
  --warning-color: #ff9e00;
  --text-dark: #2b2d42;
  --text-medium: #6c757d;
  --text-light: #adb5bd;
  --bg-color: #f8f9fa;
  --card-bg: #ffffff;
  --border-color: #e9ecef;
  --border-radius: 12px;
  --box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  --transition: all 0.3s ease;
}

/* 基础布局 */
.modern-hr-dashboard {
  min-height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-dark);
  font-family: 'Inter', -apple-system, system-ui, sans-serif;
  padding: 2rem;
}

/* 顶部导航 */
.dashboard-header {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  margin-bottom: 2rem;
  padding: 1.5rem 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: var(--primary-color);
}

.title-highlight {
  color: var(--primary-color);
  font-weight: 800;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

/* 搜索框 */
.search-container {
  display: flex;
  align-items: center;
  background: var(--bg-color);
  border-radius: 8px;
  padding: 0.6rem 1rem;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.search-container:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.search-container input {
  background: transparent;
  border: none;
  outline: none;
  min-width: 250px;
  font-size: 0.95rem;
  color: var(--text-dark);
}

/* 数据概览卡片 */
.metrics-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.metric-card {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 1.8rem;
  box-shadow: var(--box-shadow);
  border: 1px solid var(--border-color);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(67, 97, 238, 0.1);
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

.metric-label {
  font-size: 1rem;
  color: var(--text-medium);
  font-weight: 500;
}

.metric-icon {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  font-size: 2rem;
  opacity: 0.2;
}

/* 卡片颜色变体 */
.total-applications {
  border-top: 4px solid var(--primary-color);
}

.pending-review {
  border-top: 4px solid var(--warning-color);
}

.approved {
  border-top: 4px solid var(--success-color);
}

/* 主内容区域 */
.main-content {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.content-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-dark);
}

/* 表格样式 */
.applications-table {
  padding: 1.5rem;
}

.table-responsive {
  overflow-x: auto;
}

.applications-list {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
}

.applications-list th {
  padding: 1rem 1.5rem;
  font-weight: 600;
  color: var(--text-medium);
  text-align: left;
  background: var(--bg-color);
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 2px solid var(--border-color);
}

.applications-list td {
  padding: 1.2rem 1.5rem;
  vertical-align: middle;
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
}

.application-row {
  background: var(--card-bg);
  transition: var(--transition);
}

.application-row:hover {
  background: var(--primary-light);
  box-shadow: 0 2px 8px rgba(67, 97, 238, 0.1);
}

/* 列宽设置 */
.col-id { width: 100px; }
.col-candidate { width: 220px; }
.col-position { width: 180px; }
.col-status { width: 120px; }
.col-resume { width: 150px; }
.col-actions { width: 200px; }

/* 候选人信息 */
.candidate-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.candidate-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), #6a8cff);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.candidate-details {
  flex: 1;
  min-width: 0;
}

.candidate-name {
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.candidate-id {
  font-size: 0.85rem;
  color: var(--text-light);
}

/* 岗位信息 */
.position-title {
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.department {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-top: 0.3rem;
}

/* 状态标签 */
.status-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  text-align: center;
}

.status-approved {
  background: #e6f7ed;
  color: #2b8a3e;
}

.status-rejected {
  background: #ffebee;
  color: #c92a2a;
}

.status-pending {
  background: #fff8e6;
  color: #f59f00;
}

/* 按钮样式 */
.action-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 2px solid transparent; /* 添加边框 */
  outline: none;
}

.approve-btn {
  background-color: #e8f5e9; /* 浅绿色背景 */
  color: #2e7d32; /* 深绿色文字 */
  border-color: #a5d6a7; /* 边框颜色 */
}

/* 拒绝按钮 - 红色主题 */
.reject-btn {
  background-color: #ffebee; /* 浅红色背景 */
  color: #c62828; /* 深红色文字 */
  border-color: #ef9a9a; /* 边框颜色 */
}

.reject-btn:hover {
  background-color: #ffcdd2; /* 悬停时稍深的红色 */
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
/* 按钮图标样式 */
.icon-check {
  color: #2e7d32; /* 绿色图标 */
}

.icon-close {
  color: #c62828; /* 红色图标 */
}
/* 面试安排表单 */
.interview-schedule {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--bg-color);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.scheduled-info {
  font-size: 0.9rem;
  color: var(--text-medium);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.info-item a {
  color: var(--primary-color);
  text-decoration: none;
}

.info-item a:hover {
  text-decoration: underline;
}

.edit-btn {
  background: var(--warning-color);
  color: white;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.schedule-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  color: var(--text-medium);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-input {
  padding: 0.7rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 0.9rem;
  transition: var(--transition);
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.save-btn {
  background: var(--primary-color);
  color: white;
  padding: 0.7rem 1rem;
  font-size: 0.9rem;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--primary-light);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: var(--text-medium);
  font-size: 0.95rem;
}

/* 过渡动画 */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter, .slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .metrics-container {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .modern-hr-dashboard {
    padding: 1.5rem;
  }
  
  .metrics-container {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1.2rem;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    flex-direction: column;
    gap: 1rem;
  }
  /* 按钮容器 */
.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
  .search-container {
    width: 100%;
  }
  
  .content-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .applications-list th, 
  .applications-list td {
    padding: 1rem;
    font-size: 0.9rem;
  }
}

/* 数据卡片基础样式 */
.metric-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 待审核卡片样式 */
.pending-review {
  background: linear-gradient(135deg, #81D4FA, #4FC3F7);
  color: black; /* 白色文字 */
  border-left: 5px solid #E65100; /* 左侧边框 */
}

/* 已通过卡片样式 */
.approved {
  background: linear-gradient(135deg, #66BB6A, #43A047); /* 绿色渐变 */
  color: black; /* 白色文字 */
  border-left: 5px solid #2E7D32; /* 左侧边框 */
}

/* 数值样式 */
.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 8px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 标签样式 */
.metric-label {
  font-size: 1rem;
  font-weight: 500;
  opacity: 0.9;
}

/* 图标样式 */
.metric-icon {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 2.5rem;
  opacity: 0.2;
  color:black; /* 确保图标也是白色 */
}

/* 悬停效果 */
.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .metric-card {
    padding: 15px;
  }
  .metric-value {
    font-size: 2rem;
  }
}
</style>
