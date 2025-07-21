<template>
  <div class="job-list-container">
    <h1 class="page-title">岗位管理</h1>

    <!-- 搜索与筛选区域 -->
    <div class="filters-container">
      <div class="search-box">
        <input 
          v-model="searchKeyword" 
          placeholder="搜索岗位名称、公司或地点" 
          @input="fetchJobs" 
          class="search-input"
        />
      </div>
      <div class="filter-selector">
        <select v-model="selectedCity" @change="fetchJobs" class="filter-select">
          <option value="">所有地点</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
      <div class="filter-selector">
        <select v-model="selectedSalaryRange" @change="fetchJobs" class="filter-select">
          <option value="">所有薪资</option>
          <option value="0-5000">5K 以下</option>
          <option value="5000-10000">5K - 10K</option>
          <option value="10000-15000">10K - 15K</option>
          <option value="15000-20000">15K - 20K</option>
          <option value="20000-30000">20K - 30K</option>
          <option value="30000+">30K+</option>
        </select>
      </div>
      <button @click="resetFilters" class="reset-btn">重置</button>
    </div>

    <div class="divider"></div>

    <!-- 左右两栏 -->
    <div class="main-content">
      <!-- 左侧岗位列表 -->
      <div class="left-panel">
        <h2>可申请岗位</h2>
        <div v-if="loading" class="loading-state">加载中...</div>
        <div v-else-if="filteredJobs.length === 0" class="empty-state">暂无符合条件的岗位</div>
        <div v-else class="job-list">
          <div v-for="job in filteredJobs" :key="job.id" class="job-card">
            <div class="job-header">
              <h3 class="job-title">{{ job.job_title }}</h3>
              <div class="job-meta">
                <span class="company-name">{{ job.company || '知名企业' }}</span>
                <span class="job-location">{{ job.location }}</span>
                <span class="job-date">{{ job.publish_date }}</span>
              </div>
            </div>
            
            <div class="job-details">
              <div class="salary-info">
                <span class="salary">{{ job.salary }}</span>
                <span class="job-type">全职</span>
              </div>
              <div class="requirements">
                <span class="experience">{{ job.experience_req }}</span>
                <span class="education">{{ job.education_req }}</span>
              </div>
            </div>

            <div class="job-tags">
              <span v-for="(tag, index) in job.tags" :key="index" class="tag">{{ tag }}</span>
            </div>

            <div class="job-description">
              {{ job.description || '岗位描述略...' }}
            </div>

            <div class="job-footer">
              <button @click="applyJob(job.id)" class="apply-btn">立即申请</button>

              <button @click="triggerUpload(job.id)" :disabled="uploading && uploadingJobId === job.id" class="upload-btn">
                {{ uploading && uploadingJobId === job.id ? '上传中...' : '上传简历' }}
              </button>

                   <input
                      type="file"
                      :ref="'fileInput' + job.id"
                      class="hidden-file-input"
                      @change="uploadResume($event, job.id)"
                      accept=".pdf,.doc,.docx"
                    />
                   <!-- 新增查看按钮 -->
                        <button 
                          v-if="job.photo_path" 
                          @click="viewPhoto(job.photo_path)" 
                          class="view-photo-btn"
                        >
                          查看证件照
                        </button>
              <a href="#" class="view-more">查看更多</a>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧已申请岗位 -->
      <div class="right-panel">
        <h2>已申请岗位</h2>
        <div v-if="loadingApplied" class="loading-state">加载中...</div>
        <div v-else-if="appliedJobs.length === 0" class="empty-state">你还没有申请岗位</div>
        <div v-else class="job-list">
          <div v-for="job in appliedJobs" :key="job.id" class="job-card applied-job-card">
            <div class="job-header">
              <h3 class="job-title">{{ job.job_title }}</h3>
              <div class="job-meta">
                <span class="job-location">{{ job.location }}</span>
                <span class="job-date">{{ job.apply_time }}</span>
              </div>
            </div>

            <div class="job-details">
              <div class="salary-info">
                <span class="salary">{{ job.salary }}</span>
              </div>
              <div class="requirements">
                <span class="experience">{{ job.experience_req }}</span>
                <span class="education">{{ job.education_req }}</span>
              </div>
            </div>

            <div class="application-status">
              申请状态：<span :class="statusClass(job.application_status)">{{ job.application_status }}</span>
            </div>

            <!-- 通过状态显示“查看面试信息”按钮 -->
            <div v-if="job.application_status === '已通过'" class="interview-info">
              <button @click="showInterviewInfo(job)" class="view-interview-btn">查看面试信息</button>
            </div>

                          <!-- 新增：上传证件照 -->
              <div v-if="job.application_status === '已通过'" class="resume-link">
                <button 
                  @click="triggerPhotoUpload(job.id)" 
                  :disabled="uploadingPhoto && uploadingPhotoJobId === job.id"
                  class="upload-btn"
                >
                  {{ uploadingPhoto && uploadingPhotoJobId === job.id ? '上传中...' : '上传证件照' }}
                </button>
                <input
                  type="file"
                  :ref="'photoInput' + job.id"
                  class="hidden-file-input"
                  @change="uploadPhoto($event, job.id)"
                  accept="image/*"
                />
                                      <!-- 新增查看证件照按钮 -->
                              <button
                                v-if="job.photo_path"
                                @click="viewPhoto(job.photo_path)"
                                class="apply-btn"  
                              >
                                查看证件照
                              </button>

              </div>

            <div v-if="job.resume_path" class="resume-link">
              <a :href="job.resume_path" target="_blank" rel="noopener noreferrer">查看已上传简历</a>
            </div>
          </div>
        </div>
      </div>
    </div>

