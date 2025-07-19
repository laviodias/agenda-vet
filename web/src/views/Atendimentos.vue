<template>
  <div class="atendimentos-page">
    <!-- Header -->
    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <div class="navbar-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fas fa-calendar-check"></i>
            </span>
            <span>{{ brandConfig?.nome_estabelecimento || 'AgendaVet' }} - Meus Atendimentos</span>
          </span>
        </div>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" @click="voltar">
            <span class="icon">
              <i class="fas fa-arrow-left"></i>
            </span>
            <span>Voltar</span>
          </a>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-4">
      <!-- Header da página -->
      <div class="welcome-section mb-6">
        <div class="columns is-vcentered">
          <div class="column">
            <h1 class="title is-2">Meus Atendimentos</h1>
            <p class="subtitle">Histórico completo de consultas e agendamentos</p>
          </div>
          <div class="column is-narrow">
            <div class="buttons">
              <button 
                class="button is-primary is-medium"
                @click="showNovoAgendamentoModal = true"
              >
                <span class="icon">
                  <i class="fas fa-calendar-plus"></i>
                </span>
                <span>Novo Agendamento</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Estatísticas -->
      <div class="stats-section mb-6">
        <div class="columns">
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
                    <p class="title is-4">{{ atendimentos.length }}</p>
                    <p class="subtitle is-6">Total de Atendimentos</p>
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
                    <p class="title is-4">{{ atendimentosFuturos.length }}</p>
                    <p class="subtitle is-6">Próximos Atendimentos</p>
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
                      <i class="fas fa-history"></i>
                    </div>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">{{ atendimentosPassados.length }}</p>
                    <p class="subtitle is-6">Atendimentos Realizados</p>
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
                    <p class="title is-4">{{ animaisUnicos.length }}</p>
                    <p class="subtitle is-6">Pets Atendidos</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters-section mb-4">
        <div class="columns is-vcentered">
          <div class="column">
            <div class="field">
              <div class="control">
                <input 
                  v-model="searchTerm" 
                  class="input" 
                  type="text" 
                  placeholder="Buscar por serviço, pet ou observações..."
                >
              </div>
            </div>
          </div>
          <div class="column is-narrow">
            <div class="field">
              <div class="control">
                <div class="select">
                  <select v-model="periodoFilter">
                    <option value="">Todos os períodos</option>
                    <option value="futuro">Próximos atendimentos</option>
                    <option value="passado">Atendimentos realizados</option>
                    <option value="hoje">Hoje</option>
                    <option value="semana">Esta semana</option>
                    <option value="mes">Este mês</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="column is-narrow">
            <div class="field">
              <div class="control">
                <div class="select">
                  <select v-model="petFilter">
                    <option value="">Todos os pets</option>
                    <option v-for="pet in pets" :key="pet.id" :value="pet.id">
                      {{ pet.nome }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="column is-narrow">
            <div class="field">
              <div class="control">
                <div class="select">
                  <select v-model="statusFilter">
                    <option value="">Todos os status</option>
                    <option value="confirmado">Confirmados</option>
                    <option value="pendente">Pendentes</option>
                    <option value="realizado">Realizados</option>
                    <option value="cancelado">Cancelados</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de Atendimentos -->
      <div class="atendimentos-section">
        <div class="table-container">
          <table class="table is-fullwidth is-striped">
            <thead>
              <tr>
                <th>Data</th>
                <th>Horário</th>
                <th>Pet</th>
                <th>Serviço</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="atendimento in filteredAtendimentos" :key="atendimento.id">
                <td>
                  <div class="date-info">
                    <span class="date">{{ formatarData(atendimento.data_hora) }}</span>
                    <span class="period" :class="getPeriodClass(atendimento.data_hora)">
                      {{ getPeriodLabel(atendimento.data_hora) }}
                    </span>
                  </div>
                </td>
                <td>{{ formatarHora(atendimento.data_hora) }}</td>
                <td>
                  <div class="pet-info">
                    <span class="pet-name">{{ atendimento.pet_nome }}</span>
                    <span class="pet-species">{{ getPetSpecies(atendimento.pet_especie) }}</span>
                  </div>
                </td>
                <td>{{ atendimento.servico_nome || atendimento.servico }}</td>
                <td>
                  <span class="tag" :class="getStatusColor(atendimento.status)">
                    {{ getStatusText(atendimento.status) }}
                  </span>
                </td>
                <td>
                  <div class="buttons are-small">
                    <button class="button action-btn view-btn" @click="visualizarAtendimento(atendimento)">
                      <span class="icon">
                        <i class="fas fa-eye"></i>
                      </span>
                    </button>
                    <button 
                      v-if="atendimento.status !== 'realizado' && atendimento.status !== 'cancelado'"
                      @click="cancelarAtendimento(atendimento)"
                      class="button action-btn cancel-btn"
                    >
                      <span class="icon">
                        <i class="fas fa-times"></i>
                      </span>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!filteredAtendimentos.length">
                <td colspan="6" class="has-text-centered">
                  <div class="empty-state">
                    <span class="icon is-large">
                      <i class="fas fa-calendar-times"></i>
                    </span>
                    <p class="mt-3">Nenhum atendimento encontrado</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Visualização de Atendimento -->
    <div v-if="showVisualizarAtendimentoModal" class="modal is-active">
      <div class="modal-background" @click="showVisualizarAtendimentoModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Detalhes do Atendimento</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="showVisualizarAtendimentoModal = false"
          ></button>
        </header>
        <section class="modal-card-body">
          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Data</label>
                <div class="control">
                  <input class="input" type="text" :value="formatarData(atendimentoSelecionado.data_hora)" readonly>
                </div>
              </div>
            </div>
            <div class="column is-6">
              <div class="field">
                <label class="label">Horário</label>
                <div class="control">
                  <input class="input" type="text" :value="formatarHora(atendimentoSelecionado.data_hora)" readonly>
                </div>
              </div>
            </div>
          </div>
          
          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Pet</label>
                <div class="control">
                  <input class="input" type="text" :value="atendimentoSelecionado.animal_nome || atendimentoSelecionado.animal" readonly>
                </div>
              </div>
            </div>
            <div class="column is-6">
              <div class="field">
                <label class="label">Serviço</label>
                <div class="control">
                  <input class="input" type="text" :value="atendimentoSelecionado.servico_nome || atendimentoSelecionado.servico" readonly>
                </div>
              </div>
            </div>
          </div>
          
          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Status</label>
                <div class="control">
                  <span class="tag" :class="getStatusColor(atendimentoSelecionado.status)">
                    {{ getStatusText(atendimentoSelecionado.status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Observações</label>
            <div class="control">
              <textarea class="textarea" :value="atendimentoSelecionado.observacoes || 'Nenhuma observação'" readonly></textarea>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button 
            v-if="atendimentoSelecionado.status !== 'realizado' && atendimentoSelecionado.status !== 'cancelado'"
            class="button is-danger" 
            @click="confirmarCancelamento"
          >
            Cancelar Atendimento
          </button>
          <button class="button" @click="showVisualizarAtendimentoModal = false">
            Fechar
          </button>
        </footer>
      </div>
    </div>

    <!-- Modal de Confirmação de Cancelamento -->
    <div v-if="showCancelarAtendimentoModal" class="modal is-active">
      <div class="modal-background" @click="showCancelarAtendimentoModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmar Cancelamento</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="showCancelarAtendimentoModal = false"
          ></button>
        </header>
        <section class="modal-card-body">
          <p>Tem certeza que deseja cancelar o atendimento para <strong>{{ atendimentoSelecionado.animal_nome || atendimentoSelecionado.animal }}</strong> em {{ formatarData(atendimentoSelecionado.data_hora) }} às {{ formatarHora(atendimentoSelecionado.data_hora) }}?</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="confirmarCancelamento">Confirmar Cancelamento</button>
          <button class="button" @click="showCancelarAtendimentoModal = false">Cancelar</button>
        </footer>
      </div>
    </div>

    <!-- Modal de Novo Agendamento -->
    <div v-if="showNovoAgendamentoModal" class="modal is-active">
      <div class="modal-background" @click="showNovoAgendamentoModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Novo Agendamento</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="showNovoAgendamentoModal = false"
          ></button>
        </header>
        <section class="modal-card-body">
          <AgendamentoForm 
            :pets="pets"
            @close="showNovoAgendamentoModal = false"
            @agendamento-criado="handleAgendamentoCriado"
          />
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBrand } from '../composables/useBrand.js'
import authService from '../services/authService.js'
import AgendamentoForm from '../components/AgendamentoForm.vue'

const router = useRouter()
const { brandConfig } = useBrand()

// Dados reativos
const atendimentos = ref([])
const pets = ref([])
const user = ref(null)
const loading = ref(false)
const error = ref(null)

// Filtros
const searchTerm = ref('')
const periodoFilter = ref('')
const petFilter = ref('')
const statusFilter = ref('')
const showVisualizarAtendimentoModal = ref(false)
const showCancelarAtendimentoModal = ref(false)
const showNovoAgendamentoModal = ref(false)
const atendimentoSelecionado = ref(null)

// Carregar dados na montagem do componente
onMounted(async () => {
  await loadData()
})

// Função para carregar todos os dados
const loadData = async () => {
  try {
    loading.value = true
    error.value = null
    
    // Carregar dados em paralelo
    const [userData, agendamentosData, petsData] = await Promise.all([
      authService.getMe(),
      authService.getAtendimentos(),
      authService.getPets()
    ])
    
    console.log('Dados carregados:', { userData, agendamentosData, petsData })
    
    // Garantir que atendimentos seja sempre um array
    atendimentos.value = Array.isArray(agendamentosData) ? agendamentosData : []
    user.value = userData
    pets.value = Array.isArray(petsData) ? petsData : []
    
  } catch (err) {
    console.error('Erro ao carregar dados:', err)
    error.value = 'Erro ao carregar dados. Tente novamente.'
    // Garantir que atendimentos seja um array mesmo em caso de erro
    atendimentos.value = []
    pets.value = []
  } finally {
    loading.value = false
  }
}

// Computed properties
const atendimentosFuturos = computed(() => {
  const hoje = new Date()
  return atendimentos.value.filter(a => new Date(a.data_hora) > hoje)
})

const atendimentosPassados = computed(() => {
  const hoje = new Date()
  return atendimentos.value.filter(a => new Date(a.data_hora) <= hoje)
})

const animaisUnicos = computed(() => {
  // Usar os pets reais da API
  return pets.value
})

const filteredAtendimentos = computed(() => {
  let filtered = [...atendimentos.value]
  
  // Filtro por busca
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    filtered = filtered.filter(atendimento => 
      atendimento.servico_nome?.toLowerCase().includes(term) ||
      atendimento.servico?.toLowerCase().includes(term) ||
      (atendimento.animal_nome && atendimento.animal_nome.toLowerCase().includes(term)) ||
      (atendimento.animal && atendimento.animal.toLowerCase().includes(term)) ||
      (atendimento.observacoes && atendimento.observacoes.toLowerCase().includes(term))
    )
  }
  
  // Filtro por período
  if (periodoFilter.value) {
    const hoje = new Date()
    const hojeInicio = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate())
    const hojeFim = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate(), 23, 59, 59)
    
    filtered = filtered.filter(atendimento => {
      const dataAtendimento = new Date(atendimento.data_hora)
      
      switch (periodoFilter.value) {
        case 'futuro':
          return dataAtendimento > hojeFim
        case 'passado':
          return dataAtendimento < hojeInicio
        case 'hoje':
          return dataAtendimento >= hojeInicio && dataAtendimento <= hojeFim
        case 'semana':
          const inicioSemana = new Date(hoje.getTime() - (hoje.getDay() * 24 * 60 * 60 * 1000))
          const fimSemana = new Date(inicioSemana.getTime() + (6 * 24 * 60 * 60 * 1000))
          return dataAtendimento >= inicioSemana && dataAtendimento <= fimSemana
        case 'mes':
          const inicioMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1)
          const fimMes = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0, 23, 59, 59)
          return dataAtendimento >= inicioMes && dataAtendimento <= fimMes
        default:
          return true
      }
    })
  }
  
  // Filtro por pet
  if (petFilter.value) {
    const pet = pets.value.find(p => p.id == petFilter.value)
    if (pet) {
      filtered = filtered.filter(atendimento => 
        (atendimento.animal_nome && atendimento.animal_nome === pet.nome) ||
        (atendimento.animal && atendimento.animal === pet.nome)
      )
    }
  }
  
  // Filtro por status
  if (statusFilter.value) {
    filtered = filtered.filter(atendimento => atendimento.status === statusFilter.value)
  }
  
  // Ordenar por data (mais recentes primeiro)
  filtered.sort((a, b) => new Date(b.data_hora) - new Date(a.data_hora))
  
  return filtered
})

