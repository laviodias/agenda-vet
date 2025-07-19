<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AgendamentoForm from '../components/AgendamentoForm.vue'
import { useBrand } from '../composables/useBrand.js'
import authService from '../services/authService.js'

const router = useRouter()
const { brandConfig } = useBrand()

const user = ref(null)
const animais = ref([])
const agendamentos = ref([])
const loading = ref(false)
const error = ref(null)

const showAgendamentoForm = ref(false)
const showEditarPetForm = ref(false)
const showVisualizarAgendamentoModal = ref(false)
const showCancelarAgendamentoModal = ref(false)
const petSelecionado = ref(null)
const agendamentoSelecionado = ref(null)

// Carregar dados na montagem do componente
onMounted(async () => {
  await loadData()
  
  // Verificar se há um pet selecionado para agendamento na URL
  const urlParams = new URLSearchParams(window.location.search)
  const agendarPetId = urlParams.get('agendarPet')
  if (agendarPetId) {
    const pet = animais.value.find(a => a.id == agendarPetId)
    if (pet) {
      petSelecionado.value = pet
      showAgendamentoForm.value = true
    }
  }
})

// Função para carregar todos os dados
const loadData = async () => {
  try {
    loading.value = true
    error.value = null
    
    // Carregar dados do usuário e pets
    const [userData, petsData, agendamentosData] = await Promise.all([
      authService.getMe(),
      authService.getPets(),
      authService.getAgendamentosCliente()
    ])
    
    user.value = userData
    animais.value = Array.isArray(petsData) ? petsData : []
    agendamentos.value = Array.isArray(agendamentosData) ? agendamentosData : []
    
  } catch (err) {
    console.error('Erro ao carregar dados:', err)
    error.value = 'Erro ao carregar dados. Tente novamente.'
    agendamentos.value = []
    animais.value = []
  } finally {
    loading.value = false
  }
}

const logout = () => {
  authService.logout()
  router.push('/auth')
}

const visualizarAgendamento = (agendamento) => {
  agendamentoSelecionado.value = agendamento
  showVisualizarAgendamentoModal.value = true
}

const cancelarAgendamento = (agendamento) => {
  agendamentoSelecionado.value = agendamento
  showCancelarAgendamentoModal.value = true
}

const confirmarCancelamento = async () => {
  if (agendamentoSelecionado.value) {
    try {
      await authService.cancelarAgendamento(agendamentoSelecionado.value.id)
      
      // Atualizar o status localmente
      const index = agendamentos.value.findIndex(a => a.id === agendamentoSelecionado.value.id)
      if (index !== -1) {
        agendamentos.value[index].status = 'cancelado'
      }
      
      showCancelarAgendamentoModal.value = false
      agendamentoSelecionado.value = null
    } catch (err) {
      console.error('Erro ao cancelar agendamento:', err)
      error.value = 'Erro ao cancelar agendamento. Tente novamente.'
    }
  }
}

const editarPet = (animal) => {
  petSelecionado.value = { ...animal }
  showEditarPetForm.value = true
}

const agendarParaPet = (animal) => {
  petSelecionado.value = animal
  showAgendamentoForm.value = true
}

const fecharModalAgendamento = () => {
  showAgendamentoForm.value = false
  petSelecionado.value = null
}

const salvarPet = async () => {
  try {
    // Atualizar pet via API
    await authService.updatePet(petSelecionado.value.id, petSelecionado.value)
    
    // Atualizar localmente
    const index = animais.value.findIndex(a => a.id === petSelecionado.value.id)
    if (index !== -1) {
      animais.value[index] = { ...petSelecionado.value }
    }
    
    showEditarPetForm.value = false
    petSelecionado.value = null
  } catch (err) {
    console.error('Erro ao atualizar pet:', err)
    error.value = 'Erro ao atualizar pet. Tente novamente.'
  }
}

const cancelarEdicaoPet = () => {
  showEditarPetForm.value = false
  petSelecionado.value = null
}

const formatarData = (data) => {
  return new Date(data).toLocaleDateString('pt-BR')
}