<!-- ✅ 面试信息弹窗(只展示) -->
    <div v-if="showInterviewModal" class="modal-overlay" @click.self="closeInterviewModal">
      <div class="modal-content">
        <h3>面试信息</h3>
        <p><strong>岗位：</strong>{{ currentInterviewJob.job_title }}</p>
        <p><strong>时间：</strong>{{ currentInterviewJob.interview_time || '待定' }}</p>
        <p>
          <strong>会议链接：</strong>
          <span v-if="currentInterviewJob.interview_link">{{ currentInterviewJob.interview_link }}</span>
          <span v-else>无链接</span>
        </p>

        <!-- 这里改成打开摄像头预览弹窗 -->
        <button
          v-if="currentInterviewJob.interview_link"
          @click="openFacePreview"
          class="verify-btn"
        >
          身份验证并进入会议
        </button>

        <button class="close-btn" @click="closeInterviewModal">关闭</button>
      </div>
    </div>


 <!-- 证件照弹窗 -->
    <div v-if="showPhotoModal" class="modal-overlay" @click.self="closePhotoModal">
      <div class="modal-content" style="max-width: 90vw; max-height: 90vh; overflow: auto;">
        <img :src="currentPhotoPath" alt="证件照" style="max-width: 100%; max-height: 80vh;" />
        <button @click="closePhotoModal" class="close-btn">关闭</button>
      </div>
    </div>

    <!-- 身份验证摄像头预览弹窗（新增） -->
    <div v-if="showFacePreview" class="modal-overlay" @click.self="closeFacePreview">
      <div class="modal-content" style="max-width: 400px;">
        <h3>请确认摄像头画面</h3>
        <video
          ref="videoPreview"
          autoplay
          playsinline
          muted
          style="width: 100%; border-radius: 6px; background: black;"
        ></video>
        <div style="margin-top: 12px; text-align: right;">
          <button class="close-btn" @click="closeFacePreview">取消</button>
          <button class="apply-btn" @click="captureAndVerify">开始身份验证</button>
        </div>
      </div>
    </div>
<!-- ✅ 插入这里：身份验证成功后的二次确认弹窗 -->
<div
  v-if="showJoinConfirm"
  class="modal-overlay"
  @click.self="showJoinConfirm = false"
>
  <div class="modal-content">
    <h3>身份验证通过 ✅</h3>
     <p style="margin-top:12px;">
      相似度：{{ similarityScore.toFixed(2) }}%
    </p>
    <p style="margin-top:12px;">是否立即进入会议？</p>
    <div style="text-align:right;margin-top:24px;">
      <button class="close-btn" @click="showJoinConfirm = false">稍后进入</button>
      <button class="apply-btn" style="margin-left:12px;" @click="goToMeeting">
        进入会议
      </button>
    </div>
  </div>
