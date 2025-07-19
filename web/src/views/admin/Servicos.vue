<script setup>
import { ref, onMounted } from 'vue'
import adminService from '../../services/adminService.js'

const servicos = ref([])
const loading = ref(false)
const error = ref(null)
const submitting = ref(false)

const novoServico = ref({
  nome: '',
  descricao: '',
  duracao: 30,
  preco: '',
  especialidades: []
})

const especialidades = [
  'Clínico Geral',
  'Dermatologia',
  'Ortopedia',
  'Cardiologia',
  'Oftalmologia',
  'Odontologia',
  'Cirurgia',
  'Anestesiologia'
]

// Carregar serviços
const loadServicos = async () => {
  try {
    loading.value = true
    error.value = null
    
    const data = await adminService.getServicos()
    servicos.value = Array.isArray(data) ? data : []
    
  } catch (err) {
    console.error('Erro ao carregar serviços:', err)
    error.value = 'Erro ao carregar serviços. Tente novamente.'
  } finally {
    loading.value = false
  }
}

// Adicionar serviço
const adicionarServico = async () => {
  try {
    if (!novoServico.value.nome || !novoServico.value.descricao || !novoServico.value.preco) {
      error.value = 'Por favor, preencha todos os campos obrigatórios'
      return
    }

    submitting.value = true
    error.value = null

    const servicoData = {
      nome: novoServico.value.nome,
      descricao: novoServico.value.descricao,
      duracao: parseInt(novoServico.value.duracao),
      preco: parseFloat(novoServico.value.preco),
      especialidades: novoServico.value.especialidades.join(',') || ''
    }

    await adminService.createServico(servicoData)
    
    // Recarregar lista
    await loadServicos()
    
    // Limpar formulário
    novoServico.value = {
      nome: '',
      descricao: '',
      duracao: 30,
      preco: '',
      especialidades: []
    }
    
  } catch (err) {
    console.error('Erro ao adicionar serviço:', err)
    error.value = 'Erro ao adicionar serviço. Tente novamente.'
  } finally {
    submitting.value = false
  }
}

// Remover serviço
const removerServico = async (id) => {
  if (!confirm('Tem certeza que deseja remover este serviço?')) {
    return
  }

  try {
    await adminService.deleteServico(id)
    await loadServicos()
  } catch (err) {
    console.error('Erro ao remover serviço:', err)
    error.value = 'Erro ao remover serviço. Tente novamente.'
  }
}

const formatarPreco = (preco) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(preco)
}

const formatarDuracao = (minutos) => {
  if (minutos < 60) {
    return `${minutos} min`
  }
  const horas = Math.floor(minutos / 60)
  const mins = minutos % 60
  return mins > 0 ? `${horas}h ${mins}min` : `${horas}h`
}

// Carregar dados na montagem
onMounted(() => {
  loadServicos()
})
</script>

<template>
  <div class="servicos-container">
    <h1 class="title is-2 mb-4">Gerenciamento de Serviços</h1>

    <!-- Error state -->
    <div v-if="error" class="notification is-danger is-light mb-4">
      <button class="delete" @click="error = null"></button>
      {{ error }}
    </div>

    <div class="box mb-6">
      <h2 class="title is-4 mb-4">Novo Serviço</h2>
      <div class="columns is-multiline">
        <div class="column is-6">
          <div class="field">
            <label class="label">Nome do Serviço *</label>
            <div class="control">
              <input 
                v-model="novoServico.nome"
                class="input" 
                type="text" 
                placeholder="Nome do serviço"
                required
              >
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">Preço *</label>
            <div class="control">
              <input 
                v-model="novoServico.preco"
                class="input" 
                type="number" 
                step="0.01"
                min="0"
                placeholder="0.00"
                required
              >
            </div>
          </div>
        </div>

        <div class="column is-12">
          <div class="field">
            <label class="label">Descrição *</label>
            <div class="control">
              <textarea 
                v-model="novoServico.descricao"
                class="textarea" 
                placeholder="Descrição detalhada do serviço"
                required
              ></textarea>
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">Duração (minutos) *</label>
            <div class="control">
              <input 
                v-model="novoServico.duracao"
                class="input" 
                type="number" 
                min="15"
                step="15"
                required
              >
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">Especialidades Necessárias</label>
            <div class="control">
              <div class="select is-multiple is-fullwidth">
                <select 
                  v-model="novoServico.especialidades" 
                  multiple 
                  size="3"
                >
                  <option 
                    v-for="esp in especialidades" 
                    :key="esp" 
                    :value="esp"
                  >
                    {{ esp }}
                  </option>
                </select>
              </div>
            </div>
            <p class="help">Segure Ctrl (ou Cmd) para selecionar múltiplas especialidades</p>
          </div>
        </div>

        <div class="column is-12">
          <div class="field">
            <div class="control">
              <button 
                @click="adicionarServico"
                class="button is-primary is-fullwidth"
                :disabled="submitting"
              >
                <span v-if="submitting" class="icon">
                  <i class="fas fa-spinner fa-spin"></i>
                </span>
                <span v-else class="icon">
                  <i class="fas fa-plus"></i>
                </span>
                <span>{{ submitting ? 'Adicionando...' : 'Adicionar Serviço' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="title is-4 mb-4">Serviços Cadastrados</h2>
      
      <!-- Loading state -->
      <div v-if="loading" class="has-text-centered">
        <span class="icon is-large">
          <i class="fas fa-spinner fa-spin"></i>
        </span>
        <p class="mt-3">Carregando serviços...</p>
      </div>

      <!-- Table -->
      <div v-else class="table-container">
        <table class="table is-fullwidth is-striped">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Descrição</th>
              <th>Duração</th>
              <th>Preço</th>
              <th>Especialidades</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="servico in servicos" :key="servico.id">
              <td>{{ servico.nome }}</td>
              <td>{{ servico.descricao }}</td>
              <td>{{ formatarDuracao(servico.duracao) }}</td>
              <td>{{ formatarPreco(servico.preco) }}</td>
              <td>
                <span v-if="servico.especialidades" class="tags">
                  <span 
                    v-for="esp in servico.especialidades.split(',')" 
                    :key="esp" 
                    class="tag is-info is-light"
                  >
                    {{ esp.trim() }}
                  </span>
                </span>
                <span v-else class="has-text-grey-light">Nenhuma</span>
              </td>
              <td>
                <div class="buttons are-small">
                  <button class="button is-info">
                    <span class="icon">
                      <i class="fas fa-edit"></i>
                    </span>
                  </button>
                  <button 
                    @click="removerServico(servico.id)"
                    class="button is-danger"
                  >
                    <span class="icon">
                      <i class="fas fa-trash"></i>
                    </span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- Empty state -->
        <div v-if="servicos.length === 0" class="has-text-centered py-6">
          <span class="icon is-large has-text-grey-light">
            <i class="fas fa-clipboard-list"></i>
          </span>
          <p class="mt-3 has-text-grey">Nenhum serviço cadastrado</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.servicos-container {
  padding: 1rem;
}

.table-container {
  overflow-x: auto;
}

.buttons {
  margin: 0;
}

.button .icon {
  margin-right: 0;
}

.tags {
  flex-wrap: wrap;
  gap: 0.25rem;
}

.tag {
  margin-right: 0;
}
</style> 