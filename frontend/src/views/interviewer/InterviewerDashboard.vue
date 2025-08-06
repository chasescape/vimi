<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 头部栏 -->
    <header class="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg rounded-b-2xl mx-4">
      <div class="container mx-auto px-6 py-4 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-white">Vimi-面试官</h1>
        <div class="flex items-center space-x-4">
          <span class="text-white">{{ userInfo.username }}</span>
          <el-dropdown trigger="click">
            <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center cursor-pointer">
              <span class="text-blue-600 font-medium">{{ userInfo.username?.charAt(0)?.toUpperCase() }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/interviewer/profile')">
                  <el-icon><User /></el-icon>个人信息
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <div class="flex">
      <!-- 侧边栏 -->
      <nav class="w-64 bg-white shadow-lg h-screen fixed">
        <div class="p-4">
          <el-menu
            :default-active="activeMenu"
            router
            class="border-none"
          >
            <el-menu-item index="/interviewer/home">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/interviewer/create">
              <el-icon><Plus /></el-icon>
              <span>岗位信息</span>
            </el-menu-item>
            <el-menu-item index="/interviewer/schedule">
              <el-icon><Calendar /></el-icon>
              <span>审核简历</span>
            </el-menu-item>
            <el-menu-item index="/interviewer/history">
              <el-icon><List /></el-icon>
              <span>面试信息</span>
            </el-menu-item>

            <el-menu-item index="/interviewer/results">
              <el-icon><User /></el-icon>
              <span>面试结果</span>
            </el-menu-item>

            <el-menu-item index="/interviewer/profile">
              <el-icon><User /></el-icon>
              <span>个人信息</span>
            </el-menu-item>
          </el-menu>
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
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  HomeFilled, 
  Calendar, 
  List, 
  User, 
  Plus, 
  SwitchButton
} from '@element-plus/icons-vue'
import { auth } from '@/utils/auth'

const router = useRouter()
const route = useRoute()

// 用户信息
const userInfo = ref(auth.getUser() || {})

// 当前激活的菜单项
const activeMenu = computed(() => route.path)

// 退出登录
const handleLogout = () => {
  auth.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.el-menu {
  border-right: none;
}

.el-menu-item {
  height: 50px;
  line-height: 50px;
  margin: 8px 0;
  border-radius: 8px;
}

.el-menu-item.is-active {
  background-color: #e6f4ff !important;
  color: #1890ff !important;
}

.el-menu-item:hover {
  background-color: #f5f5f5 !important;
}

.el-dropdown-menu {
  padding: 5px 0;
}

.el-dropdown-menu__item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
}

.el-dropdown-menu__item .el-icon {
  margin-right: 8px;
  font-size: 16px;
}

:deep(.el-menu-item) {
  margin: 8px 16px;
  border-radius: 8px;
}

:deep(.el-menu-item.is-active) {
  background-color: #e6f4ff;
  color: #1890ff;
}

:deep(.el-menu-item:hover) {
  background-color: #f5f5f5;
}

:deep(.el-menu-item .el-icon) {
  font-size: 18px;
}
</style>