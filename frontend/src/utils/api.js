import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const user = localStorage.getItem('user')
    if (user) {
      config.headers['Authorization'] = `Bearer ${JSON.parse(user).id}`
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
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 用户相关接口
export const userApi = {
  register: data => api.post('/users/register', data),
  login: data => api.post('/users/login', data),
  getUser: id => api.get(`/users/${id}`),
  updateUser: (id, data) => api.put(`/users/${id}`, data)
}

// 剧本相关接口
export const scriptApi = {
  convert: data => api.post('/scripts/convert', data),
  getScript: id => api.get(`/scripts/${id}`),
  getUserScripts: userId => api.get(`/scripts/user/${userId}`),
  deleteScript: id => api.delete(`/scripts/${id}`)
}

export default api