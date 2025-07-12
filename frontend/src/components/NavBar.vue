<template>
  <nav class="navbar">
    <div class="logo-container">
      <h1 class="logo">AI面试系统</h1>
    </div>
    
    <ul class="nav-menu">
      <li 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="{ active: activeTab === tab.id }"
        @click="$emit('change-tab', tab.id)"
      >
        <i :class="tab.icon"></i>
        <span>{{ tab.name }}</span>
      </li>
    </ul>
    
    <div class="user-profile">
      <div class="avatar">
        <i class="fas fa-user-circle"></i>
      </div>
      <div class="user-info">
        <span class="username">应聘者</span>
        <span class="user-role">普通用户</span>
      </div>
    </div>
  </nav>
</template>

<script setup>
defineProps({
  activeTab: {
    type: String,
    required: true
  }
})

defineEmits(['change-tab'])

const tabs = [
  { id: 'dashboard', name: '首页概览', icon: 'fas fa-home' },
  { id: 'resume', name: '我的简历中心', icon: 'fas fa-file-alt' },
  { id: 'jobs', name: '职位探索', icon: 'fas fa-briefcase' },
  { id: 'interview', name: '我的面试', icon: 'fas fa-video' },
  { id: 'results', name: '结果分析', icon: 'fas fa-chart-bar' }
]
</script>

<style scoped>
.navbar {
    z-index: 1000;
  position: fixed;
  
}

.logo-container {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
  color: #42b983;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 20px 0;
  flex: 1;
}
.current-video-analysis.compact {
  max-width: 960px;              /* 限制宽度，防止撑满 */
  margin: 0 auto 25px;           /* 居中 + 间距 */
  padding: 16px;                 /* 缩小内边距 */
  box-sizing: border-box;        /* 防止padding撑出边界 */
  background: var(--dark-card);  /* 保留你已有的深色背景变量 */
  border-radius: 8px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.video-player-container video {
  width: 100%;
  height: auto;
  border-radius: 4px;
}

/* 加一点点间距与排列优化 */
.video-analysis-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.video-insights {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.insight-item {
  flex: 1 1 45%;
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 6px;
}

/* 响应式支持 */
@media screen and (max-width: 768px) {
  .current-video-analysis.compact {
    padding: 12px;
    max-width: 100%;
  }

  .video-insights {
    flex-direction: column;
  }

  .insight-item {
    flex: 1 1 100%;
  }
}

.nav-menu li {
  color: black; /* 添加这一行 */
  padding: 12px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.3s;
}

.nav-menu li:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* 修改激活状态的文字颜色 */
.nav-menu li.active {
  color: white; /* 保持激活状态文字为白色（与绿色背景对比） */
  background-color: #42b983;
}

.nav-menu li i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

.user-profile {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
}

.avatar {
  font-size: 2rem;
  margin-right: 10px;
  color: #42b983;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
}

.user-role {
  font-size: 0.8rem;
  opacity: 0.8;
}
</style>