<script setup>
import { ref, onMounted } from 'vue'
import CalendarioSemanalAdmin from '../../components/CalendarioSemanalAdmin.vue'
import adminService from '../../services/adminService.js'

// Dados do dashboard
const agendamentos = ref([])
const estatisticas = ref({
  totalAgendamentos: 0,
  agendamentosHoje: 0,
  agendamentosPendentes: 0,
  faturamentoMes: 0,
  clientesAtivos: 0
})
const agendamentosRecentes = ref([])
const servicosPopulares = ref([])

// Estados de loading
const loading = ref(true)
const loadingStats = ref(true)
const loadingAgendamentos = ref(true)

const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor)
}

const formatarData = (dataString) => {
  return new Date(dataString).toLocaleDateString('pt-BR')
}

const formatarHora = (dataString) => {
  return new Date(dataString).toLocaleTimeString('pt-BR', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const carregarDados = async () => {
  try {
    loading.value = true
    
    const [statsData, agendamentosData, agendamentosRecentesData] = await Promise.all([
      adminService.getDashboardStats(),
      adminService.getAllAgendamentos(),
      adminService.getAgendamentosRecentes()
    ])

    estatisticas.value = {
      totalAgendamentos: statsData.totalAgendamentos,
      agendamentosHoje: statsData.agendamentosHoje,
      agendamentosPendentes: statsData.agendamentosPendentes,
      faturamentoMes: statsData.faturamentoMes,
      clientesAtivos: statsData.clientesAtivos
    }

    agendamentos.value = Array.isArray(agendamentosData) ? agendamentosData : []
    agendamentosRecentes.value = Array.isArray(agendamentosRecentesData) ? agendamentosRecentesData : []
    servicosPopulares.value = Array.isArray(statsData.servicosPopulares) ? statsData.servicosPopulares : []

  } catch (error) {
    console.error('Erro ao carregar dados do dashboard:', error)
    agendamentos.value = []
    agendamentosRecentes.value = []
    servicosPopulares.value = []
    estatisticas.value = {
      totalAgendamentos: 0,
      agendamentosHoje: 0,
      agendamentosPendentes: 0,
      faturamentoMes: 0,
      clientesAtivos: 0
    }
  } finally {
    loading.value = false
    loadingStats.value = false
    loadingAgendamentos.value = false
  }
}

const confirmarAgendamento = async (agendamentoId) => {
  try {
    await adminService.confirmarAgendamento(agendamentoId)
    // Recarregar dados após confirmação
    await carregarDados()
  } catch (error) {
    console.error('Erro ao confirmar agendamento:', error)
  }
}

const cancelarAgendamento = async (agendamentoId) => {
  try {
    await adminService.cancelarAgendamento(agendamentoId)
    // Recarregar dados após cancelamento
    await carregarDados()
  } catch (error) {
    console.error('Erro ao cancelar agendamento:', error)
  }
}

onMounted(() => {
  carregarDados()
})
</script>

<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1 class="title is-2">Dashboard Administrativo</h1>
      <p class="subtitle">Visão geral das consultas e estatísticas da clínica</p>
    </div>

    <!-- Loading geral -->
    <div v-if="loading" class="has-text-centered">
      <div class="loader"></div>
      <p class="mt-3">Carregando dashboard...</p>
    </div>

    <div v-else>
      <!-- Estatísticas -->
      <div class="stats-grid mb-6">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-calendar-check"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ estatisticas.totalAgendamentos }}</div>
            <div class="stat-label">Total de Agendamentos</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-calendar-day"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ estatisticas.agendamentosHoje }}</div>
            <div class="stat-label">Agendamentos Hoje</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-dollar-sign"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatarMoeda(estatisticas.faturamentoMes) }}</div>
            <div class="stat-label">Faturamento do Mês</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ estatisticas.agendamentosPendentes }}</div>
            <div class="stat-label">Agendamentos Pendentes</div>
          </div>
        </div>
      </div>

      <!-- Serviços Populares -->
      <div v-if="servicosPopulares.length > 0" class="section mb-6">
        <div class="section-header">
          <h2 class="title is-3">Serviços Mais Populares</h2>
          <p class="subtitle">Serviços mais solicitados pelos clientes</p>
        </div>
        
        <div class="columns is-multiline">
          <div 
            v-for="servico in servicosPopulares.slice(0, 3)" 
            :key="servico.nome"
            class="column is-4"
          >
            <div class="card">
              <div class="card-content has-text-centered">
                <div class="service-icon mb-3">
                  <i class="fas fa-stethoscope" style="font-size: 2rem; color: #3273dc;"></i>
                </div>
                <h3 class="title is-5">{{ servico.nome }}</h3>
                <p class="has-text-grey">{{ servico.quantidade }} agendamentos</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Calendário Semanal -->
      <div class="calendar-section">
        <div class="section-header">
          <h2 class="title is-3">Agenda Semanal</h2>
          <p class="subtitle">Visualize todas as consultas agendadas para a semana</p>
        </div>
        
        <div v-if="loadingAgendamentos" class="has-text-centered">
          <div class="loader"></div>
          <p class="mt-3">Carregando agenda...</p>
        </div>
        
        <CalendarioSemanalAdmin v-else :agendamentos="agendamentos" />
      </div>

      <!-- Agendamentos Recentes -->
      <div class="upcoming-appointments mt-6">
        <div class="section-header">
          <h2 class="title is-3">Agendamentos Recentes</h2>
          <p class="subtitle">Últimos agendamentos realizados</p>
        </div>
        
        <div v-if="loadingAgendamentos" class="has-text-centered">
          <div class="loader"></div>
          <p class="mt-3">Carregando agendamentos...</p>
        </div>
        
        <div v-else class="appointments-list">
          <div 
            v-for="agendamento in agendamentosRecentes.slice(0, 5)" 
            :key="agendamento.id"
            class="appointment-item"
          >
            <div class="appointment-time">
              <div class="time">{{ formatarHora(agendamento.data_hora) }}</div>
              <div class="date">{{ formatarData(agendamento.data_hora) }}</div>
            </div>
            
            <div class="appointment-info">
              <div class="appointment-main">
                <strong>{{ agendamento.servico }}</strong>
                <span class="price">{{ formatarMoeda(agendamento.preco) }}</span>
              </div>
              
              <div class="appointment-details">
                <span class="animal">
                  <i class="fas fa-paw"></i>
                  {{ agendamento.pet_nome }} 
                  ({{ agendamento.pet_especie || 'N/A' }})
                </span>
                <span class="client">
                  <i class="fas fa-user"></i>
                  {{ agendamento.cliente }}
                </span>
              </div>
              
              <div v-if="agendamento.observacoes" class="appointment-notes">
                <i class="fas fa-sticky-note"></i>
                {{ agendamento.observacoes }}
              </div>
              
              <div class="status-badge" :class="agendamento.status">
                {{ agendamento.status }}
              </div>
            </div>
            
            <div class="appointment-actions">
              <button 
                v-if="agendamento.status === 'pendente'"
                @click="confirmarAgendamento(agendamento.id)"
                class="button is-small is-success"
                title="Confirmar"
              >
                <span class="icon">
                  <i class="fas fa-check"></i>
                </span>
              </button>
              <button 
                v-if="agendamento.status !== 'cancelado'"
                @click="cancelarAgendamento(agendamento.id)"
                class="button is-small is-danger"
                title="Cancelar"
              >
                <span class="icon">
                  <i class="fas fa-times"></i>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 1rem;
}

