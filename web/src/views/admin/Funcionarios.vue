<script setup>
import { ref } from 'vue'

const funcionarios = ref([
  { id: 1, nome: 'Dr. João Silva', especialidade: 'Clínico Geral', email: 'joao.silva@agendavet.com' },
  { id: 2, nome: 'Dra. Maria Santos', especialidade: 'Dermatologia', email: 'maria.santos@agendavet.com' }
])

const novoFuncionario = ref({
  nome: '',
  especialidade: '',
  email: '',
  senha: ''
})

const especialidades = [
  'Clínico Geral',
  'Dermatologia',
  'Ortopedia',
  'Cardiologia',
  'Oftalmologia',
  'Odontologia'
]

const adicionarFuncionario = () => {
  if (!novoFuncionario.value.nome || !novoFuncionario.value.email || !novoFuncionario.value.senha) {
    alert('Por favor, preencha todos os campos obrigatórios')
    return
  }

  funcionarios.value.push({
    id: funcionarios.value.length + 1,
    ...novoFuncionario.value
  })

  novoFuncionario.value = {
    nome: '',
    especialidade: '',
    email: '',
    senha: ''
  }
}

const removerFuncionario = (id) => {
  if (confirm('Tem certeza que deseja remover este funcionário?')) {
    funcionarios.value = funcionarios.value.filter(f => f.id !== id)
  }
}
</script>

<template>
  <div class="funcionarios-container">
    <h1 class="title is-2 mb-4">Gerenciamento de Funcionários</h1>

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

        <div class="column is-12">
          <div class="field">
            <div class="control">
              <button 
                @click="adicionarFuncionario"
                class="button is-primary is-fullwidth"
              >
                <span class="icon">
                  <i class="fas fa-plus"></i>
                </span>
                <span>Adicionar Funcionário</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="title is-4 mb-4">Funcionários Cadastrados</h2>
      <div class="table-container">
        <table class="table is-fullwidth is-striped">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Especialidade</th>
              <th>E-mail</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="funcionario in funcionarios" :key="funcionario.id">
              <td>{{ funcionario.nome }}</td>
              <td>{{ funcionario.especialidade }}</td>
              <td>{{ funcionario.email }}</td>
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