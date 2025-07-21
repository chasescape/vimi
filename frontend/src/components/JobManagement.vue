<template>
  <div class="job-management">
    <div class="tech-background">
      <div class="tech-circle circle-1"></div>
      <div class="tech-circle circle-2"></div>
      <div class="tech-circle circle-3"></div>
      <div class="tech-grid"></div>
    </div>
    
    <div class="content-container">
      <h2 class="tech-title">
        <span class="title-text">岗位管理</span>
        <span class="title-glare"></span>
      </h2>
      
      <div class="search-filter tech-card">
        <div class="search-box">
          <i class="fas fa-search tech-icon"></i>
          <input type="text" placeholder="搜索岗位名称、公司或地点" v-model="searchQuery" class="tech-input">
        </div>
        <div class="filters">
          <div class="tech-select-wrapper">
            <select v-model="selectedLocation" class="tech-select">
              <option value="">所有地点</option>
              <option v-for="location in locations" :value="location" :key="location">
                {{ location }}
              </option>
            </select>
            <i class="fas fa-chevron-down select-arrow"></i>
          </div>
          <div class="tech-select-wrapper">
            <select v-model="selectedSalary" class="tech-select">
              <option value="">所有薪资</option>
              <option v-for="salary in salaryRanges" :value="salary" :key="salary">
                {{ salary }}
              </option>
            </select>
            <i class="fas fa-chevron-down select-arrow"></i>
          </div>
          <button class="tech-btn filter-btn" @click="resetFilters">
            <i class="fas fa-sync-alt"></i> 重置
          </button>
        </div>
      </div>
      
      <div class="job-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
          class="tech-tab"
        >
          <span class="tab-icon">
            <i :class="tab.icon"></i>
          </span>
          {{ tab.label }}
          <span v-if="tab.id === 'applied' && appliedCount > 0" class="tab-badge">{{ appliedCount }}</span>
          <span v-if="tab.id === 'saved' && savedCount > 0" class="tab-badge">{{ savedCount }}</span>
        </button>
      </div>
      
      <div class="job-list">
        <div v-if="filteredJobs.length === 0" class="empty-state tech-card">
          <i class="fas fa-briefcase empty-icon"></i>
          <h3>没有找到匹配的岗位</h3>
          <p>尝试调整搜索条件或查看推荐岗位</p>
          <button class="tech-btn primary" @click="resetFilters">
            <i class="fas fa-sync-alt"></i> 重置筛选条件
          </button>
        </div>
        
        <div class="job-item tech-card" v-for="job in filteredJobs" :key="job.id">
          <div class="job-header">
            <div class="job-title-wrapper">
              <h3>{{ job.title }}</h3>
              <span class="job-match" v-if="job.match > 80">
                <i class="fas fa-bolt"></i> {{ job.match }}% 匹配
              </span>
            </div>
            <div class="job-company-info">
              <span class="company">
                <i class="fas fa-building"></i> {{ job.company }}
              </span>
              <span class="location">
                <i class="fas fa-map-marker-alt"></i> {{ job.location }}
              </span>
              <span class="date">
                <i class="fas fa-clock"></i> {{ formatDate(job.postDate) }}
              </span>
            </div>
          </div>
          <div class="job-details">
            <div class="job-meta">
              <span class="salary">
                <i class="fas fa-money-bill-wave"></i> {{ job.salary }}
              </span>
              <span class="type">
                <i class="fas fa-briefcase"></i> {{ job.type }}
              </span>
              <span class="experience">
                <i class="fas fa-user-tie"></i> {{ job.experience }}
              </span>
              <span class="education">
                <i class="fas fa-graduation-cap"></i> {{ job.education }}
              </span>
            </div>
            <div class="skills">
              <span class="skill-tag" v-for="skill in job.skills" :key="skill">
                {{ skill }}
              </span>
            </div>
            <p class="description">{{ truncateDescription(job.description) }}</p>
            <button class="view-more" @click="toggleDescription(job.id)" v-if="job.description.length > 100">
              {{ expandedDescriptions[job.id] ? '收起' : '查看更多' }}
            </button>
          </div>
          <div class="job-actions">
            <button 
              class="tech-btn apply-btn" 
              :class="{ applied: job.applied }"
              @click="applyJob(job.id)"
            >
              <i :class="job.applied ? 'fas fa-check' : 'fas fa-paper-plane'"></i>
              {{ job.applied ? '已申请' : '立即申请' }}
            </button>
            <button class="tech-btn icon-btn" @click="consultJob(job.id)">
              <i class="fas fa-comment-alt"></i>
              <span class="tooltip">在线咨询</span>
            </button>
            <button 
              class="tech-btn icon-btn" 
              @click="toggleSaveJob(job.id)"
              :class="{ saved: job.saved }"
            >
              <i :class="job.saved ? 'fas fa-bookmark' : 'far fa-bookmark'"></i>
              <span class="tooltip">{{ job.saved ? '取消收藏' : '收藏岗位' }}</span>
            </button>
            <button class="tech-btn icon-btn" @click="shareJob(job.id)">
              <i class="fas fa-share-alt"></i>
              <span class="tooltip">分享岗位</span>
            </button>
          </div>
        </div>
      </div>
      
      <div class="recommendation tech-card" v-if="recommendedJobs.length > 0">
        <div class="section-header">
          <h3>
            <i class="fas fa-star"></i> 基于您的简历推荐
          </h3>
          <button class="tech-btn link-btn" @click="refreshRecommendations">
            <i class="fas fa-sync-alt"></i> 换一批
          </button>
        </div>
        <div class="recommended-jobs">
          <div class="recommended-job" v-for="job in recommendedJobs" :key="job.id">
            <div class="recommended-job-header">
              <h4>{{ job.title }}</h4>
              <p class="company">
                <i class="fas fa-building"></i> {{ job.company }}
              </p>
            </div>
            <div class="match-score">
              <div class="score-info">
                <span class="score-text">匹配度</span>
                <span class="score-value">{{ job.match }}%</span>
              </div>
              <div class="score-bar">
                <div class="score-fill" :style="{ width: job.match + '%' }"></div>
              </div>
            </div>
            <div class="job-highlights">
              <span><i class="fas fa-money-bill-wave"></i> {{ job.salary }}</span>
              <span><i class="fas fa-map-marker-alt"></i> {{ job.location }}</span>
            </div>
            <button class="tech-btn primary view-btn" @click="viewJobDetails(job.id)">
              <i class="fas fa-eye"></i> 查看详情
            </button>
          </div>
        </div>
      </div>
      
      <div class="pagination" v-if="filteredJobs.length > 0">
        <button 
          class="tech-btn pagination-btn" 
          :disabled="currentPage === 1"
          @click="currentPage--"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        <button 
          v-for="page in totalPages" 
          :key="page"
          class="tech-btn pagination-btn"
          :class="{ active: currentPage === page }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
        <button 
          class="tech-btn pagination-btn" 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>
    
    <div class="tech-modal" v-if="showJobDetails">
      <div class="modal-content tech-card">
        <button class="close-modal" @click="showJobDetails = false">
          <i class="fas fa-times"></i>
        </button>
        <JobDetails :job="selectedJob" @close="showJobDetails = false" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