// Methods
const voltar = () => {
  router.push('/cliente')
}

const visualizarAtendimento = (atendimento) => {
  atendimentoSelecionado.value = atendimento
  showVisualizarAtendimentoModal.value = true
}

const cancelarAtendimento = (atendimento) => {
  atendimentoSelecionado.value = atendimento
  showCancelarAtendimentoModal.value = true
}

const confirmarCancelamento = async () => {
  if (atendimentoSelecionado.value) {
    try {
      await authService.cancelarAgendamento(atendimentoSelecionado.value.id)
      
      // Atualizar o status localmente
      const index = atendimentos.value.findIndex(a => a.id === atendimentoSelecionado.value.id)
      if (index !== -1) {
        atendimentos.value[index].status = 'cancelado'
      }
      
      showCancelarAtendimentoModal.value = false
      atendimentoSelecionado.value = null
    } catch (err) {
      console.error('Erro ao cancelar agendamento:', err)
      error.value = 'Erro ao cancelar agendamento. Tente novamente.'
    }
  }
}

const handleAgendamentoCriado = (novoAgendamento) => {
  showNovoAgendamentoModal.value = false
  loadData() // Recarrega os dados para mostrar o novo agendamento
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
  const colors = {
    'confirmado': 'is-success',
    'pendente': 'is-warning',
    'realizado': 'is-info',
    'cancelado': 'is-danger'
  }
  return colors[status] || 'is-light'
}

