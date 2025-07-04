import api from './index'

export const aiApi = {
    // 开始面试
    startInterview: (data: any) => {
        return api.post('/interview/start', data)
    },

    // 发送面试答案
    sendAnswer: (data: any) => {
        return api.post('/interview/answer', data)
    },

    // 获取面试分析
    getAnalysis: (interviewId: string) => {
        return api.get(`/interview/analysis/${interviewId}`)
    },

    // 获取实时反馈
    getFeedback: (data: any) => {
        return api.post('/interview/feedback', data)
    }
} 