</div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'JobList',
  data() {
    return {
      jobs: [],
      appliedJobs: [],
      loading: false,
      loadingApplied: false,
      searchKeyword: '',
      selectedCity: '',
      selectedSalaryRange: '',
      cities: ['广州', '上海', '北京', '深圳', '杭州', '南京', '天津', '苏州', '成都', '重庆', '武汉', '西安', '长沙', '郑州', '青岛', '合肥', '佛山', '宁波', '无锡', '东莞', '厦门', '昆明', '济南', '福州', '南昌', '南宁'],
      showInterviewModal: false,
      currentInterviewJob: {},
      uploadingJobId: null,
      uploading: false,
      uploadingPhotoJobId: null,
      uploadingPhoto: false,
      showPhotoModal: false,
      currentPhotoPath: '',
       showJoinConfirm: false,  // 是否显示二次确认弹窗
    verifiedLink: '',        // 验证成功后保存会议链接
    similarityScore: 0,
       // 新增摄像头预览相关状态
      showFacePreview: false,
      videoStream: null,
    }
  },
  computed: {
    filteredJobs() {
      return this.jobs.map(job => ({
        ...job,
        tags: job.tags || ['Vue3', 'TypeScript', '前端工程化', '性能优化', 'Webpack']
      })).filter(job => {
        const keywordMatch = this.searchKeyword === '' ||
          job.job_title.toLowerCase().includes(this.searchKeyword.toLowerCase()) ||
          job.location.toLowerCase().includes(this.searchKeyword.toLowerCase())

        const cityMatch = this.selectedCity === '' || job.location === this.selectedCity

        const salaryMatch = (() => {
          if (!this.selectedSalaryRange) return true
          const [min, max] = this.selectedSalaryRange.split('-')
          const salary = parseInt(job.salary.split('-')[0])
          if (this.selectedSalaryRange.includes('+')) return salary >= 30000
          return salary >= min && salary <= max
        })()

        return keywordMatch && cityMatch && salaryMatch
      })
    }
  },
  created() {
    this.fetchJobs()
    this.fetchAppliedJobs()
  },
  methods: {
    fetchJobs() {
      this.loading = true
      axios.get('/api/job/list')
        .then(res => this.jobs = res.data)
        .catch(err => console.error('获取岗位失败：', err))
        .finally(() => this.loading = false)
    },
    


  triggerPhotoUpload(jobId) {
  const inputRef = this.$refs['photoInput' + jobId]
  if (Array.isArray(inputRef)) {
    inputRef[0].click()
  } else if (inputRef) {
    inputRef.click()
  } else {
    console.error('找不到证件照 input ref:', jobId)
  }
},

async uploadPhoto(event, jobId) {
  const file = event.target.files[0]
  if (!file) return

  const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg']
  if (!allowedTypes.includes(file.type)) {
    alert('请上传 JPG/PNG 格式的证件照')
    event.target.value = ''
    return
  }

  this.uploadingPhoto = true
  this.uploadingPhotoJobId = jobId
  try {
    const formData = new FormData()
    formData.append('photo', file)
    formData.append('job_id', jobId)

    const res = await axios.post('/api/apply/upload_photo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    alert(res.data.msg || '证件照上传成功')
    this.fetchAppliedJobs()
  } catch (err) {
    alert(err.response?.data?.msg || '上传失败')
  } finally {
    this.uploadingPhoto = false
    this.uploadingPhotoJobId = null
    event.target.value = ''
  }
},
       // 新增这个方法，调用 /api/apply/all 获取带 photo_path 的数据
fetchApplyPhotos() {
  axios.get('/api/apply/all?user_id=1')
    .then(res => {
      const photoData = res.data || []
      this.appliedJobs = this.appliedJobs.map(job => {
        const matched = photoData.find(app => app.job_id === job.id)
        return {
          ...job,
          photo_path: matched ? matched.photo_path : ''
        }
      })
    })
    .catch(err => console.error('获取证件照数据失败：', err))
},
viewPhoto(photoPath) {
    console.log('viewPhoto triggered:', photoPath);
    this.currentPhotoPath = photoPath
    this.showPhotoModal = true
  },

  closePhotoModal() {
    this.showPhotoModal = false
    this.currentPhotoPath = ''
  },
  

fetchAppliedJobs() {
  this.loadingApplied = true
  axios.get('/api/job/applied')
    .then(res => {
      this.appliedJobs = res.data.map(job => ({
        ...job,
        interview_time: job.interview_time || '',
        interview_link: job.interview_link || ''
      }))
    })
    .then(() => this.fetchApplyPhotos())  // 这里写在 then 链外面，作用于 Promise
    .catch(err => console.error('获取已申请岗位失败：', err))
    .finally(() => this.loadingApplied = false)
},


    resetFilters() {
      this.searchKeyword = ''
      this.selectedCity = ''
      this.selectedSalaryRange = ''
      this.fetchJobs()
    },
    applyJob(jobId) {
      axios.post('/api/job/apply', {
        job_id: jobId
      })
      .then(res => {
        alert(res.data.msg || '申请成功')
        this.fetchAppliedJobs()
      })
      .catch(err => {
        const msg = err.response?.data?.msg || '申请失败'
        alert(msg)
      })
    },
    statusClass(status) {
      if(status === '已通过') return 'status-approved'
      if(status === '拒绝') return 'status-rejected'
      if(status === '待审核') return 'status-pending'
      return ''
    },

    triggerUpload(jobId) {
  const inputRef = this.$refs['fileInput' + jobId]
  // Vue 2 下，循环中ref会是数组
  if (Array.isArray(inputRef)) {
    inputRef[0].click()
  } else if (inputRef) {
    inputRef.click()
  } else {
    console.error('找不到对应的文件输入框 ref,jobId:', jobId)
  }
}
,



    async uploadResume(event, jobId) {
      const file = event.target.files[0]
      if (!file) return

      const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
      if (!allowedTypes.includes(file.type)) {
        alert('请上传 PDF 或 Word 格式的简历文件')
        event.target.value = ''
        return
      }

      this.uploading = true
      try {
        const formData = new FormData()
        formData.append('resume', file)
        formData.append('job_id', jobId)

        const res = await axios.post('/api/apply/upload_resume', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        alert(res.data.msg || '简历上传成功')
        this.fetchAppliedJobs()
      } catch (err) {
        alert(err.response?.data?.msg || '上传失败')
      } finally {
        this.uploading = false
        this.uploadingJobId = null
        event.target.value = ''
      }
    },

//比对

  async openCameraAndCaptureBlob() {
    return new Promise((resolve, reject) => {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          const video = document.createElement('video')
          video.srcObject = stream
          video.play()

          video.onloadedmetadata = () => {
            const canvas = document.createElement('canvas')
            canvas.width = video.videoWidth
            canvas.height = video.videoHeight
            const ctx = canvas.getContext('2d')

            // 等待视频稳定，截图
            setTimeout(() => {
              ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
              canvas.toBlob(blob => {
                // 关闭摄像头
                stream.getTracks().forEach(track => track.stop())
                resolve(blob)
              }, 'image/jpeg')
            }, 1000) // 延迟1秒截图
          }
        })
        .catch(err => {
          alert('无法打开摄像头，请检查权限和设备')
          reject(err)
        })
    })
  },


    //会议
 async showInterviewInfo (job) {
      try {
        const { data } = await axios.get('/api/apply/applied')
        const latest = (data || []).find(j => j.id === job.id)
        if (!latest) return alert('未找到该岗位的最新面试信息')
        this.currentInterviewJob = { ...latest }
        this.showInterviewModal = true
      } catch (e) {
        console.error(e)
        alert('获取面试信息失败')
      }
    },



    closeInterviewModal() {
      this.showInterviewModal = false
      this.currentInterviewJob = {}
    },

// 打开摄像头预览弹窗
    openFacePreview() {
      this.showInterviewModal = false  // 关闭面试信息弹窗
      this.showFacePreview = true
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.videoStream = stream
          this.$refs.videoPreview.srcObject = stream
        })
        .catch(() => {
          alert('无法打开摄像头，请检查权限和设备')
          this.showFacePreview = false
        })
    },
