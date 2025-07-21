<template>
  <div class="dashboard">
    <!-- 添加科技感背景元素 -->
    <div class="tech-background">
      <div class="tech-circle circle-1"></div>
      <div class="tech-circle circle-2"></div>
      <div class="tech-circle circle-3"></div>
      <div class="tech-grid"></div>
    </div>
     <div class="content-container">
      <h2 class="tech-title">
        <span class="title-text">首页概览</span>
        <span class="title-glare"></span>
      </h2>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-file-alt"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">3</span>
          <span class="stat-label">简历数量</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-briefcase"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">5</span>
          <span class="stat-label">申请岗位</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-calendar-check"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">2</span>
          <span class="stat-label">面试安排</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-chart-line"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">85%</span>
          <span class="stat-label">平均匹配度</span>
        </div>
      </div>
    </div>
    
    <div class="content-grid">
      <div class="upcoming-interviews">
        <h3>即将开始的面试</h3>
        <div class="interview-list">
          <div class="interview-item" v-for="interview in upcomingInterviews" :key="interview.id">
            <div class="interview-time">
              <span class="date">{{ interview.date }}</span>
              <span class="time">{{ interview.time }}</span>
            </div>
            <div class="interview-details">
              <h4>{{ interview.position }}</h4>
              <p>{{ interview.company }}</p>
            </div>
            <button class="join-btn">进入面试</button>
          </div>
        </div>
      </div>
      
      <div class="recommended-jobs">
        <h3>推荐岗位</h3>
        <div class="job-list">
          <div class="job-item" v-for="job in recommendedJobs" :key="job.id">
            <h4>{{ job.title }}</h4>
            <p class="company">{{ job.company }}</p>
            <p class="location">{{ job.location }}</p>
            <div class="job-meta">
              <span class="salary">{{ job.salary }}</span>
              <span class="match">匹配度: {{ job.match }}%</span>
            </div>
            <button class="apply-btn">立即申请</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
const upcomingInterviews = [
  {
    id: 1,
    date: '2023-11-15',
    time: '14:30',
    position: '前端开发工程师',
    company: 'ABC科技有限公司'
  },
  {
    id: 2,
    date: '2023-11-18',
    time: '10:00',
    position: 'UI设计师',
    company: 'XYZ设计公司'
  }
]

const recommendedJobs = [
  {
    id: 1,
    title: '高级前端工程师',
    company: 'DEF科技',
    location: '北京',
    salary: '25-40k',
    match: 92
  },
  {
    id: 2,
    title: '全栈开发工程师',
    company: 'GHI互联网',
    location: '上海',
    salary: '30-50k',
    match: 88
  },
  {
    id: 3,
    title: '产品经理',
    company: 'JKL产品',
    location: '深圳',
    salary: '20-35k',
    match: 76
  }
]
</script>

<style scoped>
/* 添加科技感背景样式 */
.dashboard {
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

/* 修改卡片样式以匹配科技感主题 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: rgba(25, 35, 50, 0.8);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  color: #fff;
}

.stat-icon {
  width: 50px;
  height: 50px;
  background-color: rgba(66, 185, 131, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: #42b983;
  font-size: 1.2rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

/* 修改内容区域样式 */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.upcoming-interviews, .recommended-jobs {
  background: rgba(25, 35, 50, 0.8);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}

h3 {
  color: #fff;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

/* 修改面试和职位列表项样式 */
.interview-item, .job-item {
  background: rgba(15, 22, 33, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 15px;
  transition: all 0.3s;
}

.interview-item:hover, .job-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  border-color: rgba(66, 185, 131, 0.3);
}

/* 修改按钮样式 */
.join-btn, .apply-btn {
  background: linear-gradient(135deg, #42b983, #3aa876);
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.join-btn:hover, .apply-btn:hover {
  background: linear-gradient(135deg, #3aa876, #42b983);
  box-shadow: 0 0 15px rgba(66, 185, 131, 0.3);
}

/* 修改文本颜色 */
.date, .time, .company, .location {
  color: rgba(255, 255, 255, 0.7);
}

.time {
  color: #fff;
  font-weight: bold;
}

.salary {
  color: #f39c12;
  font-weight: bold;
}

.match {
  color: #42b983;
  font-weight: bold;
}

@media (max-width: 992px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>