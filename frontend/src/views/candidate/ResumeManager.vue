 <template>
  <div class="resume-manager">
    <div class="header">
      <h1>简历管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="createNewResume">
          <el-icon><Plus /></el-icon>创建新简历
        </el-button>
        <el-dropdown @command="handleImport">
          <el-button type="success">
            <el-icon><Upload /></el-icon>导入简历
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="linkedin">
                <el-icon><Connection /></el-icon>从LinkedIn导入
              </el-dropdown-item>
              <el-dropdown-item command="file">
                <el-icon><Upload /></el-icon>从文件导入
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 简历列表 -->
    <div v-loading="loading" class="resume-list">
      <el-empty v-if="resumes.length === 0" description="暂无简历">
        <el-button type="primary" @click="createNewResume">创建简历</el-button>
      </el-empty>
      
      <div v-else class="resume-grid">
        <div v-for="resume in resumes" :key="resume.id" class="resume-card">
          <div class="resume-card-header">
            <h3>{{ resume.name }}</h3>
            <el-tag :type="getScoreType(resume.completionScore)" size="small">
              完整度: {{ resume.completionScore }}%
            </el-tag>
          </div>
          
          <div class="resume-card-body">
            <p class="update-time">
              <el-icon><Timer /></el-icon>
              最后更新: {{ resume.lastUpdated }}
            </p>
            <p class="applied-jobs" v-if="resume.appliedJobs && resume.appliedJobs > 0">
              <el-icon><Briefcase /></el-icon>
              已投递: {{ resume.appliedJobs }} 个职位
            </p>
            <div class="tags" v-if="resume.tags && resume.tags.length > 0">
              <el-tag 
                v-for="tag in resume.tags.slice(0, 3)" 
                :key="tag" 
                size="small"
                effect="plain"
              >
                {{ tag }}
              </el-tag>
              <el-tag 
                v-if="resume.tags.length > 3" 
                size="small" 
                type="info"
                effect="plain"
              >
                +{{ resume.tags.length - 3 }}
              </el-tag>
            </div>
          </div>
          
          <div class="resume-card-footer">
            <el-button-group>
              <el-button type="primary" link @click="editResume(resume)">
                <el-icon><Edit /></el-icon>编辑
              </el-button>
              <el-button type="primary" link @click="previewResume(resume)">
                <el-icon><View /></el-icon>预览
              </el-button>
              <el-button type="primary" link @click="downloadResume(resume)">
                <el-icon><Download /></el-icon>下载
              </el-button>
            </el-button-group>
            
            <el-dropdown trigger="click">
              <el-button type="primary" link>
                <el-icon><More /></el-icon>更多
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="duplicateResume(resume)">
                    <el-icon><CopyDocument /></el-icon>创建副本
                  </el-dropdown-item>
                  <el-dropdown-item @click="shareResume(resume)">
                    <el-icon><Share /></el-icon>分享
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="deleteResume(resume)">
                    <el-icon><Delete /></el-icon>删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑器对话框 -->
    <el-dialog
      :title="editingResume ? '编辑简历' : '创建新简历'"
      v-model="showResumeEditor"
      width="80%"
      :before-close="handleEditorClose"
    >
      <el-form :model="resumeForm" label-width="100px">
        <el-form-item label="简历名称" required>
          <el-input v-model="resumeForm.name" placeholder="给简历起个名字"></el-input>
        </el-form-item>
        
        <el-collapse v-model="activeNames">
          <!-- 基本信息 -->
          <el-collapse-item title="基本信息" name="basic">
            <el-form-item label="姓名" required>
              <el-input v-model="resumeForm.basicInfo.name"></el-input>
            </el-form-item>
            <el-form-item label="电话" required>
              <el-input v-model="resumeForm.basicInfo.phone"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" required>
              <el-input v-model="resumeForm.basicInfo.email"></el-input>
            </el-form-item>
            <el-form-item label="个人简介">
              <el-input
                type="textarea"
                v-model="resumeForm.basicInfo.introduction"
                :rows="4"
                placeholder="请简要介绍自己..."
              ></el-input>
            </el-form-item>
          </el-collapse-item>

          <!-- 教育经历 -->
          <el-collapse-item title="教育经历" name="education">
            <div v-for="(edu, index) in resumeForm.education" :key="index" class="section-item">
              <div class="section-item-header">
                <h4>教育经历 {{ index + 1 }}</h4>
                <el-button type="danger" link @click="removeEducation(index)">
                  <el-icon><Delete /></el-icon>删除
                </el-button>
              </div>
              
              <el-form-item label="学校名称" required>
                <el-input v-model="edu.school"></el-input>
              </el-form-item>
              <el-form-item label="专业" required>
                <el-input v-model="edu.major"></el-input>
              </el-form-item>
              <el-form-item label="学历" required>
                <el-select v-model="edu.degree" style="width: 100%">
                  <el-option label="专科" value="专科"></el-option>
                  <el-option label="本科" value="本科"></el-option>
                  <el-option label="硕士" value="硕士"></el-option>
                  <el-option label="博士" value="博士"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="在校经历">
                <el-input
                  type="textarea"
                  v-model="edu.experience"
                  :rows="4"
                  placeholder="请描述在校期间的主要经历..."
                ></el-input>
              </el-form-item>
            </div>
            
            <div class="section-add">
              <el-button type="primary" plain @click="addEducation">
                <el-icon><Plus /></el-icon>添加教育经历
              </el-button>
            </div>
          </el-collapse-item>

          <!-- 工作经历 -->
          <el-collapse-item title="工作经历" name="work">
            <div v-for="(work, index) in resumeForm.workExperience" :key="index" class="section-item">
              <div class="section-item-header">
                <h4>工作经历 {{ index + 1 }}</h4>
                <el-button type="danger" link @click="removeWork(index)">
                  <el-icon><Delete /></el-icon>删除
                </el-button>
              </div>
              
              <el-form-item label="公司名称" required>
                <el-input v-model="work.company"></el-input>
              </el-form-item>
              <el-form-item label="职位" required>
                <el-input v-model="work.position"></el-input>
              </el-form-item>
              <el-form-item label="工作时间" required>
                <el-date-picker
                  v-model="work.period"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  style="width: 100%"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="工作描述">
                <el-input
                  type="textarea"
                  v-model="work.description"
                  :rows="4"
                  placeholder="请描述工作职责和成果..."
                ></el-input>
              </el-form-item>
            </div>
            
            <div class="section-add">
              <el-button type="primary" plain @click="addWork">
                <el-icon><Plus /></el-icon>添加工作经历
              </el-button>
            </div>
          </el-collapse-item>

          <!-- 项目经历 -->
          <el-collapse-item title="项目经历" name="projects">
            <div v-for="(project, index) in resumeForm.projects" :key="index" class="section-item">
              <div class="section-item-header">
                <h4>项目经历 {{ index + 1 }}</h4>
                <el-button type="danger" link @click="removeProject(index)">
                  <el-icon><Delete /></el-icon>删除
                </el-button>
              </div>
              
              <el-form-item label="项目名称" required>
                <el-input v-model="project.name"></el-input>
              </el-form-item>
              <el-form-item label="项目角色" required>
                <el-input v-model="project.role"></el-input>
              </el-form-item>
              <el-form-item label="项目描述">
                <el-input
                  type="textarea"
                  v-model="project.description"
                  :rows="4"
                  placeholder="请描述项目内容和您的贡献..."
                ></el-input>
              </el-form-item>
            </div>
            
            <div class="section-add">
              <el-button type="primary" plain @click="addProject">
                <el-icon><Plus /></el-icon>添加项目经历
              </el-button>
            </div>
          </el-collapse-item>

          <!-- 技能特长 -->
          <el-collapse-item title="技能特长" name="skills">
            <el-form-item>
              <div class="skills-container">
                <el-tag
                  v-for="tag in resumeForm.skills"
                  :key="tag"
                  class="skill-tag"
                  closable
                  :disable-transitions="false"
                  @close="handleClose(tag)"
                >
                  {{ tag }}
                </el-tag>
                
                <el-input
                  v-if="inputVisible"
                  ref="tagInputRef"
                  v-model="inputValue"
                  class="tag-input"
                  size="small"
                  @keyup.enter="handleInputConfirm"
                  @blur="handleInputConfirm"
                />
                
                <el-button 
                  v-else 
                  class="button-new-tag" 
                  size="small" 
                  @click="showInput"
                >
                  <el-icon><Plus /></el-icon>添加技能
                </el-button>
              </div>
            </el-form-item>
          </el-collapse-item>
        </el-collapse>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleEditorClose">取消</el-button>
          <el-button type="primary" @click="saveResume">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- LinkedIn导入对话框 -->
    <el-dialog
      title="从LinkedIn导入"
      v-model="showLinkedInImport"
      width="500px"
      align-center
    >
      <div class="linkedin-import">
        <el-empty description="通过LinkedIn导入您的职业信息">
          <template #image>
            <el-icon :size="60" color="#0A66C2">
              <Connection />
            </el-icon>
          </template>
          <template #description>
            <p class="import-tip">授权访问您的LinkedIn账号以导入简历信息</p>
          </template>
          <el-button 
            type="primary" 
            :loading="authorizing"
            @click="authorizeLinkedIn"
          >
            <el-icon><Link /></el-icon>
            授权访问LinkedIn
          </el-button>
        </el-empty>
      </div>
    </el-dialog>

    <!-- 文件导入对话框 -->
    <el-dialog
      title="从文件导入"
      v-model="showFileImport"
      width="500px"
      align-center
    >
      <div class="file-import">
        <el-upload
          ref="uploadRef"
          v-bind="uploadConfig"
          class="upload-demo"
          drag
          :auto-upload="true"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :before-upload="beforeUpload"
        >
          <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持上传 PDF、Word 格式的简历文件
            </div>
          </template>
        </el-upload>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadProps } from 'element-plus'
