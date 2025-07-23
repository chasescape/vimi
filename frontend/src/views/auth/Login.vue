<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-blue-100 flex items-center justify-center p-4">
    <div class="w-full max-w-5xl bg-white rounded-xl shadow-2xl overflow-hidden flex flex-col md:flex-row">
      <!-- 左侧蓝色背景 -->
      <div class="w-full md:w-1/3 bg-gradient-to-b from-blue-500 to-blue-600 p-8 md:p-10 flex flex-col justify-center text-white">
        <h1 class="text-3xl md:text-4xl font-bold mb-4 md:mb-6">Vimi-AI面试系统</h1>
        <p class="text-lg md:text-xl mb-6 md:mb-8">智能面试平台，助力求职与招聘</p>
        <div class="flex items-center space-x-4">
          <el-icon :size="24" class="md:text-3xl"><Monitor /></el-icon>
          <span class="text-base md:text-lg">高效便捷的面试体验</span>
        </div>
      </div>

      <!-- 右侧操作部分 -->
      <div class="w-full md:w-2/3 p-8 md:p-12">
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
                    class="w-32 h-12 bg-gray-200 rounded flex items-center justify-center cursor-pointer"
                    @click="refreshCaptcha"
                  >
                    <span class="text-xl font-mono">{{ captchaText }}</span>
                  </div>
                </div>
              </el-form-item>

              <div class="flex justify-between items-center mb-6">
                <el-checkbox v-model="loginForm.remember" class="text-gray-600">记住我</el-checkbox>
                <el-button 
                  type="text" 
                  class="text-blue-600 hover:text-blue-800"
                  @click="showForgotPassword = true"
                >
            忘记密码？
                </el-button>
                  </div>

              <el-form-item class="mt-10">
                <el-button 
                  type="primary" 
                  size="large" 
                  class="w-full text-lg" 
                  :loading="loading"
                  @click="handleLogin"
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
                    class="w-32 h-12 bg-gray-200 rounded flex items-center justify-center cursor-pointer"
                    @click="refreshCaptcha"
                  >
                    <span class="text-xl font-mono">{{ captchaText }}</span>
                  </div>
                </div>
              </el-form-item>

              <div class="flex justify-between items-center mb-6">
                <el-checkbox v-model="loginForm.remember" class="text-gray-600">记住我</el-checkbox>
                <el-button 
                  type="text" 
                  class="text-blue-600 hover:text-blue-800"
                  @click="showForgotPassword = true"
                >
                  忘记密码？
                </el-button>
                  </div>

              <el-form-item class="mt-10">
                <el-button 
                  type="primary" 
                  size="large" 
                  class="w-full text-lg" 
                  :loading="loading"
                  @click="handleLogin"
                >
                  登录
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>

        <div class="text-center mt-8">
          <span class="text-gray-600">还没有账号？</span>
          <router-link to="/register" class="text-blue-600 font-medium ml-2">立即注册</router-link>
        </div>
      </div>
    </div>

    <!-- 忘记密码对话框 -->
    <el-dialog
      v-model="showForgotPassword"
      title="找回密码"
      width="90%"
      max-width="500px"
      center
    >
      <el-form :model="forgotForm" :rules="forgotRules" ref="forgotFormRef" label-width="0">
        <el-form-item prop="email">
          <el-input
            v-model="forgotForm.email"
            placeholder="请输入注册邮箱"
            size="large"
            :prefix-icon="Message"
          />
        </el-form-item>
        <el-form-item prop="captcha">
          <div class="flex items-center space-x-4">
            <el-input
              v-model="forgotForm.captcha"
              placeholder="请输入验证码"
              size="large"
              class="flex-1"
            />
            <el-button 
              type="primary" 
              :disabled="!!countdown" 
              @click="sendEmailCode"
            >
              {{ countdown ? `${countdown}s后重试` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="flex justify-end gap-4">
          <el-button @click="showForgotPassword = false">取消</el-button>
          <el-button type="primary" @click="handleForgotPassword" :loading="forgotLoading">
            确认
          </el-button>
    </div>
      </template>
    </el-dialog>

    <!-- 页脚 -->
    <footer class="absolute bottom-0 w-full py-4 bg-white text-center text-gray-600">
      未来科技AI. 保留所有权利. | 由AI驱动的智能求职平台
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { User, Lock, Monitor, Message } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { authApi } from '@/api/auth'

const router = useRouter()
const activeTab = ref('candidate')
const loading = ref(false)
const showForgotPassword = ref(false)
const forgotLoading = ref(false)
const countdown = ref(0)
const loginForm = reactive({
  username: '',
  password: '',
  captcha: '',
  remember: false
})

const loginFormRef = ref<FormInstance>()

const forgotForm = reactive({
  email: '',
  captcha: ''
})

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
    { pattern: /^[A-Za-z0-9]{4}$/, message: '验证码格式不正确', trigger: 'blur' }
  ]
}

const forgotRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  captcha: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { min: 6, max: 6, message: '验证码长度为6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    
    if (loginForm.captcha !== captchaText.value) {
      ElMessage.error('验证码错误')
      refreshCaptcha()
      return
    }

    loading.value = true
    const response = await authApi.login({
      username: loginForm.username,
      password: loginForm.password
    })

    if (response.data.success) {
    // 保存登录信息
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      
      ElMessage.success('登录成功')
      if (response.data.user.role === 'candidate') {
    router.push('/candidate/home')
      } else {
        router.push('/interviewer/home')
      }
    } else {
      ElMessage.error(response.data.message || '登录失败')
      refreshCaptcha()
    }
  } catch (error: any) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.message || '登录失败，请检查账号和密码')
    refreshCaptcha()
  } finally {
    loading.value = false
  }
}

const sendEmailCode = async () => {
  if (!forgotForm.email) {
    ElMessage.warning('请先输入邮箱')
    return
  }

  try {
    // TODO: 实现发送验证码API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success('验证码已发送到邮箱')
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error) {
    console.error('发送验证码失败:', error)
    ElMessage.error('发送验证码失败，请稍后重试')
  }
}

const handleForgotPassword = async () => {
  const forgotFormRef = ref<FormInstance>()
  if (!forgotFormRef.value) return

  try {
    await forgotFormRef.value.validate()
    forgotLoading.value = true

    // TODO: 实现重置密码API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('重置密码链接已发送到邮箱')
    showForgotPassword.value = false
  } catch (error) {
    console.error('重置密码失败:', error)
    ElMessage.error('重置密码失败，请稍后重试')
  } finally {
    forgotLoading.value = false
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
  font-size: 16px;
}

.el-button {
  height: 50px;
  font-size: 18px;
}

:deep(.el-input__wrapper) {
  background-color: #f8fafc !important;
  box-shadow: none !important;
  border: 1px solid #e2e8f0 !important;
  height: 50px;
  padding: 0 15px;
}

:deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1 !important;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #3b82f6 !important;
  background-color: white !important;
}

:deep(.el-input__inner) {
  height: 48px !important;
  line-height: 48px !important;
  font-size: 16px !important;
}

:deep(.el-input__prefix-icon) {
  font-size: 18px !important;
  color: #94a3b8 !important;
  margin-right: 8px;
}

:deep(.el-form-item__error) {
  color: #ef4444 !important;
  font-size: 14px !important;
  padding-top: 4px !important;
}

:deep(.el-checkbox__label) {
  font-size: 14px;
  color: #64748b;
}

:deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: #3b82f6;
}

@media (max-width: 768px) {
  .el-tabs__item {
    font-size: 16px;
    padding: 0 15px;
    height: 44px;
  }

  .el-input {
    font-size: 14px;
  }

  :deep(.el-input__wrapper) {
    height: 44px;
  }

  :deep(.el-input__inner) {
    height: 42px !important;
    line-height: 42px !important;
    font-size: 14px !important;
  }

  :deep(.el-input__prefix-icon) {
    font-size: 16px !important;
  }

  .el-button {
    height: 44px;
    font-size: 16px;
  }
}
</style>