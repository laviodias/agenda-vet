<template>
  <div class="disponibilidade-container">
    <div class="header">
      <h3>Disponibilidade do Profissional</h3>
    </div>

    <div class="disponibilidade-form">
      <div class="form-row">
        <div class="form-group">
          <label>Dia da Semana</label>
          <select v-model="form.dia_semana" class="form-control">
            <option value="">Selecione um dia</option>
            <option value="0">Segunda-feira</option>
            <option value="1">Terça-feira</option>
            <option value="2">Quarta-feira</option>
            <option value="3">Quinta-feira</option>
            <option value="4">Sexta-feira</option>
            <option value="5">Sábado</option>
            <option value="6">Domingo</option>
          </select>
        </div>
        <div class="form-group">
          <label>Hora de Início</label>
          <input type="time" v-model="form.hora_inicio" class="form-control" />
        </div>
        <div class="form-group">
          <label>Hora de Fim</label>
          <input type="time" v-model="form.hora_fim" class="form-control" />
        </div>
        <div class="form-group">
          <label>Ativo</label>
          <input type="checkbox" v-model="form.ativo" class="form-checkbox" />
        </div>
      </div>
      <div class="form-actions">
        <button @click="adicionarDisponibilidade" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Adicionando...' : 'Adicionar' }}
        </button>
      </div>
    </div>

    <div class="disponibilidades-list">
      <h4>Disponibilidades Cadastradas</h4>
      <div v-if="disponibilidades.length === 0" class="no-data">
        Nenhuma disponibilidade cadastrada
      </div>
      <div v-else class="disponibilidades-grid">
        <div 
          v-for="disp in disponibilidades" 
          :key="disp.id" 
          class="disponibilidade-card"
          :class="{ 'inativo': !disp.ativo }"
        >
          <div class="disponibilidade-header">
            <h5>{{ disp.dia_semana_nome }}</h5>
            <div class="status-badge" :class="{ 'ativo': disp.ativo, 'inativo': !disp.ativo }">
              {{ disp.ativo ? 'Ativo' : 'Inativo' }}
            </div>
          </div>
          <div class="disponibilidade-horario">
            <span>{{ formatTime(disp.hora_inicio) }} - {{ formatTime(disp.hora_fim) }}</span>
          </div>
          <div class="disponibilidade-actions">
            <button @click="editarDisponibilidade(disp)" class="btn btn-sm btn-outline-primary">
              Editar
            </button>
            <button @click="deletarDisponibilidade(disp.id)" class="btn btn-sm btn-outline-danger">
              Excluir
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edição -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>Editar Disponibilidade</h4>
          <button @click="closeEditModal" class="btn-close">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Dia da Semana</label>
              <select v-model="editForm.dia_semana" class="form-control">
                <option value="0">Segunda-feira</option>
                <option value="1">Terça-feira</option>
                <option value="2">Quarta-feira</option>
                <option value="3">Quinta-feira</option>
                <option value="4">Sexta-feira</option>
                <option value="5">Sábado</option>
                <option value="6">Domingo</option>
              </select>
            </div>
            <div class="form-group">
              <label>Hora de Início</label>
              <input type="time" v-model="editForm.hora_inicio" class="form-control" />
            </div>
            <div class="form-group">
              <label>Hora de Fim</label>
              <input type="time" v-model="editForm.hora_fim" class="form-control" />
            </div>
            <div class="form-group">
              <label>Ativo</label>
              <input type="checkbox" v-model="editForm.ativo" class="form-checkbox" />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeEditModal" class="btn btn-secondary">Cancelar</button>
          <button @click="salvarEdicao" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Salvar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import adminService from '../services/adminService'

