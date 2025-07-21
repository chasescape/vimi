import request from '@/config/axios'

export interface LoginData {
  username: string
  password: string
  captcha?: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  role?: 'interviewer' | 'candidate'
  inviteCode?: string
}

export const authApi = {
  // 登录
  login: (data: LoginData) => {
    return request.post('/api/auth/login', data)
  },

  // 注册
  register: (data: RegisterData) => {
    return request.post('/api/auth/register', data)
  },

  // 验证token
  verifyToken: () => {
    return request.post('/api/auth/verify-token')
  }
} 