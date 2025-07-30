<template>
  <div class="modern-hr-dashboard">
    <!-- 简历预览模态框 -->
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
    <div class="metrics-container" style="margin-top: 20px;">
      <div class="metric-card total-applications" style="padding: 16px; height: 100px;">
        <div class="metric-value" style="font-size: 28px;">{{ applications.length }}</div>
        <div class="metric-label">总申请数</div>
        <div class="metric-icon" style="font-size: 36px;">
          <i class="icon-document"></i>
        </div>
      </div>
      
      <div class="metric-card pending-review" style="padding: 16px; height: 100px;">
        <div class="metric-value" style="font-size: 28px;">{{ pendingCount }}</div>
        <div class="metric-label">待审核</div>
        <div class="metric-icon" style="font-size: 36px;">
          <i class="icon-clock"></i>
        </div>
      </div>
      
      <div class="metric-card approved" style="padding: 16px; height: 100px;">
        <div class="metric-value" style="font-size: 28px;">{{ approvedCount }}</div>
        <div class="metric-label">已通过</div>
        <div class="metric-icon" style="font-size: 36px;">
          <i class="icon-check"></i>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <div class="content-header">
        <h2 class="section-title">候选人申请列表</h2>
        <div class="section-actions">
          <div class="filter-container">
            <select v-model="statusFilter" class="status-filter">
              <option value="">全部状态</option>
              <option value="待审核">待审核</option>
              <option value="已通过">已通过</option>
              <option value="已拒绝">已拒绝</option>
            </select>
          </div>
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
              <tr v-for="app in paginatedApplications" :key="app.application_id" class="application-row">
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
                          <a :href="interviewLinks[app.application_id]" target="_blank" rel="noopener noreferrer">面试链接</a>
                        </div>
                        <button @click="editInterview(app.application_id)" class="edit-btn">
                          <i class="icon-edit"></i> 编辑安排
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

        <!-- 分页控件 -->
        <div class="pagination-container">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            上一页
          </button>
          <span class="page-info">
            第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
          </span>
          <button 
            @click="nextPage" 
            :disabled="currentPage === totalPages"
            class="pagination-btn"
          >
            下一页
          </button>
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
      showResumeModal: false,
      currentResume: {
        url: '',
        candidateName: ''
      },
      statusFilter: '',
      currentPage: 1,
      pageSize: 5
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
      let filtered = this.applications
      
      // 状态筛选
      if (this.statusFilter) {
        filtered = filtered.filter(app => app.status === this.statusFilter)
      }
      
      // 搜索筛选
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(app => 
          app.username.toLowerCase().includes(query) || 
          app.job_title.toLowerCase().includes(query) ||
          app.application_id.toString().includes(query)
      )}
      
      return filtered
    },
    paginatedApplications() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredApplications.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredApplications.length / this.pageSize) || 1
    }
  },
  watch: {
    statusFilter() {
      this.currentPage = 1
    },
    searchQuery() {
      this.currentPage = 1
    }
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
        this.showMessage('申请已拒绝', 'success')
      }).catch(err => {
        console.error(err)
        this.showMessage('拒绝失败', 'error')
      })
    },
    editInterview(applicationId) {
      this.isEditingInterview[applicationId] = true
    },
    setInterview(applicationId) {
      if (!this.interviewTimes[applicationId]) {
        this.showMessage('请填写面试时间', 'warning')
        return
      }
      this.isSubmittingInterview[applicationId] = true

      // 自动生成面试链接
      if (!this.interviewLinks[applicationId]) {
        this.interviewLinks[applicationId] = `https://interview.example.com/${applicationId}`
      }

      axios.post('/api/apply/admin/interview', {
        application_id: applicationId,
        interview_time: this.interviewTimes[applicationId],
        interview_link: this.interviewLinks[applicationId]
      }).then(() => {
        this.isEditingInterview[applicationId] = false
        this.showMessage('面试安排已保存', 'success')
      }).catch(err => {
        console.error(err)
        this.showMessage('保存失败', 'error')
      }).finally(() => {
        this.isSubmittingInterview[applicationId] = false
      })
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
    getStatusClass(status) {
      switch (status) {
        case '待审核': return 'status-pending'
        case '已通过': return 'status-approved'
        case '已拒绝': return 'status-rejected'
        default: return 'status-unknown'
      }
    },
    previewResume(url, candidateName) {
      this.currentResume.url = url
      this.currentResume.candidateName = candidateName
      this.showResumeModal = true
    },
    closeResumeModal() {
      this.showResumeModal = false
      this.currentResume = { url: '', candidateName: '' }
    },
    getPreviewUrl(path) {
      // 使用Google文档预览器预览简历
      return `https://docs.google.com/gview?url=${encodeURIComponent(path)}&embedded=true`
    },
    downloadResume(url) {
      if (!url) return
      window.open(url, '_blank')
    },
    showMessage(msg, type = 'info') {
      // 可替换为ElementUI的Message组件
      alert(`[${type}] ${msg}`)
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    }
  }
}
</script>