import axios from '@/config/axios'
import { auth } from '@/utils/auth'
import { useRouter } from 'vue-router'
import {
  Connection,
  Link,
  Plus,
  Upload,
  Timer,
  Briefcase,
  Edit,
  View,
  Download,
  More,
  CopyDocument,
  Share,
  Delete,
  UploadFilled
} from '@element-plus/icons-vue'

// 类型定义
interface BasicInfo {
  name: string
  phone: string
  email: string
  introduction: string
}

interface Education {
  school: string
  major: string
  degree: string
  experience: string
}

interface WorkExperience {
  company: string
  position: string
  period: [Date | null, Date | null]
  description: string
}

interface Project {
  name: string
  role: string
  description: string
}

interface Resume {
  id: number
  name: string
  content: any
  basicInfo: BasicInfo
  education: Education[]
  workExperience: WorkExperience[]
  projects: Project[]
  skills: string[]
  completionScore?: number
  lastUpdated?: string
  appliedJobs?: number
  tags?: string[]
  updated_at?: string
}

// 状态定义
const resumes = ref<Resume[]>([])
const loading = ref(false)
const editingResume = ref<Resume | null>(null)
const showResumeEditor = ref(false)
const showPreview = ref(false)
const activeNames = ref(['basic'])
const inputVisible = ref(false)
const inputValue = ref('')
const tagInputRef = ref<{ input: HTMLInputElement } | null>(null)

