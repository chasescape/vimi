import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/AIInterview.vue')
        },
        {
            path: '/resume',
            name: 'resume',
            component: () => import('../views/ResumePage.vue')
        },
        {
            path: '/AIInterview',
            name: 'AIInterview',
            component: () => import('../views/AIInterview.vue')
        },
        // auth 文件夹路由
        {
            path: '/auth/register',
            name: 'register',
            component: () => import('../views/auth/Register.vue')
        },
        {
            path: '/auth/login',
            name: 'login',
            component: () => import('../views/auth/Login.vue')
        },
        // candidate 文件夹路由
        {
            path: '/candidate/dashboard',
            name: 'candidate-dashboard',
            component: () => import('../views/candidate/CandidateDashboard.vue'),
            children:[
                {
                    path: '/candidate/home',
                    name: 'candidate-home',
                    component: () => import('../views/candidate/Home.vue')
                },
                {
                    path: '/candidate/profile',
                    name: 'candidate-profile',
                    component: () => import('../views/candidate/Profile.vue')
                },
                {
                    path: '/candidate/interview-schedule',
                    name: 'candidate-interview-schedule',
                    component: () => import('../views/candidate/InterviewSchedule.vue')
                },
                {
                    path: '/candidate/interview-history',
                    name: 'candidate-interview-history',
                    component: () => import('../views/candidate/InterviewHistory.vue')
                },
                {
                    path: '/candidate/interview-page',
                    name: 'candidate-interview-page',
                    component: () => import('../views/candidate/InterviewPage.vue')
                },
                {
                    path: '/candidate/interview-search',
                    name: 'candidate-interview-search',
                    component: () => import('../views/candidate/InterviewSearch.vue')
                },
                {
                    path: '/candidate/interview-test',
                    name: 'candidate-interview-test',
                    component: () => import('../views/candidate/InterviewTest.vue')
                },
                {
                    path: '/candidate/interview-performance',
                    name: 'candidate-interview-performance',
                    component: () => import('../views/candidate/InterviewPerformance.vue')
                },
                {
                    path: '/candidate/interview-result',
                    name: 'candidate-interview-result',
                    component: () => import('../views/candidate/InterviewResult.vue')
                },
            ]
        },

        // interviewer 文件夹路由
        {
            path: '/interviewer/dashboard',
            name: 'interviewer-dashboard',
            component: () => import('../views/interviewer/InterviewerDashboard.vue'),
            children:[
                {
                    path: '/interviewer/home',
                    name: 'interviewer-home',
                    component: () => import('../views/interviewer/Home.vue')
                },
                {
                    path: '/interviewer/profile',
                    name: 'interviewer-profile',
                    component: () => import('../views/interviewer/Profile.vue')
                },
                {
                    path: '/interviewer/interview-create',
                    name: 'interviewer-interview-create',
                    component: () => import('../views/interviewer/InterviewCreate.vue')
                },
                {
                    path: '/interviewer/interview-schedule',
                    name: 'interviewer-interview-schedule',
                    component: () => import('../views/interviewer/InterviewSchedule.vue')
                },
                {
                    path: '/interviewer/interview-history',
                    name: 'interviewer-interview-history',
                    component: () => import('../views/interviewer/InterviewHistory.vue')
                },
                {
                    path: '/interviewer/interview-page',
                    name: 'interviewer-interview-page',
                    component: () => import('../views/interviewer/InterviewPage.vue')
                },
            ]
        },
    ]
})

export default router