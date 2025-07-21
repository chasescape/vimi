<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 头部栏 -->
    <header class="bg-gradient-to-r from-blue-500 to-blue-700 shadow-lg rounded-b-2xl mx-4">
      <div class="container mx-auto px-6 py-4 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-white">Vimi-应聘者</h1>
        <div class="flex items-center space-x-4">
          <span class="text-white">{{ username }}</span>
          <router-link to="/profile">
            <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center">
              <span class="text-blue-600 font-medium">U</span>
            </div>
          </router-link>
        </div>
      </div>
    </header>

    <div class="flex">
      <!-- 侧边栏 -->
      <nav class="w-64 bg-white shadow-lg h-screen fixed" >
        <div class="p-4" >
          <DashboardSidebar 
            :items="sidebarItems"
            :activeRoute="$route.path"
            is-root
            @navigate="handleNavigation"
          />
        </div>
      </nav>

      <!-- 主要内容 -->
      <main class="ml-64 p-8 flex-1">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import DashboardSidebar from '@/components/layout/DashboardSidebar.vue'
import {Guide, House, Calendar, User as UserIcon, Document, Search, View, VideoCamera, Histogram, Reading } from '@element-plus/icons-vue'

const router = useRouter()
const username = ref('候选人_张伟')

const sidebarItems = ref([
  {
    title: '主页',
    icon: House,
    route: '/candidate/home',
    children: []
  },
  {
    title: '面试选项',
    icon: Guide,
    route: '',
    children: [
        {
        title: '搜索面试',
        icon: Search,
        route: '/candidate/interview-search'
      },
      {
        title: '面试安排',
        icon: Calendar,
        route: '/candidate/interview-schedule'
      },
      {
        title: '开始面试',
        icon: View,
        route: '/candidate/interview-page'
      },
      {
        title: '模拟面试',
        icon: VideoCamera,
        route: '/candidate/interview-test'
      },
      {
        title: '面试表现',
        icon: Histogram,
        route: '/candidate/interview-performance'
      },
      {
        title: '面试历史',
        icon: Reading,
        route: '/candidate/interview-history'
      },
      {
        title: '面试分析',
        icon: Reading,
        route: '/candidate/interview-result'
      },
    ]
  },
  {
    title: '个人中心',
    icon: UserIcon,
    route: '/candidate/profile'
  }
])

const handleNavigation = (route: string) => {
  router.push(route)
}
</script>