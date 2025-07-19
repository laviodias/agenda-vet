<template>
  <div class="agendamentos-management">
    <div class="container">
      <h1 class="title">Gestão de Agendamentos</h1>
      
      <!-- Estatísticas -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ stats.totalAgendamentos }}</div>
          <div class="stat-label">Total de Agendamentos</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.agendamentosHoje }}</div>
          <div class="stat-label">Agendamentos Hoje</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.agendamentosSemana }}</div>
          <div class="stat-label">Esta Semana</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.agendamentosMes }}</div>
          <div class="stat-label">Este Mês</div>
        </div>
      </div>

      <!-- Filtros e Busca -->
      <div class="filters-section">
        <div class="search-box">
          <input 
            v-model="searchTerm" 
            type="text" 
            placeholder="Buscar por cliente, animal ou serviço..."
            @input="filterAgendamentos"
          >
          <i class="fas fa-search"></i>
        </div>
        
        <div class="filter-controls">
          <select v-model="statusFilter" @change="filterAgendamentos">
            <option value="">Todos os status</option>
            <option value="confirmado">Confirmados</option>
            <option value="pendente">Pendentes</option>
            <option value="cancelado">Cancelados</option>
            <option value="realizado">Realizados</option>
          </select>
          
          <select v-model="periodoFilter" @change="filterAgendamentos">
            <option value="">Todos os períodos</option>
            <option value="hoje">Hoje</option>
            <option value="semana">Esta Semana</option>
            <option value="mes">Este Mês</option>
            <option value="passado">Passados</option>
            <option value="futuro">Futuros</option>
          </select>
          
          <select v-model="sortBy" @change="filterAgendamentos">
            <option value="data_hora">Ordenar por Data</option>
            <option value="cliente">Ordenar por Cliente</option>
            <option value="animal">Ordenar por Animal</option>
            <option value="servico">Ordenar por Serviço</option>
          </select>
        </div>
      </div>

      <!-- Lista de Agendamentos -->
      <div class="agendamentos-section">
        <div class="agendamentos-header">
          <h2>Agendamentos ({{ filteredAgendamentos.length }})</h2>
          <button @click="showCreateAgendamentoModal = true" class="btn btn-success">
            <i class="fas fa-plus"></i> Novo Agendamento
          </button>
        </div>
        
        <!-- Loading state -->
        <div v-if="loading" class="loading">
          Carregando agendamentos...
        </div>
        
        <!-- Empty state -->
        <div v-else-if="filteredAgendamentos.length === 0" class="empty-state">
          <p>{{ searchTerm ? 'Nenhum agendamento encontrado para a busca.' : 'Nenhum agendamento cadastrado.' }}</p>
        </div>
        
        <!-- Agendamentos list -->
        <div v-else class="agendamentos-list">
          <div v-for="agendamento in filteredAgendamentos" :key="agendamento.id" class="agendamento-card">
            <div class="agendamento-header">
              <div class="agendamento-info-main">
                <h3>{{ agendamento.servico_nome }}</h3>
                <span :class="['status-badge', agendamento.status]">
                  {{ getStatusLabel(agendamento.status) }}
                </span>
              </div>
              <div class="agendamento-time">
                <i class="fas fa-clock"></i>
                {{ formatDateTime(agendamento.data_hora) }}
              </div>
            </div>
            
            <div class="agendamento-details">
              <div class="detail-row">
                <div class="detail-item">
                  <i class="fas fa-user"></i>
                  <strong>Cliente:</strong> 
                  <router-link :to="`/admin/clientes/${agendamento.cliente_id}`" class="link">
                    {{ agendamento.cliente_nome }}
                  </router-link>
                </div>
                <div class="detail-item">
                  <i class="fas fa-paw"></i>
                  <strong>Animal:</strong> 
                  <router-link :to="`/admin/animais/${agendamento.animal_id}`" class="link">
                    {{ agendamento.animal_nome }}
                  </router-link>
                </div>
              </div>
              
              <div class="detail-row">
                <div class="detail-item">
                  <i class="fas fa-calendar"></i>
                  <strong>Data:</strong> {{ formatDate(agendamento.data_hora) }}
                </div>
              </div>
              
              <div v-if="agendamento.observacoes" class="observacoes">
                <i class="fas fa-sticky-note"></i>
                <strong>Observações:</strong> {{ agendamento.observacoes }}
              </div>
            </div>
            
            <div class="agendamento-actions">
              <button @click="editAgendamento(agendamento)" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-edit"></i> Editar
              </button>
              <button @click="toggleStatus(agendamento)" :class="['btn', 'btn-sm', getStatusButtonClass(agendamento.status)]">
                {{ getStatusActionLabel(agendamento.status) }}
              </button>
              <button @click="deleteAgendamento(agendamento)" class="btn btn-sm btn-outline-danger">
                <i class="fas fa-trash"></i> Excluir
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Criar Agendamento -->
    <div v-if="showCreateAgendamentoModal" class="modal-overlay" @click="showCreateAgendamentoModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Novo Agendamento</h3>
          <button @click="showCreateAgendamentoModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="createAgendamento" class="modal-body">
          <div class="form-group">
            <label>Cliente:</label>
            <select v-model="newAgendamento.cliente_id" @change="loadClienteAnimais" required>
              <option value="">Selecione um cliente</option>
              <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                {{ cliente.nome }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Animal:</label>
            <select v-model="newAgendamento.animal_id" required>
              <option value="">Selecione um animal</option>
              <option v-for="animal in clienteAnimais" :key="animal.id" :value="animal.id">
                {{ animal.nome }} ({{ animal.especie }})
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Serviço:</label>
            <select v-model="newAgendamento.servico_id" required>
              <option value="">Selecione um serviço</option>
              <option v-for="servico in servicos" :key="servico.id" :value="servico.id">
                {{ servico.nome }}
              </option>
            </select>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Data:</label>
              <input v-model="newAgendamento.data" type="date" required>
            </div>
            <div class="form-group">
              <label>Hora:</label>
              <input v-model="newAgendamento.hora" type="time" required>
            </div>
          </div>
          
          <div class="form-group">
            <label>Observações:</label>
            <textarea v-model="newAgendamento.observacoes"></textarea>
          </div>
          
          <div class="modal-footer">
            <button type="button" @click="showCreateAgendamentoModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-success">
              Criar Agendamento
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar Agendamento -->
    <div v-if="showEditAgendamentoModal" class="modal-overlay" @click="showEditAgendamentoModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Editar Agendamento</h3>
          <button @click="showEditAgendamentoModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="updateAgendamento" class="modal-body">
          <div class="form-group">
            <label>Cliente:</label>
            <select v-model="editingAgendamento.cliente_id" @change="loadClienteAnimais" required>
              <option value="">Selecione um cliente</option>
              <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                {{ cliente.nome }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Animal:</label>
            <select v-model="editingAgendamento.animal_id" required>
              <option value="">Selecione um animal</option>
              <option v-for="animal in clienteAnimais" :key="animal.id" :value="animal.id">
                {{ animal.nome }} ({{ animal.especie }})
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Serviço:</label>
            <select v-model="editingAgendamento.servico_id" required>
              <option value="">Selecione um serviço</option>
              <option v-for="servico in servicos" :key="servico.id" :value="servico.id">
                {{ servico.nome }}
              </option>
            </select>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Data:</label>
              <input v-model="editingAgendamento.data" type="date" required>
            </div>
            <div class="form-group">
              <label>Hora:</label>
              <input v-model="editingAgendamento.hora" type="time" required>
            </div>
          </div>
          
          <div class="form-group">
            <label>Status:</label>
            <select v-model="editingAgendamento.status">
              <option value="confirmado">Confirmado</option>
              <option value="pendente">Pendente</option>
              <option value="cancelado">Cancelado</option>
              <option value="realizado">Realizado</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Observações:</label>
            <textarea v-model="editingAgendamento.observacoes"></textarea>
          </div>
          
          <div class="modal-footer">
            <button type="button" @click="showEditAgendamentoModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Atualizar Agendamento
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import adminService from '../../services/adminService'

export default {
  name: 'AgendamentosManagement',
  data() {
    return {
      agendamentos: [],
      filteredAgendamentos: [],
      clientes: [],
      servicos: [],
      clienteAnimais: [],
      stats: {
        totalAgendamentos: 0,
        agendamentosHoje: 0,
        agendamentosSemana: 0,
        agendamentosMes: 0
      },
      loading: false,
      searchTerm: '',
      statusFilter: '',
      periodoFilter: '',
      sortBy: 'data_hora',
      showCreateAgendamentoModal: false,
      showEditAgendamentoModal: false,
      newAgendamento: {
        cliente_id: '',
        animal_id: '',
        servico_id: '',
        data: '',
        hora: '',
        observacoes: ''
      },
      editingAgendamento: {
        id: null,
        cliente_id: '',
        animal_id: '',
        servico_id: '',
        data: '',
        hora: '',
        status: 'confirmado',
        observacoes: ''
      }
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        this.loading = true
        await Promise.all([
          this.loadAgendamentos(),
          this.loadClientes(),
          this.loadServicos(),
          this.loadStats()
        ])
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    async loadAgendamentos() {
      try {
        const response = await adminService.getAgendamentos()
        this.agendamentos = Array.isArray(response) ? response : []
        this.filteredAgendamentos = [...this.agendamentos]
      } catch (error) {
        console.error('Erro ao carregar agendamentos:', error)
      }
    },
    async loadClientes() {
      try {
        const response = await adminService.getClientes()
        this.clientes = Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Erro ao carregar clientes:', error)
      }
    },
    async loadServicos() {
      try {
        const response = await adminService.getServicos()
        this.servicos = Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Erro ao carregar serviços:', error)
      }
    },
    async loadStats() {
      try {
        const response = await adminService.getAgendamentoStats()
        this.stats = response || {
          totalAgendamentos: this.agendamentos.length,
          agendamentosHoje: 0,
          agendamentosSemana: 0,
          agendamentosMes: 0
        }
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
      }
    },
    async loadClienteAnimais() {
      if (!this.newAgendamento.cliente_id) {
        this.clienteAnimais = []
        return
      }
      
      try {
        const response = await adminService.getClienteAnimais(this.newAgendamento.cliente_id)
        this.clienteAnimais = Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Erro ao carregar animais do cliente:', error)
        this.clienteAnimais = []
      }
    },
    filterAgendamentos() {
      let filtered = [...this.agendamentos]
      
      // Filtro por busca
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase()
        filtered = filtered.filter(agendamento => 
          agendamento.cliente_nome.toLowerCase().includes(term) ||
          agendamento.animal_nome.toLowerCase().includes(term) ||
          agendamento.servico_nome.toLowerCase().includes(term)
        )
      }
      
      // Filtro por status
      if (this.statusFilter) {
        filtered = filtered.filter(agendamento => agendamento.status === this.statusFilter)
      }
      
      // Filtro por período
      if (this.periodoFilter) {
        const hoje = new Date()
        const hojeInicio = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate())
        const hojeFim = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate(), 23, 59, 59)
        
        filtered = filtered.filter(agendamento => {
          const dataAgendamento = new Date(agendamento.data_hora)
          
          switch (this.periodoFilter) {
            case 'hoje':
              return dataAgendamento >= hojeInicio && dataAgendamento <= hojeFim
            case 'semana':
              const semanaInicio = new Date(hoje.getTime() - (hoje.getDay() * 24 * 60 * 60 * 1000))
              const semanaFim = new Date(semanaInicio.getTime() + (6 * 24 * 60 * 60 * 1000))
              return dataAgendamento >= semanaInicio && dataAgendamento <= semanaFim
            case 'mes':
              const mesInicio = new Date(hoje.getFullYear(), hoje.getMonth(), 1)
              const mesFim = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0, 23, 59, 59)
              return dataAgendamento >= mesInicio && dataAgendamento <= mesFim
            case 'passado':
              return dataAgendamento < hojeInicio
            case 'futuro':
              return dataAgendamento > hojeFim
            default:
              return true
          }
        })
      }
      
      // Ordenação
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'data_hora':
            return new Date(a.data_hora) - new Date(b.data_hora)
          case 'cliente':
            return a.cliente_nome.localeCompare(b.cliente_nome)
          case 'animal':
            return a.animal_nome.localeCompare(b.animal_nome)
          case 'servico':
            return a.servico_nome.localeCompare(b.servico_nome)
          default:
            return 0
        }
      })
      
      this.filteredAgendamentos = filtered
    },
    async createAgendamento() {
      try {
        const dataHora = new Date(`${this.newAgendamento.data}T${this.newAgendamento.hora}`)
        const agendamentoData = {
          ...this.newAgendamento,
          data_hora: dataHora.toISOString()
        }
        
        await adminService.createAgendamento(agendamentoData)
        this.showCreateAgendamentoModal = false
        this.resetNewAgendamento()
        await this.loadData()
        this.$toast.success('Agendamento criado com sucesso!')
      } catch (error) {
        console.error('Erro ao criar agendamento:', error)
        this.$toast.error('Erro ao criar agendamento')
      }
    },
    editAgendamento(agendamento) {
      const dataHora = new Date(agendamento.data_hora)
      this.editingAgendamento = {
        id: agendamento.id,
        cliente_id: agendamento.cliente_id,
        animal_id: agendamento.animal_id,
        servico_id: agendamento.servico_id,
        data: dataHora.toISOString().split('T')[0],
        hora: dataHora.toTimeString().slice(0, 5),
        status: agendamento.status,
        observacoes: agendamento.observacoes
      }
      this.showEditAgendamentoModal = true
    },
    async updateAgendamento() {
      try {
        const dataHora = new Date(`${this.editingAgendamento.data}T${this.editingAgendamento.hora}`)
        const agendamentoData = {
          ...this.editingAgendamento,
          data_hora: dataHora.toISOString()
        }
        
        await adminService.updateAgendamento(this.editingAgendamento.id, agendamentoData)
        this.showEditAgendamentoModal = false
        this.resetEditingAgendamento()
        await this.loadData()
        this.$toast.success('Agendamento atualizado com sucesso!')
      } catch (error) {
        console.error('Erro ao atualizar agendamento:', error)
        this.$toast.error('Erro ao atualizar agendamento')
      }
    },
    async toggleStatus(agendamento) {
      try {
        const novoStatus = agendamento.status === 'confirmado' ? 'cancelado' : 'confirmado'
        await adminService.updateAgendamentoStatus(agendamento.id, novoStatus)
        
        const index = this.agendamentos.findIndex(a => a.id === agendamento.id)
        if (index !== -1) {
          this.agendamentos[index].status = novoStatus
        }
        this.filterAgendamentos()
        this.$toast.success(`Agendamento ${novoStatus === 'confirmado' ? 'confirmado' : 'cancelado'} com sucesso!`)
      } catch (error) {
        console.error('Erro ao alterar status do agendamento:', error)
        this.$toast.error('Erro ao alterar status do agendamento')
      }
    },
    async deleteAgendamento(agendamento) {
      if (!confirm('Tem certeza que deseja excluir este agendamento?')) {
        return
      }
      
      try {
        await adminService.deleteAgendamento(agendamento.id)
        const index = this.agendamentos.findIndex(a => a.id === agendamento.id)
        if (index !== -1) {
          this.agendamentos.splice(index, 1)
        }
        this.filterAgendamentos()
        this.$toast.success('Agendamento excluído com sucesso!')
      } catch (error) {
        console.error('Erro ao excluir agendamento:', error)
        this.$toast.error('Erro ao excluir agendamento')
      }
    },
    getStatusLabel(status) {
      const labels = {
        'confirmado': 'Confirmado',
        'pendente': 'Pendente',
        'cancelado': 'Cancelado',
        'realizado': 'Realizado'
      }
      return labels[status] || status
    },
    getStatusActionLabel(status) {
      const labels = {
        'confirmado': 'Cancelar',
        'pendente': 'Confirmar',
        'cancelado': 'Confirmar',
        'realizado': 'Realizado'
      }
      return labels[status] || status
    },
    getStatusButtonClass(status) {
      const classes = {
        'confirmado': 'btn-outline-warning',
        'pendente': 'btn-outline-success',
        'cancelado': 'btn-outline-success',
        'realizado': 'btn-outline-secondary'
      }
      return classes[status] || 'btn-outline-primary'
    },
    resetNewAgendamento() {
      this.newAgendamento = {
        cliente_id: '',
        animal_id: '',
        servico_id: '',
        data: '',
        hora: '',
        observacoes: ''
      }
      this.clienteAnimais = []
    },
    resetEditingAgendamento() {
      this.editingAgendamento = {
        id: null,
        cliente_id: '',
        animal_id: '',
        servico_id: '',
        data: '',
        hora: '',
        status: 'confirmado',
        observacoes: ''
      }
    },
    formatDate(date) {
      if (!date) return 'N/A'
      return new Date(date).toLocaleDateString('pt-BR')
    },
    formatDateTime(dateTime) {
      if (!dateTime) return 'N/A'
      return new Date(dateTime).toLocaleString('pt-BR')
    }
  }
}
</script>

