<template>
  <div class="cliente-detalhes">
    <div class="container">
      <!-- Header com botão voltar -->
      <div class="header">
        <button @click="$router.go(-1)" class="btn btn-outline-secondary">
          <i class="fas fa-arrow-left"></i> Voltar
        </button>
        <h1>Detalhes do Cliente</h1>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="loading">
        Carregando detalhes do cliente...
      </div>

      <!-- Cliente não encontrado -->
      <div v-else-if="!cliente" class="error">
        Cliente não encontrado
      </div>

      <!-- Detalhes do cliente -->
      <div v-else class="cliente-content">
        <!-- Informações principais -->
        <div class="info-section">
          <div class="cliente-header">
            <h2>{{ cliente.nome }}</h2>
            <span :class="['status-badge', cliente.is_active ? 'active' : 'inactive']">
              {{ cliente.is_active ? 'Ativo' : 'Inativo' }}
            </span>
          </div>

          <div class="cliente-info-grid">
            <div class="info-card">
              <h3><i class="fas fa-envelope"></i> Contato</h3>
              <p><strong>Email:</strong> {{ cliente.email }}</p>
              <p><strong>Telefone:</strong> {{ cliente.telefone || 'Não informado' }}</p>
            </div>

            <div class="info-card">
              <h3><i class="fas fa-map-marker-alt"></i> Endereço</h3>
              <p>{{ cliente.endereco || 'Não informado' }}</p>
            </div>

            <div class="info-card">
              <h3><i class="fas fa-calendar"></i> Informações</h3>
              <p><strong>Cadastrado em:</strong> {{ formatDate(cliente.data_cadastro) }}</p>
              <p><strong>Total de animais:</strong> {{ cliente.animais_count || 0 }}</p>
              <p><strong>Total de agendamentos:</strong> {{ cliente.agendamentos_count || 0 }}</p>
            </div>
          </div>

          <!-- Ações -->
          <div class="actions">
            <button @click="editCliente" class="btn btn-primary">
              <i class="fas fa-edit"></i> Editar Cliente
            </button>
            <button @click="toggleStatus" :class="['btn', cliente.is_active ? 'btn-warning' : 'btn-success']">
              {{ cliente.is_active ? 'Desativar' : 'Ativar' }} Cliente
            </button>
          </div>
        </div>

        <!-- Seção de animais -->
        <div class="animais-section">
          <div class="section-header">
            <h3><i class="fas fa-paw"></i> Animais do Cliente</h3>
            <button @click="showAddAnimalModal = true" class="btn btn-success">
              <i class="fas fa-plus"></i> Adicionar Animal
            </button>
          </div>

          <!-- Loading animais -->
          <div v-if="loadingAnimais" class="loading">
            Carregando animais...
          </div>

          <!-- Lista de animais -->
          <div v-else-if="animais.length > 0" class="animais-grid">
            <div v-for="animal in animais" :key="animal.id" class="animal-card">
              <div class="animal-header">
                <h4>
                  <router-link :to="`/admin/animais/${animal.id}`" class="animal-link">
                    {{ animal.nome }}
                  </router-link>
                </h4>
                <span class="especie-badge">{{ animal.especie }}</span>
              </div>
              
              <div class="animal-info">
                <p><strong>Raça:</strong> {{ animal.raca || 'Não informada' }}</p>
                <p><strong>Idade:</strong> {{ animal.idade ? `${animal.idade} anos` : 'Não informada' }}</p>
                <p><strong>Peso:</strong> {{ animal.peso ? `${animal.peso}kg` : 'Não informado' }}</p>
                <p><strong>Agendamentos:</strong> {{ animal.agendamentos_count || 0 }}</p>
              </div>

              <div class="animal-actions">
                <button @click="editAnimal(animal)" class="btn btn-sm btn-outline-primary">
                  <i class="fas fa-edit"></i> Editar
                </button>
                <button @click="viewAnimal(animal)" class="btn btn-sm btn-outline-secondary">
                  <i class="fas fa-eye"></i> Ver Detalhes
                </button>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-else class="empty-state">
            <p>Este cliente ainda não possui animais cadastrados.</p>
          </div>
        </div>

        <!-- Seção de agendamentos -->
        <div class="agendamentos-section">
          <div class="section-header">
            <h3><i class="fas fa-calendar-check"></i> Agendamentos Recentes</h3>
          </div>

          <!-- Loading agendamentos -->
          <div v-if="loadingAgendamentos" class="loading">
            Carregando agendamentos...
          </div>

          <!-- Lista de agendamentos -->
          <div v-else-if="agendamentos.length > 0" class="agendamentos-list">
            <div v-for="agendamento in agendamentos" :key="agendamento.id" class="agendamento-card">
              <div class="agendamento-header">
                <h4>{{ agendamento.servico_nome }}</h4>
                <span :class="['status-badge', agendamento.status]">
                  {{ agendamento.status }}
                </span>
              </div>
              
              <div class="agendamento-info">
                <p><strong>Animal:</strong> {{ agendamento.animal_nome }}</p>
                <p><strong>Data:</strong> {{ formatDateTime(agendamento.data_hora) }}</p>
                <p><strong>Responsável:</strong> {{ agendamento.responsavel_nome || 'Não atribuído' }}</p>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-else class="empty-state">
            <p>Este cliente ainda não possui agendamentos.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Editar Cliente -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Editar Cliente</h3>
          <button @click="showEditModal = false" class="close-btn">&times;</button>
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
            <button type="button" @click="showEditModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Atualizar Cliente
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Adicionar Animal -->
    <div v-if="showAddAnimalModal" class="modal-overlay" @click="showAddAnimalModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Adicionar Animal</h3>
          <button @click="showAddAnimalModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="createAnimal" class="modal-body">
          <div class="form-group">
            <label>Nome do Animal:</label>
            <input v-model="newAnimal.nome" type="text" required>
          </div>
          <div class="form-group">
            <label>Espécie:</label>
            <select v-model="newAnimal.especie" required>
              <option value="">Selecione a espécie</option>
              <option value="cachorro">Cachorro</option>
              <option value="gato">Gato</option>
              <option value="ave">Ave</option>
              <option value="roedor">Roedor</option>
              <option value="outro">Outro</option>
            </select>
          </div>
          <div class="form-group">
            <label>Raça:</label>
            <input v-model="newAnimal.raca" type="text">
          </div>
          <div class="form-group">
            <label>Data de Nascimento:</label>
            <input v-model="newAnimal.data_nascimento" type="date">
          </div>
          <div class="form-group">
            <label>Peso (kg):</label>
            <input v-model="newAnimal.peso" type="number" min="0" step="0.1">
          </div>
          <div class="form-group">
            <label>Observações:</label>
            <textarea v-model="newAnimal.observacoes"></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showAddAnimalModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-success">
              Criar Animal
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
  name: 'ClienteDetalhes',
  data() {
    return {
      cliente: null,
      animais: [],
      agendamentos: [],
      loading: false,
      loadingAnimais: false,
      loadingAgendamentos: false,
      showEditModal: false,
      showAddAnimalModal: false,
      editingCliente: {
        id: null,
        nome: '',
        email: '',
        telefone: '',
        endereco: '',
        is_active: true
      },
      newAnimal: {
        nome: '',
        especie: '',
        raca: '',
        data_nascimento: '',
        peso: '',
        observacoes: ''
      }
    }
  },
  async mounted() {
    await this.loadCliente()
  },
  methods: {
    async loadCliente() {
      try {
        this.loading = true
        const clienteId = this.$route.params.id
        const response = await adminService.getCliente(clienteId)
        this.cliente = response
        
        // Carregar dados relacionados
        await Promise.all([
          this.loadAnimais(),
          this.loadAgendamentos()
        ])
      } catch (error) {
        console.error('Erro ao carregar cliente:', error)
        this.$toast.error('Erro ao carregar dados do cliente')
      } finally {
        this.loading = false
      }
    },
    async loadAnimais() {
      try {
        this.loadingAnimais = true
        const response = await adminService.getClienteAnimais(this.$route.params.id)
        this.animais = Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Erro ao carregar animais:', error)
      } finally {
        this.loadingAnimais = false
      }
    },
    async loadAgendamentos() {
      try {
        this.loadingAgendamentos = true
        const response = await adminService.getClienteAgendamentos(this.$route.params.id)
        this.agendamentos = Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Erro ao carregar agendamentos:', error)
      } finally {
        this.loadingAgendamentos = false
      }
    },
    editCliente() {
      this.editingCliente = { ...this.cliente }
      this.showEditModal = true
    },
    async updateCliente() {
      try {
        await adminService.updateCliente(this.cliente.id, this.editingCliente)
        this.showEditModal = false
        await this.loadCliente()
        this.$toast.success('Cliente atualizado com sucesso!')
      } catch (error) {
        console.error('Erro ao atualizar cliente:', error)
        this.$toast.error('Erro ao atualizar cliente')
      }
    },
    async toggleStatus() {
      try {
        await adminService.toggleClienteStatus(this.cliente.id)
        this.cliente.is_active = !this.cliente.is_active
        this.$toast.success(`Cliente ${this.cliente.is_active ? 'ativado' : 'desativado'} com sucesso!`)
      } catch (error) {
        console.error('Erro ao alterar status do cliente:', error)
        this.$toast.error('Erro ao alterar status do cliente')
      }
    },
    async createAnimal() {
      try {
        this.newAnimal.cliente_id = this.cliente.id
        await adminService.createAnimal(this.newAnimal)
        this.showAddAnimalModal = false
        this.resetNewAnimal()
        await this.loadAnimais()
        this.$toast.success('Animal criado com sucesso!')
      } catch (error) {
        console.error('Erro ao criar animal:', error)
        this.$toast.error('Erro ao criar animal')
      }
    },
    editAnimal(animal) {
      // Navegar para página de edição do animal
      this.$router.push(`/admin/animais/${animal.id}`)
    },
    viewAnimal(animal) {
      // Navegar para página de detalhes do animal
      this.$router.push(`/admin/animais/${animal.id}`)
    },
    resetNewAnimal() {
      this.newAnimal = {
        nome: '',
        especie: '',
        raca: '',
        data_nascimento: '',
        peso: '',
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
.cliente-detalhes {
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.header h1 {
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

.btn-outline-secondary {
  background: transparent;
  color: #6c757d;
  border: 1px solid #6c757d;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
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

.loading, .error, .empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
  font-style: italic;
}

.error {
  color: #dc3545;
}

.cliente-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.info-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.cliente-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.cliente-header h2 {
  margin: 0;
  color: #333;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
}

.cliente-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.info-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  background: #f8f9fa;
}

.info-card h3 {
  margin: 0 0 10px 0;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-card i {
  color: #007bff;
}

.info-card p {
  margin: 5px 0;
  color: #666;
}

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.animais-section, .agendamentos-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header i {
  color: #007bff;
}

.animais-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.animal-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  background: white;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.animal-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.animal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.animal-header h4 {
  margin: 0;
  color: #333;
}

.animal-link {
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
}

.animal-link:hover {
  text-decoration: underline;
}

.especie-badge {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
  background: #e9ecef;
  color: #495057;
}

.animal-info p {
  margin: 3px 0;
  color: #666;
  font-size: 14px;
}

.animal-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.agendamentos-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.agendamento-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  background: white;
}

.agendamento-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.agendamento-header h4 {
  margin: 0;
  color: #333;
}

.agendamento-info p {
  margin: 3px 0;
  color: #666;
  font-size: 14px;
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