const searchQuery = ref('')
const selectedLocation = ref('')
const selectedSalary = ref('')
const activeTab = ref('all')
const currentPage = ref(1)
const itemsPerPage = ref(5)
const showJobDetails = ref(false)
const selectedJob = ref(null)
const expandedDescriptions = ref({})

const tabs = [
  { id: 'all', label: '全部岗位', icon: 'fas fa-list' },
  { id: 'applied', label: '已申请', icon: 'fas fa-paper-plane' },
  { id: 'saved', label: '已收藏', icon: 'fas fa-bookmark' }
]

const locations = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京', '苏州', '西安']
const salaryRanges = ['5k以下', '5k-10k', '10k-20k', '20k-50k', '50k以上']
const educationLevels = ['大专', '本科', '硕士', '博士', '不限']

const jobs = ref([
  {
    id: 1,
    title: '高级前端开发工程师 (Vue3/TypeScript)',
    company: 'ABC科技有限公司',
    location: '北京',
    salary: '25k-40k·15薪',
    type: '全职',
    experience: '3-5年',
    education: '本科及以上',
    description: '负责公司核心产品的前端架构设计与开发，使用Vue3+TypeScript技术栈，参与前端工程化建设和技术方案评审。要求熟悉前端性能优化、组件化开发，有大型项目开发经验者优先。我们提供有竞争力的薪资和广阔的发展空间。',
    skills: ['Vue3', 'TypeScript', '前端工程化', '性能优化', 'Webpack'],
    postDate: new Date('2023-05-15'),
    applied: false,
    saved: false,
    match: 92
  },
  {
    id: 2,
    title: 'UI/UX设计师 (移动端)',
    company: 'XYZ设计公司',
    location: '上海',
    salary: '18k-30k·13薪',
    type: '全职',
    experience: '3年以上',
    education: '本科及以上',
    description: '负责公司移动端产品的UI/UX设计工作，参与设计规范的制定和维护，输出高质量的设计方案。要求精通Figma/Sketch等设计工具，有完整的移动端项目设计经验，对用户体验有深刻理解。',
    skills: ['UI设计', 'UX设计', 'Figma', '移动端设计', '交互设计'],
    postDate: new Date('2023-06-20'),
    applied: true,
    saved: true,
    match: 85
  },
  {
    id: 3,
    title: '产品经理 (电商方向)',
    company: 'DEF互联网有限公司',
    location: '深圳',
    salary: '30k-50k·16薪',
    type: '全职',
    experience: '5年以上',
    education: '本科及以上',
    description: '负责电商平台的产品规划、需求分析和项目管理，协调设计、开发和测试团队，推动产品迭代和优化。要求有大型电商平台产品经验，熟悉电商业务流程，具备优秀的沟通协调能力和数据分析能力。',
    skills: ['产品规划', '需求分析', '项目管理', '电商业务', '数据分析'],
    postDate: new Date('2023-07-10'),
    applied: false,
    saved: false,
    match: 76
  },
  {
    id: 4,
    title: 'Java后端开发工程师',
    company: 'GHI金融科技',
    location: '杭州',
    salary: '20k-35k·14薪',
    type: '全职',
    experience: '3年以上',
    education: '本科及以上',
    description: '负责金融科技平台的后端服务开发，使用Java/Spring Cloud技术栈，参与系统架构设计和性能优化。要求熟悉分布式系统开发，有高并发系统开发经验者优先。',
    skills: ['Java', 'Spring Cloud', 'MySQL', '分布式系统', '高并发'],
    postDate: new Date('2023-07-05'),
    applied: false,
    saved: true,
    match: 68
  },
  {
    id: 5,
    title: '数据科学家 (机器学习方向)',
    company: 'JKL人工智能实验室',
    location: '北京',
    salary: '35k-60k·16薪',
    type: '全职',
    experience: '3年以上',
    education: '硕士及以上',
    description: '负责机器学习模型的研发和优化，参与从数据预处理到模型部署的全流程工作。要求精通Python和主流机器学习框架，有扎实的数学基础和算法能力，在CV/NLP领域有实际项目经验者优先。',
    skills: ['机器学习', 'Python', 'TensorFlow', 'PyTorch', '数据分析'],
    postDate: new Date('2023-07-12'),
    applied: false,
    saved: false,
    match: 89
  }
])

