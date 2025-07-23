<template>
  <div class="profile-container p-6">
    <el-card class="mb-6">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">基本信息</h2>
          <el-button type="primary" @click="saveBasicInfo">保存修改</el-button>
        </div>
      </template>
      
      <el-form :model="basicInfo" label-width="100px">
        <el-form-item label="头像">
          <el-upload
            class="avatar-uploader"
            action="/api/user/avatar"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <el-avatar v-if="basicInfo.avatar" :size="100" :src="basicInfo.avatar" />
            <el-icon v-else class="avatar-uploader-icon" :size="30"><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="姓名">
          <el-input v-model="basicInfo.name" placeholder="请输入姓名"></el-input>
        </el-form-item>

        <el-form-item label="性别">
          <el-radio-group v-model="basicInfo.gender">
            <el-radio label="male">男</el-radio>
            <el-radio label="female">女</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="生日">
          <el-date-picker
            v-model="basicInfo.birthday"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="电话">
          <el-input v-model="basicInfo.phone" placeholder="请输入电话号码"></el-input>
        </el-form-item>

        <el-form-item label="邮箱">
          <el-input v-model="basicInfo.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>

        <el-form-item label="所在城市">
          <el-cascader
            v-model="basicInfo.location"
            :options="cityOptions"
            placeholder="请选择城市"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">账号设置</h2>
        </div>
      </template>

      <el-form :model="accountSettings" label-width="100px">
        <el-form-item label="修改密码">
          <el-button type="primary" @click="showChangePassword = true">
            修改密码
          </el-button>
        </el-form-item>

        <el-form-item label="账号绑定">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <el-icon color="#0A66C2" :size="24"><Connection /></el-icon>
              <span>LinkedIn</span>
            </div>
            <el-button 
              :type="accountSettings.linkedinBound ? 'danger' : 'primary'"
              @click="handleLinkedInBinding"
            >
              {{ accountSettings.linkedinBound ? '解除绑定' : '绑定账号' }}
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="消息通知">
          <el-switch
            v-model="accountSettings.emailNotification"
            active-text="开启邮件通知"
          />
        </el-form-item>

        <el-form-item label="账号注销">
          <el-button type="danger" @click="handleDeleteAccount">
            注销账号
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showChangePassword"
      title="修改密码"
      width="500px"
    >
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="当前密码" required>
          <el-input
            v-model="passwordForm.oldPassword"
            type="password"
            placeholder="请输入当前密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="新密码" required>
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            placeholder="请输入新密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" required>
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
          ></el-input>
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Connection } from '@element-plus/icons-vue'
import type { UploadProps } from 'element-plus'

// 基本信息
const basicInfo = reactive({
  avatar: '',
  name: '',
  gender: 'male',
  birthday: '',
  phone: '',
  email: '',
  location: []
})

// 账号设置
const accountSettings = reactive({
  linkedinBound: false,
  emailNotification: true
})

// 修改密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const showChangePassword = ref(false)

// 城市选项（示例数据）
const cityOptions = [
  {
    value: 'beijing',
    label: '北京',
    children: [
      { value: 'chaoyang', label: '朝阳区' },
      { value: 'haidian', label: '海淀区' }
    ]
  },
  {
    value: 'shanghai',
    label: '上海',
    children: [
      { value: 'pudong', label: '浦东新区' },
      { value: 'huangpu', label: '黄浦区' }
    ]
  }
]

// 头像上传
const handleAvatarSuccess: UploadProps['onSuccess'] = (response) => {
  if (response.success) {
    basicInfo.avatar = response.data.url
    ElMessage.success('头像上传成功')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (file) => {
  const isJpgOrPng = ['image/jpeg', 'image/png'].includes(file.type)
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJpgOrPng) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}

// 保存基本信息
const saveBasicInfo = async () => {
  try {
    // 这里添加保存逻辑
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 处理 LinkedIn 绑定/解绑
const handleLinkedInBinding = async () => {
  if (accountSettings.linkedinBound) {
    try {
      await ElMessageBox.confirm('确定要解除 LinkedIn 账号绑定吗？', '提示', {
        type: 'warning'
      })
      accountSettings.linkedinBound = false
      ElMessage.success('解绑成功')
    } catch {
      // 用户取消操作
    }
  } else {
    // 这里添加 LinkedIn 绑定逻辑
    accountSettings.linkedinBound = true
    ElMessage.success('绑定成功')
  }
}

// 修改密码
const handleChangePassword = async () => {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  try {
    // 这里添加修改密码逻辑
    showChangePassword.value = false
    ElMessage.success('密码修改成功')
  } catch (error) {
    ElMessage.error('密码修改失败')
  }
}

// 注销账号
const handleDeleteAccount = async () => {
  try {
    await ElMessageBox.confirm(
      '注销账号后，所有数据将被永久删除且无法恢复，是否继续？',
      '警告',
      {
        confirmButtonText: '确认注销',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    // 这里添加注销账号逻辑
    ElMessage.success('账号已注销')
  } catch {
    // 用户取消操作
  }
}
</script>

<style scoped>
.avatar-uploader {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 100px;
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
  cursor: pointer;
  overflow: hidden;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  color: #8c939d;
}
</style>