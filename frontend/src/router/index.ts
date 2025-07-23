import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import { auth } from '@/utils/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            name: 'Login',
            component: () => import('@/views/auth/Login.vue')
        },
        {
            path: '/register',
            name: 'Register',
            component: () => import('@/views/auth/Register.vue')
        },
        {
            path: '/candidate',
            component: () => import('@/views/candidate/CandidateDashboard.vue'),
            redirect: '/candidate/home',
            meta: { requiresAuth: true, role: 'candidate' },
            children: [
                {
                    path: 'home',
                    name: 'CandidateHome',
                    component: () => import('@/views/candidate/Home.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'resume',
                    name: 'ResumeManager',
                    component: () => import('@/views/candidate/ResumeManager.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'search',
                    name: 'InterviewSearch',
                    component: () => import('@/views/candidate/InterviewSearch.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'schedule',
                    name: 'InterviewSchedule',
                    component: () => import('@/views/candidate/InterviewSchedule.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'history',
                    name: 'InterviewHistory',
                    component: () => import('@/views/candidate/InterviewHistory.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'test',
                    name: 'InterviewTest',
                    component: () => import('@/views/candidate/InterviewTest.vue'),
                    meta: { keepAlive: false }
                },
                {
                    path: 'profile',
                    name: 'CandidateProfile',
                    component: () => import('@/views/candidate/Profile.vue'),
                    meta: { keepAlive: true }
                }
            ]
        },
        {
            path: '/interviewer',
            component: () => import('@/views/interviewer/InterviewerDashboard.vue'),
            redirect: '/interviewer/home',
            meta: { requiresAuth: true, role: 'interviewer' },
            children: [
                {
                    path: 'home',
                    name: 'InterviewerHome',
                    component: () => import('@/views/interviewer/Home.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'schedule',
                    name: 'InterviewerSchedule',
                    component: () => import('@/views/interviewer/InterviewSchedule.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'history',
                    name: 'InterviewerHistory',
                    component: () => import('@/views/interviewer/InterviewHistory.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'create',
                    name: 'InterviewCreate',
                    component: () => import('@/views/interviewer/InterviewCreate.vue'),
                    meta: { keepAlive: false }
                },
                {
                    path: 'profile',
                    name: 'InterviewerProfile',
                    component: () => import('@/views/interviewer/Profile.vue'),
                    meta: { keepAlive: true }
                },
                {
                    path: 'interview/:id',
                    name: 'InterviewDetail',
                    component: () => import('@/views/interviewer/InterviewPage.vue'),
                    meta: { keepAlive: false }
                }
            ]
        }
    ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
    // 检查是否需要登录
    if (to.meta.requiresAuth && !auth.isLoggedIn()) {
        ElMessage.warning('请先登录')
        next('/login')
        return
    }

    // 检查角色权限
    if (to.meta.role) {
        const user = auth.getUser()
        if (user?.role !== to.meta.role) {
            ElMessage.error('无权访问该页面')
            next(auth.isCandidate() ? '/candidate/home' : '/interviewer/home')
            return
        }
    }

    // 如果已登录且访问登录页，重定向到首页
    if (to.path === '/login' && auth.isLoggedIn()) {
        next(auth.isCandidate() ? '/candidate/home' : '/interviewer/home')
        return
    }

    // 正常导航
    next()
})

export default router