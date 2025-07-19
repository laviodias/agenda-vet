import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import authService from '../services/authService.js'

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
    component: () => import('../views/ClienteDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/perfil',
    name: 'Perfil',
    component: () => import('../views/Perfil.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/meus-pets',
    name: 'MeusPets',
    component: () => import('../views/MeusPets.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { 
      requiresAuth: true, 
      requiresAdmin: true,
      roles: ['admin', 'veterinario', 'recepcionista']
    },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/admin/Dashboard.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'funcionarios',
        name: 'Funcionarios',
        component: () => import('../views/admin/Funcionarios.vue'),
        meta: { 
          requiresAuth: true, 
          requiresAdmin: true,
          permissions: [{ resource: 'usuarios', action: 'manage' }]
        }
      },
      {
        path: 'servicos',
        name: 'Servicos',
        component: () => import('../views/admin/Servicos.vue'),
        meta: { 
          requiresAuth: true, 
          requiresAdmin: true,
          permissions: [{ resource: 'servicos', action: 'manage' }]
        }
      },
      {
        path: 'agenda',
        name: 'Agenda',
        component: () => import('../views/admin/Agenda.vue'),
        meta: { 
          requiresAuth: true, 
          requiresAdmin: true,
          permissions: [{ resource: 'agendamentos', action: 'manage' }]
        }
      },
      {
        path: 'marca',
        name: 'Marca',
        component: () => import('../views/admin/Marca.vue'),
        meta: { 
          requiresAuth: true, 
          requiresAdmin: true,
          permissions: [{ resource: 'brand', action: 'manage' }]
        }
      },
      {
        path: 'roles',
        name: 'Roles',
        component: () => import('../views/admin/Roles.vue'),
        meta: { 
          requiresAuth: true, 
          requiresAdmin: true,
          permissions: [{ resource: 'usuarios', action: 'manage' }]
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegação global
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()

  // Se a rota requer autenticação
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/auth')
  }

  // Bloquear acesso à área admin para quem não tem permissão
  if (to.path.startsWith('/admin')) {
    try {
      const response = await fetch('/api/can-access-admin/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      const data = await response.json()
      if (!data.can_access_admin) {
        alert('Acesso negado: você não tem permissão para acessar o painel administrativo.')
        return next('/cliente')
      }
    } catch (e) {
      // Se der erro, bloqueia por padrão
      alert('Acesso negado: erro ao verificar permissão.')
      return next('/cliente')
    }
  }

  // Redirecionar usuário autenticado para dashboard apropriado
  if (to.path === '/auth' && isAuthenticated) {
    return next('/cliente')
  }

  // Permitir acesso à Home (/) para todos
  next()
})

export default router 