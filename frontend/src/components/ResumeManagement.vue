<template>
  <div class="resume-dashboard">
    <!-- 背景装饰元素 -->
    <div class="bg-circle circle-1"></div>
    <div class="bg-circle circle-2"></div>
    <div class="bg-circle circle-3"></div>
    
    <header class="dashboard-header">
      <h1>简历管理中心</h1>
      <div class="header-actions">
        <button class="notification-btn">
          <i class="fas fa-bell"></i>
          <span class="badge">3</span>
        </button>
        <div class="user-profile">
          <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="用户头像">
          <span>张伟</span>
        </div>
      </div>
    </header>
    
    <div class="dashboard-content">
      <div class="stats-overview">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-file-alt"></i>
          </div>
          <div class="stat-info">
            <h3>简历总数</h3>
            <p>{{ resumes.length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-star"></i>
          </div>
          <div class="stat-info">
            <h3>默认简历</h3>
            <p>{{ resumes.filter(r => r.isDefault).length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-cloud-upload-alt"></i>
          </div>
          <div class="stat-info">
            <h3>附件总数</h3>
            <p>{{ totalAttachments }}</p>
          </div>
        </div>
      </div>
      
      <div class="action-bar">
        <div class="search-bar">
          <i class="fas fa-search"></i>
          <input type="text" placeholder="搜索简历..." v-model="searchQuery">
          <button class="clear-search" @click="searchQuery = ''" v-if="searchQuery">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="action-buttons">
          <button class="create-btn" @click="showCreateModal = true">
            <i class="fas fa-plus"></i> 新建简历
          </button>
          <button class="optimize-btn" @click="showOptimizeModal = true">
            <i class="fas fa-magic"></i> AI优化
          </button>
          <button class="import-btn" @click="showImportModal = true">
            <i class="fas fa-file-import"></i> 导入
          </button>
        </div>
      </div>
      
      <div class="resume-grid">
        <div class="resume-card" v-for="resume in filteredResumes" :key="resume.id" 
             :class="{ 'default-resume': resume.isDefault }">
          <div class="card-header">
            <h3>{{ resume.title }}</h3>
            <div class="card-actions">
              <button class="quick-action" @click="toggleDefault(resume.id)" 
                      :title="resume.isDefault ? '取消默认' : '设为默认'">
                <i class="fas" :class="resume.isDefault ? 'fa-star' : 'fa-star-o'"></i>
              </button>
              <button class="quick-action" @click="editResume(resume.id)" title="编辑">
                <i class="fas fa-edit"></i>
              </button>
              <button class="quick-action" @click="showShareModal(resume)" title="分享">
                <i class="fas fa-share-alt"></i>
              </button>
              <button class="quick-action danger" @click="confirmDelete(resume.id)" title="删除">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          
          <div class="card-body">
            <div class="resume-meta">
              <div class="meta-item">
                <i class="fas fa-user"></i>
                <span>{{ resume.name }}</span>
              </div>
              <div class="meta-item">
                <i class="fas fa-graduation-cap"></i>
                <span>{{ resume.education }}</span>
              </div>
              <div class="meta-item">
                <i class="fas fa-briefcase"></i>
                <span>{{ resume.experience }}年经验</span>
              </div>
              <div class="meta-item">
                <i class="fas fa-calendar"></i>
                <span>更新于 {{ formatDate(resume.updatedAt) }}</span>
              </div>
            </div>
            
            <div class="resume-preview" @click="previewResume(resume)">
              <div class="preview-content">
                <div class="preview-text">
                  <p v-for="(item, index) in resume.previewText" :key="index">{{ item }}</p>
                </div>
                <div class="preview-watermark">
                  <i class="fas fa-file-alt"></i>
                </div>
              </div>
            </div>
            
            <div class="attachments-section">
              <div class="section-header">
                <h4><i class="fas fa-paperclip"></i> 附件 ({{ resume.attachments.length }})</h4>
                <button class="add-attachment" @click.stop="addAttachment(resume.id)">
                  <i class="fas fa-plus"></i>
                </button>
              </div>
              <div class="attachments-list">
                <div class="attachment-item" v-for="file in resume.attachments" :key="file.name">
                  <div class="attachment-icon">
                    <i :class="getFileIcon(file.name)"></i>
                  </div>
                  <div class="attachment-info">
                    <div class="attachment-name">{{ file.name }}</div>
                    <div class="attachment-size">{{ file.size }}</div>
                  </div>
                  <div class="attachment-actions">
                    <button class="download-btn" @click.stop="downloadFile(file)" title="下载">
                      <i class="fas fa-download"></i>
                    </button>
                    <button class="preview-btn" @click.stop="previewFile(file)" title="预览">
                      <i class="fas fa-eye"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card-footer">
            <button class="view-btn" @click="previewResume(resume)">
              <i class="fas fa-expand"></i> 完整预览
            </button>
            <button class="export-btn" @click="exportResume(resume.id)">
              <i class="fas fa-file-export"></i> 导出
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创建简历模态框 -->
    <Modal v-if="showCreateModal" @close="showCreateModal = false" title="创建新简历" size="large">
      <template #body>
        <div class="create-resume-form">
          <div class="form-section">
            <h3>基本信息</h3>
            <div class="form-row">
              <div class="form-group">
                <label>简历名称 <span class="required">*</span></label>
                <input type="text" v-model="newResume.title" placeholder="例如: 高级前端开发工程师简历">
              </div>
              <div class="form-group">
                <label>求职岗位 <span class="required">*</span></label>
                <input type="text" v-model="newResume.position" placeholder="例如: 前端开发工程师">
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>姓名 <span class="required">*</span></label>
                <input type="text" v-model="newResume.name">
              </div>
              <div class="form-group">
                <label>期望薪资</label>
                <input type="text" v-model="newResume.salary" placeholder="例如: 20-30K">
              </div>
            </div>
          </div>
          
          <div class="form-section">
            <h3>教育背景</h3>
            <div class="form-row">
              <div class="form-group">
                <label>学历 <span class="required">*</span></label>
                <select v-model="newResume.education">
                  <option value="">请选择</option>
                  <option value="大专">大专</option>
                  <option value="本科">本科</option>
                  <option value="硕士">硕士</option>
                  <option value="博士">博士</option>
                </select>
              </div>
              <div class="form-group">
                <label>毕业院校</label>
                <input type="text" v-model="newResume.school">
              </div>
            </div>
          </div>
          
          <div class="form-section">
            <h3>工作经历</h3>
            <div class="experience-list">
              <div class="experience-item" v-for="(exp, index) in newResume.experiences" :key="index">
                <div class="experience-header">
                  <h4>工作经历 #{{ index + 1 }}</h4>
                  <button class="remove-btn" @click="removeExperience(index)">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>公司名称</label>
                    <input type="text" v-model="exp.company">
                  </div>
                  <div class="form-group">
                    <label>职位</label>
                    <input type="text" v-model="exp.position">
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>工作时间</label>
                    <div class="duration-input">
                      <input type="month" v-model="exp.startDate" placeholder="开始时间">
                      <span>至</span>
                      <input type="month" v-model="exp.endDate" placeholder="结束时间">
                      <label class="checkbox-container">
                        <input type="checkbox" v-model="exp.isCurrent"> 至今
                      </label>
                    </div>
                  </div>
                </div>
                <div class="form-group full-width">
                  <label>工作内容</label>
                  <textarea v-model="exp.description" placeholder="描述你的工作职责和成就..."></textarea>
                </div>
              </div>
              <button class="add-experience" @click="addExperience">
                <i class="fas fa-plus"></i> 添加工作经历
              </button>
            </div>
          </div>
          
          <div class="form-section">
            <h3>上传附件</h3>
            <FileUploader @files-uploaded="handleFilesUploaded" />
          </div>
        </div>
      </template>
      <template #footer>
        <button class="btn secondary" @click="showCreateModal = false">取消</button>
        <button class="btn primary" @click="createResume">创建简历</button>
      </template>
    </Modal>
    
    <!-- AI优化模态框 -->
    <Modal v-if="showOptimizeModal" @close="showOptimizeModal = false" title="AI简历优化" size="large">
      <template #body>
        <div class="optimize-container">
          <div class="optimize-sidebar">
            <h4>优化建议</h4>
            <div class="suggestion-list">
              <div class="suggestion-item" v-for="(suggestion, index) in aiSuggestions" :key="index"
                   :class="{ active: activeSuggestion === index }"
                   @click="activeSuggestion = index">
                <div class="suggestion-icon">
                  <i :class="suggestion.icon"></i>
                </div>
                <div class="suggestion-content">
                  <h5>{{ suggestion.title }}</h5>
                  <p>{{ suggestion.summary }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="optimize-main">
            <div class="optimize-header">
              <h4>{{ activeSuggestionData.title }}</h4>
              <div class="severity" :class="activeSuggestionData.severity">
                {{ activeSuggestionData.severity === 'high' ? '高优先级' : 
                   activeSuggestionData.severity === 'medium' ? '中优先级' : '低优先级' }}
              </div>
            </div>
            <div class="optimize-content">
              <div class="before-section">
                <h5>当前内容</h5>
                <div class="content-box">
                  <p>{{ activeSuggestionData.currentContent }}</p>
                </div>
              </div>
              <div class="after-section">
                <h5>优化建议</h5>
                <div class="content-box">
                  <p>{{ activeSuggestionData.suggestedContent }}</p>
                </div>
              </div>
            </div>
            <div class="optimize-actions">
              <button class="btn secondary">
                <i class="fas fa-times"></i> 忽略
              </button>
              <button class="btn primary">
                <i class="fas fa-check"></i> 应用修改
              </button>
            </div>
          </div>
        </div>
      </template>
    </Modal>
    
    <!-- 分享模态框 -->
    <Modal v-if="showShareModal" @close="showShareModal = null" title="分享简历">
      <template #body>
        <div class="share-container">
          <div class="share-methods">
            <div class="method-item" @click="copyShareLink">
              <div class="method-icon link">
                <i class="fas fa-link"></i>
              </div>
              <span>复制链接</span>
            </div>
            <div class="method-item" @click="shareViaEmail">
              <div class="method-icon email">
                <i class="fas fa-envelope"></i>
              </div>
              <span>邮件发送</span>
            </div>
            <div class="method-item" @click="generateQRCode">
              <div class="method-icon qrcode">
                <i class="fas fa-qrcode"></i>
              </div>
              <span>生成二维码</span>
            </div>
          </div>
          <div class="share-settings">
            <h4>分享设置</h4>
            <div class="setting-item">
              <label class="checkbox-container">
                <input type="checkbox" v-model="shareSettings.passwordProtected"> 密码保护
                <span class="checkmark"></span>
              </label>
            </div>
            <div class="setting-item" v-if="shareSettings.passwordProtected">
              <label>设置密码</label>
              <input type="password" v-model="shareSettings.password" placeholder="输入访问密码">
            </div>
            <div class="setting-item">
              <label class="checkbox-container">
                <input type="checkbox" v-model="shareSettings.expiryEnabled"> 设置有效期
                <span class="checkmark"></span>
              </label>
            </div>
            <div class="setting-item" v-if="shareSettings.expiryEnabled">
              <label>有效期至</label>
              <input type="date" v-model="shareSettings.expiryDate">
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <button class="btn secondary" @click="showShareModal = null">取消</button>
        <button class="btn primary" @click="confirmShare">确认分享</button>
      </template>
    </Modal>
    
    <!-- 确认删除对话框 -->
    <Dialog v-if="resumeToDelete" @close="resumeToDelete = null" 
            title="确认删除" type="danger">
      <template #body>
        <p>确定要删除简历 <strong>{{ getResumeName(resumeToDelete) }}</strong> 吗？此操作无法撤销。</p>
      </template>
      <template #footer>
        <button class="btn secondary" @click="resumeToDelete = null">取消</button>
        <button class="btn danger" @click="deleteResume">确认删除</button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'


// 背景音乐控制
const bgMusic = ref(null)
const isMusicPlaying = ref(false)

const toggleMusic = () => {
  if (isMusicPlaying.value) {
    bgMusic.value.pause()
  } else {
    bgMusic.value.play()
  }
  isMusicPlaying.value = !isMusicPlaying.value
}

// 简历数据
const resumes = ref([
  {
    id: 1,
    title: '高级前端开发工程师简历',
    name: '张伟',
    position: '高级前端开发工程师',
    education: '本科',
    school: '清华大学',
    experience: 5,
    salary: '25-35K',
    updatedAt: '2023-11-15T14:30:00',
    isDefault: true,
    previewText: [
      '5年前端开发经验，精通Vue.js和React',
      '主导过多个大型项目架构设计',
      '熟悉TypeScript和前端工程化',
      '良好的团队协作和沟通能力'
    ],
    experiences: [
      {
        company: '字节跳动',
        position: '高级前端工程师',
        startDate: '2020-06',
        endDate: '2023-10',
        isCurrent: false,
        description: '负责抖音电商平台前端架构设计和核心功能开发，带领3人前端团队完成多个重点项目。'
      },
      {
        company: '腾讯',
        position: '前端开发工程师',
        startDate: '2018-03',
        endDate: '2020-05',
        isCurrent: false,
        description: '参与微信小程序生态相关工具开发，优化开发体验和性能。'
      }
    ],
    attachments: [
      { name: '张伟_前端开发_简历.pdf', size: '2.4MB' },
      { name: '张伟_作品集.pdf', size: '5.1MB' },
      { name: '证书_前端高级工程师.pdf', size: '1.2MB' }
    ]
  },
  {
    id: 2,
    title: '全栈工程师简历',
    name: '张伟',
    position: '全栈工程师',
    education: '硕士',
    school: '北京大学',
    experience: 3,
    salary: '20-30K',
    updatedAt: '2023-10-28T09:15:00',
    isDefault: false,
    previewText: [
      '3年全栈开发经验，熟悉Node.js和Python',
      '精通React和Vue前端框架',
      '有微服务架构设计经验',
      '熟悉Docker和Kubernetes'
    ],
    experiences: [
      {
        company: '阿里巴巴',
        position: '全栈工程师',
        startDate: '2020-07',
        endDate: '2023-10',
        isCurrent: true,
        description: '负责电商平台前后端功能开发，参与系统架构优化和性能调优。'
      }
    ],
    attachments: [
      { name: '张伟_全栈工程师_简历.pdf', size: '2.1MB' },
      { name: '项目案例.pdf', size: '3.8MB' }
    ]
  }
])

// 计算属性
const totalAttachments = computed(() => {
  return resumes.value.reduce((total, resume) => total + resume.attachments.length, 0)
})

const filteredResumes = computed(() => {
  if (!searchQuery.value) return resumes.value
  const query = searchQuery.value.toLowerCase()
  return resumes.value.filter(resume => 
    resume.title.toLowerCase().includes(query) ||
    resume.name.toLowerCase().includes(query) ||
    resume.position.toLowerCase().includes(query) ||
    resume.education.toLowerCase().includes(query)

  )  })

// 搜索功能
const searchQuery = ref('')

// 模态框状态
const showCreateModal = ref(false)
const showOptimizeModal = ref(false)
const resumeToDelete = ref(null)

// 新简历数据
const newResume = ref({
  title: '',
  name: '',
  position: '',
  education: '',
  school: '',
  experience: '',
  salary: '',
  isDefault: false,
  experiences: [],
  attachments: []
})

// AI优化建议数据
const aiSuggestions = ref([
  {
    title: '技能关键词优化',
    summary: '增加行业相关关键词以提高ATS通过率',
    icon: 'fas fa-key',
    severity: 'high',
    currentContent: '熟悉前端开发技术',
    suggestedContent: '精通Vue.js和React框架，熟悉TypeScript，掌握前端工程化工具如Webpack和Vite'
  },
  {
    title: '工作经历量化',
    summary: '建议添加量化成果以增强说服力',
    icon: 'fas fa-chart-line',
    severity: 'medium',
    currentContent: '负责电商平台前端开发',
    suggestedContent: '主导电商平台前端重构，页面加载性能提升40%，用户转化率提高15%'
  },
  {
    title: '教育背景补充',
    summary: '可添加相关课程或荣誉',
    icon: 'fas fa-graduation-cap',
    severity: 'low',
    currentContent: '清华大学计算机科学与技术专业',
    suggestedContent: '清华大学计算机科学与技术专业，主修Web开发相关课程，获得校级优秀毕业生荣誉'
  }
])

const activeSuggestion = ref(0)
const activeSuggestionData = computed(() => aiSuggestions.value[activeSuggestion.value])

// 分享设置
const shareSettings = ref({
  passwordProtected: false,
  password: '',
  expiryEnabled: false,
  expiryDate: ''
})

// 方法
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const getFileIcon = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  switch(ext) {
    case 'pdf': return 'fas fa-file-pdf'
    case 'doc':
    case 'docx': return 'fas fa-file-word'
    case 'xls':
    case 'xlsx': return 'fas fa-file-excel'
    case 'ppt':
    case 'pptx': return 'fas fa-file-powerpoint'
    case 'jpg':
    case 'jpeg':
    case 'png':
    case 'gif': return 'fas fa-file-image'
    case 'zip':
    case 'rar': return 'fas fa-file-archive'
    default: return 'fas fa-file'
  }
}

const toggleDefault = (id) => {
  resumes.value.forEach(resume => {
    resume.isDefault = resume.id === id ? !resume.isDefault : false
  })
}

const editResume = (id) => {
  const resume = resumes.value.find(r => r.id === id)
  newResume.value = JSON.parse(JSON.stringify(resume))
  showCreateModal.value = true
}

const confirmDelete = (id) => {
  resumeToDelete.value = id
}

const deleteResume = () => {
  resumes.value = resumes.value.filter(r => r.id !== resumeToDelete.value)
  resumeToDelete.value = null
}

const getResumeName = (id) => {
  const resume = resumes.value.find(r => r.id === id)
  return resume ? resume.title : ''
}

const previewResume = (resume) => {
  console.log('预览简历:', resume.title)
  // 实际应用中这里会打开预览窗口或跳转到预览页面
}

const exportResume = (id) => {
  console.log('导出简历:', id)
  // 实际应用中这里会触发导出功能
}

const downloadFile = (file) => {
  console.log('下载文件:', file.name)
  // 实际应用中这里会触发下载
}

const previewFile = (file) => {
  console.log('预览文件:', file.name)
  // 实际应用中这里会打开文件预览
}

const addAttachment = (resumeId) => {
  console.log('为简历添加附件:', resumeId)
  // 实际应用中这里会打开文件选择器
}

const showShareModal = (resume) => {
  showShareModal.value = resume
}

const copyShareLink = () => {
  console.log('复制分享链接')
  // 实际应用中这里会生成并复制分享链接
}

const shareViaEmail = () => {
  console.log('通过邮件分享')
  // 实际应用中这里会打开邮件分享界面
}

const generateQRCode = () => {
  console.log('生成二维码')
  // 实际应用中这里会生成二维码
}

const confirmShare = () => {
  console.log('确认分享', showShareModal.value, shareSettings.value)
  showShareModal.value = null
}

const addExperience = () => {
  newResume.value.experiences.push({
    company: '',
    position: '',
    startDate: '',
    endDate: '',
    isCurrent: false,
    description: ''
  })
}

const removeExperience = (index) => {
  newResume.value.experiences.splice(index, 1)
}

const handleFilesUploaded = (files) => {
  newResume.value.attachments = [
    ...newResume.value.attachments,
    ...files.map(file => ({
      name: file.name,
      size: (file.size / (1024 * 1024)).toFixed(1) + 'MB'
    }))
  ]
}

const createResume = () => {
  const newId = Math.max(...resumes.value.map(r => r.id), 0) + 1
  const now = new Date().toISOString()
  
  const resume = {
    ...newResume.value,
    id: newId,
    updatedAt: now,
    previewText: generatePreviewText(newResume.value)
  }
  
  resumes.value.push(resume)
  showCreateModal.value = false
  resetNewResume()
}

const generatePreviewText = (resume) => {
  const text = []
  if (resume.position) text.push(`应聘职位: ${resume.position}`)
  if (resume.experience) text.push(`${resume.experience}年相关工作经验`)
  if (resume.education) text.push(`学历: ${resume.education}`)
  if (resume.school) text.push(`毕业院校: ${resume.school}`)
  if (resume.experiences.length > 0) {
    text.push(`最近工作: ${resume.experiences[0].company}`)
  }
  return text
}

const resetNewResume = () => {
  newResume.value = {
    title: '',
    name: '',
    position: '',
    education: '',
    school: '',
    experience: '',
    salary: '',
    isDefault: false,
    experiences: [],
    attachments: []
  }
}

// 初始化
onMounted(() => {
  // 可以在这里加载用户数据
})
</script>

<style scoped>
.resume-dashboard {
  position: relative;
  min-height: 100vh;
  background-color: #0f1621;
  color: #e0e6ed;
  padding: 20px;
  overflow-x: hidden;
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 背景装饰元素 */
.bg-circle {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  z-index: 0;
}

.circle-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(45deg, #42b983, #3498db);
  top: -100px;
  left: -100px;
}

.circle-2 {
  width: 600px;
  height: 600px;
  background: linear-gradient(45deg, #3498db, #9b59b6);
  bottom: -150px;
  right: -150px;
}

.circle-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(45deg, #e74c3c, #f39c12);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* 网格背景 */
.resume-dashboard::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: 0;
}

/* 主要内容区域 */
.dashboard-header {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  z-index: 1;
}

.dashboard-header h1 {
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(90deg, #42b983, #3498db);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.notification-btn {
  position: relative;
  background: none;
  border: none;
  color: #e0e6ed;
  font-size: 1.2rem;
  cursor: pointer;
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #e74c3c;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.user-profile img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #42b983;
}

.dashboard-content {
  position: relative;
  z-index: 1;
}

/* 统计卡片 */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-card:nth-child(1) .stat-icon {
  background: rgba(66, 185, 131, 0.2);
  color: #42b983;
}

.stat-card:nth-child(2) .stat-icon {
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
}

.stat-card:nth-child(3) .stat-icon {
  background: rgba(155, 89, 182, 0.2);
  color: #9b59b6;
}

.stat-info h3 {
  margin: 0 0 5px 0;
  font-size: 0.9rem;
  font-weight: 500;
  color: #94a3b8;
}

.stat-info p {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

/* 操作栏 */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(30, 41, 59, 0.7);
  border-radius: 8px;
  padding: 8px 15px;
  width: 300px;
  max-width: 100%;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.search-bar:focus-within {
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.search-bar i {
  color: #94a3b8;
  margin-right: 10px;
}

.search-bar input {
  flex: 1;
  background: transparent;
  border: none;
  color: #e0e6ed;
  outline: none;
  font-size: 0.9rem;
}

.clear-search {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 5px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.create-btn, .optimize-btn, .import-btn {
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.create-btn {
  background-color: #42b983;
  color: white;
}

.optimize-btn {
  background-color: #3498db;
  color: white;
}

.import-btn {
  background-color: #9b59b6;
  color: white;
}

.create-btn:hover, .optimize-btn:hover, .import-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* 简历网格 */
.resume-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.resume-card {
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.resume-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  border-color: rgba(66, 185, 131, 0.3);
}

.default-resume {
  border: 1px solid #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.card-header {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e0e6ed;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.quick-action {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  background: rgba(255, 255, 255, 0.05);
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.quick-action:hover {
  background: rgba(66, 185, 131, 0.2);
  color: #42b983;
}

.quick-action.danger:hover {
  background: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.card-body {
  padding: 20px;
}

.resume-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.meta-item i {
  color: #42b983;
  width: 16px;
  text-align: center;
}

.resume-preview {
  background: rgba(15, 22, 33, 0.5);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  min-height: 120px;
}

.resume-preview:hover {
  background: rgba(15, 22, 33, 0.7);
}

.preview-content {
  position: relative;
  z-index: 1;
}

.preview-text {
  font-size: 0.85rem;
  line-height: 1.6;
  color: #cbd5e1;
}

.preview-text p {
  margin: 0 0 8px 0;
}

.preview-watermark {
  position: absolute;
  right: 15px;
  bottom: 15px;
  font-size: 3rem;
  opacity: 0.05;
  color: #42b983;
}

.attachments-section {
  background: rgba(15, 22, 33, 0.5);
  border-radius: 8px;
  padding: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-header h4 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 500;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header i {
  color: #42b983;
}

.add-attachment {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: none;
  background: rgba(66, 185, 131, 0.1);
  color: #42b983;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.add-attachment:hover {
  background: rgba(66, 185, 131, 0.2);
}

.attachments-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 6px;
  background: rgba(30, 41, 59, 0.5);
  transition: all 0.2s ease;
}

.attachment-item:hover {
  background: rgba(30, 41, 59, 0.8);
}

.attachment-icon {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  background: rgba(52, 152, 219, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3498db;
}

.attachment-info {
  flex: 1;
  min-width: 0;
}

.attachment-name {
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.attachment-size {
  font-size: 0.75rem;
  color: #94a3b8;
}

.attachment-actions {
  display: flex;
  gap: 5px;
}

.download-btn, .preview-btn {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  border: none;
  background: rgba(255, 255, 255, 0.05);
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.download-btn:hover {
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
}

.preview-btn:hover {
  background: rgba(66, 185, 131, 0.2);
  color: #42b983;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.03);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.view-btn, .export-btn {
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.view-btn {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
}

.view-btn:hover {
  background: rgba(52, 152, 219, 0.2);
}

.export-btn {
  background: rgba(66, 185, 131, 0.1);
  color: #42b983;
}

.export-btn:hover {
  background: rgba(66, 185, 131, 0.2);
}

/* 创建简历表单 */
.create-resume-form {
  padding: 20px;
}

.form-section {
  margin-bottom: 25px;
}

.form-section h3 {
  margin: 0 0 15px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #e0e6ed;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.85rem;
  color: #94a3b8;
}

.form-group input, 
.form-group select, 
.form-group textarea {
  width: 100%;
  padding: 10px;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #e0e6ed;
  font-size: 0.9rem;
  outline: none;
  transition: all 0.3s ease;
}

.form-group input:focus, 
.form-group select:focus, 
.form-group textarea:focus {
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.form-group.full-width {
  width: 100%;
}

.required {
  color: #e74c3c;
}

.duration-input {
  display: flex;
  align-items: center;
  gap: 10px;
}

.duration-input span {
  color: #94a3b8;
  font-size: 0.9rem;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  color: #94a3b8;
}

.checkbox-container input {
  width: auto;
}

.experience-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.experience-item {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  padding: 15px;
}

.experience-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.experience-header h4 {
  margin: 0;
  font-size: 0.9rem;
  color: #e0e6ed;
}

.remove-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 5px;
}

.remove-btn:hover {
  color: #e74c3c;
}

.add-experience {
  padding: 10px 15px;
  border: 1px dashed rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  background: none;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.add-experience:hover {
  border-color: #42b983;
  color: #42b983;
  background: rgba(66, 185, 131, 0.1);
}

/* AI优化界面 */
.optimize-container {
  display: flex;
  height: 500px;
}

.optimize-sidebar {
  width: 280px;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 15px;
  overflow-y: auto;
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.suggestion-item {
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(30, 41, 59, 0.3);
}

.suggestion-item:hover {
  background: rgba(30, 41, 59, 0.5);
}

.suggestion-item.active {
  background: rgba(66, 185, 131, 0.2);
  border-left: 3px solid #42b983;
}

.suggestion-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(52, 152, 219, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3498db;
  margin-bottom: 10px;
}

.suggestion-content h5 {
  margin: 0 0 5px 0;
  font-size: 0.9rem;
  color: #e0e6ed;
}

.suggestion-content p {
  margin: 0;
  font-size: 0.8rem;
  color: #94a3b8;
}

.optimize-main {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.optimize-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.optimize-header h4 {
  margin: 0;
  font-size: 1.1rem;
  color: #e0e6ed;
}

.severity {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.severity.high {
  background: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.severity.medium {
  background: rgba(241, 196, 15, 0.2);
  color: #f1c40f;
}

.severity.low {
  background: rgba(66, 185, 131, 0.2);
  color: #42b983;
}

.optimize-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.before-section, .after-section {
  display: flex;
  flex-direction: column;
}

.before-section h5, .after-section h5 {
  margin: 0 0 10px 0;
  font-size: 0.9rem;
  color: #94a3b8;
}

.content-box {
  flex: 1;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  padding: 15px;
  font-size: 0.9rem;
  line-height: 1.6;
}

.after-section .content-box {
  border: 1px solid rgba(66, 185, 131, 0.3);
}

.optimize-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* 分享界面 */
.share-container {
  padding: 20px;
}

.share-methods {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}

.method-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px;
  border-radius: 8px;
  background: rgba(30, 41, 59, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.method-item:hover {
  background: rgba(30, 41, 59, 0.8);
  transform: translateY(-3px);
}

.method-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.method-icon.link {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
}

.method-icon.email {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.method-icon.qrcode {
  background: rgba(66, 185, 131, 0.1);
  color: #42b983;
}

.share-settings {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  padding: 20px;
}

.share-settings h4 {
  margin: 0 0 15px 0;
  font-size: 0.9rem;
  color: #94a3b8;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.setting-item {
  margin-bottom: 15px;
}

.setting-item label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.85rem;
  color: #94a3b8;
}

.setting-item input[type="password"],
.setting-item input[type="date"] {
  width: 100%;
  padding: 10px;
  background: rgba(15, 22, 33, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #e0e6ed;
  font-size: 0.9rem;
  outline: none;
}

/* 按钮样式 */
.btn {
  padding: 10px 15px;
  border-radius: 6px;
  border: none;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn.secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #e0e6ed;
}

.btn.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.btn.primary {
  background: #42b983;
  color: white;
}

.btn.primary:hover {
  background: #3aa876;
}

.btn.danger {
  background: #e74c3c;
  color: white;
}

.btn.danger:hover {
  background: #d62c1a;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .resume-grid {
    grid-template-columns: 1fr;
  }
  
  .optimize-container {
    flex-direction: column;
    height: auto;
  }
  
  .optimize-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .optimize-content {
    grid-template-columns: 1fr;
  }
  
  .share-methods {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    flex-direction: column;
    gap: 15px;
  }
}
</style>