const getStatusText = (status) => {
  const texts = {
    'confirmado': 'Confirmado',
    'pendente': 'Pendente',
    'realizado': 'Realizado',
    'cancelado': 'Cancelado'
  }
  return texts[status] || status
}

const getPetSpecies = (animalNome) => {
  const pet = pets.value.find(p => p.nome === animalNome)
  return pet ? pet.especie : ''
}

const getPeriodClass = (dataHora) => {
  const hoje = new Date()
  const dataAtendimento = new Date(dataHora)
  
  if (dataAtendimento > hoje) {
    return 'is-info'
  } else if (dataAtendimento.toDateString() === hoje.toDateString()) {
    return 'is-warning'
  } else {
    return 'is-light'
  }
}

const getPeriodLabel = (dataHora) => {
  const hoje = new Date()
  const dataAtendimento = new Date(dataHora)
  
  if (dataAtendimento > hoje) {
    return 'Futuro'
  } else if (dataAtendimento.toDateString() === hoje.toDateString()) {
    return 'Hoje'
  } else {
    return 'Passado'
  }
}
</script>

<style scoped>
.atendimentos-page {
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

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 1px solid #e9ecef;
}

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

.date-info {
  display: flex;
  flex-direction: column;
}

.date {
  font-weight: 600;
  color: #495057;
}

