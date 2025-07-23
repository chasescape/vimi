<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 侧边栏 -->
    <div class="fixed left-0 top-0 w-64 h-full bg-white shadow-lg z-10">
      <div class="p-6">
        <h1 class="text-2xl font-bold text-gray-800">VIMI</h1>
      </div>
      <nav class="mt-4">
        <router-link
          v-for="item in sidebarItems"
          :key="item.route"
          :to="item.route"
          class="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 transition-colors"
          :class="{ 'bg-gray-100 text-blue-600': isRouteActive(item.route) }"
        >
          <el-icon class="mr-3" :size="18">
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.title }}</span>
        </router-link>
      </nav>
    </div>

    <!-- 主内容区 -->
    <div class="ml-64 min-h-screen">
      <!-- 顶部栏 -->
      <div class="bg-white shadow-sm">
        <div class="container mx-auto px-6 py-4">
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold text-gray-800">{{ currentPageTitle }}</h2>
            <el-dropdown trigger="click">
              <div class="flex items-center cursor-pointer">
                <el-avatar :size="32" class="mr-2">
                  {{ userInitials }}
                </el-avatar>
                <span class="text-gray-700">{{ username }}</span>
                <el-icon class="ml-1"><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="goToProfile">
                    <el-icon><User /></el-icon>个人中心
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>

      <!-- 页面内容 -->
      <div class="container mx-auto p-6">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import {
  House,
  Document,
  Search,
  Calendar,
  Timer,
  VideoCamera,
  User,
  ArrowDown,
  SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

// 用户信息
const username = ref(localStorage.getItem('username') || '用户')
const userInitials = computed(() => {
  return username.value.charAt(0).toUpperCase()
})

// 侧边栏菜单项
const sidebarItems = [
  { title: '主页', route: '/candidate/home', icon: House },
  { title: '简历管理', route: '/candidate/resume', icon: Document },
  { title: '职位搜索', route: '/candidate/search', icon: Search },
  { title: '面试日程', route: '/candidate/schedule', icon: Calendar },
  { title: '面试历史', route: '/candidate/history', icon: Timer },
  { title: '模拟面试', route: '/candidate/test', icon: VideoCamera }
]

// 检查路由是否激活
const isRouteActive = (path: string) => {
  return route.path === path
}

// 当前页面标题
const currentPageTitle = computed(() => {
  const currentItem = sidebarItems.find(item => item.route === route.path)
  return currentItem ? currentItem.title : ''
})

// 跳转到个人中心
const goToProfile = () => {
  router.push('/candidate/profile')
}

// 处理退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 清除登录信息
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('role')
    
    // 跳转到登录页
    router.push('/login')
  } catch {
    // 用户取消操作
  }
}
</script>

<style scoped>
.router-link-active {
  @apply bg-gray-100 text-blue-600;
}

.el-dropdown-menu {
  @apply min-w-[120px];
}

.el-dropdown-menu__item {
  @apply flex items-center;
}

.el-dropdown-menu__item .el-icon {
  @apply mr-2;
}
</style>