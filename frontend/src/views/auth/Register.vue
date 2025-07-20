<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-blue-100 flex items-center justify-center p-4">
    <div class="w-full max-w-5xl bg-white rounded-xl shadow-2xl overflow-hidden flex">
      <!-- 左侧蓝色背景 -->
      <div class="w-1/3 bg-gradient-to-b from-blue-500 to-blue-600 p-10 flex flex-col justify-center text-white">
        <h1 class="text-4xl font-bold mb-6">Vimi-AI面试系统</h1>
        <p class="text-xl mb-8">智能面试平台，助力求职与招聘</p>
        <div class="flex items-center space-x-4">
          <el-icon :size="30"><Opportunity /></el-icon>
          <span class="text-lg">开启您的职业新旅程</span>
        </div>
      </div>

      <!-- 右侧操作部分 -->
      <div class="w-2/3 p-12">
        <el-tabs v-model="activeTab" class="mb-8" type="card">
          <el-tab-pane label="应聘者注册" name="candidate">
            <el-form 
              :model="formData" 
              :rules="rules" 
              ref="registerFormRef"
              class="mt-6"
            >
              <el-form-item prop="email" class="mb-6">
                <el-input 
                  v-model="formData.email" 
                  placeholder="请输入邮箱" 
                  size="large"
                  :prefix-icon="Message"
                  clearable
                />
              </el-form-item>
              
              <el-form-item prop="username" class="mb-6">
                <el-input 
                  v-model="formData.username" 
                  placeholder="请输入用户名" 
                  size="large"
                  :prefix-icon="User"
                  clearable
                />
              </el-form-item>
              
              <el-form-item prop="password" class="mb-6">
                <el-input 
                  v-model="formData.password" 
                  type="password" 
                  placeholder="请输入密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                />
              </el-form-item>
              
              <el-form-item prop="confirmPassword" class="mb-6">
                <el-input 
                  v-model="formData.confirmPassword" 
                  type="password" 
                  placeholder="请确认密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                />
              </el-form-item>
              
              <el-form-item prop="captcha" class="mb-6">
                <div class="flex items-center space-x-4">
                  <el-input 
                    v-model="formData.captcha" 
                    placeholder="请输入验证码" 
                    size="large"
                    class="flex-1"
                  />
                  <div 
                    class="w-32 h-12 bg-gray-100 rounded-lg flex items-center justify-center cursor-pointer hover:bg-gray-200 transition-colors"
                    @click="refreshCaptcha"
                  >
                    <span class="text-xl font-mono">{{ captchaText }}</span>
                  </div>
                </div>
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  size="large" 
                  class="w-full" 
                  :loading="loading"
                  @click="handleRegister"
                >
                  注册
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="面试官注册" name="interviewer">
            <el-form 
              :model="formData" 
              :rules="rules" 
              ref="registerFormRef"
              class="mt-6"
            >
              <el-form-item prop="email" class="mb-6">
                <el-input 
                  v-model="formData.email" 
                  placeholder="请输入邮箱" 
                  size="large"
                  :prefix-icon="Message"
                  clearable
                />
              </el-form-item>
              
              <el-form-item prop="username" class="mb-6">
                <el-input 
                  v-model="formData.username" 
                  placeholder="请输入用户名" 
                  size="large"
                  :prefix-icon="User"
                  clearable
                />
              </el-form-item>
              
              <el-form-item prop="password" class="mb-6">
                <el-input 
                  v-model="formData.password" 
                  type="password" 
                  placeholder="请输入密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                />
              </el-form-item>
              
              <el-form-item prop="confirmPassword" class="mb-6">
                <el-input 
                  v-model="formData.confirmPassword" 
                  type="password" 
                  placeholder="请确认密码" 
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                />
              </el-form-item>
              
              <el-form-item prop="inviteCode" class="mb-6">
                <el-input 
                  v-model="formData.inviteCode" 
                  placeholder="请输入邀请码(仅面试官需要)" 
                  size="large"
                  :prefix-icon="Key"
                  clearable
                />
              </el-form-item>
              
              <el-form-item prop="captcha" class="mb-6">
                <div class="flex items-center space-x-4">
                  <el-input 
                    v-model="formData.captcha" 
                    placeholder="请输入验证码" 
                    size="large"
                    class="flex-1"
                  />
                  <div 
                    class="w-32 h-12 bg-gray-100 rounded-lg flex items-center justify-center cursor-pointer hover:bg-gray-200 transition-colors"
                    @click="refreshCaptcha"
                  >
                    <span class="text-xl font-mono">{{ captchaText }}</span>
                  </div>
                </div>
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  size="large" 
                  class="w-full" 
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
          <router-link to="/auth/login" class="text-blue-600 font-medium ml-2 hover:text-blue-700 transition-colors">
            立即登录
          </router-link>
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
import { authApi } from '@/api/auth'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const activeTab = ref('candidate')
const registerFormRef = ref<FormInstance>()
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

const formData = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
  inviteCode: '',
  captcha: ''
})

const validatePassword = (rule: any, value: string, callback: Function) => {
  if (value !== formData.password) {
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
    { pattern: /^[A-Z0-9]{4}$/, message: '验证码格式不正确', trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()

    // 验证码检查
    if (formData.captcha !== captchaText.value) {
      ElMessage.error('验证码错误')
      refreshCaptcha()
      return
    }

    if (formData.password !== formData.confirmPassword) {
      ElMessage.error('两次输入密码不一致')
      return
    }

    loading.value = true

    // 调用注册API
    const response = await authApi.register({
      username: formData.username,
      email: formData.email,
      password: formData.password,
      role: activeTab.value === 'interviewer' ? 'interviewer' : 'candidate',
      inviteCode: activeTab.value === 'interviewer' ? formData.inviteCode : undefined
    })

    if (response.data.success) {
      ElMessage.success('注册成功')
      router.push('/auth/login')
    } else {
      ElMessage.error(response.data.message || '注册失败')
      refreshCaptcha()
    }
  } catch (error: any) {
    console.error('注册错误:', error)
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

:deep(.el-input__inner) {
  height: 44px !important;
  line-height: 44px !important;
  font-size: 16px !important;
}

:deep(.el-input__prefix-icon) {
  font-size: 18px !important;
  color: #94a3b8 !important;
}

.el-button {
  height: 44px;
  font-size: 16px;
}

:deep(.el-form-item__error) {
  color: #ef4444 !important;
  font-size: 14px !important;
  padding-top: 4px !important;
}
</style>