// 表单数据
const resumeForm = reactive<Resume>({
  id: 0,
  name: '',
  content: {},
  basicInfo: {
    name: '',
    phone: '',
    email: '',
    introduction: ''
  },
  education: [],
  workExperience: [],
  projects: [],
  skills: []
})

// 导入相关
const showLinkedInImport = ref(false)
const showFileImport = ref(false)
const authorizing = ref(false)
const uploadRef = ref(null)

// 错误处理
const handleError = (error: unknown) => {
  if (error instanceof Error) {
    ElMessage.error(error.message)
  } else {
    ElMessage.error('操作失败')
  }
  console.error(error)
}

// 获取简历列表
const fetchResumes = async () => {
  try {
    loading.value = true
    // 模拟数据
    const mockResumes = [
      {
        id: 1,
        name: '软件工程师简历',
        content: {},
        basicInfo: {
          name: '张三',
          phone: '13800138000',
          email: 'zhangsan@example.com',
          introduction: '3年工作经验，专注于前端开发，熟悉Vue、React等主流框架。'
        },
        education: [
          {
            school: '某某大学',
            major: '计算机科学与技术',
            degree: '本科',
            experience: '在校期间参与多个项目开发，担任科技协会会长。'
          }
        ],
        workExperience: [
          {
            company: '某某科技有限公司',
            position: '前端开发工程师',
            period: [new Date('2020-06'), new Date('2023-06')] as [Date, Date],
            description: '负责公司主要产品的前端开发，实现了多个关键功能模块。'
          }
        ],
        projects: [
          {
            name: '企业管理系统',
            role: '前端负责人',
            description: '使用Vue3 + TypeScript开发的现代化企业管理系统，实现了用户管理、权限控制等功能。'
          }
        ],
        skills: ['Vue', 'React', 'TypeScript', 'Node.js'],
        updated_at: '2024-01-15'
      },
      {
        id: 2,
        name: '实习简历',
        content: {},
        basicInfo: {
          name: '张三',
          phone: '13800138000',
          email: 'zhangsan@example.com',
          introduction: '应届毕业生，热爱编程，有强烈的学习意愿。'
        },
        education: [
          {
            school: '某某大学',
            major: '计算机科学与技术',
            degree: '本科',
            experience: '专业课程成绩优秀，多次获得奖学金。'
          }
        ],
        workExperience: [],
        projects: [
          {
            name: '毕业设计 - AI面试助手',
            role: '独立开发者',
            description: '基于人工智能的面试辅助系统，帮助求职者提高面试成功率。'
          }
        ],
        skills: ['JavaScript', 'Python', 'MySQL'],
        updated_at: '2024-01-10'
      }
    ] as Resume[]

    resumes.value = mockResumes.map(resume => ({
      ...resume,
      completionScore: calculateCompletionScore(resume),
      lastUpdated: resume.updated_at 
        ? new Date(resume.updated_at).toLocaleDateString('zh-CN')
        : '未更新',
      appliedJobs: 0,
      tags: resume.skills || []
    }))
  } catch (error) {
    handleError(error)
  } finally {
    loading.value = false
  }
}

