import axios from '@/config/axios'

export const authApi = {
  // 登录
  login: (data: { username: string; password: string }) => {
    return axios.post('/api/auth/login', data)
  },

  // 注册
  register: (data: {
    username: string
    email: string
    password: string
    role: 'candidate' | 'interviewer'
    inviteCode?: string  // 面试官邀请码，可选
  }) => {
    return axios.post('/api/auth/register', data)
  },

  // 获取用户信息
  getProfile: () => {
    return axios.get('/api/auth/profile')
  },

  // 发送验证码
  sendCode: (email: string) => {
    return axios.post('/api/auth/send-code', { email })
  },

  // 重置密码
  resetPassword: (data: { email: string; code: string; newPassword: string }) => {
    return axios.post('/api/auth/reset-password', data)
  }
} 