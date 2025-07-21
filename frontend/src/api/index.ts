import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
    baseURL: '/api',
    timeout: 15000
})

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// 响应拦截器
api.interceptors.response.use(
    (response) => {
        return response.data
    },
    (error) => {
        ElMessage.error(error.response?.data?.message || '服务器错误')
        return Promise.reject(error)
    }
)

export default api 