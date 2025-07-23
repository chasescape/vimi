<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-blue-100 flex items-center justify-center p-4">
    <div class="w-full max-w-5xl bg-white rounded-xl shadow-2xl overflow-hidden flex flex-col md:flex-row">
      <!-- 左侧蓝色背景 -->
      <div class="w-full md:w-1/3 bg-gradient-to-b from-blue-500 to-blue-600 p-8 md:p-10 flex flex-col justify-center text-white">
        <h1 class="text-3xl md:text-4xl font-bold mb-4 md:mb-6">Vimi-AI面试系统</h1>
        <p class="text-lg md:text-xl mb-6 md:mb-8">智能面试平台，助力求职与招聘</p>
        <div class="flex items-center space-x-4">
          <el-icon :size="24" class="md:text-3xl"><Opportunity /></el-icon>
          <span class="text-base md:text-lg">开启您的职业新旅程</span>
        </div>
      </div>

      <!-- 右侧操作部分 -->
      <div class="w-full md:w-2/3 p-8 md:p-12">
        <el-tabs v-model="activeTab" class="mb-8">
          <el-tab-pane label="应聘者注册" name="candidate">
            <el-form :model="registerForm" :rules="rules" ref="registerFormRef" class="mt-6">
              <el-form-item prop="email" class="mb-6">
                <el-input 
                  v-model="registerForm.email" 
                  placeholder="请输入邮箱" 
                  size="large"
                  :prefix-icon="Message"
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="username" class="mb-6">
                <el-input 
                  v-model="registerForm.username" 
                  placeholder="请输入用户名" 
                  size="large"
                  :prefix-icon="User"
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="password" class="mb-6">
                <el-input 
                  v-model="registerForm.password" 
                  type="password" 
                  placeholder="请输入密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="confirmPassword" class="mb-6">
                <el-input 
                  v-model="registerForm.confirmPassword" 
                  type="password" 
                  placeholder="请确认密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="captcha" class="mb-6">
                <div class="flex items-center space-x-4">
                  <el-input 
                    v-model="registerForm.captcha" 
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
              <el-form-item class="mt-10">
                <el-button 
                  type="primary" 
                  size="large" 
                  class="w-full text-lg" 
                  :loading="loading"
                  @click="handleRegister"
                >
                  注册
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="面试官注册" name="interviewer">
            <el-form :model="registerForm" :rules="rules" ref="registerFormRef" class="mt-6">
              <el-form-item prop="email" class="mb-6">
                <el-input 
                  v-model="registerForm.email" 
                  placeholder="请输入邮箱" 
                  size="large"
                  :prefix-icon="Message"
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="username" class="mb-6">
                <el-input 
                  v-model="registerForm.username" 
                  placeholder="请输入用户名" 
                  size="large"
                  :prefix-icon="User"
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="password" class="mb-6">
                <el-input 
                  v-model="registerForm.password" 
                  type="password" 
                  placeholder="请输入密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="confirmPassword" class="mb-6">
                <el-input 
                  v-model="registerForm.confirmPassword" 
                  type="password" 
                  placeholder="请确认密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                  class="text-lg"
                />
              </el-form-item>
              <el-form-item prop="inviteCode" class="mb-6">
                <el-input 
                  v-model="registerForm.inviteCode" 
                  placeholder="请输入邀请码 VIMI2024" 
                  size="large"
                  :prefix-icon="Key"
                  class="text-lg"
                />
                <div class="text-gray-500 text-sm mt-1">
                  * 面试官注册需要输入邀请码：VIMI2024
                </div>
              </el-form-item>
              <el-form-item prop="captcha" class="mb-6">
                <div class="flex items-center space-x-4">
                  <el-input 
                    v-model="registerForm.captcha" 
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
              <el-form-item class="mt-10">
                <el-button 
                  type="primary" 
                  size="large" 
                  class="w-full text-lg" 
                  :loading="loading"
                  @click="handleRegister"
                >
                  注册
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>

        <div class="text-center mt-8">
          <span class="text-gray-600">已有账号？</span>
          <router-link to="/login" class="text-blue-600 font-medium ml-2">立即登录</router-link>
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
import { User, Lock, Message, Key, Opportunity } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { authApi } from '@/api/auth'

const router = useRouter()
const activeTab = ref('candidate')
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

const registerForm = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
  inviteCode: '',
  captcha: ''
})

const registerFormRef = ref<FormInstance>()

const validatePassword = (rule: any, value: string, callback: Function) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const validateEmail = (rule: any, value: string, callback: Function) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(value)) {
    callback(new Error('邮箱格式不正确'))
  } else {
    callback()
  }
}

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { validator: validateEmail, trigger: 'blur' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 4, max: 16, message: '长度在4到16个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在6到20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ],
  inviteCode: [
    { required: activeTab.value === 'interviewer', message: '请输入邀请码', trigger: 'blur' }
  ],
  captcha: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { pattern: /^[A-Za-z0-9]{4}$/, message: '验证码格式不正确', trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()

    // 验证码检查
    if (registerForm.captcha !== captchaText.value) {
      ElMessage.error('验证码错误')
      refreshCaptcha()
      return
    }

    if (registerForm.password !== registerForm.confirmPassword) {
      ElMessage.error('两次输入密码不一致')
      return
    }

    if (activeTab.value === 'interviewer' && !registerForm.inviteCode) {
      ElMessage.error('请输入邀请码')
      return
    }

    loading.value = true

    const response = await authApi.register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password,
      role: activeTab.value as 'candidate' | 'interviewer',
      inviteCode: activeTab.value === 'interviewer' ? registerForm.inviteCode : undefined
    })

    if (response.data.success) {
      ElMessage.success('注册成功')
      router.push('/login')
    } else {
      ElMessage.error(response.data.message || '注册失败')
      refreshCaptcha()
    }
  } catch (error: any) {
    console.error('注册失败:', error)
    ElMessage.error(error.response?.data?.message || '注册失败，请稍后重试')
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

:deep(.el-tabs__nav) {
  width: 100%;
  display: flex;
}

:deep(.el-tabs__item) {
  flex: 1;
  text-align: center;
  font-size: 16px;
  color: #64748b;
}

:deep(.el-tabs__item.is-active) {
  color: #3b82f6;
  font-weight: 500;
}

:deep(.el-tabs__active-bar) {
  background-color: #3b82f6;
}

.captcha-box {
  height: 50px !important;
  font-family: 'Courier New', monospace;
  letter-spacing: 2px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.captcha-box:hover {
  background-color: #e2e8f0 !important;
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

  .captcha-box {
    height: 44px !important;
  }
}
</style>