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

  // Obter dados do usuário atual
  getCurrentUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  }

  // Salvar usuário no localStorage
  setCurrentUser(user) {
    localStorage.setItem('user', JSON.stringify(user))
  }

  // Remover usuário do localStorage
  removeCurrentUser() {
    localStorage.removeItem('user')
  }

  // Verificar se está autenticado
  isAuthenticated() {
    return !!localStorage.getItem('token')
  }

  // Logout
  logout() {
    this.removeToken()
    this.removeCurrentUser()
  }

  // Gerenciar token
  setToken(token) {
    localStorage.setItem('token', token)
  }

  removeToken() {
    localStorage.removeItem('token')
  }
}

export default new AuthService() 