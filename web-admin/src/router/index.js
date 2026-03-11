import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/students'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/students',
    name: 'Students',
    component: () => import('../views/Students.vue')
  },
  {
    path: '/attendance',
    name: 'Attendance',
    component: () => import('../views/Attendance.vue')
  },
  {
    path: '/homework',
    name: 'Homework',
    component: () => import('../views/Homework.vue')
  },
  {
    path: '/scores',
    name: 'Scores',
    component: () => import('../views/Scores.vue')
  },
  {
    path: '/meals',
    name: 'Meals',
    component: () => import('../views/Meals.vue')
  },
  {
    path: '/ai-analysis',
    name: 'AIAnalysis',
    component: () => import('../views/AIAnalysis.vue')
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('../views/Statistics.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