// 计算属性
const appliedCount = computed(() => {
  return jobs.value.filter(job => job.applied).length
})

const savedCount = computed(() => {
  return jobs.value.filter(job => job.saved).length
})

const recommendedJobs = computed(() => {
  return [...jobs.value]
    .sort((a, b) => b.match - a.match)
    .slice(0, 3)
})

const filteredJobs = computed(() => {
  let result = jobs.value.filter(job => {
    // 搜索过滤
    const matchesSearch = searchQuery.value === '' || 
                         job.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         job.company.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         job.location.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    // 地点过滤
    const matchesLocation = selectedLocation.value === '' || 
                           job.location === selectedLocation.value
    
    // 薪资过滤
    const matchesSalary = selectedSalary.value === '' || 
                         job.salary.includes(selectedSalary.value)
    
    // 标签过滤
    let matchesTab = true
    if (activeTab.value === 'applied') {
      matchesTab = job.applied
    } else if (activeTab.value === 'saved') {
      matchesTab = job.saved
    }
    
    return matchesSearch && matchesLocation && matchesSalary && matchesTab
  })
  
  // 按匹配度排序
  result.sort((a, b) => b.match - a.match)
  
  return result
})

const paginatedJobs = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredJobs.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredJobs.value.length / itemsPerPage.value)
})

// 方法
const formatDate = (date) => {
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  return `${Math.floor(days / 30)}个月前`
}

const truncateDescription = (description) => {
  const jobId = jobs.value.find(j => j.description === description)?.id
  if (jobId && expandedDescriptions.value[jobId]) {
    return description
  }
  return description.length > 100 ? description.substring(0, 100) + '...' : description
}

