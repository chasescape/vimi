<template>
  <div class="profile-page p-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- 左侧个人信息卡片 -->
      <div class="md:col-span-1">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="text-center mb-6">
            <el-avatar 
              :size="100" 
              :src="userInfo.avatar"
              class="mb-4"
            >
              {{ userInfo.name?.charAt(0)?.toUpperCase() }}
            </el-avatar>
            <h2 class="text-xl font-bold">{{ userInfo.name }}</h2>
            <p class="text-gray-500">{{ userInfo.title }}</p>
          </div>

          <div class="border-t pt-4">
            <div class="flex items-center mb-4">
              <el-icon class="text-gray-400 mr-2"><Message /></el-icon>
              <span class="text-gray-600">{{ userInfo.email }}</span>
            </div>
            <div class="flex items-center mb-4">
              <el-icon class="text-gray-400 mr-2"><Iphone as Phone /></el-icon>
              <span class="text-gray-600">{{ userInfo.phone }}</span>
            </div>
            <div class="flex items-center mb-4">
              <el-icon class="text-gray-400 mr-2"><Location /></el-icon>
              <span class="text-gray-600">{{ userInfo.location }}</span>
            </div>
            <div class="flex items-center">
              <el-icon class="text-gray-400 mr-2"><House as Office /></el-icon>
              <span class="text-gray-600">{{ userInfo.department }}</span>
            </div>
          </div>

          <div class="border-t pt-4 mt-4">
            <h3 class="text-lg font-medium mb-3">专业领域</h3>
            <div class="flex flex-wrap gap-2">
              <el-tag 
                v-for="skill in userInfo.skills" 
                :key="skill"
                size="small"
              >
                {{ skill }}
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 面试统计 -->
        <div class="bg-white rounded-lg shadow-md p-6 mt-6">
          <h3 class="text-lg font-medium mb-4">面试统计</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <p class="text-2xl font-bold text-blue-600">{{ stats.totalInterviews }}</p>
              <p class="text-gray-600">总面试场次</p>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <p class="text-2xl font-bold text-green-600">{{ stats.thisMonth }}</p>
              <p class="text-gray-600">本月面试</p>
            </div>
            <div class="text-center p-4 bg-purple-50 rounded-lg">
              <p class="text-2xl font-bold text-purple-600">{{ stats.avgScore }}分</p>
              <p class="text-gray-600">平均评分</p>
            </div>
            <div class="text-center p-4 bg-orange-50 rounded-lg">
              <p class="text-2xl font-bold text-orange-600">{{ stats.passRate }}%</p>
              <p class="text-gray-600">通过率</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧内容区 -->
      <div class="md:col-span-2">
        <!-- 个人信息设置 -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-lg font-medium">个人信息设置</h3>
            <el-button type="primary" @click="handleSaveProfile">
              保存修改
            </el-button>
          </div>

          <el-form :model="profileForm" label-width="100px">
            <el-form-item label="姓名">
              <el-input v-model="profileForm.name" />
            </el-form-item>
            <el-form-item label="职位">
              <el-input v-model="profileForm.title" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="profileForm.email" />
            </el-form-item>
            <el-form-item label="手机">
              <el-input v-model="profileForm.phone" />
            </el-form-item>
            <el-form-item label="所在地">
              <el-input v-model="profileForm.location" />
            </el-form-item>
            <el-form-item label="部门">
              <el-input v-model="profileForm.department" />
            </el-form-item>
            <el-form-item label="专业领域">
              <el-select
                v-model="profileForm.skills"
                multiple
                filterable
                allow-create
                default-first-option
                placeholder="请选择或输入专业领域"
                class="w-full"
              >
                <el-option
                  v-for="skill in skillOptions"
                  :key="skill"
                  :label="skill"
                  :value="skill"
                />
              </el-select>
            </el-form-item>
          </el-form>
        </div>

        <!-- 账号安全设置 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-medium mb-6">账号安全设置</h3>
          
          <div class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h4 class="font-medium">修改密码</h4>
                <p class="text-gray-500 text-sm">定期更改密码可以提高账号安全性</p>
              </div>
              <el-button @click="showChangePassword = true">修改</el-button>
            </div>

            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h4 class="font-medium">绑定手机</h4>
                <p class="text-gray-500 text-sm">已绑定：{{ maskPhone(userInfo.phone) }}</p>
              </div>
              <el-button @click="showChangePhone = true">更换</el-button>
            </div>

            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h4 class="font-medium">绑定邮箱</h4>
                <p class="text-gray-500 text-sm">已绑定：{{ maskEmail(userInfo.email) }}</p>
              </div>
              <el-button @click="showChangeEmail = true">更换</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showChangePassword"
      title="修改密码"
      width="400px"
    >
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="当前密码">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showChangePassword = false">取消</el-button>
          <el-button type="primary" @click="handleChangePassword">
            确认修改
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 更换手机对话框 -->
    <el-dialog
      v-model="showChangePhone"
      title="更换手机"
      width="400px"
    >
      <el-form :model="phoneForm" label-width="100px">
        <el-form-item label="新手机号">
          <el-input v-model="phoneForm.phone" />
        </el-form-item>
        <el-form-item label="验证码">
          <div class="flex gap-4">
            <el-input v-model="phoneForm.code" />
            <el-button 
              type="primary" 
              :disabled="!!countdown"
              @click="sendPhoneCode"
            >
              {{ countdown ? `${countdown}s` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showChangePhone = false">取消</el-button>
          <el-button type="primary" @click="handleChangePhone">
            确认更换
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 更换邮箱对话框 -->
    <el-dialog
      v-model="showChangeEmail"
      title="更换邮箱"
      width="400px"
    >
      <el-form :model="emailForm" label-width="100px">
        <el-form-item label="新邮箱">
          <el-input v-model="emailForm.email" />
        </el-form-item>
        <el-form-item label="验证码">
          <div class="flex gap-4">
            <el-input v-model="emailForm.code" />
            <el-button 
              type="primary" 
              :disabled="!!countdown"
              @click="sendEmailCode"
            >
              {{ countdown ? `${countdown}s` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showChangeEmail = false">取消</el-button>
          <el-button type="primary" @click="handleChangeEmail">
            确认更换
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Message, 
  Iphone as Phone,
  Location, 
  House as Office,
  Timer,
  CircleCheckFilled as CircleCheck,
  CircleCloseFilled as CircleClose,
  Loading
} from '@element-plus/icons-vue'

// 用户信息
const userInfo = ref({
  name: '李明',
  title: '高级面试官',
  email: 'liming@example.com',
  phone: '13800138000',
  location: '北京市朝阳区',
  department: '技术部-面试组',
  avatar: '',
  skills: ['前端开发', 'Vue', 'React', 'Node.js', 'TypeScript']
})

// 面试统计
const stats = ref({
  totalInterviews: 86,
  thisMonth: 12,
  avgScore: 4.5,
  passRate: 85
})

// 个人信息表单
const profileForm = ref({
  name: userInfo.value.name,
  title: userInfo.value.title,
  email: userInfo.value.email,
  phone: userInfo.value.phone,
  location: userInfo.value.location,
  department: userInfo.value.department,
  skills: userInfo.value.skills
})

// 专业领域选项
const skillOptions = [
  '前端开发',
  '后端开发',
  'Vue',
  'React',
  'Angular',
  'Node.js',
  'Python',
  'Java',
  'Go',
  'TypeScript',
  '微服务',
  '架构设计',
  '数据库',
  '算法'
]

// 修改密码
const showChangePassword = ref(false)
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 更换手机
const showChangePhone = ref(false)
const phoneForm = ref({
  phone: '',
  code: ''
})

// 更换邮箱
const showChangeEmail = ref(false)
const emailForm = ref({
  email: '',
  code: ''
})

// 验证码倒计时
const countdown = ref(0)

// 保存个人信息
const handleSaveProfile = () => {
  ElMessage.success('保存成功')
}

// 修改密码
const handleChangePassword = () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  ElMessage.success('密码修改成功')
  showChangePassword.value = false
}

// 发送手机验证码
const sendPhoneCode = () => {
  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
  ElMessage.success('验证码已发送')
}

// 发送邮箱验证码
const sendEmailCode = () => {
  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
  ElMessage.success('验证码已发送')
}

// 更换手机
const handleChangePhone = () => {
  ElMessage.success('手机号更换成功')
  showChangePhone.value = false
}

// 更换邮箱
const handleChangeEmail = () => {
  ElMessage.success('邮箱更换成功')
  showChangeEmail.value = false
}

// 手机号脱敏
const maskPhone = (phone: string) => {
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

// 邮箱脱敏
const maskEmail = (email: string) => {
  const [name, domain] = email.split('@')
  return `${name.charAt(0)}***@${domain}`
}
</script>

<style scoped>
.profile-page {
  min-height: calc(100vh - 64px);
}

:deep(.el-tag) {
  margin: 2px;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}
</style>
