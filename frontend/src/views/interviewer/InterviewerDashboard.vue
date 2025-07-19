<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 头部栏 -->
    <header class="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg rounded-b-2xl mx-4">
      <div class="container mx-auto px-6 py-4 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-white">Vimi-面试官</h1>
        <div class="flex items-center space-x-4">
          <span class="text-white">{{ username }}</span>
          <router-link to="/interviewer/profile">
            <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center">
              <span class="text-blue-600 font-medium">A</span>
            </div>
          </router-link>
        </div>
      </div>
    </header>

    <div class="flex">
      <!-- 侧边栏 -->
      <nav class="w-64 bg-white shadow-lg h-screen fixed">
        <div class="p-4">
          <DashboardSidebar 
            :items="sidebarItems"
            :activeRoute="$route.path"
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
import { House, Guide, Plus, Calendar , User as UserIcon, View, Reading } from '@element-plus/icons-vue'

const router = useRouter()
const username = ref('面试官_李明')

const sidebarItems = ref([
  {
    title: '主页',
    icon: House,
    route: '/interviewer/home',
    children: []
  },
  {
    title: '面试选项',
    icon: Guide,
    children: [
        {
        title: '新建面试',
        icon: Plus,
        route: '/interviewer/interview-create'
      },
      {
        title: '面试安排',
        icon: Calendar,
        route: '/interviewer/interview-schedule'
      },
      {
        title: '开始面试',
        icon: View,
        route: '/interviewer/interview-page'
      },
      {
        title: '面试历史',
        icon: Reading,
        route: '/interviewer/interview-history'
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