const toggleDescription = (jobId) => {
  expandedDescriptions.value[jobId] = !expandedDescriptions.value[jobId]
}

const applyJob = (id) => {
  const job = jobs.value.find(j => j.id === id)
  if (job) {
    job.applied = !job.applied
    if (job.applied) {
      // 可以添加申请成功的提示或动画
    }
  }
}

const toggleSaveJob = (id) => {
  const job = jobs.value.find(j => j.id === id)
  if (job) {
    job.saved = !job.saved
  }
}

const consultJob = (id) => {
  // 这里可以打开咨询对话框或跳转到咨询页面
  console.log('咨询岗位:', id)
}

const shareJob = (id) => {
  // 这里可以实现分享功能
  console.log('分享岗位:', id)
}

const viewJobDetails = (id) => {
  selectedJob.value = jobs.value.find(j => j.id === id)
  showJobDetails.value = true
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedLocation.value = ''
  selectedSalary.value = ''
  activeTab.value = 'all'
  currentPage.value = 1
}

const refreshRecommendations = () => {
  // 这里可以添加刷新推荐逻辑
  console.log('刷新推荐岗位')
}

// 生命周期钩子
onMounted(() => {
  // 可以添加初始化逻辑
})
</script>

<style scoped>
.job-management {
  position: relative;
  min-height: 100vh;
  padding: 30px;
  background-color: #0f1621;
  color: #e0e0e0;
  overflow-x: hidden;
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.tech-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
}

.tech-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.15;
}

.circle-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #42b983, #2c3e50);
  top: -100px;
  left: -100px;
}

.circle-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3498db, #9b59b6);
  bottom: -150px;
  right: -100px;
}

.circle-3 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #e74c3c, #f39c12);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.tech-grid {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 30px 30px;
}

.content-container {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
}

.tech-title {
  position: relative;
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #fff;
  text-shadow: 0 0 10px rgba(66, 185, 131, 0.5);
  display: inline-block;
}

.title-text {
  position: relative;
  z-index: 2;
}

.title-glare {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: skewX(-20deg);
  z-index: 1;
  animation: glare 3s infinite;
}

@keyframes glare {
  0% { left: -100%; }
  50% { left: 100%; }
  100% { left: 100%; }
}

.tech-card {
  background: rgba(25, 35, 50, 0.8);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.tech-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(66, 185, 131, 0.1), transparent);
  z-index: -1;
}

.tech-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  border-color: rgba(66, 185, 131, 0.3);
}

.search-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 300px;
  position: relative;
}

.tech-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #42b983;
  font-size: 1.1rem;
}

.tech-input {
  width: 100%;
  padding: 12px 20px 12px 45px;
  background: rgba(15, 22, 33, 0.7);
  border: 1px solid rgba(66, 185, 131, 0.3);
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s;
}

.tech-input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.tech-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.filters {
  display: flex;
  gap: 10px;
  align-items: center;
}

.tech-select-wrapper {
  position: relative;
}

.tech-select {
  padding: 12px 35px 12px 15px;
  background: rgba(15, 22, 33, 0.7);
  border: 1px solid rgba(66, 185, 131, 0.3);
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  appearance: none;
  cursor: pointer;
  min-width: 120px;
  transition: all 0.3s;
}

.tech-select:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #42b983;
  pointer-events: none;
}

.tech-btn {
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  position: relative;
  overflow: hidden;
}

.tech-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}

.tech-btn:hover::before {
  opacity: 1;
}

