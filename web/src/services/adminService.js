import apiService from './api.js'

class AdminService {
  // ===== DASHBOARD =====
  
  // Buscar estatísticas do dashboard
  async getDashboardStats() {
    try {
      return await apiService.get('/admin/dashboard/stats')
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
      return await apiService.get('/admin/agendamentos/recentes')
    } catch (error) {
      console.error('Erro ao buscar agendamentos recentes:', error)
      // Retornar dados mockados em caso de erro
      return [
        {
          id: 1,
          data: '2025-08-15',
          horario: '14:00',
          cliente: 'João Silva',
          pet: 'Rex',
          servico: 'Consulta Veterinária',
          profissional: 'Dr. João Silva',
          status: 'confirmado',
          preco: 80.00
        },
        {
          id: 2,
          data: '2025-08-15',
          horario: '15:30',
          cliente: 'Maria Santos',
          pet: 'Luna',
          servico: 'Vacinação',
          profissional: 'Dra. Maria Santos',
          status: 'pendente',
          preco: 60.00
        },
        {
          id: 3,
          data: '2025-08-16',
          horario: '09:00',
          cliente: 'Pedro Costa',
          pet: 'Thor',
          servico: 'Banho e Tosa',
          profissional: 'Dr. Pedro Costa',
          status: 'confirmado',
          preco: 50.00
        }
      ]
    }
  }

  // ===== AGENDAMENTOS =====
  
  // Listar todos os agendamentos
  async getAllAgendamentos(params = {}) {
    try {
      return await apiService.get('/admin/agendamentos', params)
    } catch (error) {
      console.error('Erro ao buscar agendamentos:', error)
      throw error
    }
  }

  // Confirmar agendamento
  async confirmarAgendamento(agendamentoId) {
    try {
      return await apiService.patch(`/admin/agendamentos/${agendamentoId}/confirmar`)
    } catch (error) {
      console.error('Erro ao confirmar agendamento:', error)
      throw error
    }
  }

  // Cancelar agendamento
  async cancelarAgendamento(agendamentoId, motivo = '') {
    try {
      return await apiService.patch(`/admin/agendamentos/${agendamentoId}/cancelar`, { motivo })
    } catch (error) {
      console.error('Erro ao cancelar agendamento:', error)
      throw error
    }
  }

  // ===== SERVIÇOS =====
  
  // Listar serviços
  async getServicos() {
    try {
      return await apiService.get('/admin/servicos')
    } catch (error) {
      console.error('Erro ao buscar serviços:', error)
      throw error
    }
  }

  // Criar serviço
  async createServico(servicoData) {
    try {
      return await apiService.post('/admin/servicos', servicoData)
    } catch (error) {
      console.error('Erro ao criar serviço:', error)
      throw error
    }
  }

  // Atualizar serviço
  async updateServico(servicoId, servicoData) {
    try {
      return await apiService.put(`/admin/servicos/${servicoId}`, servicoData)
    } catch (error) {
      console.error('Erro ao atualizar serviço:', error)
      throw error
    }
  }

  // Deletar serviço
  async deleteServico(servicoId) {
    try {
      return await apiService.delete(`/admin/servicos/${servicoId}`)
    } catch (error) {
      console.error('Erro ao deletar serviço:', error)
      throw error
    }
  }

  // ===== PROFISSIONAIS =====
  
  // Listar profissionais
  async getProfissionais() {
    try {
      return await apiService.get('/admin/profissionais')
    } catch (error) {
      console.error('Erro ao buscar profissionais:', error)
      throw error
    }
  }

  // Criar profissional
  async createProfissional(profissionalData) {
    try {
      return await apiService.post('/admin/profissionais', profissionalData)
    } catch (error) {
      console.error('Erro ao criar profissional:', error)
      throw error
    }
  }

  // Atualizar profissional
  async updateProfissional(profissionalId, profissionalData) {
    try {
      return await apiService.put(`/admin/profissionais/${profissionalId}`, profissionalData)
    } catch (error) {
      console.error('Erro ao atualizar profissional:', error)
      throw error
    }
  }

  // Deletar profissional
  async deleteProfissional(profissionalId) {
    try {
      return await apiService.delete(`/admin/profissionais/${profissionalId}`)
    } catch (error) {
      console.error('Erro ao deletar profissional:', error)
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
}

export default new AdminService() 