// 关闭摄像头预览弹窗并释放摄像头
    closeFacePreview() {
      this.showFacePreview = false
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop())
        this.videoStream = null
      }
    },
    // 点击“开始身份验证”抓拍、调用接口
    captureAndVerify() {
      if (!this.videoStream) {
        alert('摄像头未启动')
        return
      }
      const video = this.$refs.videoPreview
      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      canvas.toBlob(async (blob) => {
        this.closeFacePreview()  // 关闭预览并释放摄像头

        try {
          const fd = new FormData()
          fd.append('user_id', 1) // TODO：实际用户ID
          fd.append('job_id', this.currentInterviewJob.id)
          fd.append('photo', blob, 'live.jpg')

          const { data: res } = await axios.post(
            '/api/apply/face-verify',
            fd,
            { headers: { 'Content-Type': 'multipart/form-data' } }
          )

          if (res.passed) {
            this.similarityScore = (res.score || 0) * 100
            this.verifiedLink = this.currentInterviewJob.interview_link
            this.showJoinConfirm = true
          } else {
            alert(`身份验证失败，相似度 ${(res.score * 100).toFixed(2)}%，请重试`)
          }
        } catch (e) {
          alert('身份验证出错，请稍后再试')
          console.error(e)
        }
      }, 'image/jpeg')
    },

