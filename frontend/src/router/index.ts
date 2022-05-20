import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'root',
        component: () => import('../components/Root.vue'),
    },
    {
        path: '/project/:project_id',
        name: 'project',
        component: () => import('../components/Project.vue'),
    },


]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})