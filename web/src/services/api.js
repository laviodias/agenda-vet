import axios from 'axios'

// Configuração base da API
const API_BASE_URL = 'http://localhost:8000/api'

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para adicionar token automaticamente
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para tratar respostas
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error)
    
    // Se for erro 401, limpar token e redirecionar para login
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/auth'
    }
    
    throw error
  }
)

// Classe para gerenciar requisições HTTP
class ApiService {
  // Métodos HTTP
  async get(endpoint, params = {}) {
    const response = await api.get(endpoint, { params })
    return response.data
  }

  async post(endpoint, data = {}) {
    const response = await api.post(endpoint, data)
    return response.data
  }

  async put(endpoint, data = {}) {
    const response = await api.put(endpoint, data)
    return response.data
  }

  async patch(endpoint, data = {}) {
    const response = await api.patch(endpoint, data)
    return response.data
  }

  async delete(endpoint) {
    const response = await api.delete(endpoint)
    return response.data
  }

  // Gerenciar token
  setToken(token) {
    localStorage.setItem('token', token)
  }

  removeToken() {
    localStorage.removeItem('token')
  }

  // Verificar se está autenticado
  isAuthenticated() {
    return !!localStorage.getItem('token')
  }
}

// Instância única do serviço
const apiService = new ApiService()

export default apiService 