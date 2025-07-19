<template>
  <div class="animais-management">
    <div class="container">
      <h1 class="title">Gestão de Animais</h1>
      
      <!-- Estatísticas -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ stats.totalAnimais }}</div>
          <div class="stat-label">Total de Animais</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.animaisAtivos }}</div>
          <div class="stat-label">Animais Ativos</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.totalClientes }}</div>
          <div class="stat-label">Clientes com Animais</div>
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
            placeholder="Buscar por nome do animal, raça ou cliente..."
            @input="filterAnimais"
          >
          <i class="fas fa-search"></i>
        </div>
        
        <div class="filter-controls">
          <select v-model="especieFilter" @change="filterAnimais">
            <option value="">Todas as espécies</option>
            <option value="cachorro">Cachorro</option>
            <option value="gato">Gato</option>
            <option value="ave">Ave</option>
            <option value="roedor">Roedor</option>
            <option value="outro">Outro</option>
          </select>
          
          <select v-model="sortBy" @change="filterAnimais">
            <option value="nome">Ordenar por Nome</option>
            <option value="cliente">Ordenar por Cliente</option>
            <option value="data_cadastro">Ordenar por Data de Cadastro</option>
            <option value="especie">Ordenar por Espécie</option>
          </select>
        </div>
      </div>

      <!-- Lista de Animais -->
      <div class="animais-section">
        <div class="animais-header">
          <h2>Animais ({{ filteredAnimais.length }})</h2>
          <button @click="showCreateAnimalModal = true" class="btn btn-success">
            <i class="fas fa-plus"></i> Novo Animal
          </button>
        </div>
        
        <!-- Loading state -->
        <div v-if="loading" class="loading">
          Carregando animais...
        </div>
        
        <!-- Empty state -->
        <div v-else-if="filteredAnimais.length === 0" class="empty-state">
          <p>{{ searchTerm ? 'Nenhum animal encontrado para a busca.' : 'Nenhum animal cadastrado.' }}</p>
        </div>
        
        <!-- Animais grid -->
        <div v-else class="animais-grid">
          <div v-for="animal in filteredAnimais" :key="animal.id" class="animal-card">
            <div class="animal-header">
              <h3>{{ animal.nome }}</h3>
              <span class="status-badge active">
                Ativo
              </span>
            </div>
            
            <div class="animal-info">
              <p><i class="fas fa-user"></i> <strong>Cliente:</strong> {{ animal.cliente_nome }}</p>
              <p><i class="fas fa-paw"></i> <strong>Espécie:</strong> {{ animal.especie }}</p>
              <p><i class="fas fa-dna"></i> <strong>Raça:</strong> {{ animal.raca || 'Não informada' }}</p>
              <p><i class="fas fa-birthday-cake"></i> <strong>Idade:</strong> {{ animal.idade ? `${animal.idade} anos` : 'Não informada' }}</p>
              <p><i class="fas fa-weight"></i> <strong>Peso:</strong> {{ animal.peso ? `${animal.peso}kg` : 'Não informado' }}</p>
              <p><i class="fas fa-calendar"></i> <strong>Cadastrado:</strong> {{ formatDate(animal.data_cadastro) }}</p>
              <p><i class="fas fa-calendar-check"></i> <strong>Agendamentos:</strong> {{ animal.agendamentos_count || 0 }}</p>
            </div>
            
            <div class="animal-actions">
              <button @click="viewAnimal(animal)" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-eye"></i> Ver Detalhes
              </button>
              <button @click="editAnimal(animal)" class="btn btn-sm btn-outline-secondary">
                <i class="fas fa-edit"></i> Editar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Criar Animal -->
    <div v-if="showCreateAnimalModal" class="modal-overlay" @click="showCreateAnimalModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Novo Animal</h3>
          <button @click="showCreateAnimalModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="createAnimal" class="modal-body">
          <div class="form-group">
            <label>Nome do Animal:</label>
            <input v-model="newAnimal.nome" type="text" required>
          </div>
          <div class="form-group">
            <label>Cliente:</label>
            <select v-model="newAnimal.cliente_id" required>
              <option value="">Selecione um cliente</option>
              <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                {{ cliente.nome }}
              </option>
            </select>
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
            <button type="button" @click="showCreateAnimalModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-success">
              Criar Animal
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar Animal -->
    <div v-if="showEditAnimalModal" class="modal-overlay" @click="showEditAnimalModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Editar Animal</h3>
          <button @click="showEditAnimalModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="updateAnimal" class="modal-body">
          <div class="form-group">
            <label>Nome do Animal:</label>
            <input v-model="editingAnimal.nome" type="text" required>
          </div>
          <div class="form-group">
            <label>Cliente:</label>
            <select v-model="editingAnimal.cliente_id" required>
              <option value="">Selecione um cliente</option>
              <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                {{ cliente.nome }}
              </option>
            </select>
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
            <button type="button" @click="showEditAnimalModal = false" class="btn btn-secondary">
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
  name: 'AnimaisManagement',
  data() {
    return {
      animais: [],
      filteredAnimais: [],
      clientes: [],
      stats: {
        totalAnimais: 0,
        animaisAtivos: 0,
        totalClientes: 0,
        agendamentosMes: 0
      },
      loading: false,
      searchTerm: '',
      especieFilter: '',
      sortBy: 'nome',
      showCreateAnimalModal: false,
      showEditAnimalModal: false,
      newAnimal: {
        nome: '',
        cliente_id: '',
        especie: '',
        raca: '',
        data_nascimento: '',
        peso: '',
        observacoes: ''
      },
      editingAnimal: {
        id: null,
        nome: '',
        cliente_id: '',
        especie: '',
        raca: '',
        data_nascimento: '',
        peso: '',
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
          this.loadAnimais(),
          this.loadClientes(),
          this.loadStats()
        ])
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    async loadAnimais() {
      try {
        const response = await adminService.getAnimais()
        this.animais = Array.isArray(response) ? response : []
        this.filteredAnimais = [...this.animais]
      } catch (error) {
        console.error('Erro ao carregar animais:', error)
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
    async loadStats() {
      try {
        const response = await adminService.getAnimalStats()
        this.stats = response || {
          totalAnimais: this.animais.length,
          animaisAtivos: this.animais.filter(a => a.is_active).length,
          totalClientes: this.clientes.length,
          agendamentosMes: 0
        }
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
      }
    },
    filterAnimais() {
      let filtered = [...this.animais]
      
      // Filtro por busca
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase()
        filtered = filtered.filter(animal => 
          animal.nome.toLowerCase().includes(term) ||
          animal.raca?.toLowerCase().includes(term) ||
          animal.cliente_nome?.toLowerCase().includes(term)
        )
      }
      
      // Filtro por espécie
      if (this.especieFilter) {
        filtered = filtered.filter(animal => animal.especie === this.especieFilter)
      }
      
      // Ordenação
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'nome':
            return a.nome.localeCompare(b.nome)
          case 'cliente':
            return a.cliente_nome.localeCompare(b.cliente_nome)
          case 'data_cadastro':
            return new Date(b.data_cadastro) - new Date(a.data_cadastro)
          case 'especie':
            return a.especie.localeCompare(b.especie)
          default:
            return 0
        }
      })
      
      this.filteredAnimais = filtered
    },
    async createAnimal() {
      try {
        await adminService.createAnimal(this.newAnimal)
        this.showCreateAnimalModal = false
        this.resetNewAnimal()
        await this.loadData()
        this.$toast.success('Animal criado com sucesso!')
      } catch (error) {
        console.error('Erro ao criar animal:', error)
        this.$toast.error('Erro ao criar animal')
      }
    },
    editAnimal(animal) {
      this.editingAnimal = { ...animal }
      this.showEditAnimalModal = true
    },
    async updateAnimal() {
      try {
        await adminService.updateAnimal(this.editingAnimal.id, this.editingAnimal)
        this.showEditAnimalModal = false
        this.resetEditingAnimal()
        await this.loadData()
        this.$toast.success('Animal atualizado com sucesso!')
      } catch (error) {
        console.error('Erro ao atualizar animal:', error)
        this.$toast.error('Erro ao atualizar animal')
      }
    },
    viewAnimal(animal) {
      // Navegar para página de detalhes do animal
      this.$router.push(`/admin/animais/${animal.id}`)
    },
    resetNewAnimal() {
      this.newAnimal = {
        nome: '',
        cliente_id: '',
        especie: '',
        raca: '',
        data_nascimento: '',
        peso: '',
        observacoes: ''
      }
    },
    resetEditingAnimal() {
      this.editingAnimal = {
        id: null,
        nome: '',
        cliente_id: '',
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
    }
  }
}
</script>

<style scoped>
.animais-management {
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

.animais-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.animais-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.animais-header h2 {
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

.animais-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.animal-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  background: white;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.animal-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.animal-card.inactive {
  opacity: 0.7;
  background-color: #f8f9fa;
}

.animal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.animal-header h3 {
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

.animal-info {
  margin-bottom: 15px;
}

.animal-info p {
  margin: 5px 0;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;
}

.animal-info i {
  width: 16px;
  color: #007bff;
}

.animal-actions {
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