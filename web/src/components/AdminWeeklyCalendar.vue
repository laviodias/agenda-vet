<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  agendamentos: {
    type: Array,
    default: () => []
  }
})

const currentWeek = ref(new Date())
const weekDaysShort = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

const weekStart = computed(() => {
  const start = new Date(currentWeek.value)
  const day = start.getDay()
  start.setDate(start.getDate() - day)
  return start
})

const weekDaysArray = computed(() => {
  const days = []
  for (let i = 0; i < 7; i++) {
    const day = new Date(weekStart.value)
    day.setDate(day.getDate() + i)
    days.push(day)
  }
  return days
})

const agendamentosPorDia = computed(() => {
  const agendamentosPorDia = {}
  
  weekDaysArray.value.forEach(day => {
    const dayKey = day.toISOString().split('T')[0]
    agendamentosPorDia[dayKey] = props.agendamentos.filter(agendamento => {
      const agendamentoDate = new Date(agendamento.data_hora).toISOString().split('T')[0]
      return agendamentoDate === dayKey
    })
  })
  
  return agendamentosPorDia
})

const previousWeek = () => {
  const newWeek = new Date(currentWeek.value)
  newWeek.setDate(newWeek.getDate() - 7)
  currentWeek.value = newWeek
}

const nextWeek = () => {
  const newWeek = new Date(currentWeek.value)
  newWeek.setDate(newWeek.getDate() + 7)
  currentWeek.value = newWeek
}

const goToCurrentWeek = () => {
  currentWeek.value = new Date()
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('pt-BR')
}

const formatTime = (dateTime) => {
  return new Date(dateTime).toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(price)
}

const isToday = (date) => {
  const today = new Date()
  return date.toDateString() === today.toDateString()
}

const isWeekend = (date) => {
  const day = date.getDay()
  return day === 0 || day === 6
}
</script>

<template>
  <div class="admin-weekly-calendar">
    <div class="calendar-header">
      <div class="calendar-navigation">
        <button @click="previousWeek" class="button is-small">
          <span class="icon">
            <i class="fas fa-chevron-left"></i>
          </span>
        </button>
        
        <div class="week-info">
          <h3 class="title is-4">
            {{ formatDate(weekStart) }} - {{ formatDate(new Date(weekStart.getTime() + 6 * 24 * 60 * 60 * 1000)) }}
          </h3>
        </div>
        
        <button @click="nextWeek" class="button is-small">
          <span class="icon">
            <i class="fas fa-chevron-right"></i>
          </span>
        </button>
      </div>
      
      <button @click="goToCurrentWeek" class="button is-primary is-small">
        <span class="icon">
          <i class="fas fa-calendar-day"></i>
        </span>
        <span>Hoje</span>
      </button>
    </div>

    <div class="calendar-grid">
      <div class="calendar-days-header">
        <div 
          v-for="(day, index) in weekDaysArray" 
          :key="index"
          class="calendar-day-header"
          :class="{ 'is-today': isToday(day), 'is-weekend': isWeekend(day) }"
        >
          <div class="day-name">{{ weekDaysShort[index] }}</div>
          <div class="day-number">{{ day.getDate() }}</div>
        </div>
      </div>

      <div class="calendar-days-content">
        <div 
          v-for="(day, index) in weekDaysArray" 
          :key="index"
          class="calendar-day-content"
          :class="{ 'is-today': isToday(day), 'is-weekend': isWeekend(day) }"
        >
          <div 
            v-for="agendamento in agendamentosPorDia[day.toISOString().split('T')[0]]" 
            :key="agendamento.id"
            class="appointment-card"
          >
            <div class="appointment-time">
              {{ formatTime(agendamento.data_hora) }}
            </div>
            
            <div class="appointment-details">
              <div class="appointment-service">
                <strong>{{ agendamento.servico.nome }}</strong>
              </div>
              
              <div class="appointment-professional">
                <i class="fas fa-user-md"></i>
                {{ agendamento.responsavel?.nome || 'Não atribuído' }}
              </div>
              
              <div class="appointment-animal">
                <i class="fas fa-paw"></i>
                {{ agendamento.animal.nome }} ({{ agendamento.animal.especie }})
              </div>
              
              <div class="appointment-owner">
                <i class="fas fa-user"></i>
                {{ agendamento.cliente.nome }}
              </div>
              
              <div class="appointment-price">
                <i class="fas fa-dollar-sign"></i>
                {{ formatPrice(agendamento.servico.preco) }}
              </div>
              
              <div v-if="agendamento.observacoes" class="appointment-notes">
                <i class="fas fa-sticky-note"></i>
                {{ agendamento.observacoes }}
              </div>
            </div>
          </div>
          
          <div v-if="!agendamentosPorDia[day.toISOString().split('T')[0]]?.length" class="no-appointments">
            <i class="fas fa-calendar-times"></i>
            <span>Nenhuma consulta</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-weekly-calendar {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.calendar-navigation {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.week-info {
  text-align: center;
}

.calendar-grid {
  display: flex;
  flex-direction: column;
}

.calendar-days-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.calendar-day-header {
  padding: 0.75rem;
  text-align: center;
  border-right: 1px solid #e9ecef;
  transition: background-color 0.2s;
}

.calendar-day-header:last-child {
  border-right: none;
}

.calendar-day-header.is-today {
  background: #e3f2fd;
  color: #1976d2;
  font-weight: bold;
}

.calendar-day-header.is-weekend {
  background: #fff3e0;
  color: #f57c00;
}

.day-name {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.day-number {
  font-size: 1.25rem;
  font-weight: bold;
}

.calendar-days-content {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  min-height: 400px;
}

.calendar-day-content {
  padding: 0.5rem;
  border-right: 1px solid #e9ecef;
  min-height: 400px;
  background: white;
  transition: background-color 0.2s;
}

.calendar-day-content:last-child {
  border-right: none;
}

.calendar-day-content.is-today {
  background: #f3f8ff;
}

.calendar-day-content.is-weekend {
  background: #fffbf0;
}

.appointment-card {
  background: #e8f5e8;
  border: 1px solid #c8e6c9;
  border-radius: 6px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.appointment-card:hover {
  background: #c8e6c9;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.appointment-time {
  font-weight: bold;
  color: #2e7d32;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.appointment-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.appointment-service {
  color: #1b5e20;
  margin-bottom: 0.25rem;
}

.appointment-professional,
.appointment-animal,
.appointment-owner,
.appointment-price,
.appointment-notes {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #424242;
  font-size: 0.8rem;
}

.appointment-professional i,
.appointment-animal i,
.appointment-owner i,
.appointment-price i,
.appointment-notes i {
  color: #666;
  width: 12px;
}

.no-appointments {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: 0.875rem;
  gap: 0.5rem;
}

.no-appointments i {
  font-size: 1.5rem;
}

@media (max-width: 768px) {
  .calendar-days-header,
  .calendar-days-content {
    grid-template-columns: 1fr;
  }
  
  .calendar-day-header,
  .calendar-day-content {
    border-right: none;
    border-bottom: 1px solid #e9ecef;
  }
  
  .calendar-day-content:last-child {
    border-bottom: none;
  }
  
  .appointment-card {
    font-size: 0.8rem;
    padding: 0.5rem;
  }
}
</style> 