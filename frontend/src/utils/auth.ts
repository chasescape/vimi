import { ElMessage } from 'element-plus'
import router from '@/router'

export const auth = {
    // 检查是否登录
    isLoggedIn(): boolean {
        const token = localStorage.getItem('token')
        const user = localStorage.getItem('user')
        return !!token && !!user
    },

    // 获取用户信息
    getUser() {
        const user = localStorage.getItem('user')
        return user ? JSON.parse(user) : null
    },

    // 获取token
    getToken(): string | null {
        return localStorage.getItem('token')
    },

    // 登出
    logout() {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
        ElMessage.success('已退出登录')
    },

    // 检查是否是应聘者
    isCandidate(): boolean {
        const user = this.getUser()
        return user?.role === 'candidate'
    },

    // 检查是否是面试官
    isInterviewer(): boolean {
        const user = this.getUser()
        return user?.role === 'interviewer'
    }
} 