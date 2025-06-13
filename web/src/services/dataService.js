import apiService from './api.js'

class DataService {
  // ===== PETS =====
  
  // Listar pets do cliente
  async getPets() {
    return await apiService.get('/pets')
  }

  // Criar novo pet
  async createPet(petData) {
    return await apiService.post('/pets', petData)
  }

  // Atualizar pet
  async updatePet(petId, petData) {
    return await apiService.put(`/pets/${petId}`, petData)
  }

  // Deletar pet
  async deletePet(petId) {
    return await apiService.delete(`/pets/${petId}`)
  }

  // ===== AGENDAMENTOS =====
  
  // Listar agendamentos do cliente
  async getAgendamentos() {
    return await apiService.get('/agendamentos')
  }

  // Listar todos os agendamentos (admin)
  async getAllAgendamentos() {
    return await apiService.get('/admin/agendamentos')
  }

  // Criar agendamento
  async createAgendamento(agendamentoData) {
    return await apiService.post('/agendamentos', agendamentoData)
  }

  // Atualizar agendamento
  async updateAgendamento(agendamentoId, agendamentoData) {
    return await apiService.put(`/agendamentos/${agendamentoId}`, agendamentoData)
  }

  // Cancelar agendamento
  async cancelAgendamento(agendamentoId) {
    return await apiService.patch(`/agendamentos/${agendamentoId}/cancelar`)
  }

  // Confirmar agendamento (admin)
  async confirmAgendamento(agendamentoId) {
    return await apiService.patch(`/admin/agendamentos/${agendamentoId}/confirmar`)
  }

  // ===== SERVIÇOS =====
  
  // Listar serviços disponíveis
  async getServicos() {
    return await apiService.get('/servicos')
  }

  // Criar serviço (admin)
  async createServico(servicoData) {
    return await apiService.post('/admin/servicos', servicoData)
  }

  // Atualizar serviço (admin)
  async updateServico(servicoId, servicoData) {
    return await apiService.put(`/admin/servicos/${servicoId}`, servicoData)
  }

  // Deletar serviço (admin)
  async deleteServico(servicoId) {
    return await apiService.delete(`/admin/servicos/${servicoId}`)
  }

  // ===== PROFISSIONAIS =====
  
  // Listar profissionais
  async getProfissionais() {
    return await apiService.get('/profissionais')
  }

  // Criar profissional (admin)
  async createProfissional(profissionalData) {
    return await apiService.post('/admin/profissionais', profissionalData)
  }

  // Atualizar profissional (admin)
  async updateProfissional(profissionalId, profissionalData) {
    return await apiService.put(`/admin/profissionais/${profissionalId}`, profissionalData)
  }

  // Deletar profissional (admin)
  async deleteProfissional(profissionalId) {
    return await apiService.delete(`/admin/profissionais/${profissionalId}`)
  }

  // ===== HORÁRIOS DISPONÍVEIS =====
  
  // Buscar horários disponíveis
  async getHorariosDisponiveis(data, servicoId, profissionalId = null) {
    const params = new URLSearchParams({
      data,
      servico_id: servicoId
    })
    
    if (profissionalId) {
      params.append('profissional_id', profissionalId)
    }
    
    return await apiService.get(`/horarios-disponiveis?${params}`)
  }

  // ===== RELATÓRIOS (ADMIN) =====
  
  // Relatório de agendamentos por período
  async getRelatorioAgendamentos(dataInicio, dataFim) {
    const params = new URLSearchParams({
      data_inicio: dataInicio,
      data_fim: dataFim
    })
    
    return await apiService.get(`/admin/relatorios/agendamentos?${params}`)
  }

  // Relatório financeiro
  async getRelatorioFinanceiro(dataInicio, dataFim) {
    const params = new URLSearchParams({
      data_inicio: dataInicio,
      data_fim: dataFim
    })
    
    return await apiService.get(`/admin/relatorios/financeiro?${params}`)
  }
}

export default new DataService() 