// src/views/MyHome.vue
<template>
  <div class="app-container">
    <NavBar :active-tab="activeTab" @change-tab="changeTab" />
    
    <div class="main-content">
      <Dashboard v-if="activeTab === 'dashboard'" />
      <ResumeManagement v-if="activeTab === 'resume'" />
      <JobManagement v-if="activeTab === 'jobs'" />
      <InterviewModule v-if="activeTab === 'interview'" />
      <ResultAnalysis v-if="activeTab === 'results'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from '../components/NavBar.vue'
import Dashboard from '../components/Dashboard.vue'
import ResumeManagement from '../components/ResumeManagement.vue'
import JobManagement from '../components/JobManagement.vue'
import InterviewModule from '../components/InterviewModule.vue'
import ResultAnalysis from '../components/ResultAnalysis.vue'

const activeTab = ref('dashboard')
const changeTab = (tab) => {
  activeTab.value = tab
}
</script>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.main-content {
  flex: 1;
  padding: 24px;
  background-color: #fff;
  margin-left: 220px;
}
</style>
