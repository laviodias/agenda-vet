import apiService from './api.js'

class AuthService {
  // Login
  async login(email, senha) {
    try {
      const response = await apiService.post('/auth/login/', {
        email,
        senha
      })
      
      if (response.token) {
        apiService.setToken(response.token)
        return response
      }
      
      throw new Error('Token não recebido')
    } catch (error) {
      if (error.response?.data?.message) {
        throw new Error(error.response.data.message)
      }
      throw error
    }
  }

  // Registro de cliente
  async registerCliente(dadosCliente) {
    try {
      const response = await apiService.post('/auth/register/cliente/', dadosCliente)
      
      if (response.token) {
        apiService.setToken(response.token)
      }
      
      return response
    } catch (error) {
      if (error.response?.data?.message) {
        throw new Error(error.response.data.message)
      }
      throw error
    }
  }

  // Logout
  logout() {
    apiService.removeToken()
    localStorage.removeItem('user')
  }

  // Verificar se está autenticado
  isAuthenticated() {
    return apiService.isAuthenticated()
  }

  // Obter dados do usuário atual
  getCurrentUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  }

  // Salvar dados do usuário
  setCurrentUser(user) {
    localStorage.setItem('user', JSON.stringify(user))
  }

  // Verificar se é admin
  isAdmin() {
    const user = this.getCurrentUser()
    return user && user.tipo === 'admin'
  }

  // Verificar se é cliente
  isCliente() {
    const user = this.getCurrentUser()
    return user && user.tipo === 'cliente'
  }
}

export default new AuthService() 