.dashboard-header {
  margin-bottom: 2rem;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3273dc, #209cee);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: bold;
  color: #3273dc;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: #666;
  font-size: 0.875rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.calendar-section {
  margin-bottom: 2rem;
}

.appointments-list {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.appointment-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}

.appointment-item:last-child {
  border-bottom: none;
}

.appointment-item:hover {
  background: #f8f9fa;
}

.appointment-time {
  min-width: 80px;
  text-align: center;
  margin-right: 1rem;
}

.appointment-time .time {
  font-size: 1.25rem;
  font-weight: bold;
  color: #3273dc;
}

.appointment-time .date {
  font-size: 0.875rem;
  color: #666;
}

.appointment-info {
  flex: 1;
  margin-right: 1rem;
}

.appointment-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.appointment-main strong {
  color: #1b5e20;
  font-size: 1.1rem;
}

.price {
  color: #3273dc;
  font-weight: bold;
}

.appointment-details {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.appointment-details span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.appointment-details i {
  color: #999;
  width: 12px;
}

.appointment-notes {
  font-size: 0.8rem;
  color: #666;
  font-style: italic;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.appointment-notes i {
  color: #999;
  width: 12px;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  margin-top: 0.5rem;
}

.status-badge.confirmado {
  background-color: var(--success-color);
  color: white;
}

.status-badge.pendente {
  background-color: var(--warning-color);
  color: #333;
}

.status-badge.cancelado {
  background-color: var(--danger-color);
  color: white;
}

.appointment-actions {
  display: flex;
  gap: 0.5rem;
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3273dc;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .appointment-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .appointment-time {
    min-width: auto;
    text-align: left;
    margin-right: 0;
  }
  
  .appointment-details {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style> 