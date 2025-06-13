import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('../views/Auth.vue')
  },
  {
    path: '/cliente',
    name: 'ClienteDashboard',
    component: () => import('../views/ClienteDashboard.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/admin/Dashboard.vue')
      },
      {
        path: 'funcionarios',
        name: 'Funcionarios',
        component: () => import('../views/admin/Funcionarios.vue')
      },
      {
        path: 'servicos',
        name: 'Servicos',
        component: () => import('../views/admin/Servicos.vue')
      },
      {
        path: 'agenda',
        name: 'Agenda',
        component: () => import('../views/admin/Agenda.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 