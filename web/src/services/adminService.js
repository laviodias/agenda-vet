import apiService from './api.js'

class AdminService {
  // ===== DASHBOARD =====
  
  // Buscar estatísticas do dashboard
  async getDashboardStats() {
    try {
      return await apiService.get('/agendamentos/dashboard/')
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error)
      // Retornar dados mockados em caso de erro
      return {
        totalAgendamentos: 45,
        agendamentosHoje: 8,
        agendamentosPendentes: 12,
        faturamentoMes: 8500.00,
        clientesAtivos: 23,
        servicosPopulares: [
          { nome: 'Consulta Veterinária', quantidade: 25 },
          { nome: 'Vacinação', quantidade: 15 },
          { nome: 'Banho e Tosa', quantidade: 10 }
        ]
      }
    }
  }

  // Buscar agendamentos recentes
  async getAgendamentosRecentes() {
    try {
      return await apiService.get('/agendamentos/recentes/')
    } catch (error) {
      console.error('Erro ao buscar agendamentos recentes:', error)
    }
  }

  // ===== AGENDAMENTOS =====
  
  // Listar todos os agendamentos
  async getAllAgendamentos(params = {}) {
    try {
      return await apiService.get('/agendamentos/listar/', params)
    } catch (error) {
      console.error('Erro ao buscar agendamentos:', error)
      throw error
    }
  }

  // Confirmar agendamento
  async confirmarAgendamento(agendamentoId) {
    try {
      return await apiService.patch(`/agendamentos/${agendamentoId}/confirmar/`)
    } catch (error) {
      console.error('Erro ao confirmar agendamento:', error)
      throw error
    }
  }

  // Cancelar agendamento
  async cancelarAgendamento(agendamentoId, motivo = '') {
    try {
      return await apiService.patch(`/agendamentos/${agendamentoId}/cancelar/`, { motivo })
    } catch (error) {
      console.error('Erro ao cancelar agendamento:', error)
      throw error
    }
  }

  // ===== SERVIÇOS =====
  
  // Listar serviços
  async getServicos() {
    try {
      return await apiService.get('/admin/servicos/')
    } catch (error) {
      console.error('Erro ao buscar serviços:', error)
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

  // Atualizar serviço
  async updateServico(servicoId, servicoData) {
    try {
      return await apiService.put(`/admin/servicos/${servicoId}/`, servicoData)
    } catch (error) {
      console.error('Erro ao atualizar serviço:', error)
      throw error
    }
  }

  // Deletar serviço
  async deleteServico(servicoId) {
    try {
      return await apiService.delete(`/admin/servicos/${servicoId}/delete/`)
    } catch (error) {
      console.error('Erro ao deletar serviço:', error)
      throw error
    }
  }

  // ===== RELATÓRIOS =====
  
  // Relatório de agendamentos por período
  async getRelatorioAgendamentos(dataInicio, dataFim) {
    try {
      return await apiService.get('/admin/relatorios/agendamentos', {
        data_inicio: dataInicio,
        data_fim: dataFim
      })
    } catch (error) {
      console.error('Erro ao buscar relatório de agendamentos:', error)
      throw error
    }
  }

  // Relatório financeiro
  async getRelatorioFinanceiro(dataInicio, dataFim) {
    try {
      return await apiService.get('/admin/relatorios/financeiro', {
        data_inicio: dataInicio,
        data_fim: dataFim
      })
    } catch (error) {
      console.error('Erro ao buscar relatório financeiro:', error)
      throw error
    }
  }

  // ===== CONFIGURAÇÕES DE MARCA =====
  
  // Buscar configuração de marca ativa
  async getBrandConfig() {
    try {
      return await apiService.get('/brand/ativa/')
    } catch (error) {
      console.error('Erro ao buscar configuração de marca:', error)
      throw error
    }
  }

  // Listar todas as configurações de marca
  async getAllBrandConfigs() {
    try {
      return await apiService.get('/brand/')
    } catch (error) {
      console.error('Erro ao buscar configurações:', error)
      throw error
    }
  }

  // Criar nova configuração de marca
  async createBrandConfig(brandData) {
    try {
      return await apiService.post('/brand/', brandData)
    } catch (error) {
      console.error('Erro ao criar configuração:', error)
      throw error
    }
  }

  // Atualizar configuração de marca
  async updateBrandConfig(id, brandData) {
    try {
      return await apiService.put(`/brand/${id}/`, brandData)
    } catch (error) {
      console.error('Erro ao atualizar configuração:', error)
      throw error
    }
  }

  // Ativar configuração de marca
  async activateBrandConfig(id) {
    try {
      return await apiService.post(`/brand/${id}/ativar/`)
    } catch (error) {
      console.error('Erro ao ativar configuração:', error)
      throw error
    }
  }

  // Deletar configuração de marca
  async deleteBrandConfig(id) {
    try {
      return await apiService.delete(`/brand/${id}/`)
    } catch (error) {
      console.error('Erro ao deletar configuração:', error)
      throw error
    }
  }

  // ===== ROLES E PERMISSÕES =====
  
  // Buscar todos os roles
  async getRoles(includeInactive = false) {
    try {
      const params = includeInactive ? { include_inactive: 'true' } : {}
      return await apiService.get('/admin/roles/', params)
    } catch (error) {
      console.error('Erro ao buscar roles:', error)
      throw error
    }
  }

  // Criar novo role
  async createRole(roleData) {
    try {
      return await apiService.post('/admin/roles/create/', roleData)
    } catch (error) {
      console.error('Erro ao criar role:', error)
      throw error
    }
  }

  // Atualizar role
  async updateRole(roleId, roleData) {
    try {
      return await apiService.put(`/admin/roles/${roleId}/`, roleData)
    } catch (error) {
      console.error('Erro ao atualizar role:', error)
      throw error
    }
  }

  // Deletar role
  async deleteRole(roleId) {
    try {
      return await apiService.delete(`/admin/roles/${roleId}/delete/`)
    } catch (error) {
      console.error('Erro ao deletar role:', error)
      throw error
    }
  }

  // Ativar/desativar role
  async toggleRoleStatus(roleId) {
    try {
      return await apiService.patch(`/admin/roles/${roleId}/toggle/`)
    } catch (error) {
      console.error('Erro ao alterar status do role:', error)
      throw error
    }
  }

  // Buscar todas as permissões
  async getPermissions() {
    try {
      return await apiService.get('/admin/permissions/')
    } catch (error) {
      console.error('Erro ao buscar permissões:', error)
      throw error
    }
  }

  // Atribuir permissões a um role
  async assignPermissions(roleId, permissions) {
    try {
      return await apiService.post(`/admin/roles/${roleId}/permissions/`, {
        permissions: permissions
      })
    } catch (error) {
      console.error('Erro ao atribuir permissões:', error)
      throw error
    }
  }

  // Buscar usuários
  async getUsers() {
    try {
      return await apiService.get('/admin/users/')
    } catch (error) {
      console.error('Erro ao buscar usuários:', error)
      throw error
    }
  }

  // Atribuir roles a um usuário
  async assignUserRoles(userId, roles) {
    try {
      return await apiService.post('/admin/users/assign-roles/', {
        user_id: userId,
        roles: roles
      })
    } catch (error) {
      console.error('Erro ao atribuir roles ao usuário:', error)
      throw error
    }
  }

  // Buscar roles de um usuário específico
  async getUserRoles(userId) {
    try {
      return await apiService.get(`/admin/users/${userId}/roles/`)
    } catch (error) {
      console.error('Erro ao buscar roles do usuário:', error)
      throw error
    }
  }

  // Buscar estatísticas de roles
  async getRoleStats() {
    try {
      return await apiService.get('/admin/roles/stats/')
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error)
      throw error
    }
  }

  // ===== CLIENTES =====
  
  // Buscar todos os clientes
  async getClientes() {
    try {
      return await apiService.get('/admin/clientes/')
    } catch (error) {
      console.error('Erro ao buscar clientes:', error)
      throw error
    }
  }

  // Criar novo cliente
  async createCliente(clienteData) {
    try {
      return await apiService.post('/admin/clientes/', clienteData)
    } catch (error) {
      console.error('Erro ao criar cliente:', error)
      throw error
    }
  }

  // Atualizar cliente
  async updateCliente(clienteId, clienteData) {
    try {
      return await apiService.put(`/admin/clientes/${clienteId}/`, clienteData)
    } catch (error) {
      console.error('Erro ao atualizar cliente:', error)
      throw error
    }
  }

  // Ativar/desativar cliente
  async toggleClienteStatus(clienteId) {
    try {
      return await apiService.patch(`/admin/clientes/${clienteId}/toggle/`)
    } catch (error) {
      console.error('Erro ao alterar status do cliente:', error)
      throw error
    }
  }

  // Buscar estatísticas de clientes
  async getClienteStats() {
    try {
      return await apiService.get('/admin/clientes/stats/')
    } catch (error) {
      console.error('Erro ao buscar estatísticas de clientes:', error)
      throw error
    }
  }

  // Buscar cliente específico
  async getCliente(clienteId) {
    try {
      return await apiService.get(`/admin/clientes/${clienteId}/detail/`)
    } catch (error) {
      console.error('Erro ao buscar cliente:', error)
      throw error
    }
  }

  // Buscar animais de um cliente
  async getClienteAnimais(clienteId) {
    try {
      return await apiService.get(`/admin/clientes/${clienteId}/animais/`)
    } catch (error) {
      console.error('Erro ao buscar animais do cliente:', error)
      throw error
    }
  }

  // Buscar agendamentos de um cliente
  async getClienteAgendamentos(clienteId) {
    try {
      return await apiService.get(`/admin/clientes/${clienteId}/agendamentos/`)
    } catch (error) {
      console.error('Erro ao buscar agendamentos do cliente:', error)
      throw error
    }
  }

  // ===== ANIMAIS =====
  
  // Buscar todos os animais
  async getAnimais() {
    try {
      return await apiService.get('/admin/animais/')
    } catch (error) {
      console.error('Erro ao buscar animais:', error)
      throw error
    }
  }

  // Criar novo animal
  async createAnimal(animalData) {
    try {
      return await apiService.post('/admin/animais/create/', animalData)
    } catch (error) {
      console.error('Erro ao criar animal:', error)
      throw error
    }
  }

  // Atualizar animal
  async updateAnimal(animalId, animalData) {
    try {
      return await apiService.put(`/admin/animais/${animalId}/`, animalData)
    } catch (error) {
      console.error('Erro ao atualizar animal:', error)
      throw error
    }
  }



  // Buscar estatísticas de animais
  async getAnimalStats() {
    try {
      return await apiService.get('/admin/animais/stats/')
    } catch (error) {
      console.error('Erro ao buscar estatísticas de animais:', error)
      throw error
    }
  }

  // Buscar animal específico
  async getAnimal(animalId) {
    try {
      return await apiService.get(`/admin/animais/${animalId}/detail/`)
    } catch (error) {
      console.error('Erro ao buscar animal:', error)
      throw error
    }
  }

  // Buscar agendamentos de um animal
  async getAnimalAgendamentos(animalId) {
    try {
      return await apiService.get(`/admin/animais/${animalId}/agendamentos/`)
    } catch (error) {
      console.error('Erro ao buscar agendamentos do animal:', error)
      throw error
    }
  }

  // ===== AGENDAMENTOS =====
  
  // Buscar todos os agendamentos
  async getAgendamentos() {
    try {
      return await apiService.get('/admin/agendamentos/')
    } catch (error) {
      console.error('Erro ao buscar agendamentos:', error)
      throw error
    }
  }

  // Criar novo agendamento
  async createAgendamento(agendamentoData) {
    try {
      return await apiService.post('/admin/agendamentos/create/', agendamentoData)
    } catch (error) {
      console.error('Erro ao criar agendamento:', error)
      throw error
    }
  }

  // Atualizar agendamento
  async updateAgendamento(agendamentoId, agendamentoData) {
    try {
      return await apiService.put(`/admin/agendamentos/${agendamentoId}/`, agendamentoData)
    } catch (error) {
      console.error('Erro ao atualizar agendamento:', error)
      throw error
    }
  }

  // Atualizar status do agendamento
  async updateAgendamentoStatus(agendamentoId, status) {
    try {
      return await apiService.patch(`/admin/agendamentos/${agendamentoId}/status/`, { status })
    } catch (error) {
      console.error('Erro ao atualizar status do agendamento:', error)
      throw error
    }
  }

  // Excluir agendamento
  async deleteAgendamento(agendamentoId) {
    try {
      return await apiService.delete(`/admin/agendamentos/${agendamentoId}/delete/`)
    } catch (error) {
      console.error('Erro ao excluir agendamento:', error)
      throw error
    }
  }

  // Buscar estatísticas de agendamentos
  async getAgendamentoStats() {
    try {
      return await apiService.get('/admin/agendamentos/stats/')
    } catch (error) {
      console.error('Erro ao buscar estatísticas de agendamentos:', error)
      throw error
    }
  }

  // Buscar serviços
  async getServicos() {
    try {
      return await apiService.get('/admin/servicos/')
    } catch (error) {
      console.error('Erro ao buscar serviços:', error)
      throw error
    }
  }

  // ===== USUÁRIOS =====
  
  // Deletar usuário
  async deleteUser(userId) {
    try {
      return await apiService.delete(`/usuarios/${userId}/deletar/`)
    } catch (error) {
      console.error('Erro ao deletar usuário:', error)
      throw error
    }
  }

  // ===== SERVIÇOS ADMIN =====
  
  // Criar serviço (admin)
  async createServico(servicoData) {
    try {
      return await apiService.post('/admin/servicos/create/', servicoData)
    } catch (error) {
      console.error('Erro ao criar serviço:', error)
      throw error
    }
  }

  // Deletar serviço (admin)
  async deleteServico(servicoId) {
    try {
      return await apiService.delete(`/servicos/${servicoId}/deletar/`)
    } catch (error) {
      console.error('Erro ao deletar serviço:', error)
      throw error
    }
  }
}

export default new AdminService() 