const formatarHora = (dataHora) => {
  return new Date(dataHora).toLocaleTimeString('pt-BR', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const getStatusColor = (status) => {
  switch (status) {
    case 'confirmado':
      return 'is-success'
    case 'cancelado':
      return 'is-danger'
    case 'realizado':
      return 'is-info'
    default:
      return 'is-warning'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'confirmado':
      return 'Confirmado'
    case 'cancelado':
      return 'Cancelado'
    case 'realizado':
      return 'Realizado'
    default:
      return 'Pendente'
  }
}

const calcularIdade = (dataNascimento) => {
  if (!dataNascimento) return 'Idade não informada'
  
  const hoje = new Date()
  const nascimento = new Date(dataNascimento)
  const diffTime = Math.abs(hoje - nascimento)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  const anos = Math.floor(diffDays / 365)
  const meses = Math.floor((diffDays % 365) / 30)
  
  if (anos > 0) {
    return `${anos} ano${anos > 1 ? 's' : ''}${meses > 0 ? ` e ${meses} mes${meses > 1 ? 'es' : ''}` : ''}`
  } else {
    return `${meses} mes${meses > 1 ? 'es' : ''}`
  }
}

// Função para lidar com agendamento criado
const handleAgendamentoCriado = async (novoAgendamento) => {
  try {
    // Recarregar agendamentos
    const agendamentosData = await authService.getAgendamentosCliente()
    agendamentos.value = Array.isArray(agendamentosData) ? agendamentosData : []
    
    // Fechar modal
    showAgendamentoForm.value = false
    petSelecionado.value = null
  } catch (err) {
    console.error('Erro ao recarregar agendamentos:', err)
    error.value = 'Agendamento criado, mas erro ao atualizar lista.'
  }
}
</script>

<template>
  <div class="cliente-dashboard">
    <!-- Header -->
    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <div class="navbar-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fas fa-paw"></i>
            </span>
            <span>{{ brandConfig?.nome_estabelecimento || 'AgendaVet' }} - Cliente</span>
          </span>
        </div>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" @click="showAgendamentoForm = true">
            <span class="icon">
              <i class="fas fa-calendar-plus"></i>
            </span>
            <span>Novo Agendamento</span>
          </a>
        </div>

        <div class="navbar-end">
          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              <span class="icon">
                <i class="fas fa-user"></i>
              </span>
              <span>{{ user?.nome || 'Usuário' }}</span>
            </a>

            <div class="navbar-dropdown is-right">
              <a class="navbar-item" @click="router.push('/perfil')">
                <span class="icon">
                  <i class="fas fa-user-edit"></i>
                </span>
                <span>Meu Perfil</span>
              </a>
              <a class="navbar-item" @click="router.push('/meus-pets')">
                <span class="icon">
                  <i class="fas fa-paw"></i>
                </span>
                <span>Meus Pets</span>
              </a>
              <a class="navbar-item" @click="router.push('/atendimentos')">
                <span class="icon">
                  <i class="fas fa-calendar-check"></i>
                </span>
                <span>Meus Atendimentos</span>
              </a>
              <hr class="navbar-divider">
              <a class="navbar-item" @click="logout">
                <span class="icon">
                  <i class="fas fa-sign-out-alt"></i>
                </span>
                <span>Sair</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-4">
      <!-- Error state -->
      <div v-if="error" class="notification is-danger is-light mb-4">
        <button class="delete" @click="error = null"></button>
        {{ error }}
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="has-text-centered">
        <span class="icon is-large">
          <i class="fas fa-spinner fa-spin"></i>
        </span>
        <p class="mt-3">Carregando dados...</p>
      </div>

      <!-- Content -->
      <div v-else>
        <!-- Welcome Section -->
        <div class="welcome-section mb-6">
          <h1 class="title is-2">Bem-vindo, {{ user?.nome || 'Usuário' }}!</h1>
          <p class="subtitle">Gerencie seus agendamentos e pets</p>
        </div>

        <!-- Stats Cards -->
        <div class="columns mb-6">
          <div class="column">
            <div class="card">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <div class="stat-icon">
                      <i class="fas fa-calendar-check"></i>
                    </div>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">{{ agendamentos.length }}</p>
                    <p class="subtitle is-6">Agendamentos</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="column">
            <div class="card">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <div class="stat-icon">
                      <i class="fas fa-paw"></i>
                    </div>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">{{ animais.length }}</p>
                    <p class="subtitle is-6">Pets</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="column">
            <div class="card">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <div class="stat-icon">
                      <i class="fas fa-clock"></i>
                    </div>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">{{ agendamentos.filter(a => a.status === 'pendente').length }}</p>
                    <p class="subtitle is-6">Pendentes</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Próximos Agendamentos -->
        <div class="section">
          <div class="columns is-vcentered mb-4">
            <div class="column">
              <h2 class="title is-3">Próximos Agendamentos</h2>
            </div>
            <div class="column is-narrow">
              <button 
                class="button is-info"
                @click="router.push('/atendimentos')"
              >
                <span class="icon">
                  <i class="fas fa-calendar-check"></i>
                </span>
                <span>Ver Todos os Atendimentos</span>
              </button>
            </div>
          </div>
          <div class="table-container">
            <table class="table is-fullwidth is-striped">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Horário</th>
                  <th>Serviço</th>
                  <th>Pet</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="agendamento in agendamentos" :key="agendamento.id">
                  <td>{{ formatarData(agendamento.data_hora) }}</td>
                  <td>{{ formatarHora(agendamento.data_hora) }}</td>
                  <td>{{ agendamento.servico_nome || agendamento.servico }}</td>
                  <td>{{ agendamento.animal_nome || agendamento.animal }}</td>
                  <td>
                    <span class="tag" :class="getStatusColor(agendamento.status)">
                      {{ getStatusText(agendamento.status) }}
                    </span>
                  </td>
                  <td>
                    <div class="buttons are-small">
                      <button class="button action-btn view-btn" @click="visualizarAgendamento(agendamento)">
                        <span class="icon">
                          <i class="fas fa-eye"></i>
                        </span>
                      </button>
                      <button 
                        v-if="agendamento.status !== 'cancelado'"
                        @click="cancelarAgendamento(agendamento)"
                        class="button action-btn cancel-btn"
                      >
                        <span class="icon">
                          <i class="fas fa-times"></i>
                        </span>
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="!agendamentos.length">
                  <td colspan="6" class="has-text-centered">
                    Nenhum agendamento encontrado
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Meus Pets -->
        <div class="section">
          <div class="columns is-vcentered mb-4">
            <div class="column">
              <h2 class="title is-3">Meus Pets</h2>
            </div>
            <div class="column is-narrow">
              <button 
                class="button is-primary"
                @click="router.push('/meus-pets')"
              >
                <span class="icon">
                  <i class="fas fa-paw"></i>
                </span>
                <span>Gerenciar Pets</span>
              </button>
            </div>
          </div>
          <div class="columns is-multiline">
            <div 
              v-for="animal in animais" 
              :key="animal.id"
              class="column is-4"
            >
              <div class="card">
                <div class="card-content">
                  <div class="media">
                    <div class="media-left">
                      <div class="pet-avatar">
                        <i class="fas fa-paw"></i>
                      </div>
                    </div>
                    <div class="media-content">
                      <p class="title is-4">{{ animal.nome }}</p>
                      <p class="subtitle is-6">{{ animal.especie }} - {{ animal.raca || 'Raça não informada' }}</p>
                      <p class="help">{{ calcularIdade(animal.data_nascimento) }}</p>
                    </div>
                  </div>
                </div>
                <footer class="card-footer">
                  <a class="card-footer-item" @click="editarPet(animal)">
                    <span class="icon">
                      <i class="fas fa-edit"></i>
                    </span>
                    <span>Editar</span>
                  </a>
                  <a class="card-footer-item" @click="agendarParaPet(animal)">
                    <span class="icon">
                      <i class="fas fa-calendar-plus"></i>
                    </span>
                    <span>Agendar</span>
                  </a>
                </footer>
              </div>
            </div>
            <div v-if="!animais.length" class="column is-12">
              <div class="has-text-centered py-6">
                <span class="icon is-large has-text-grey-light">
                  <i class="fas fa-paw"></i>
                </span>
                <p class="mt-3 has-text-grey">Nenhum pet cadastrado</p>
                <button 
                  class="button is-primary mt-3"
                  @click="router.push('/meus-pets')"
                >
                  <span class="icon">
                    <i class="fas fa-plus"></i>
                  </span>
                  <span>Cadastrar Primeiro Pet</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Agendamento -->
    <div v-if="showAgendamentoForm" class="modal is-active">
      <div class="modal-background" @click="fecharModalAgendamento"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Novo Agendamento</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="fecharModalAgendamento"
          ></button>
        </header>
        <section class="modal-card-body">
          <AgendamentoForm 
            :pets="animais" 
            :pet-selecionado="petSelecionado"
            @agendamento-criado="handleAgendamentoCriado"
          />
        </section>
      </div>
    </div>

    <!-- Modal de Edição de Pet -->
    <div v-if="showEditarPetForm" class="modal is-active">
      <div class="modal-background" @click="cancelarEdicaoPet"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Editar Pet</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="cancelarEdicaoPet"
          ></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Nome</label>
            <div class="control">
              <input 
                class="input" 
                type="text" 
                v-model="petSelecionado.nome"
                placeholder="Nome do pet"
              >
            </div>
          </div>
          
          <div class="field">
            <label class="label">Espécie</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="petSelecionado.especie">
                  <option value="Cão">Cão</option>
                  <option value="Gato">Gato</option>
                  <option value="Ave">Ave</option>
                  <option value="Réptil">Réptil</option>
                  <option value="Outro">Outro</option>
                </select>
              </div>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Raça</label>
            <div class="control">
              <input 
                class="input" 
                type="text" 
                v-model="petSelecionado.raca"
                placeholder="Raça do pet"
              >
            </div>
          </div>
          
          <div class="field">
            <label class="label">Data de Nascimento</label>
            <div class="control">
              <input 
                class="input" 
                type="date" 
                v-model="petSelecionado.data_nascimento"
              >
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="salvarPet">Salvar</button>
          <button class="button" @click="cancelarEdicaoPet">Cancelar</button>
        </footer>
      </div>
    </div>

    <!-- Modal de Visualização de Agendamento -->
    <div v-if="showVisualizarAgendamentoModal" class="modal is-active">
      <div class="modal-background" @click="showVisualizarAgendamentoModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Visualizar Agendamento</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="showVisualizarAgendamentoModal = false"
          ></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Data</label>
            <div class="control">
              <input class="input" type="text" :value="formatarData(agendamentoSelecionado.data_hora)" readonly>
            </div>
          </div>
          <div class="field">
            <label class="label">Horário</label>
            <div class="control">
              <input class="input" type="text" :value="formatarHora(agendamentoSelecionado.data_hora)" readonly>
            </div>
          </div>
          <div class="field">
            <label class="label">Serviço</label>
            <div class="control">
              <input class="input" type="text" :value="agendamentoSelecionado.servico_nome || agendamentoSelecionado.servico" readonly>
            </div>
          </div>
          <div class="field">
            <label class="label">Pet</label>
            <div class="control">
              <input class="input" type="text" :value="agendamentoSelecionado.animal_nome || agendamentoSelecionado.animal" readonly>
            </div>
          </div>
          <div class="field">
            <label class="label">Status</label>
            <div class="control">
              <span class="tag" :class="getStatusColor(agendamentoSelecionado.status)">
                {{ getStatusText(agendamentoSelecionado.status) }}
              </span>
            </div>
          </div>
          <div class="field">
            <label class="label">Observações</label>
            <div class="control">
              <textarea class="textarea" :value="agendamentoSelecionado.observacoes || ''" readonly></textarea>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            v-if="agendamentoSelecionado.status !== 'cancelado'"
            class="button is-danger" 
            @click="confirmarCancelamento"
          >
            Cancelar Agendamento
          </button>
          <button class="button" @click="showVisualizarAgendamentoModal = false">Fechar</button>
        </footer>
      </div>
    </div>

    <!-- Modal de Confirmação de Cancelamento -->
    <div v-if="showCancelarAgendamentoModal" class="modal is-active">
      <div class="modal-background" @click="showCancelarAgendamentoModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmar Cancelamento</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="showCancelarAgendamentoModal = false"
          ></button>
        </header>
        <section class="modal-card-body">
          <p>Tem certeza que deseja cancelar o agendamento para {{ agendamentoSelecionado.animal_nome || agendamentoSelecionado.animal }} em {{ formatarData(agendamentoSelecionado.data_hora) }} às {{ formatarHora(agendamentoSelecionado.data_hora) }}?</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="confirmarCancelamento">Confirmar Cancelamento</button>
          <button class="button" @click="showCancelarAgendamentoModal = false">Cancelar</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cliente-dashboard {
  min-height: 100vh;
  background: #f8f9fa;
}

.welcome-section {
  text-align: center;
  padding: 2rem 0;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007bff, #0056b3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.pet-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #e3f2fd;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1976d2;
  font-size: 1.25rem;
}

.card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #e9ecef;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.card-footer-item {
  cursor: pointer;
  transition: background-color 0.2s;
  color: #495057;
}

.card-footer-item:hover {
  background-color: #f8f9fa;
  color: #007bff;
}

.card-footer-item:active {
  background-color: #e9ecef;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 1px solid #e9ecef;
}

.modal-card {
  max-width: 1000px;
  width: 95%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-card-body {
  max-height: 80vh;
  overflow-y: auto;
}

.modal-card-foot {
  padding: 1rem 1.5rem;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.modal-card-foot .button {
  margin-right: 0.5rem;
}

.modal-card-foot .button:last-child {
  margin-right: 0;
}

/* Melhorias nos botões */
.button.is-info {
  background-color: #17a2b8;
  border-color: #17a2b8;
}

.button.is-info:hover {
  background-color: #138496;
  border-color: #117a8b;
}

.button.is-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.button.is-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.button.is-success {
  background-color: #28a745;
  border-color: #28a745;
}

.button.is-success:hover {
  background-color: #218838;
  border-color: #1e7e34;
}

.button.is-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.button.is-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

/* Melhorias na tabela */
.table {
  background: white;
}

.table thead th {
  background: #f8f9fa;
  color: #495057;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}

/* Melhorias nos tags de status */
.tag.is-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.tag.is-warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

/* Melhorias nos campos de formulário */
.input, .select select, .textarea {
  border: 1px solid #ced4da;
  border-radius: 4px;
}

.input:focus, .select select:focus, .textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Melhorias nos labels */
.label {
  color: #495057;
  font-weight: 600;
}

/* Melhorias na navbar */
.navbar.is-primary {
  background-color: #007bff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

/* Melhorias nos cards de estatísticas */
.card .card-content {
  padding: 1.5rem;
}

.card .title {
  color: #007bff;
}

.card .subtitle {
  color: #6c757d;
}

/* Botões de ação dos agendamentos */
.action-btn {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  color: #6c757d;
  transition: all 0.2s ease;
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background-color: #e9ecef;
  border-color: #adb5bd;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-btn .icon {
  font-size: 0.875rem;
}

.view-btn .icon {
  color: #17a2b8;
}

.view-btn:hover .icon {
  color: #138496;
}

.cancel-btn .icon {
  color: #dc3545;
}

.cancel-btn:hover .icon {
  color: #c82333;
}

/* Espaçamento entre botões de ação */
.buttons.are-small .action-btn {
  margin-right: 0.25rem;
}

.buttons.are-small .action-btn:last-child {
  margin-right: 0;
}

@media (max-width: 768px) {
  .columns {
    margin: 0;
  }
  
  .column {
    padding: 0.5rem;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .modal-card-foot .button {
    margin-bottom: 0.5rem;
    width: 100%;
  }
  
  .modal-card-foot .button:last-child {
    margin-bottom: 0;
  }
}
</style> 