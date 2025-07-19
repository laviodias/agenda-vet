<template>
  <div class="clientes-management">
    <div class="container">
      <h1 class="title">Gestão de Clientes</h1>
      
      <!-- Estatísticas -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ stats.totalClientes }}</div>
          <div class="stat-label">Total de Clientes</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.clientesAtivos }}</div>
          <div class="stat-label">Clientes Ativos</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.totalAnimais }}</div>
          <div class="stat-label">Total de Animais</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.agendamentosMes }}</div>
          <div class="stat-label">Agendamentos este Mês</div>
        </div>
      </div>

      <!-- Filtros e Busca -->
      <div class="filters-section">
        <div class="search-box">
          <input 
            v-model="searchTerm" 
            type="text" 
            placeholder="Buscar por nome, email ou telefone..."
            @input="filterClientes"
          >
          <i class="fas fa-search"></i>
        </div>
        
        <div class="filter-controls">
          <select v-model="statusFilter" @change="filterClientes">
            <option value="">Todos os status</option>
            <option value="ativo">Ativos</option>
            <option value="inativo">Inativos</option>
          </select>
          
          <select v-model="sortBy" @change="filterClientes">
            <option value="nome">Ordenar por Nome</option>
            <option value="data_cadastro">Ordenar por Data de Cadastro</option>
            <option value="ultimo_agendamento">Ordenar por Último Agendamento</option>
          </select>
        </div>
      </div>

      <!-- Lista de Clientes -->
      <div class="clientes-section">
        <div class="clientes-header">
          <h2>Clientes ({{ filteredClientes.length }})</h2>
          <button @click="showCreateClienteModal = true" class="btn btn-success">
            <i class="fas fa-plus"></i> Novo Cliente
          </button>
        </div>
        
        <!-- Loading state -->
        <div v-if="loading" class="loading">
          Carregando clientes...
        </div>
        
        <!-- Empty state -->
        <div v-else-if="filteredClientes.length === 0" class="empty-state">
          <p>{{ searchTerm ? 'Nenhum cliente encontrado para a busca.' : 'Nenhum cliente cadastrado.' }}</p>
        </div>
        
        <!-- Clientes grid -->
        <div v-else class="clientes-grid">
          <div v-for="cliente in filteredClientes" :key="cliente.id" class="cliente-card">
            <div class="cliente-header">
              <h3>{{ cliente.nome }}</h3>
              <span :class="['status-badge', cliente.is_active ? 'ativo' : 'inativo']">
                {{ cliente.is_active ? 'Ativo' : 'Inativo' }}
              </span>
            </div>
            
            <div class="cliente-info">
              <p><i class="fas fa-envelope"></i> {{ cliente.email }}</p>
              <p><i class="fas fa-phone"></i> {{ cliente.telefone || 'Não informado' }}</p>
              <p><i class="fas fa-calendar"></i> Cadastrado em: {{ formatDate(cliente.data_cadastro) }}</p>
              <p><i class="fas fa-paw"></i> {{ cliente.animais_count || 0 }} animais</p>
              <p><i class="fas fa-calendar-check"></i> {{ cliente.agendamentos_count || 0 }} agendamentos</p>
            </div>
            
            <div class="cliente-actions">
              <button @click="viewCliente(cliente)" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-eye"></i> Ver Detalhes
              </button>
              <button @click="editCliente(cliente)" class="btn btn-sm btn-outline-secondary">
                <i class="fas fa-edit"></i> Editar
              </button>
              <button @click="toggleClienteStatus(cliente)" :class="['btn', 'btn-sm', cliente.is_active ? 'btn-outline-warning' : 'btn-outline-success']">
                {{ cliente.is_active ? 'Desativar' : 'Ativar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Criar Cliente -->
    <div v-if="showCreateClienteModal" class="modal-overlay" @click="showCreateClienteModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Novo Cliente</h3>
          <button @click="showCreateClienteModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="createCliente" class="modal-body">
          <div class="form-group">
            <label>Nome Completo:</label>
            <input v-model="newCliente.nome" type="text" required>
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input v-model="newCliente.email" type="email" required>
          </div>
          <div class="form-group">
            <label>Telefone:</label>
            <input v-model="newCliente.telefone" type="tel">
          </div>
          <div class="form-group">
            <label>Endereço:</label>
            <textarea v-model="newCliente.endereco"></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showCreateClienteModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-success">
              Criar Cliente
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar Cliente -->
    <div v-if="showEditClienteModal" class="modal-overlay" @click="showEditClienteModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Editar Cliente</h3>
          <button @click="showEditClienteModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="updateCliente" class="modal-body">
          <div class="form-group">
            <label>Nome Completo:</label>
            <input v-model="editingCliente.nome" type="text" required>
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input v-model="editingCliente.email" type="email" required>
          </div>
          <div class="form-group">
            <label>Telefone:</label>
            <input v-model="editingCliente.telefone" type="tel">
          </div>
          <div class="form-group">
            <label>Endereço:</label>
            <textarea v-model="editingCliente.endereco"></textarea>
          </div>
          <div class="form-group">
            <label>Status:</label>
            <select v-model="editingCliente.is_active">
              <option :value="true">Ativo</option>
              <option :value="false">Inativo</option>
            </select>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showEditClienteModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Atualizar Cliente
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
  name: 'ClientesManagement',
  data() {
    return {
      clientes: [],
      filteredClientes: [],
      stats: {
        totalClientes: 0,
        clientesAtivos: 0,
        totalAnimais: 0,
        agendamentosMes: 0
      },
      loading: false,
      searchTerm: '',
      statusFilter: '',
      sortBy: 'nome',
      showCreateClienteModal: false,
      showEditClienteModal: false,
      newCliente: {
        nome: '',
        email: '',
        telefone: '',
        endereco: ''
      },
      editingCliente: {
        id: null,
        nome: '',
        email: '',
        telefone: '',
        endereco: '',
        is_active: true
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
          this.loadClientes(),
          this.loadStats()
        ])
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    async loadClientes() {
      try {
        const response = await adminService.getClientes()
        this.clientes = Array.isArray(response) ? response : []
        this.filteredClientes = [...this.clientes]
      } catch (error) {
        console.error('Erro ao carregar clientes:', error)
      }
    },
    async loadStats() {
      try {
        const response = await adminService.getClienteStats()
        this.stats = response || {
          totalClientes: this.clientes.length,
          clientesAtivos: this.clientes.filter(c => c.is_active).length,
          totalAnimais: 0,
          agendamentosMes: 0
        }
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
      }
    },
    filterClientes() {
      let filtered = [...this.clientes]
      
      // Filtro por busca
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase()
        filtered = filtered.filter(cliente => 
          cliente.nome.toLowerCase().includes(term) ||
          cliente.email.toLowerCase().includes(term) ||
          (cliente.telefone && cliente.telefone.includes(term))
        )
      }
      
      // Filtro por status
      if (this.statusFilter) {
        filtered = filtered.filter(cliente => 
          this.statusFilter === 'ativo' ? cliente.is_active : !cliente.is_active
        )
      }
      
      // Ordenação
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'nome':
            return a.nome.localeCompare(b.nome)
          case 'data_cadastro':
            return new Date(b.data_cadastro) - new Date(a.data_cadastro)
          case 'ultimo_agendamento':
            return new Date(b.ultimo_agendamento || 0) - new Date(a.ultimo_agendamento || 0)
          default:
            return 0
        }
      })
      
      this.filteredClientes = filtered
    },
    async createCliente() {
      try {
        await adminService.createCliente(this.newCliente)
        this.showCreateClienteModal = false
        this.resetNewCliente()
        await this.loadData()
        this.$toast.success('Cliente criado com sucesso!')
      } catch (error) {
        console.error('Erro ao criar cliente:', error)
        this.$toast.error('Erro ao criar cliente')
      }
    },
    editCliente(cliente) {
      this.editingCliente = { ...cliente }
      this.showEditClienteModal = true
    },
    async updateCliente() {
      try {
        await adminService.updateCliente(this.editingCliente.id, this.editingCliente)
        this.showEditClienteModal = false
        this.resetEditingCliente()
        await this.loadData()
        this.$toast.success('Cliente atualizado com sucesso!')
      } catch (error) {
        console.error('Erro ao atualizar cliente:', error)
        this.$toast.error('Erro ao atualizar cliente')
      }
    },
    async toggleClienteStatus(cliente) {
      try {
        await adminService.toggleClienteStatus(cliente.id)
        const index = this.clientes.findIndex(c => c.id === cliente.id)
        if (index !== -1) {
          this.clientes[index].is_active = !this.clientes[index].is_active
        }
        this.filterClientes()
        this.$toast.success(`Cliente ${cliente.is_active ? 'desativado' : 'ativado'} com sucesso!`)
      } catch (error) {
        console.error('Erro ao alterar status do cliente:', error)
        this.$toast.error('Erro ao alterar status do cliente')
      }
    },
    viewCliente(cliente) {
      // Navegar para página de detalhes do cliente
      this.$router.push(`/admin/clientes/${cliente.id}`)
    },
    resetNewCliente() {
      this.newCliente = {
        nome: '',
        email: '',
        telefone: '',
        endereco: ''
      }
    },
    resetEditingCliente() {
      this.editingCliente = {
        id: null,
        nome: '',
        email: '',
        telefone: '',
        endereco: '',
        is_active: true
      }
    },
    formatDate(date) {
      if (!date) return 'N/A'
      return new Date(date).toLocaleDateString('pt-BR')
    }
  }
}
</script>

<style scoped>
.clientes-management {
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

.clientes-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.clientes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.clientes-header h2 {
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

.btn-outline-warning {
  background: transparent;
  color: #ffc107;
  border: 1px solid #ffc107;
}

.btn-outline-success {
  background: transparent;
  color: #28a745;
  border: 1px solid #28a745;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

.clientes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.cliente-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  background: white;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.cliente-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.cliente-card.inactive {
  opacity: 0.7;
  background-color: #f8f9fa;
}

.cliente-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.cliente-header h3 {
  margin: 0;
  color: #333;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.ativo {
  background: var(--success-color);
  color: white;
}

.status-badge.inativo {
  color: var(--warning-color);
  border: 1px solid var(--warning-color);
}

.status-badge.ativo {
  color: var(--success-color);
  border: 1px solid var(--success-color);
}

.cliente-info {
  margin-bottom: 15px;
}

.cliente-info p {
  margin: 5px 0;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;
}

.cliente-info i {
  width: 16px;
  color: #007bff;
}

.cliente-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.loading, .empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
  font-style: italic;
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