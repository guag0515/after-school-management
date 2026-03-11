import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
      return Promise.reject(error.response.data)
    }
    return Promise.reject(error)
  }
)

// 认证相关
const authApi = {
  login: (data) => api.post('/auth/login', data)
}

// 学生管理
const studentApi = {
  getList: (params) => api.get('/students', { params }),
  getById: (id) => api.get(`/students/${id}`),
  create: (data) => api.post('/students', data),
  update: (id, data) => api.put(`/students/${id}`, data),
  delete: (id) => api.delete(`/students/${id}`),
  createParent: (data) => api.post('/students/parent', data)
}

// 考勤管理
const attendanceApi = {
  getList: (params) => api.get('/attendance', { params }),
  getById: (id) => api.get(`/attendance/${id}`),
  create: (data) => api.post('/attendance', data),
  update: (id, data) => api.put(`/attendance/${id}`, data),
  delete: (id) => api.delete(`/attendance/${id}`)
}

// 作业管理
const homeworkApi = {
  getList: (params) => api.get('/homework', { params }),
  getById: (id) => api.get(`/homework/${id}`),
  create: (data) => api.post('/homework', data),
  update: (id, data) => api.put(`/homework/${id}`, data),
  delete: (id) => api.delete(`/homework/${id}`)
}

// 成绩管理
const scoreApi = {
  getList: (params) => api.get('/scores', { params }),
  getById: (id) => api.get(`/scores/${id}`),
  create: (data) => api.post('/scores', data),
  update: (id, data) => api.put(`/scores/${id}`, data),
  delete: (id) => api.delete(`/scores/${id}`)
}

// 餐饮管理
const mealApi = {
  getList: (params) => api.get('/meals', { params }),
  getById: (id) => api.get(`/meals/${id}`),
  create: (data) => api.post('/meals', data),
  update: (id, data) => api.put(`/meals/${id}`, data),
  delete: (id) => api.delete(`/meals/${id}`)
}

// AI分析
const aiAnalysisApi = {
  getList: (params) => api.get('/ai-analysis', { params }),
  getById: (id) => api.get(`/ai-analysis/${id}`),
  create: (data) => api.post('/ai-analysis', data),
  delete: (id) => api.delete(`/ai-analysis/${id}`),
  generate: (data) => api.post('/ai-analysis/analyze', data)
}

export {
  authApi,
  studentApi,
  attendanceApi,
  homeworkApi,
  scoreApi,
  mealApi,
  aiAnalysisApi
}