/* ② 身份验证并决定是否弹出二次确认 */
async handleFaceVerifyAndJoin () {
  try {
    this.showInterviewModal = false

    const photoBlob = await this.openCameraAndCaptureBlob()
    const fd = new FormData()
    fd.append('user_id', 1)                     
    fd.append('job_id', this.currentInterviewJob.id)
    fd.append('photo', photoBlob, 'live.jpg')

    const { data: res } = await axios.post(
      '/api/apply/face-verify',
      fd,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )

    if (res.passed) {
      this.similarityScore = (res.score || 0) * 100
      this.verifiedLink = this.currentInterviewJob.interview_link
      this.showJoinConfirm = true   // 打开二次确认弹窗
    } else {
      alert(`身份验证失败，相似度 ${(res.score * 100).toFixed(2)}%，请重试`)
    }
  } catch (e) {
    console.error('验证过程出错:', e)
    alert('身份验证出错，请稍后再试')
  }
}
,

   /* ③ 真正跳转会议 */
    goToMeeting () {
      if (this.verifiedLink) window.open(this.verifiedLink, '_blank')
      this.showJoinConfirm = false
    },

    /* ④ 保留原来的 openCameraAndCaptureBlob 等方法 */
  },


  }
</script>

<style>
.job-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #333;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #1a1a1a;
  position: relative;
  padding-bottom: 12px;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: #1890ff;
}

.filters-container {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 10px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
}

.search-input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  outline: none;
}

.filter-selector {
  min-width: 150px;
}

.filter-select {
  width: 100%;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  background-color: white;
  cursor: pointer;
}

.reset-btn {
  padding: 10px 16px;
  background-color: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.reset-btn:hover {
  background-color: #e6e6e6;
}

.divider {
  height: 1px;
  background: #f0f0f0;
  margin: 20px 0;
}

.main-content {
  display: flex;
  gap: 24px;
}

.left-panel, .right-panel {
  flex: 1;
  max-height: calc(100vh - 250px);
  overflow-y: auto;
  border-radius: 8px;
  padding: 16px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.right-panel {
  background-color: #fafafa;
}

h2 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #1a1a1a;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 40px 0;
  color: #666;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-card {
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  padding: 20px;
  transition: all 0.3s;
  background: white;
}

.job-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.job-header {
  margin-bottom: 12px;
}

.job-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1a1a1a;
}

.job-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #666;
}

.job-details {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.salary-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.salary {
  color: #ff6a00;
  font-weight: 600;
  font-size: 16px;
}

.job-type {
  background: #f0f7ff;
  color: #1890ff;
  padding: 2px 6px;
  border-radius: 2px;
  font-size: 12px;
}

.requirements {
  display: flex;
  gap: 12px;
  color: #666;
  font-size: 13px;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.tag {
  background: #f5f5f5;
  color: #666;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.job-description {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.job-footer {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}

.apply-btn {
  background: #1890ff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.apply-btn:hover {
  background: #40a9ff;
}

.upload-btn {
  background: #52c41a;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-btn:hover {
  background: #73d13d;
}

.view-more {
  color: #1890ff;
  text-decoration: none;
  font-size: 14px;
  margin-left: auto;
}

.view-more:hover {
  text-decoration: underline;
}

.applied-job-card {
  background-color: #f9f9f9;
}

.application-status {
  margin-top: 8px;
  font-size: 14px;
}

.status-approved {
  color: #52c41a;
  font-weight: 600;
}

.status-rejected {
  color: #ff4d4f;
  font-weight: 600;
}

.status-pending {
  color: #faad14;
  font-weight: 600;
}

.interview-info {
  margin-top: 12px;
}

.view-interview-btn {
  background-color: #1890ff;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.view-interview-btn:hover {
  background-color: #40a9ff;
}

.resume-link {
  margin-top: 8px;
}
.hidden-file-input {
  display: none;
}

.resume-link a {
  color: #1890ff;
  font-size: 13px;
  text-decoration: none;
}

.resume-link a:hover {
  text-decoration: underline;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 24px 32px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  text-align: left;
}

.modal-content h3 {
  margin-bottom: 16px;
  font-weight: 600;
  font-size: 22px;
  color: #1a1a1a;
}

.modal-content p {
  margin-bottom: 12px;
  font-size: 16px;
  color: #333;
}

.close-btn {
  background-color: #ff4d4f;
  border: none;
  color: white;
  padding: 8px 20px;
  border-radius: 4px;
  cursor: pointer;
  float: right;
  margin-top: 12px;
  transition: all 0.3s;
}

.close-btn:hover {
  background-color: #ff7875;
}


</style> 