<style scoped>
.agendamentos-management {
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  color: #333;
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #007bff;
}

.stat-label {
  color: #6c757d;
  margin-top: 5px;
}

.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-box input {
  width: 100%;
  padding: 10px 40px 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-box i {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
}

.filter-controls {
  display: flex;
  gap: 10px;
}

.filter-controls select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.agendamentos-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.agendamentos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.agendamentos-header h2 {
  margin: 0;
  color: #333;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-outline-primary {
  background: transparent;
  color: #007bff;
  border: 1px solid #007bff;
}

.btn-outline-secondary {
  background: transparent;
  color: #6c757d;
  border: 1px solid #6c757d;
}

.btn-outline-success {
  background: transparent;
  color: #28a745;
  border: 1px solid #28a745;
}

.btn-outline-warning {
  background: transparent;
  color: #ffc107;
  border: 1px solid #ffc107;
}

.btn-outline-danger {
  background: transparent;
  color: #dc3545;
  border: 1px solid #dc3545;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

.loading, .empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
  font-style: italic;
}

.agendamentos-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.agendamento-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  background: white;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.agendamento-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.agendamento-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.agendamento-info-main {
  display: flex;
  align-items: center;
  gap: 10px;
}

.agendamento-info-main h3 {
  margin: 0;
  color: #333;
}

.agendamento-time {
  color: #666;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.confirmado {
  background: var(--success-color);
  color: white;
}

.status-badge.pendente {
  color: var(--warning-color);
  border: 1px solid var(--warning-color);
}

.status-badge.cancelado {
  color: var(--danger-color);
  border: 1px solid var(--danger-color);
}

.status-badge.realizado {
  background: #e2e3e5;
  color: #383d41;
}

.agendamento-details {
  margin-bottom: 15px;
}

.detail-row {
  display: flex;
  gap: 20px;
  margin-bottom: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
  font-size: 14px;
}

.detail-item i {
  width: 16px;
  color: #007bff;
}

.link {
  color: #007bff;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.observacoes {
  margin-top: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
  color: #666;
  font-size: 14px;
  display: flex;
  align-items: flex-start;
  gap: 5px;
}

.observacoes i {
  color: #007bff;
  margin-top: 2px;
}

.agendamento-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  height: 80px;
  resize: vertical;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #dee2e6;
}
</style> 