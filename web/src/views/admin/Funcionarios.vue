<script setup>
import { ref, onMounted } from 'vue'
import authService from '../../services/authService.js'

const funcionarios = ref([])
const loading = ref(false)
const error = ref(null)
const submitting = ref(false)

const novoFuncionario = ref({
  nome: '',
  especialidade: '',
  email: '',
  senha: '',
  crmv: '',
  telefone: ''
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

// Carregar funcionários
const loadFuncionarios = async () => {
  try {
    loading.value = true
    error.value = null
    
    const data = await authService.getProfissionais()
    funcionarios.value = Array.isArray(data) ? data : []
    
  } catch (err) {
    console.error('Erro ao carregar funcionários:', err)
    error.value = 'Erro ao carregar funcionários. Tente novamente.'
  } finally {
    loading.value = false
  }
}

// Adicionar funcionário
const adicionarFuncionario = async () => {
  try {
    if (!novoFuncionario.value.nome || !novoFuncionario.value.email || !novoFuncionario.value.senha) {
      error.value = 'Por favor, preencha todos os campos obrigatórios'
      return
    }

    submitting.value = true
    error.value = null

    const funcionarioData = {
      nome: novoFuncionario.value.nome,
      email: novoFuncionario.value.email,
      senha: novoFuncionario.value.senha,
      especialidade: novoFuncionario.value.especialidade || '',
      crmv: novoFuncionario.value.crmv || '',
      telefone: novoFuncionario.value.telefone || '',
      tipo: 'profissional'
    }

    await authService.register(funcionarioData)
    
    // Recarregar lista
    await loadFuncionarios()
    
    // Limpar formulário
    novoFuncionario.value = {
      nome: '',
      especialidade: '',
      email: '',
      senha: '',
      crmv: '',
      telefone: ''
    }
    
  } catch (err) {
    console.error('Erro ao adicionar funcionário:', err)
    error.value = 'Erro ao adicionar funcionário. Tente novamente.'
  } finally {
    submitting.value = false
  }
}

// Remover funcionário
const removerFuncionario = async (id) => {
  if (!confirm('Tem certeza que deseja remover este funcionário?')) {
    return
  }

  try {
    await authService.deleteUser(id)
    await loadFuncionarios()
  } catch (err) {
    console.error('Erro ao remover funcionário:', err)
    error.value = 'Erro ao remover funcionário. Tente novamente.'
  }
}

// Carregar dados na montagem
onMounted(() => {
  loadFuncionarios()
})
</script>

<template>
  <div class="funcionarios-container">
    <h1 class="title is-2 mb-4">Gerenciamento de Funcionários</h1>

    <!-- Error state -->
    <div v-if="error" class="notification is-danger is-light mb-4">
      <button class="delete" @click="error = null"></button>
      {{ error }}
    </div>

    <div class="box mb-6">
      <h2 class="title is-4 mb-4">Novo Funcionário</h2>
      <div class="columns is-multiline">
        <div class="column is-6">
          <div class="field">
            <label class="label">Nome Completo *</label>
            <div class="control">
              <input 
                v-model="novoFuncionario.nome"
                class="input" 
                type="text" 
                placeholder="Nome do funcionário"
                required
              >
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">Especialidade</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="novoFuncionario.especialidade">
                  <option value="">Selecione uma especialidade</option>
                  <option v-for="esp in especialidades" :key="esp" :value="esp">
                    {{ esp }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">E-mail *</label>
            <div class="control">
              <input 
                v-model="novoFuncionario.email"
                class="input" 
                type="email" 
                placeholder="email@agendavet.com"
                required
              >
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">Senha *</label>
            <div class="control">
              <input 
                v-model="novoFuncionario.senha"
                class="input" 
                type="password" 
                placeholder="Senha de acesso"
                required
              >
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">CRMV</label>
            <div class="control">
              <input 
                v-model="novoFuncionario.crmv"
                class="input" 
                type="text" 
                placeholder="CRMV (opcional)"
              >
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">Telefone</label>
            <div class="control">
              <input 
                v-model="novoFuncionario.telefone"
                class="input" 
                type="tel" 
                placeholder="(11) 99999-9999"
              >
            </div>
          </div>
        </div>

        <div class="column is-12">
          <div class="field">
            <div class="control">
              <button 
                @click="adicionarFuncionario"
                class="button is-primary is-fullwidth"
                :disabled="submitting"
              >
                <span v-if="submitting" class="icon">
                  <i class="fas fa-spinner fa-spin"></i>
                </span>
                <span v-else class="icon">
                  <i class="fas fa-plus"></i>
                </span>
                <span>{{ submitting ? 'Adicionando...' : 'Adicionar Funcionário' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="title is-4 mb-4">Funcionários Cadastrados</h2>
      
      <!-- Loading state -->
      <div v-if="loading" class="has-text-centered">
        <span class="icon is-large">
          <i class="fas fa-spinner fa-spin"></i>
        </span>
        <p class="mt-3">Carregando funcionários...</p>
      </div>

      <!-- Table -->
      <div v-else class="table-container">
        <table class="table is-fullwidth is-striped">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Especialidade</th>
              <th>E-mail</th>
              <th>CRMV</th>
              <th>Telefone</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="funcionario in funcionarios" :key="funcionario.id">
              <td>{{ funcionario.nome }}</td>
              <td>{{ funcionario.especialidade || 'Não informado' }}</td>
              <td>{{ funcionario.email }}</td>
              <td>{{ funcionario.crmv || 'Não informado' }}</td>
              <td>{{ funcionario.telefone || 'Não informado' }}</td>
              <td>
                <div class="buttons are-small">
                  <button class="button is-info">
                    <span class="icon">
                      <i class="fas fa-edit"></i>
                    </span>
                  </button>
                  <button 
                    @click="removerFuncionario(funcionario.id)"
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
        <div v-if="funcionarios.length === 0" class="has-text-centered py-6">
          <span class="icon is-large has-text-grey-light">
            <i class="fas fa-users"></i>
          </span>
          <p class="mt-3 has-text-grey">Nenhum funcionário cadastrado</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.funcionarios-container {
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
</style> 