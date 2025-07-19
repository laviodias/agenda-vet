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

  // Buscar profissionais
  async getProfissionais() {
    try {
      return await apiService.get('/usuarios/profissionais/')
    } catch (error) {
      console.error('Erro ao buscar profissionais:', error)
      throw error
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

  // Buscar horários disponíveis
  async getHorariosDisponiveis(data, profissional) {
    try {
      const params = new URLSearchParams({
        data: data,
        profissional: profissional || ''
      })
      return await apiService.get(`/admin/horarios-disponiveis/?${params}`)
    } catch (error) {
      console.error('Erro ao buscar horários disponíveis:', error)
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

  // Deletar usuário
  async deleteUser(userId) {
    try {
      return await apiService.delete(`/usuarios/${userId}/deletar/`)
    } catch (error) {
      console.error('Erro ao deletar usuário:', error)
      throw error
    }
  }

  // Criar serviço
  async createServico(servicoData) {
    try {
      return await apiService.post('/admin/servicos/create/', servicoData)
    } catch (error) {
      console.error('Erro ao criar serviço:', error)
      throw error
    }
  }

  // Deletar serviço
  async deleteServico(servicoId) {
    try {
      return await apiService.delete(`/servicos/${servicoId}/deletar/`)
    } catch (error) {
      console.error('Erro ao deletar serviço:', error)
      throw error
    }
  }

  // Criar horário disponível
  async createHorarioDisponivel(horarioData) {
    try {
      return await apiService.post('/admin/horarios-disponiveis/create/', horarioData)
    } catch (error) {
      console.error('Erro ao criar horário disponível:', error)
      throw error
    }
  }

  // Deletar horário disponível
  async deleteHorarioDisponivel(horarioId) {
    try {
      return await apiService.delete(`/admin/horarios-disponiveis/${horarioId}/delete/`)
    } catch (error) {
      console.error('Erro ao deletar horário disponível:', error)
      throw error
    }
  }

  // Buscar profissionais disponíveis para um dia específico
  async getProfissionaisDisponiveis(diaSemana) {
    try {
      return await apiService.get(`/admin/profissionais/disponiveis/?dia_semana=${diaSemana}`)
    } catch (error) {
      console.error('Erro ao buscar profissionais disponíveis:', error)
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