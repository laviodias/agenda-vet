<script setup>
import { ref, onMounted } from 'vue'
import AdminWeeklyCalendar from '../../components/AdminWeeklyCalendar.vue'

// Dados mockados até integrar com o backend
const agendamentos = ref([
  {
    id: 1,
    data_hora: '2025-06-20T09:00:00',
    servico: {
      nome: 'Consulta Clínica',
      preco: 150.00
    },
    responsavel: {
      nome: 'Dr. João Silva'
    },
    animal: {
      nome: 'Rex',
      especie: 'Cão'
    },
    cliente: {
      nome: 'Maria Santos'
    },
    observacoes: 'Primeira consulta, checkup completo'
  },
  {
    id: 2,
    data_hora: '2025-06-20T14:00:00',
    servico: {
      nome: 'Banho e Tosa',
      preco: 80.00
    },
    responsavel: {
      nome: 'Dra. Ana Costa'
    },
    animal: {
      nome: 'Luna',
      especie: 'Gato'
    },
    cliente: {
      nome: 'Carlos Oliveira'
    },
    observacoes: 'Tosa higiênica'
  },
  {
    id: 3,
    data_hora: '2025-06-21T10:30:00',
    servico: {
      nome: 'Vacinação',
      preco: 120.00
    },
    responsavel: {
      nome: 'Dr. João Silva'
    },
    animal: {
      nome: 'Thor',
      especie: 'Cão'
    },
    cliente: {
      nome: 'Fernanda Lima'
    },
    observacoes: 'Vacina V10'
  },
  {
    id: 4,
    data_hora: '2025-06-22T16:00:00',
    servico: {
      nome: 'Consulta Dermatológica',
      preco: 200.00
    },
    responsavel: {
      nome: 'Dra. Maria Santos'
    },
    animal: {
      nome: 'Mia',
      especie: 'Gato'
    },
    cliente: {
      nome: 'Roberto Silva'
    },
    observacoes: 'Alergia na pele'
  },
  {
    id: 5,
    data_hora: '2025-06-23T11:00:00',
    servico: {
      nome: 'Exame de Sangue',
      preco: 180.00
    },
    responsavel: {
      nome: 'Dr. João Silva'
    },
    animal: {
      nome: 'Bella',
      especie: 'Cão'
    },
    cliente: {
      nome: 'Patrícia Costa'
    },
    observacoes: 'Checkup anual'
  }
])

const estatisticas = ref({
  totalConsultas: 0,
  consultasHoje: 0,
  faturamentoEstimado: 0,
  consultasPendentes: 0
})

const calcularEstatisticas = () => {
  const hoje = new Date().toISOString().split('T')[0]
  
  estatisticas.value = {
    totalConsultas: agendamentos.value.length,
    consultasHoje: agendamentos.value.filter(a => 
      a.data_hora.startsWith(hoje)
    ).length,
    faturamentoEstimado: agendamentos.value.reduce((total, a) => 
      total + parseFloat(a.servico.preco), 0
    ),
    consultasPendentes: agendamentos.value.filter(a => 
      new Date(a.data_hora) > new Date()
    ).length
  }
}

const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor)
}

onMounted(() => {
  calcularEstatisticas()
})
</script>

<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1 class="title is-2">Dashboard Administrativo</h1>
      <p class="subtitle">Visão geral das consultas e estatísticas da clínica</p>
    </div>

    <div class="stats-grid mb-6">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-calendar-check"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ estatisticas.totalConsultas }}</div>
          <div class="stat-label">Total de Consultas</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-calendar-day"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ estatisticas.consultasHoje }}</div>
          <div class="stat-label">Consultas Hoje</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-dollar-sign"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ formatarMoeda(estatisticas.faturamentoEstimado) }}</div>
          <div class="stat-label">Faturamento Estimado</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-clock"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ estatisticas.consultasPendentes }}</div>
          <div class="stat-label">Consultas Pendentes</div>
        </div>
      </div>
    </div>

    <div class="calendar-section">
      <div class="section-header">
        <h2 class="title is-3">Agenda Semanal</h2>
        <p class="subtitle">Visualize todas as consultas agendadas para a semana</p>
      </div>
      
      <AdminWeeklyCalendar :agendamentos="agendamentos" />
    </div>

    <div class="upcoming-appointments mt-6">
      <div class="section-header">
        <h2 class="title is-3">Próximas Consultas</h2>
        <p class="subtitle">Consultas agendadas para os próximos dias</p>
      </div>
      
      <div class="appointments-list">
        <div 
          v-for="agendamento in agendamentos.slice(0, 5)" 
          :key="agendamento.id"
          class="appointment-item"
        >
          <div class="appointment-time">
            <div class="time">{{ new Date(agendamento.data_hora).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) }}</div>
            <div class="date">{{ new Date(agendamento.data_hora).toLocaleDateString('pt-BR') }}</div>
          </div>
          
          <div class="appointment-info">
            <div class="appointment-main">
              <strong>{{ agendamento.servico.nome }}</strong>
              <span class="price">{{ formatarMoeda(agendamento.servico.preco) }}</span>
            </div>
            
            <div class="appointment-details">
              <span class="professional">
                <i class="fas fa-user-md"></i>
                {{ agendamento.responsavel.nome }}
              </span>
              <span class="animal">
                <i class="fas fa-paw"></i>
                {{ agendamento.animal.nome }} ({{ agendamento.animal.especie }})
              </span>
              <span class="client">
                <i class="fas fa-user"></i>
                {{ agendamento.cliente.nome }}
              </span>
            </div>
            
            <div v-if="agendamento.observacoes" class="appointment-notes">
              <i class="fas fa-sticky-note"></i>
              {{ agendamento.observacoes }}
            </div>
          </div>
          
          <div class="appointment-actions">
            <button class="button is-small is-info">
              <span class="icon">
                <i class="fas fa-edit"></i>
              </span>
            </button>
            <button class="button is-small is-danger">
              <span class="icon">
                <i class="fas fa-trash"></i>
              </span>
            </button>
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
  background: linear-gradient(135deg, #2E7D32, #A5D6A7);
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
  color: #2E7D32;
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
  color: #2E7D32;
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
  color: #2E7D32;
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

.appointment-actions {
  display: flex;
  gap: 0.5rem;
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
  
  .appointment-actions {
    align-self: flex-end;
  }
}
</style> 