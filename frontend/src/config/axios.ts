import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建axios实例
const request = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 15000,
    withCredentials: true,  // 允许跨域携带cookie
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
request.interceptors.request.use(
    config => {
        // 确保headers对象存在
        config.headers = config.headers || {}

        // 从localStorage获取token
        const token = localStorage.getItem('token')
        if (token) {
            // 添加token到Authorization头
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        console.error('请求错误:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器
request.interceptors.response.use(
    response => {
        return response
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // token过期或无效
                    localStorage.removeItem('token')
                    localStorage.removeItem('user')
                    ElMessage.error('登录已过期，请重新登录')
                    // 如果不是登录页面，才跳转
                    if (router.currentRoute.value.path !== '/login') {
                        router.push('/login')
                    }
                    break
                case 403:
                    ElMessage.error('没有权限访问')
                    break
                case 404:
                    ElMessage.error('请求的资源不存在')
                    break
                case 500:
                    ElMessage.error('服务器错误，请稍后重试')
                    break
                default:
                    ElMessage.error(error.response.data?.message || '请求失败')
            }
        } else if (error.code === 'ERR_NETWORK') {
            ElMessage.error('网络错误，请检查后端服务是否启动')
        } else {
            ElMessage.error('网络错误，请检查网络连接')
        }
        return Promise.reject(error)
    }
)

export default request 