<template>
  <div class="weekly-calendar">
    <div class="calendar-header mb-4">
      <button class="button is-light" @click="previousWeek">
        <span class="icon">
          <i class="fas fa-chevron-left"></i>
        </span>
      </button>
      <h2 class="title is-4 has-text-centered">
        {{ weekRange }}
      </h2>
      <button class="button is-light" @click="nextWeek">
        <span class="icon">
          <i class="fas fa-chevron-right"></i>
        </span>
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="has-text-centered mb-4">
      <span class="icon">
        <i class="fas fa-spinner fa-spin"></i>
      </span>
      <p class="mt-2">Carregando horários...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="notification is-warning is-light mb-4">
      <button class="delete" @click="error = null"></button>
      {{ error }}
    </div>

    <div class="calendar-container">
      <div class="calendar-grid">
        <div class="calendar-row header sticky-header">
          <div v-for="day in weekDays" :key="day.date" class="day-column">
            <div class="day-header" :class="{ 'is-today': day.isToday }">
              <span class="weekday">{{ day.weekday }}</span>
              <span class="date">{{ day.date }}</span>
            </div>
          </div>
        </div>

        <div class="calendar-body">
          <div v-for="timeSlot in timeSlots" :key="timeSlot.value" class="calendar-row">
            <div 
              v-for="day in weekDays" 
              :key="`${day.value}-${timeSlot.value}`"
              class="day-column"
            >
              <button
                v-if="isTimeSlotAvailable(day.value, timeSlot.value)"
                class="time-slot"
                :class="{ 'is-selected': isSelected(day.value, timeSlot.value) }"
                @click="selectTimeSlot(day.value, timeSlot.value)"
              >
                {{ timeSlot.label }}
              </button>
              <div v-else class="time-slot is-unavailable">
                {{ timeSlot.label }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import authService from '../services/authService.js';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ date: '', time: '' })
  },
  profissional: {
    type: [String, Number],
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);

const currentWeekStart = ref(new Date());
const loading = ref(false);
const error = ref(null);
const horariosDisponiveis = ref({});

const timeSlots = [
  { value: '08:00', label: '08:00' },
  { value: '09:00', label: '09:00' },
  { value: '10:00', label: '10:00' },
  { value: '11:00', label: '11:00' },
  { value: '14:00', label: '14:00' },
  { value: '15:00', label: '15:00' },
  { value: '16:00', label: '16:00' },
  { value: '17:00', label: '17:00' },
];

const weekDays = computed(() => {
  const days = [];
  const today = new Date();
  
  for (let i = 0; i < 5; i++) {
    const date = new Date(currentWeekStart.value);
    date.setDate(currentWeekStart.value.getDate() + i);
    
    days.push({
      value: date.toISOString().split('T')[0],
      weekday: date.toLocaleDateString('pt-BR', { weekday: 'short' }),
      date: date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }),
      isToday: date.toDateString() === today.toDateString()
    });
  }
  
  return days;
});

const weekRange = computed(() => {
  const start = new Date(currentWeekStart.value);
  const end = new Date(currentWeekStart.value);
  end.setDate(end.getDate() + 4);
  
  return `${start.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })} - ${end.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })}`;
});

// Carregar horários disponíveis quando a semana ou profissional mudar
watch([currentWeekStart, () => props.profissional], async () => {
  await loadHorariosDisponiveis();
});

async function loadHorariosDisponiveis() {
  try {
    loading.value = true;
    error.value = null;
    
    const horarios = {};
    
    // Buscar horários para cada dia da semana
    for (const day of weekDays.value) {
      try {
        const disponiveis = await authService.getHorariosDisponiveis(day.value, props.profissional);
        horarios[day.value] = disponiveis || [];
      } catch (err) {
        console.error(`Erro ao buscar horários para ${day.value}:`, err);
        horarios[day.value] = [];
      }
    }
    
    horariosDisponiveis.value = horarios;
    
  } catch (err) {
    console.error('Erro ao carregar horários disponíveis:', err);
    error.value = 'Erro ao carregar horários. Tente novamente.';
  } finally {
    loading.value = false;
  }
}

function previousWeek() {
  const newDate = new Date(currentWeekStart.value);
  newDate.setDate(newDate.getDate() - 7);
  currentWeekStart.value = newDate;
}

function nextWeek() {
  const newDate = new Date(currentWeekStart.value);
  newDate.setDate(newDate.getDate() + 7);
  currentWeekStart.value = newDate;
}

function isTimeSlotAvailable(date, time) {
  // Se não há dados de horários disponíveis, considerar todos disponíveis
  if (!horariosDisponiveis.value[date]) {
    return true;
  }
  
  // Verificar se o horário está na lista de disponíveis
  return horariosDisponiveis.value[date].includes(time);
}

function isSelected(date, time) {
  return props.modelValue.date === date && props.modelValue.time === time;
}

function selectTimeSlot(date, time) {
  emit('update:modelValue', { date, time });
}

onMounted(async () => {
  const today = new Date();
  const dayOfWeek = today.getDay();
  const daysUntilMonday = dayOfWeek === 0 ? 1 : dayOfWeek === 1 ? 0 : 8 - dayOfWeek;
  
  const nextMonday = new Date(today);
  nextMonday.setDate(today.getDate() + daysUntilMonday);
  currentWeekStart.value = nextMonday;
  
  // Carregar horários disponíveis
  await loadHorariosDisponiveis();
});
</script>

<style scoped>
.weekly-calendar {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: var(--shadow-md);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.calendar-container {
  max-height: 400px;
  overflow: hidden;
  border: 1px solid #dbdbdb;
  border-radius: 4px;
}

.calendar-grid {
  display: flex;
  flex-direction: column;
}

.calendar-body {
  overflow-y: auto;
  max-height: 300px;
}

.calendar-row {
  display: flex;
  border-bottom: 1px solid #dbdbdb;
}

.calendar-row:last-child {
  border-bottom: none;
}

.calendar-row.header {
  background-color: #f5f5f5;
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 1;
}

.sticky-header {
  position: sticky;
  top: 0;
  z-index: 1;
  background-color: #f5f5f5;
}

.day-column {
  flex: 1;
  min-width: 120px;
  padding: 0.5rem;
  border-right: 1px solid #dbdbdb;
  text-align: center;
}

.day-column:last-child {
  border-right: none;
}

.day-header {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.5rem;
  background-color: #f5f5f5;
}

.day-header.is-today {
  color: var(--primary);
  font-weight: bold;
}

.weekday {
  font-size: 0.9rem;
  text-transform: uppercase;
}

.date {
  font-size: 1.1rem;
}

.time-slot {
  width: 100%;
  padding: 0.75rem 0.5rem;
  border: 1px solid #dbdbdb;
  border-radius: 4px;
  background-color: #fafafa;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.time-slot:hover {
  background-color: #f0f0f0;
  border-color: #b5b5b5;
}

.time-slot.is-selected {
  background-color: #2E7D32;
  color: white;
  border-color: #2E7D32;
}

.time-slot.is-unavailable {
  background-color: #f5f5f5;
  color: #7a7a7a;
  cursor: not-allowed;
  border: 1px dashed #dbdbdb;
}

.calendar-body::-webkit-scrollbar {
  width: 8px;
}

.calendar-body::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.calendar-body::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.calendar-body::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style> 