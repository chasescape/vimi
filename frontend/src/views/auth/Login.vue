<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-blue-100 flex items-center justify-center p-4">
    <div class="w-full max-w-5xl bg-white rounded-xl shadow-2xl overflow-hidden flex">
      <!-- 左侧蓝色背景 -->
      <div class="w-1/3 bg-gradient-to-b from-blue-500 to-blue-600 p-10 flex flex-col justify-center text-white">
        <h1 class="text-4xl font-bold mb-6">Vimi-AI面试系统</h1>
        <p class="text-xl mb-8">智能面试平台，助力求职与招聘</p>
        <div class="flex items-center space-x-4">
          <el-icon :size="30"><Monitor /></el-icon>
          <span class="text-lg">高效便捷的面试体验</span>
        </div>
      </div>

      <!-- 右侧操作部分 -->
      <div class="w-2/3 p-12">
        <el-tabs v-model="activeTab" class="mb-8" type="card">
          <el-tab-pane label="应聘者登录" name="candidate">
            <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="mt-6">
              <el-form-item prop="username" class="mb-6">
                <el-input 
                  v-model="loginForm.username" 
                  placeholder="请输入账号" 
                  size="large"
                  :prefix-icon="User"
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="password" class="mb-6">
                <el-input 
                  v-model="loginForm.password" 
                  type="password" 
                  placeholder="请输入密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="captcha" class="mb-6">
                <div class="flex items-center space-x-4">
                  <el-input 
                    v-model="loginForm.captcha" 
                    placeholder="请输入验证码" 
                    size="large"
                    class="text-lg flex-1"
                  />
                  <div 
                    class="w-32 h-12 bg-gray-200 rounded flex items-center justify-center cursor-pointer hover:bg-gray-300 transition-colors"
                    @click="refreshCaptcha"
                  >
                    <span class="text-xl font-mono">{{ captchaText }}</span>
                  </div>
                </div>
              </el-form-item>
              <el-form-item class="mt-10">
                <el-button 
                  type="primary" 
                  size="large" 
                  class="w-full text-lg" 
                  @click="handleLogin"
                  :loading="loading"
                >
                  登录
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="面试官登录" name="interviewer">
            <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="mt-6">
              <el-form-item prop="username" class="mb-6">
                <el-input 
                  v-model="loginForm.username" 
                  placeholder="请输入账号" 
                  size="large"
                  :prefix-icon="User"
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="password" class="mb-6">
                <el-input 
                  v-model="loginForm.password" 
                  type="password" 
                  placeholder="请输入密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="captcha" class="mb-6">
                <div class="flex items-center space-x-4">
                  <el-input 
                    v-model="loginForm.captcha" 
                    placeholder="请输入验证码" 
                    size="large"
                    class="text-lg flex-1"
                  />
                  <div 
                    class="w-32 h-12 bg-gray-200 rounded flex items-center justify-center cursor-pointer hover:bg-gray-300 transition-colors"
                    @click="refreshCaptcha"
                  >
                    <span class="text-xl font-mono">{{ captchaText }}</span>
                  </div>
                </div>
              </el-form-item>
              <el-form-item class="mt-10">
                <el-button 
                  type="primary" 
                  size="large" 
                  class="w-full text-lg" 
                  @click="handleLogin"
                  :loading="loading"
                >
                  登录
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>

        <div class="text-center mt-8">
          <span class="text-gray-600">还没有账号？</span>
          <router-link to="/auth/register" class="text-blue-600 font-medium ml-2">立即注册</router-link>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="absolute bottom-0 w-full py-4 bg-white text-center text-gray-600">
      未来科技AI. 保留所有权利. | 由AI驱动的智能求职平台
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { User, Lock, Monitor } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authApi } from '@/api/auth'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const activeTab = ref('candidate')
const loginFormRef = ref<FormInstance>()
const loading = ref(false)

// 生成随机验证码
const generateCaptcha = () => {
  const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  let result = ''
  for (let i = 0; i < 4; i++) {
    result += chars[Math.floor(Math.random() * chars.length)]
  }
  return result
}

const captchaText = ref(generateCaptcha())
const refreshCaptcha = () => {
  captchaText.value = generateCaptcha()
}

const loginForm = reactive({
  username: '',
  password: '',
  captcha: ''
})

const rules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 4, max: 16, message: '长度在4到16个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在6到20个字符', trigger: 'blur' }
  ],
  captcha: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { pattern: /^[A-Z0-9]{4}$/, message: '验证码格式不正确', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    
    // 验证码检查
    if (loginForm.captcha !== captchaText.value) {
      ElMessage.error('验证码错误')
      refreshCaptcha()
      return
    }

    loading.value = true

    // 调用登录API
    const response = await authApi.login({
      username: loginForm.username,
      password: loginForm.password
    })

    if (response.data.success) {
      // 保存token和用户信息
      localStorage.setItem('token', response.data.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.data.user))
      
      ElMessage.success('登录成功')
      
      // 根据用户角色跳转
      if (response.data.data.user.role === 1) {
        router.push('/interviewer/dashboard')
      } else {
        router.push('/candidate/dashboard')
      }
    } else {
      ElMessage.error(response.data.message || '登录失败')
      refreshCaptcha()
    }
  } catch (error: any) {
    console.error('登录错误:', error)
    ElMessage.error(error.response?.data?.message || '登录失败，请稍后重试')
    refreshCaptcha()
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.el-tabs__item {
  font-size: 18px;
  padding: 0 20px;
  height: 50px;
}

.el-input {
  font-size: 18px;
}

.el-button {
  height: 50px;
  font-size: 18px;
}

:deep(.el-input__wrapper) {
  background-color: #f8fafc !important;
  box-shadow: none !important;
  border: 1px solid #e2e8f0 !important;
}

:deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1 !important;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #3b82f6 !important;
  background-color: white !important;
}
</style>