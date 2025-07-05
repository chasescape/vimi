import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/Home.vue')
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
        {
            path: '/interview-result',
            name: 'interview-result',
            component: () => import('../views/InterviewResult.vue')
        }
    ]
})

export default router 