// 计算简历完整度
const calculateCompletionScore = (resume: Resume): number => {
  let score = 0
  const totalFields = 5 // 基本信息、教育经历、工作经历、项目经历、技能特长
  
  if (resume.basicInfo?.name && resume.basicInfo?.phone && resume.basicInfo?.email) score++
  if (resume.education?.length > 0) score++
  if (resume.workExperience?.length > 0) score++
  if (resume.projects?.length > 0) score++
  if (resume.skills?.length > 0) score++
  
  return Math.round((score / totalFields) * 100)
}

// 评分类型计算
const getScoreType = (score: number | undefined): '' | 'success' | 'warning' | 'danger' => {
  if (!score) return ''
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}

// 创建新简历
const createNewResume = () => {
  editingResume.value = null
  resetForm()
  showResumeEditor.value = true
}

// 编辑简历
const editResume = (resume: Resume) => {
  editingResume.value = resume
  Object.assign(resumeForm, resume)
  showResumeEditor.value = true
}

// 预览简历
const previewResume = (resume: Resume) => {
  editingResume.value = resume
  showPreview.value = true
}

// 下载简历
const downloadResume = async (resume: Resume) => {
  try {
    const response = await axios.get(`/api/resume/${resume.id}/download`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${resume.name}.pdf`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    handleError(error)
  }
}

// 分享简历
const shareResume = async (resume: Resume) => {
  try {
    const response = await axios.post(`/api/resume/${resume.id}/share`)
    if (response.data.success) {
      ElMessage.success('分享链接已复制到剪贴板')
      await navigator.clipboard.writeText(response.data.shareLink)
    } else {
      throw new Error(response.data.message || '分享失败')
    }
  } catch (error) {
    handleError(error)
  }
}

// 删除简历
const deleteResume = async (resume: Resume) => {
  try {
    await ElMessageBox.confirm('确定要删除这份简历吗？', '提示', {
      type: 'warning'
    })
    
    await axios.delete(`/api/resume/${resume.id}`)
    ElMessage.success('删除成功')
    fetchResumes()
  } catch (error) {
    if (error !== 'cancel') {
      handleError(error)
    }
  }
}

// 复制简历
const duplicateResume = async (resume: Resume) => {
  try {
    const response = await axios.post('/api/resume/duplicate', {
      resumeId: resume.id
    })
    ElMessage.success('复制成功')
    fetchResumes()
  } catch (error) {
    handleError(error)
  }
}

// 保存简历
const saveResume = async () => {
  try {
    const method = editingResume.value ? 'put' : 'post'
    const url = editingResume.value 
      ? `/api/resume/${editingResume.value.id}`
      : '/api/resume'
    
    await axios[method](url, resumeForm)
    ElMessage.success('保存成功')
    showResumeEditor.value = false
    fetchResumes()
  } catch (error) {
    handleError(error)
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(resumeForm, {
    id: 0,
    name: '',
    content: {},
    basicInfo: {
      name: '',
      phone: '',
      email: '',
      introduction: ''
    },
    education: [],
    workExperience: [],
    projects: [],
    skills: []
  })
}

// 关闭编辑器
const handleEditorClose = () => {
  showResumeEditor.value = false
  resetForm()
}

// 添加教育经历
const addEducation = () => {
  resumeForm.education.push({
    school: '',
    major: '',
    degree: '',
    experience: ''
  })
}

// 删除教育经历
const removeEducation = (index: number) => {
  resumeForm.education.splice(index, 1)
}

// 添加工作经历
const addWork = () => {
  resumeForm.workExperience.push({
    company: '',
    position: '',
    period: [null, null],
    description: ''
  })
}

// 删除工作经历
const removeWork = (index: number) => {
  resumeForm.workExperience.splice(index, 1)
}

// 添加项目经历
const addProject = () => {
  resumeForm.projects.push({
    name: '',
    role: '',
    description: ''
  })
}

// 删除项目经历
const removeProject = (index: number) => {
  resumeForm.projects.splice(index, 1)
}

// 技能标签相关
const handleClose = (tag: string) => {
  resumeForm.skills.splice(resumeForm.skills.indexOf(tag), 1)
}

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    tagInputRef.value?.input?.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value && !resumeForm.skills.includes(inputValue.value)) {
    resumeForm.skills.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

// 导入相关
const handleImport = (command: 'linkedin' | 'file') => {
  if (command === 'linkedin') {
    showLinkedInImport.value = true
  } else if (command === 'file') {
    showFileImport.value = true
  }
}

const authorizeLinkedIn = async () => {
  try {
    authorizing.value = true
    const response = await axios.get('/api/resume/linkedin/auth')
    const { authUrl } = response.data
    
    // 打开新窗口进行授权
    const authWindow = window.open(
      authUrl,
      'LinkedIn授权',
      'width=600,height=600,left=200,top=100'
    )
    
    // 监听消息
    window.addEventListener('message', async (event) => {
      if (event.data.type === 'linkedin-auth-success') {
        const { code } = event.data
        try {
          const importResponse = await axios.post('/api/resume/linkedin/import', { code })
          
          if (importResponse.data.success) {
            Object.assign(resumeForm, importResponse.data.data)
            ElMessage.success('LinkedIn数据导入成功')
            showLinkedInImport.value = false
            showResumeEditor.value = true
          } else {
            throw new Error(importResponse.data.message || '导入失败')
          }
        } catch (error) {
          handleError(error)
        }
      }
    })
  } catch (error) {
    handleError(error)
  } finally {
    authorizing.value = false
  }
}

const uploadConfig = {
  action: '/api/resume/import',
  headers: {
    Authorization: `Bearer ${localStorage.getItem('token')}`
  },
  accept: '.pdf,.doc,.docx',
  limit: 1
}

const handleUploadSuccess: UploadProps['onSuccess'] = (response) => {
  if (response.success) {
    Object.assign(resumeForm, response.data)
    ElMessage.success('文件导入成功')
    showFileImport.value = false
    showResumeEditor.value = true
  } else {
    handleError(response.message || '导入失败')
  }
}

const handleUploadError: UploadProps['onError'] = () => {
  handleError('文件上传失败')
}

const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const isValidType = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ].includes(file.type)
  
  if (!isValidType) {
    handleError('请上传PDF或Word格式的文件')
    return false
  }
  return true
}

const router = useRouter()

// 初始化
onMounted(() => {
  if (!auth.isLoggedIn()) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  if (!auth.isCandidate()) {
    ElMessage.warning('无权访问此页面')
    router.push('/login')
    return
  }
  
  fetchResumes()
})

// 导出所有需要的变量和方法
defineExpose({
  resumes,
  loading,
  showResumeEditor,
  showPreview,
  editingResume,
  resumeForm,
  activeNames,
  inputVisible,
  inputValue,
  tagInputRef,
  showLinkedInImport,
  showFileImport,
  authorizing,
  uploadRef,
  uploadConfig,
  handleImport,
  handleClose,
  showInput,
  handleInputConfirm,
  createNewResume,
  editResume,
  deleteResume,
  duplicateResume,
  previewResume,
  downloadResume,
  shareResume,
  saveResume,
  handleEditorClose,
  addEducation,
  removeEducation,
  addWork,
  removeWork,
  addProject,
  removeProject,
  handleUploadSuccess,
  handleUploadError,
  beforeUpload,
  authorizeLinkedIn,
  getScoreType
})
</script>

<style scoped>
.resume-manager {
  padding: 24px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: calc(100vh - 120px);
  overflow-y: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e8e8e8;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.resume-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.resume-card {
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 20px;
  background: white;
  transition: all 0.3s;
}

.resume-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.resume-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.resume-card-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.resume-card-body {
  color: #666;
  font-size: 14px;
}

.resume-card-body p {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.resume-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.section-item {
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 16px;
}

.section-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-item-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.section-add {
  text-align: center;
  margin-top: 16px;
}

.skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.tag-input {
  width: 90px;
  margin-right: 8px;
  vertical-align: bottom;
}

.button-new-tag {
  margin-right: 8px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.linkedin-import {
  text-align: center;
  padding: 20px;
}

.import-tip {
  color: #666;
  font-size: 14px;
  margin-top: 10px;
}

.file-import {
  padding: 20px;
}

.el-upload {
  width: 100%;
}

.el-upload-dragger {
  width: 100%;
}

.el-upload__tip {
  margin-top: 10px;
  color: #666;
}

.el-icon {
  vertical-align: middle;
  margin-right: 4px;
}

.el-button .el-icon {
  font-size: 16px;
}

.el-dropdown-menu .el-icon {
  font-size: 14px;
}

.resume-card-body .el-icon {
  font-size: 14px;
  color: #666;
}

.el-icon--upload {
  font-size: 48px;
  color: #909399;
  margin: 20px 0 16px;
}

.linkedin-import .el-icon {
  font-size: 60px;
  color: #0A66C2;
  margin-bottom: 16px;
}

.section-item-header .el-icon {
  font-size: 16px;
  color: #f56c6c;
}

.section-add .el-icon {
  font-size: 14px;
  margin-right: 4px;
}
</style>