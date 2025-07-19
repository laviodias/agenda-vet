<template>
  <div class="animal-detalhes">
    <div class="container">
      <!-- Header com botão voltar -->
      <div class="header">
        <button @click="$router.go(-1)" class="btn btn-outline-secondary">
          <i class="fas fa-arrow-left"></i> Voltar
        </button>
        <h1>Detalhes do Animal</h1>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="loading">
        Carregando detalhes do animal...
      </div>

      <!-- Animal não encontrado -->
      <div v-else-if="!animal" class="error">
        Animal não encontrado
      </div>

      <!-- Detalhes do animal -->
      <div v-else class="animal-content">
        <!-- Informações principais -->
        <div class="info-section">
          <div class="animal-header">
            <h2>{{ animal.nome }}</h2>
            <span class="especie-badge">{{ animal.especie }}</span>
          </div>

          <div class="animal-info-grid">
            <div class="info-card">
              <h3><i class="fas fa-user"></i> Proprietário</h3>
              <p><strong>Nome:</strong> {{ animal.cliente_nome }}</p>
              <p><strong>Email:</strong> {{ animal.cliente_email }}</p>
              <p><strong>Telefone:</strong> {{ animal.cliente_telefone || 'Não informado' }}</p>
              <div class="cliente-actions">
                <router-link :to="`/admin/clientes/${animal.cliente_id}`" class="btn btn-sm btn-outline-primary">
                  <i class="fas fa-eye"></i> Ver Detalhes
                </router-link>
              </div>
            </div>

            <div class="info-card">
              <h3><i class="fas fa-paw"></i> Informações</h3>
              <p><strong>Espécie:</strong> {{ animal.especie }}</p>
              <p><strong>Raça:</strong> {{ animal.raca || 'Não informada' }}</p>
              <p><strong>Data de Nascimento:</strong> {{ formatDate(animal.data_nascimento) }}</p>
              <p><strong>Idade:</strong> {{ animal.idade ? `${animal.idade} anos` : 'Não informada' }}</p>
              <p><strong>Peso:</strong> {{ animal.peso ? `${animal.peso}kg` : 'Não informado' }}</p>
            </div>

            <div class="info-card">
              <h3><i class="fas fa-calendar"></i> Estatísticas</h3>
              <p><strong>Total de Agendamentos:</strong> {{ animal.agendamentos_count || 0 }}</p>
              <p><strong>Último Agendamento:</strong> {{ animal.ultimo_agendamento ? formatDateTime(animal.ultimo_agendamento) : 'Nenhum' }}</p>
            </div>
          </div>

          <!-- Observações -->
          <div v-if="animal.observacoes" class="observacoes-section">
            <h3><i class="fas fa-sticky-note"></i> Observações</h3>
            <p>{{ animal.observacoes }}</p>
          </div>

          <!-- Ações -->
          <div class="actions">
            <button @click="editAnimal" class="btn btn-primary">
              <i class="fas fa-edit"></i> Editar Animal
            </button>
          </div>
        </div>

        <!-- Seção de agendamentos -->
        <div class="agendamentos-section">
          <div class="section-header">
            <h3><i class="fas fa-calendar-check"></i> Agendamentos do Animal</h3>
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
                <p><strong>Data:</strong> {{ formatDateTime(agendamento.data_hora) }}</p>
                <p><strong>Responsável:</strong> {{ agendamento.responsavel_nome || 'Não atribuído' }}</p>
                <p v-if="agendamento.observacoes"><strong>Observações:</strong> {{ agendamento.observacoes }}</p>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-else class="empty-state">
            <p>Este animal ainda não possui agendamentos.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Editar Animal -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Editar Animal</h3>
          <button @click="showEditModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="updateAnimal" class="modal-body">
          <div class="form-group">
            <label>Nome do Animal:</label>
            <input v-model="editingAnimal.nome" type="text" required>
          </div>
          <div class="form-group">
            <label>Espécie:</label>
            <select v-model="editingAnimal.especie" required>
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
            <input v-model="editingAnimal.raca" type="text">
          </div>
          <div class="form-group">
            <label>Data de Nascimento:</label>
            <input v-model="editingAnimal.data_nascimento" type="date">
          </div>
          <div class="form-group">
            <label>Peso (kg):</label>
            <input v-model="editingAnimal.peso" type="number" min="0" step="0.1">
          </div>
          <div class="form-group">
            <label>Observações:</label>
            <textarea v-model="editingAnimal.observacoes"></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showEditModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Atualizar Animal
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
  name: 'AnimalDetalhes',
  data() {
    return {
      animal: null,
      agendamentos: [],
      loading: false,
      loadingAgendamentos: false,
      showEditModal: false,
      editingAnimal: {
        id: null,
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
    await this.loadAnimal()
  },
  methods: {
    async loadAnimal() {
      try {
        this.loading = true
        const animalId = this.$route.params.id
        const response = await adminService.getAnimal(animalId)
        this.animal = response
        
        // Carregar agendamentos do animal
        await this.loadAgendamentos()
      } catch (error) {
        console.error('Erro ao carregar animal:', error)
        this.$toast.error('Erro ao carregar dados do animal')
      } finally {
        this.loading = false
      }
    },
    async loadAgendamentos() {
      try {
        this.loadingAgendamentos = true
        const response = await adminService.getAnimalAgendamentos(this.$route.params.id)
        this.agendamentos = Array.isArray(response) ? response : []
      } catch (error) {
        console.error('Erro ao carregar agendamentos:', error)
      } finally {
        this.loadingAgendamentos = false
      }
    },
    editAnimal() {
      this.editingAnimal = { ...this.animal }
      this.showEditModal = true
    },
    async updateAnimal() {
      try {
        await adminService.updateAnimal(this.animal.id, this.editingAnimal)
        this.showEditModal = false
        await this.loadAnimal()
        this.$toast.success('Animal atualizado com sucesso!')
      } catch (error) {
        console.error('Erro ao atualizar animal:', error)
        this.$toast.error('Erro ao atualizar animal')
      }
    },
    formatDate(date) {
      if (!date) return 'Não informada'
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
.animal-detalhes {
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

.btn-secondary {
  background: #6c757d;
  color: white;
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

.animal-content {
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

.animal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.animal-header h2 {
  margin: 0;
  color: #333;
}

.especie-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  background: #e9ecef;
  color: #495057;
  font-weight: bold;
}

.animal-info-grid {
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

.cliente-actions {
  margin-top: 10px;
  display: flex;
  gap: 5px;
}

.observacoes-section {
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.observacoes-section h3 {
  margin: 0 0 10px 0;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.observacoes-section i {
  color: #007bff;
}

.observacoes-section p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.agendamentos-section {
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
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.agendamento-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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

.status-badge {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.status-badge.confirmado {
  background: #d4edda;
  color: #155724;
}

.status-badge.pendente {
  background: #fff3cd;
  color: #856404;
}

.status-badge.cancelado {
  background: #f8d7da;
  color: #721c24;
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