<style scoped>
/* 新增的筛选和分页样式 */
.filter-container {
  margin-right: 16px;
}

.status-filter {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #d1d9ff;
  background: #fff;
  color: #4354e8;
  font-weight: 600;
  outline: none;
  cursor: pointer;
}

.status-filter:focus {
  border-color: #4354e8;
  box-shadow: 0 0 6px #4354e8aa;
}

.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 24px;
  gap: 16px;
}

.pagination-btn {
  padding: 8px 16px;
  background: #4354e8;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #3547c9;
}

.pagination-btn:disabled {
  background: #a8b4ff;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #4354e8;
  font-weight: 600;
}


.modern-hr-dashboard {
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background: #f9fbff;
  min-height: 100vh;
  color: #333;
  padding: 24px 36px;
}

/* 顶部导航 */
.dashboard-header {
  background: linear-gradient(90deg, #4354e8 0%, #5a63e5 100%);
  padding: 18px 36px;
  border-radius: 12px;
  box-shadow: 0 12px 28px rgba(67, 84, 232, 0.3);
  margin-bottom: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.header-content {
  max-width: 1440px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.dashboard-title {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}
.title-highlight {
  color: #f5a623;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}
.action-btn {
  cursor: pointer;
  border: none;
  background: transparent;
  color: #fff;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}
.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}
.refresh-btn i, .search-container i {
  font-size: 18px;
}
.search-container {
  position: relative;
  display: flex;
  align-items: center;
}
.search-container input {
  padding: 6px 12px 6px 32px;
  border-radius: 20px;
  border: none;
  outline: none;
  font-size: 14px;
  width: 200px;
  transition: box-shadow 0.3s ease;
}
.search-container input:focus {
  box-shadow: 0 0 8px #4354e8;
}
.search-container i {
  position: absolute;
  left: 10px;
  color: #666;
}

/* 数据概览卡片 */
.metrics-container {
  display: flex;
  gap: 24px;
  margin-bottom: 36px;
  justify-content: center;
  max-width: 1440px;
  margin-left: auto;
  margin-right: auto;
}
.metric-card {
  flex: 1;
  max-width: 280px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 12px 24px rgba(67, 84, 232, 0.12);
  padding: 24px;
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.3s ease;
  cursor: default;
}
.metric-card:hover {
  box-shadow: 0 20px 36px rgba(67, 84, 232, 0.2);
}
.metric-value {
  font-size: 40px;
  font-weight: 700;
  color: #2c3e80;
  margin-bottom: 8px;
  user-select: none;
}
.metric-label {
  font-size: 16px;
  color: #7b8abe;
  margin-bottom: 16px;
  user-select: none;
}
.metric-icon {
  position: absolute;
  right: 20px;
  bottom: 20px;
  font-size: 48px;
  color: #d0d6f9;
  user-select: none;
}
/* 颜色区分 */
.total-applications {
  border-left: 5px solid #4354e8;
}
.pending-review {
  border-left: 5px solid #f5a623;
}
.approved {
  border-left: 5px solid #27ae60;
}

/* 主内容 */
.main-content {
  max-width: 1440px;
  margin-left: auto;
  margin-right: auto;
}
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e80;
}
.section-actions .export-btn {
  background: #4354e8;
  color: #fff;
  border-radius: 24px;
  padding: 8px 18px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}
.section-actions .export-btn:hover {
  background: #2f3bbb;
}

/* 加载 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 0;
  color: #7b8abe;
}
.loading-spinner {
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

/* 表格 */
.applications-table {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 14px 40px rgba(67, 84, 232, 0.1);
  padding: 20px;
  overflow-x: auto;
}
.applications-list {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 16px;
  font-size: 14px;
  color: #3a3a3a;
}
.applications-list thead th {
  text-align: left;
  font-weight: 700;
  padding: 12px 24px;
  background: #f2f4ff;
  color: #4354e8;
  user-select: none;
  border-bottom: 2px solid #d1d9ff;
}
.applications-list tbody tr {
  background: #fff;
  box-shadow: 0 4px 16px rgba(67, 84, 232, 0.08);
  border-radius: 12px;
}
.applications-list tbody tr:hover {
  background: #f8faff;
}
.applications-list td {
  padding: 16px 24px;
  vertical-align: middle;
}
.col-id { width: 80px; }
.col-candidate { width: 220px; }
.col-position { width: 200px; }
.col-status { width: 110px; }
.col-resume { width: 120px; }
.col-actions { width: 320px; }

/* 候选人头像和信息 */
.candidate-avatar {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #4354e8 0%, #5a63e5 100%);
  border-radius: 50%;
  color: #fff;
  font-weight: 700;
  font-size: 20px;
  line-height: 44px;
  text-align: center;
  user-select: none;
  margin-right: 12px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(67, 84, 232, 0.3);
}
.candidate-info {
  display: flex;
  align-items: center;
}
.candidate-details {
  display: flex;
  flex-direction: column;
}
.candidate-name {
  font-weight: 600;
  color: #2c3e80;
}
.candidate-id {
  font-size: 12px;
  color: #7b8abe;
  user-select: text;
}

/* 职位和部门 */
.position-title {
  font-weight: 600;
  color: #2c3e80;
}
.department {
  font-size: 12px;
  color: #7b8abe;
  margin-top: 4px;
}

/* 状态标签 */
.status-badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-weight: 600;
  user-select: none;
  width: fit-content;
  min-width: 68px;
  text-align: center;
}
.status-pending {
  background: #f5a62333;
  color: #f5a623;
  box-shadow: 0 0 8px #f5a62399;
}
.status-approved {
  background: #27ae6033;
  color: #27ae60;
  box-shadow: 0 0 8px #27ae6099;
}
.status-rejected {
  background: #e74c3c33;
  color: #e74c3c;
  box-shadow: 0 0 8px #e74c3c99;
}
.status-unknown {
  background: #bdc3c733;
  color: #7b8abe;
}

/* 简历按钮 */
.resume-btn {
  background: transparent;
  border: 1.5px solid #4354e8;
  color: #4354e8;
  padding: 6px 14px;
  border-radius: 24px;
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.resume-btn:hover {
  background: #4354e8;
  color: #fff;
}
.no-resume {
  font-size: 13px;
  color: #999;
  user-select: none;
}

/* 操作按钮 */
.application-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.action-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}
.action-btn {
  flex: 1;
  padding: 10px 16px;
  font-weight: 600;
  font-size: 14px;
  border-radius: 30px;
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.3s ease;
  user-select: none;
}
.approve-btn {
  background: #27ae60;
  color: #fff;
  box-shadow: 0 6px 12px rgba(39, 174, 96, 0.3);
}
.approve-btn:hover {
  background: #219150;
  box-shadow: 0 8px 16px rgba(33, 145, 80, 0.45);
}
.reject-btn {
  background: #e74c3c;
  color: #fff;
  box-shadow: 0 6px 12px rgba(231, 76, 60, 0.3);
}
.reject-btn:hover {
  background: #cf3a2e;
  box-shadow: 0 8px 16px rgba(207, 58, 46, 0.45);
}

/* 面试安排卡片 */
.interview-schedule {
  background: #f5f7ff;
  border-radius: 20px;
  box-shadow: inset 0 0 12px rgba(67, 84, 232, 0.06);
  padding: 16px 20px;
  font-size: 14px;
  color: #2c3e80;
  user-select: none;
}
.scheduled-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}
.info-item i {
  color: #4354e8;
  font-size: 18px;
}
.info-item a {
  color: #4354e8;
  font-weight: 600;
  text-decoration: none;
}
.info-item a:hover {
  text-decoration: underline;
}
.edit-btn {
  background: #4354e8;
  color: #fff;
  border-radius: 20px;
  padding: 6px 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease;
}
.edit-btn:hover {
  background: #3547c9;
}

/* 面试编辑表单 */
.schedule-form {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-group label {
  font-weight: 600;
  color: #4354e8;
  display: flex;
  align-items: center;
  gap: 6px;
}
.form-group label i {
  font-size: 18px;
}
.form-input {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1.8px solid #d1d9ff;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
}
.form-input:focus {
  border-color: #4354e8;
  box-shadow: 0 0 6px #4354e8aa;
}
.save-btn {
  align-self: flex-start;
  background: #4354e8;
  color: #fff;
  font-weight: 700;
  border: none;
  padding: 10px 22px;
  border-radius: 24px;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(67, 84, 232, 0.35);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s ease;
}
.save-btn:disabled {
  background: #a8b4ff;
  cursor: not-allowed;
  box-shadow: none;
}
.save-btn:hover:not(:disabled) {
  background: #3547c9;
}

/* 动画 */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.35s ease;
}
.slide-fade-enter-from, .slide-fade-leave-to {
  max-height: 0;
  opacity: 0;
  padding: 0 20px;
}
.slide-fade-enter-to, .slide-fade-leave-from {
  max-height: 200px;
  opacity: 1;
  padding: 16px 20px;
}

/* 模态框 */
.resume-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(18, 26, 44, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.resume-modal {
  background: #fff;
  border-radius: 24px;
  width: 720px;
  max-width: 95vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(67, 84, 232, 0.3);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #4354e8;
  color: #fff;
  padding: 18px 24px;
  font-size: 18px;
  font-weight: 700;
}
.modal-close-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #fff;
  font-size: 22px;
  line-height: 1;
  padding: 0;
  display: flex;
  align-items: center;
}
.modal-close-btn i {
  pointer-events: none;
}
.modal-body {
  flex: 1;
  overflow: auto;
  background: #f9fbff;
}
.resume-iframe {
  width: 100%;
  height: 100%;
  border: none;
  min-height: 480px;
}
.no-resume {
  padding: 40px;
  color: #7b8abe;
  font-size: 16px;
  text-align: center;
  user-select: none;
}
.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #d1d9ff;
  background: #f2f4ff;
  display: flex;
  justify-content: flex-end;
}
.download-btn {
  background: #4354e8;
  color: #fff;
  border-radius: 24px;
  border: none;
  padding: 10px 20px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s ease;
}
.download-btn:hover {
  background: #3547c9;
}

/* 图标字体定义 */
.icon-refresh::before { content: "⟳"; }
.icon-search::before { content: "🔍"; }
.icon-document::before { content: "📄"; }
.icon-clock::before { content: "⏰"; }
.icon-check::before { content: "✔"; }
.icon-close::before { content: "✖"; }
.icon-eye::before { content: "👁"; }
.icon-download::before { content: "⬇"; }
.icon-edit::before { content: "✎"; }
.icon-calendar::before { content: "📅"; }
.icon-link::before { content: "🔗"; }
.icon-video::before { content: "🎥"; }
.icon-save::before { content: "💾"; }
</style>