.period {
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.pet-info {
  display: flex;
  flex-direction: column;
}

.pet-name {
  font-weight: 600;
  color: #495057;
}

.pet-species {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

/* Botões de ação */
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

.buttons.are-small .action-btn {
  margin-right: 0.25rem;
}

.buttons.are-small .action-btn:last-child {
  margin-right: 0;
}

/* Tags de status */
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

.tag.is-info {
  background-color: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.tag.is-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.tag.is-light {
  background-color: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

/* Modal */
.modal-card {
  max-width: 800px;
  width: 95%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* Modal de agendamento específico */
.modal-card .agendamento-container {
  min-height: auto;
  padding: 0;
  background: transparent;
}

.modal-card .agendamento-form {
  box-shadow: none;
  padding: 0;
  background: transparent;
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

/* Botões */
.button.is-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.button.is-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.button.is-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.button.is-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

/* Campos de formulário */
.input, .textarea {
  border: 1px solid #ced4da;
  border-radius: 4px;
}

.input:focus, .textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Labels */
.label {
  color: #495057;
  font-weight: 600;
}

/* Navbar */
.navbar.is-primary {
  background-color: #007bff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

/* Cards */
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

.card .card-content {
  padding: 1.5rem;
}

.card .title {
  color: #007bff;
}

.card .subtitle {
  color: #6c757d;
}

/* Empty state */
.empty-state {
  padding: 2rem;
  text-align: center;
  color: #6c757d;
}

.empty-state .icon {
  color: #dee2e6;
  font-size: 3rem;
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