export default {
  name: 'DisponibilidadeProfissional',
  props: {
    profissionalId: {
      type: [Number, String],
      required: true
    }
  },
  setup(props) {
    const loading = ref(false)
    const disponibilidades = ref([])
    const showEditModal = ref(false)
    const editingDisponibilidade = ref(null)

    const form = reactive({
      dia_semana: '',
      hora_inicio: '',
      hora_fim: '',
      ativo: true
    })

    const editForm = reactive({
      id: null,
      dia_semana: '',
      hora_inicio: '',
      hora_fim: '',
      ativo: true
    })

    const diasSemana = {
      0: 'Segunda-feira',
      1: 'Terça-feira',
      2: 'Quarta-feira',
      3: 'Quinta-feira',
      4: 'Sexta-feira',
      5: 'Sábado',
      6: 'Domingo'
    }

    const formatTime = (time) => {
      if (!time) return ''
      return time.substring(0, 5)
    }

    const carregarDisponibilidades = async () => {
      try {
        loading.value = true
        const response = await adminService.getDisponibilidadesProfissional(props.profissionalId)
        disponibilidades.value = response || []
      } catch (error) {
        console.error('Erro ao carregar disponibilidades:', error)
      } finally {
        loading.value = false
      }
    }

    // Watch para recarregar disponibilidades quando o profissionalId mudar
    watch(() => props.profissionalId, async (newId) => {
      if (newId) {
        await carregarDisponibilidades()
      } else {
        disponibilidades.value = []
      }
    }, { immediate: true })

    const adicionarDisponibilidade = async () => {
      if (!form.dia_semana || !form.hora_inicio || !form.hora_fim) {
        alert('Preencha todos os campos obrigatórios')
        return
      }

      if (form.hora_inicio >= form.hora_fim) {
        alert('Hora de início deve ser menor que hora de fim')
        return
      }

      try {
        loading.value = true
        const data = {
          profissional: props.profissionalId,
          dia_semana: parseInt(form.dia_semana),
          hora_inicio: form.hora_inicio,
          hora_fim: form.hora_fim,
          ativo: form.ativo
        }

        await adminService.createDisponibilidadeProfissional(data)
        
        // Limpar formulário
        form.dia_semana = ''
        form.hora_inicio = ''
        form.hora_fim = ''
        form.ativo = true

        // Recarregar lista
        await carregarDisponibilidades()
        
        alert('Disponibilidade adicionada com sucesso!')
      } catch (error) {
        console.error('Erro ao adicionar disponibilidade:', error)
        alert('Erro ao adicionar disponibilidade')
      } finally {
        loading.value = false
      }
    }

    const editarDisponibilidade = (disp) => {
      editingDisponibilidade.value = disp
      editForm.id = disp.id
      editForm.dia_semana = disp.dia_semana.toString()
      editForm.hora_inicio = formatTime(disp.hora_inicio)
      editForm.hora_fim = formatTime(disp.hora_fim)
      editForm.ativo = disp.ativo
      showEditModal.value = true
    }

    const salvarEdicao = async () => {
      if (!editForm.dia_semana || !editForm.hora_inicio || !editForm.hora_fim) {
        alert('Preencha todos os campos obrigatórios')
        return
      }

      if (editForm.hora_inicio >= editForm.hora_fim) {
        alert('Hora de início deve ser menor que hora de fim')
        return
      }

      try {
        loading.value = true
        const data = {
          profissional: props.profissionalId,
          dia_semana: parseInt(editForm.dia_semana),
          hora_inicio: editForm.hora_inicio,
          hora_fim: editForm.hora_fim,
          ativo: editForm.ativo
        }

        await adminService.updateDisponibilidadeProfissional(editForm.id, data)
        
        closeEditModal()
        await carregarDisponibilidades()
        
        alert('Disponibilidade atualizada com sucesso!')
      } catch (error) {
        console.error('Erro ao atualizar disponibilidade:', error)
        alert('Erro ao atualizar disponibilidade')
      } finally {
        loading.value = false
      }
    }

    const deletarDisponibilidade = async (id) => {
      if (!confirm('Tem certeza que deseja excluir esta disponibilidade?')) {
        return
      }

      try {
        loading.value = true
        await adminService.deleteDisponibilidadeProfissional(id)
        await carregarDisponibilidades()
        alert('Disponibilidade excluída com sucesso!')
      } catch (error) {
        console.error('Erro ao excluir disponibilidade:', error)
        alert('Erro ao excluir disponibilidade')
      } finally {
        loading.value = false
      }
    }

    const closeEditModal = () => {
      showEditModal.value = false
      editingDisponibilidade.value = null
      editForm.id = null
      editForm.dia_semana = ''
      editForm.hora_inicio = ''
      editForm.hora_fim = ''
      editForm.ativo = true
    }

    return {
      loading,
      disponibilidades,
      form,
      editForm,
      showEditModal,
      formatTime,
      adicionarDisponibilidade,
      editarDisponibilidade,
      salvarEdicao,
      deletarDisponibilidade,
      closeEditModal
    }
  }
}
</script>

<style scoped>
.disponibilidade-container {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header {
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.header h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.profissional-nome {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.disponibilidade-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: 15px;
  align-items: end;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-checkbox {
  width: 20px;
  height: 20px;
}

.form-actions {
  margin-top: 15px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
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

.btn-outline-danger {
  background: transparent;
  color: #dc3545;
  border: 1px solid #dc3545;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.disponibilidades-list {
  margin-top: 20px;
}

.disponibilidades-list h4 {
  margin-bottom: 15px;
  color: #333;
}

.no-data {
  text-align: center;
  color: #666;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 6px;
}

.disponibilidades-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.disponibilidade-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 15px;
  transition: all 0.2s;
}

.disponibilidade-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.disponibilidade-card.inativo {
  opacity: 0.6;
  background: #f8f9fa;
}

.disponibilidade-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.disponibilidade-header h5 {
  margin: 0;
  color: #333;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.ativo {
  background: #d4edda;
  color: #155724;
}

.status-badge.inativo {
  background: #f8d7da;
  color: #721c24;
}

.disponibilidade-horario {
  margin-bottom: 10px;
  color: #666;
  font-size: 14px;
}

.disponibilidade-actions {
  display: flex;
  gap: 8px;
}

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
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h4 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #eee;
}
</style> 