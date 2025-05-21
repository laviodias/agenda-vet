<script setup>
import { ref } from 'vue'

const servicos = ref([
  // Dados de exemplo
  { 
    id: 1, 
    nome: 'Consulta Clínica', 
    descricao: 'Consulta veterinária de rotina', 
    duracao: 30,
    preco: 150.00,
    especialidades: ['Clínico Geral']
  },
  { 
    id: 2, 
    nome: 'Banho e Tosa', 
    descricao: 'Serviço completo de higiene e tosa', 
    duracao: 60,
    preco: 80.00,
    especialidades: []
  }
])

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
  'Odontologia'
]

const adicionarServico = () => {
  if (!novoServico.value.nome || !novoServico.value.descricao || !novoServico.value.preco) {
    alert('Por favor, preencha todos os campos obrigatórios')
    return
  }

  servicos.value.push({
    id: servicos.value.length + 1,
    ...novoServico.value,
    preco: parseFloat(novoServico.value.preco)
  })

  // Limpar formulário
  novoServico.value = {
    nome: '',
    descricao: '',
    duracao: 30,
    preco: '',
    especialidades: []
  }
}

const removerServico = (id) => {
  if (confirm('Tem certeza que deseja remover este serviço?')) {
    servicos.value = servicos.value.filter(s => s.id !== id)
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
</script>

<template>
  <div class="servicos-container">
    <h1 class="title is-2 mb-4">Gerenciamento de Serviços</h1>

    <!-- Formulário de Cadastro -->
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
              >
                <span class="icon">
                  <i class="fas fa-plus"></i>
                </span>
                <span>Adicionar Serviço</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de Serviços -->
    <div class="box">
      <h2 class="title is-4 mb-4">Serviços Cadastrados</h2>
      <div class="table-container">
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
                <div class="tags">
                  <span 
                    v-for="esp in servico.especialidades" 
                    :key="esp"
                    class="tag is-info is-light"
                  >
                    {{ esp }}
                  </span>
                  <span v-if="!servico.especialidades.length" class="tag is-light">
                    Nenhuma
                  </span>
                </div>
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