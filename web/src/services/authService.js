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

  // Registro de funcionário
  async register(dadosFuncionario) {
    try {
      const response = await apiService.post('/usuarios/usuarios/', dadosFuncionario)
      return response
    } catch (error) {
      if (error.response?.data?.message) {
        throw new Error(error.response.data.message)
      }
      throw error
    }
  }

  // Buscar perfil do usuário
  async getMe() {
    try {
      return await apiService.get('/usuarios/auth/me/')
    } catch (error) {
      console.error('Erro ao buscar perfil:', error)
      throw error
    }
  }

  // Buscar atendimentos do cliente
  async getAtendimentos() {
    try {
      // Usar o endpoint específico para agendamentos do cliente
      return await apiService.get('/agendamentos/listar-cliente/')
    } catch (error) {
      console.error('Erro ao buscar atendimentos:', error)
      throw error
    }
  }

  // Alias para getAtendimentos - usado no ClienteDashboard
  async getAgendamentosCliente() {
    return this.getAtendimentos()
  }

  // Buscar pets do cliente
  async getPets() {
    try {
      return await apiService.get('/animais/')
    } catch (error) {
      console.error('Erro ao buscar pets:', error)
      throw error
    }
  }

  // Criar pet
  async createPet(petData) {
    try {
      return await apiService.post('/animais/criar/', petData)
    } catch (error) {
      console.error('Erro ao criar pet:', error)
      throw error
    }
  }

  // Atualizar pet
  async updatePet(petId, petData) {
    try {
      return await apiService.put(`/animais/${petId}/`, petData)
    } catch (error) {
      console.error('Erro ao atualizar pet:', error)
      throw error
    }
  }

  // Deletar pet
  async deletePet(petId) {
    try {
      return await apiService.delete(`/animais/${petId}/deletar/`)
    } catch (error) {
      console.error('Erro ao deletar pet:', error)
      throw error
    }
  }

  // Buscar horários disponíveis
  async getHorariosDisponiveis(data) {
    try {
      return await apiService.get(`/agendamentos/horarios-disponiveis/?data=${data}`)
    } catch (error) {
      console.error('Erro ao buscar horários disponíveis:', error)
      throw error
    }
  }

  // Buscar profissionais (mantido para compatibilidade, mas retorna lista vazia)
  async getProfissionais() {
    try {
      return await apiService.get('/usuarios/profissionais/')
    } catch (error) {
      console.error('Erro ao buscar profissionais:', error)
      return []
    }
  }

  // Buscar serviços
  async getServicos() {
    try {
      return await apiService.get('/servicos/')
    } catch (error) {
      console.error('Erro ao buscar serviços:', error)
      throw error
    }
  }

  // Criar agendamento
  async createAgendamento(agendamentoData) {
    try {
      return await apiService.post('/agendamentos/criar/', agendamentoData)
    } catch (error) {
      console.error('Erro ao criar agendamento:', error)
      throw error
    }
  }

  // Cancelar agendamento
  async cancelarAgendamento(agendamentoId) {
    try {
      return await apiService.patch(`/agendamentos/${agendamentoId}/cancelar/`)
    } catch (error) {
      console.error('Erro ao cancelar agendamento:', error)
      throw error
    }
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