.primary {
  background: linear-gradient(135deg, #42b983, #3aa876);
  color: white;
}

.primary:hover {
  background: linear-gradient(135deg, #3aa876, #42b983);
  box-shadow: 0 0 15px rgba(66, 185, 131, 0.5);
}

.filter-btn {
  background: rgba(66, 185, 131, 0.1);
  color: #42b983;
  border: 1px solid rgba(66, 185, 131, 0.3);
}

.filter-btn:hover {
  background: rgba(66, 185, 131, 0.2);
  color: #fff;
}

.icon-btn {
  width: 40px;
  height: 40px;
  padding: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  color: #e0e0e0;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.icon-btn .tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  margin-top: 5px;
}

.icon-btn:hover .tooltip {
  opacity: 1;
  visibility: visible;
  margin-top: 10px;
}

.link-btn {
  background: transparent;
  color: #42b983;
  padding: 0;
}

.link-btn:hover {
  color: #fff;
  text-decoration: underline;
}

.job-tabs {
  display: flex;
  margin-bottom: 20px;
  background: rgba(25, 35, 50, 0.8);
  border-radius: 8px;
  padding: 5px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tech-tab {
  flex: 1;
  padding: 12px 0;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.tech-tab.active {
  color: #fff;
  background: rgba(66, 185, 131, 0.2);
  border-radius: 6px;
}

.tech-tab.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: #42b983;
  border-radius: 2px;
}

.tab-icon {
  font-size: 1.1rem;
}

.tab-badge {
  background: #e74c3c;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 0.7rem;
  margin-left: 5px;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.job-item {
  transition: all 0.3s;
}

.job-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
}

.job-header {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.job-title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.job-title-wrapper h3 {
  margin: 0;
  font-size: 1.3rem;
  color: #fff;
}

.job-match {
  background: rgba(66, 185, 131, 0.2);
  color: #42b983;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 5px;
}

.job-company-info {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.job-company-info span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.job-details {
  margin-bottom: 15px;
}

.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.job-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
  color: rgba(255, 255, 255, 0.8);
}

.salary {
  color: #f39c12 !important;
}

.skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.skill-tag {
  background: rgba(66, 185, 131, 0.1);
  color: #42b983;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 10px;
}

.view-more {
  background: transparent;
  border: none;
  color: #42b983;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
}

.view-more:hover {
  text-decoration: underline;
}

.job-actions {
  display: flex;
  gap: 10px;
}

.apply-btn {
  flex: 1;
  max-width: 150px;
}

.apply-btn.applied {
  background: rgba(66, 185, 131, 0.1);
  color: #42b983;
  border: 1px solid rgba(66, 185, 131, 0.3);
}

.apply-btn.applied:hover {
  background: rgba(66, 185, 131, 0.2);
}

.saved {
  color: #f39c12 !important;
}

.recommendation {
  margin-top: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 10px;
}

.recommended-jobs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.recommended-job {
  padding: 20px;
  background: rgba(15, 22, 33, 0.7);
  border-radius: 8px;
  border: 1px solid rgba(66, 185, 131, 0.2);
  transition: all 0.3s;
}

.recommended-job:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.recommended-job-header {
  margin-bottom: 15px;
}

.recommended-job-header h4 {
  margin: 0 0 5px 0;
  color: #fff;
  font-size: 1.1rem;
}

.recommended-job-header .company {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.match-score {
  margin: 15px 0;
}

.score-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.score-text {
  color: rgba(255, 255, 255, 0.7);
}

.score-value {
  color: #42b983;
  font-weight: bold;
}

.score-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, #42b983, #3aa876);
  transition: width 1s ease;
}

.job-highlights {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 15px 0;
  font-size: 0.9rem;
}

.job-highlights span {
  display: flex;
  align-items: center;
  gap: 5px;
  color: rgba(255, 255, 255, 0.8);
}

.view-btn {
  width: 100%;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-top: 30px;
}

.pagination-btn {
  min-width: 40px;
  height: 40px;
  padding: 0;
  background: rgba(255, 255, 255, 0.05);
  color: #e0e0e0;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.pagination-btn.active {
  background: rgba(66, 185, 131, 0.2);
  color: #42b983;
  border-color: rgba(66, 185, 131, 0.3);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 3rem;
  color: rgba(255, 255, 255, 0.2);
  margin-bottom: 20px;
}

.empty-state h3 {
  color: #fff;
  margin-bottom: 10px;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 20px;
}

.tech-modal {
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
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.close-modal {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.3s;
}

.close-modal:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

@media (max-width: 768px) {
  .job-management {
    padding: 15px;
  }
  
  .search-filter {
    flex-direction: column;
  }
  
  .search-box {
    min-width: auto;
    width: 100%;
  }
  
  .filters {
    width: 100%;
    flex-direction: column;
  }
  
  .tech-select {
    width: 100%;
  }
  
  .job-tabs {
    overflow-x: auto;
    white-space: nowrap;
    justify-content: flex-start;
  }
  
  .tech-tab {
    flex: none;
    padding: 12px 20px;
  }
  
  .recommended-jobs {
    grid-template-columns: 1fr;
  }
  
  .job-actions {
    flex-wrap: wrap;
  }
  
  .apply-btn {
    max-width: none;
    flex: 1 1 100%;
  }
}
</style>