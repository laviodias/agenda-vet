<script setup>
import { ref, onMounted, computed } from 'vue'
import adminService from '../../services/adminService.js'
import brandService from '../../services/brandService.js'

const configuracoes = ref([])
const configuracaoAtiva = ref(null)
const showForm = ref(false)
const editando = ref(false)
const loading = ref(false)

const formData = ref({
  nome_estabelecimento: '',
  cor_primaria: '#00d1b2',
  cor_secundaria: '#363636',
  cor_accent: '#3273dc',
  cor_background: '#f5f5f5',
  cor_success: '#48c774',
  cor_danger: '#f14668',
  cor_warning: '#ffdd57',
  cor_info: '#3298dc',
  cor_texto: '#363636',
  cor_borda: '#dbdbdb',
  cor_sombra: '#000000',
  endereco: '',
  telefone: '',
  email: '',
  website: '',
  ativo: false
})

const logoFile = ref(null)
const logoPreview = ref(null)

// Computed para verificar se o formulário é válido
const isFormValid = computed(() => {
  return formData.value.nome_estabelecimento.trim() !== '' &&
         brandService.validarCorHex(formData.value.cor_primaria) &&
         brandService.validarCorHex(formData.value.cor_secundaria) &&
         brandService.validarCorHex(formData.value.cor_accent) &&
         brandService.validarCorHex(formData.value.cor_background) &&
         brandService.validarCorHex(formData.value.cor_success) &&
         brandService.validarCorHex(formData.value.cor_danger) &&
         brandService.validarCorHex(formData.value.cor_warning) &&
         brandService.validarCorHex(formData.value.cor_info) &&
         brandService.validarCorHex(formData.value.cor_texto) &&
         brandService.validarCorHex(formData.value.cor_borda) &&
         brandService.validarCorHex(formData.value.cor_sombra)
})

// Carregar dados
const carregarDados = async () => {
  loading.value = true
  try {
    const [todasConfigs, configAtiva] = await Promise.all([
      adminService.getAllBrandConfigs(),
      adminService.getBrandConfig()
    ])
    
    configuracoes.value = todasConfigs.results || todasConfigs
    configuracaoAtiva.value = configAtiva
  } catch (error) {
    console.error('Erro ao carregar dados:', error)
  } finally {
    loading.value = false
  }
}

// Abrir formulário para nova configuração
const novaConfiguracao = () => {
  originalData.value = null // Limpar dados originais
  formData.value = {
    nome_estabelecimento: '',
    cor_primaria: '#00d1b2',
    cor_secundaria: '#363636',
    cor_accent: '#3273dc',
    cor_background: '#f5f5f5',
    cor_success: '#48c774',
    cor_danger: '#f14668',
    cor_warning: '#ffdd57',
    cor_info: '#3298dc',
    cor_texto: '#363636',
    cor_borda: '#dbdbdb',
    cor_sombra: '#000000',
    endereco: '',
    telefone: '',
    email: '',
    website: '',
    ativo: false
  }
  logoFile.value = null
  logoPreview.value = null
  editando.value = false
  showForm.value = true
}

// Dados originais para comparação
const originalData = ref(null)

// Editar configuração existente
const editarConfiguracao = (config) => {
  originalData.value = { ...config } // Salvar dados originais
  formData.value = { ...config }
  logoFile.value = null
  logoPreview.value = config.logo_url || null
  editando.value = true
  showForm.value = true
}

// Verificar se os dados do formulário mudaram (exceto logo)
const formDataChanged = () => {
  if (!editando.value || !originalData.value) return true // Novo registro sempre salva
  
  const fieldsToCompare = [
    'nome_estabelecimento', 
    'cor_primaria', 
    'cor_secundaria', 
    'cor_accent', 
    'cor_background',
    'cor_success',
    'cor_danger',
    'cor_warning',
    'cor_info',
    'cor_texto',
    'cor_borda',
    'cor_sombra',
    'endereco', 
    'telefone', 
    'email', 
    'website', 
    'ativo'
  ]
  
  return fieldsToCompare.some(field => {
    return formData.value[field] !== originalData.value[field]
  })
}

// Salvar configuração
const salvarConfiguracao = async () => {
  if (!isFormValid.value) {
    alert('Por favor, preencha todos os campos obrigatórios corretamente.')
    return
  }

  loading.value = true
  try {
    let resultado = formData.value // Usar dados atuais como base
    
    const hasFormChanges = formDataChanged()
    const hasLogoChange = logoFile.value !== null
    
    // 1. Se mudaram dados do formulário, salvar configuração
    if (hasFormChanges) {
      // Preparar dados sem o logo
      const dataToSend = { ...formData.value }
      delete dataToSend.logo

      if (editando.value) {
        resultado = await adminService.updateBrandConfig(formData.value.id, dataToSend)
      } else {
        resultado = await adminService.createBrandConfig(dataToSend)
      }
    }

    // 2. Se mudou o logo, fazer upload separadamente
    if (hasLogoChange && resultado.id) {
      try {
        const logoResult = await brandService.uploadLogo(resultado.id, logoFile.value)
        resultado = logoResult.configuracao || logoResult // Usar o resultado com logo atualizado
      } catch (uploadError) {
        const errorMsg = uploadError.response?.data?.error || uploadError.message || 'Erro desconhecido'
        
        if (hasFormChanges) {
          alert(`Configuração salva, mas houve erro no upload do logo: ${errorMsg}`)
        } else {
          alert(`Erro no upload do logo: ${errorMsg}`)
          loading.value = false
          return
        }
      }
    }

    // 3. Se não houve nenhuma mudança
    if (!hasFormChanges && !hasLogoChange) {
      alert('Nenhuma alteração foi detectada.')
      loading.value = false
      return
    }

    showForm.value = false
    await carregarDados()
    
    // Se a configuração foi marcada como ativa, aplicar o tema
    if (formData.value.ativo) {
      brandService.aplicarTema(resultado)
    }

    alert('Configuração salva com sucesso!')
    
  } catch (error) {
    console.error('Erro ao salvar configuração:', error)
    alert('Erro ao salvar configuração. Tente novamente.')
  } finally {
    loading.value = false
  }
}

// Ativar configuração
const ativarConfiguracao = async (config) => {
  if (confirm(`Deseja ativar a configuração "${config.nome_estabelecimento}"?`)) {
    loading.value = true
    try {
      await adminService.activateBrandConfig(config.id)
      await carregarDados()
      
      // Aplicar tema imediatamente
      brandService.aplicarTema(config)
      
      alert('Configuração ativada com sucesso!')
    } catch (error) {
      console.error('Erro ao ativar configuração:', error)
      alert('Erro ao ativar configuração.')
    } finally {
      loading.value = false
    }
  }
}

// Deletar configuração
const deletarConfiguracao = async (config) => {
  if (config.ativo) {
    alert('Não é possível deletar a configuração ativa.')
    return
  }

  if (confirm(`Deseja deletar a configuração "${config.nome_estabelecimento}"?`)) {
    loading.value = true
    try {
      await adminService.deleteBrandConfig(config.id)
      await carregarDados()
      alert('Configuração deletada com sucesso!')
    } catch (error) {
      console.error('Erro ao deletar configuração:', error)
      alert('Erro ao deletar configuração.')
    } finally {
      loading.value = false
    }
  }
}

// Manipular upload de logo
const handleLogoUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validar tipo de arquivo
    if (!file.type.startsWith('image/')) {
      alert('Por favor, selecione uma imagem.')
      return
    }
    
    // Validar tamanho (máx 2MB)
    if (file.size > 2 * 1024 * 1024) {
      alert('A imagem deve ter no máximo 2MB.')
      return
    }
    
    logoFile.value = file
    
    // Gerar preview
    const reader = new FileReader()
    reader.onload = (e) => {
      logoPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// Cancelar formulário
const cancelarForm = () => {
  showForm.value = false
  logoFile.value = null
  logoPreview.value = null
}

// Preview de cores
const previewCores = () => {
  const root = document.documentElement
  root.style.setProperty('--preview-primary', formData.value.cor_primaria)
  root.style.setProperty('--preview-secondary', formData.value.cor_secundaria)
  root.style.setProperty('--preview-accent', formData.value.cor_accent)
  root.style.setProperty('--preview-background', formData.value.cor_background)
  root.style.setProperty('--preview-success', formData.value.cor_success)
  root.style.setProperty('--preview-danger', formData.value.cor_danger)
  root.style.setProperty('--preview-warning', formData.value.cor_warning)
  root.style.setProperty('--preview-info', formData.value.cor_info)
}

onMounted(() => {
  carregarDados()
})
</script>

<template>
  <div class="marca-admin">
    <!-- Header -->
    <div class="columns is-vcentered mb-6">
      <div class="column">
        <h1 class="title is-2">Personalização da Marca</h1>
        <p class="subtitle">Configure a identidade visual do seu estabelecimento</p>
      </div>
      <div class="column is-narrow">
        <button 
          class="button is-primary"
          @click="novaConfiguracao"
          :disabled="loading"
        >
          <span class="icon">
            <i class="fas fa-plus"></i>
          </span>
          <span>Nova Configuração</span>
        </button>
      </div>
    </div>

    <!-- Configuração Ativa -->
    <div v-if="configuracaoAtiva" class="card mb-6">
      <header class="card-header">
        <p class="card-header-title">
          <span class="icon">
            <i class="fas fa-star"></i>
          </span>
          <span>Configuração Ativa</span>
        </p>
      </header>
      <div class="card-content">
        <div class="columns">
          <div class="column is-2" v-if="configuracaoAtiva.logo_url">
            <figure class="image is-128x128">
              <img :src="configuracaoAtiva.logo_url" alt="Logo" class="is-rounded">
            </figure>
          </div>
          <div class="column">
            <h3 class="title is-4">{{ configuracaoAtiva.nome_estabelecimento }}</h3>
            <div class="color-palette mt-4">
              <div class="color-item">
                <div 
                  class="color-swatch" 
                  :style="{ backgroundColor: configuracaoAtiva.cor_primaria }"
                ></div>
                <span>Primária</span>
              </div>
              <div class="color-item">
                <div 
                  class="color-swatch" 
                  :style="{ backgroundColor: configuracaoAtiva.cor_secundaria }"
                ></div>
                <span>Secundária</span>
              </div>
              <div class="color-item">
                <div 
                  class="color-swatch" 
                  :style="{ backgroundColor: configuracaoAtiva.cor_accent }"
                ></div>
                <span>Destaque</span>
              </div>
              <div class="color-item">
                <div 
                  class="color-swatch" 
                  :style="{ backgroundColor: configuracaoAtiva.cor_background }"
                ></div>
                <span>Fundo</span>
              </div>
            </div>
            
            <div class="color-palette mt-3">
              <div class="color-item">
                <div 
                  class="color-swatch" 
                  :style="{ backgroundColor: configuracaoAtiva.cor_success }"
                ></div>
                <span>Sucesso</span>
              </div>
              <div class="color-item">
                <div 
                  class="color-swatch" 
                  :style="{ backgroundColor: configuracaoAtiva.cor_danger }"
                ></div>
                <span>Erro</span>
              </div>
              <div class="color-item">
                <div 
                  class="color-swatch" 
                  :style="{ backgroundColor: configuracaoAtiva.cor_warning }"
                ></div>
                <span>Aviso</span>
              </div>
              <div class="color-item">
                <div 
                  class="color-swatch" 
                  :style="{ backgroundColor: configuracaoAtiva.cor_info }"
                ></div>
                <span>Info</span>
              </div>
            </div>
          </div>
          <div class="column is-narrow">
            <button 
              class="button is-info"
              @click="editarConfiguracao(configuracaoAtiva)"
            >
              <span class="icon">
                <i class="fas fa-edit"></i>
              </span>
              <span>Editar</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de Configurações -->
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">Todas as Configurações</p>
      </header>
      <div class="card-content">
        <div v-if="loading" class="has-text-centered">
          <div class="loader"></div>
        </div>
        
        <div v-else-if="configuracoes.length" class="table-container">
          <table class="table is-fullwidth is-striped">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Status</th>
                <th>Criado em</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="config in configuracoes" :key="config.id">
                <td>
                  <div class="media">
                    <div class="media-left" v-if="config.logo_url">
                      <figure class="image is-32x32">
                        <img :src="config.logo_url" alt="Logo" class="is-rounded">
                      </figure>
                    </div>
                    <div class="media-content">
                      <strong>{{ config.nome_estabelecimento }}</strong>
                    </div>
                  </div>
                </td>
                <td>
                  <span 
                    class="tag" 
                    :class="config.ativo ? 'is-success' : 'is-light'"
                  >
                    {{ config.ativo ? 'Ativa' : 'Inativa' }}
                  </span>
                </td>
                <td>{{ new Date(config.criado_em).toLocaleDateString('pt-BR') }}</td>
                <td>
                  <div class="buttons are-small">
                    <button 
                      v-if="!config.ativo"
                      class="button is-success"
                      @click="ativarConfiguracao(config)"
                      title="Ativar"
                    >
                      <span class="icon">
                        <i class="fas fa-check"></i>
                      </span>
                    </button>
                    <button 
                      class="button is-info"
                      @click="editarConfiguracao(config)"
                      title="Editar"
                    >
                      <span class="icon">
                        <i class="fas fa-edit"></i>
                      </span>
                    </button>
                    <button 
                      v-if="!config.ativo"
                      class="button is-danger"
                      @click="deletarConfiguracao(config)"
                      title="Deletar"
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
        
        <div v-else class="has-text-centered">
          <p>Nenhuma configuração encontrada.</p>
        </div>
      </div>
    </div>

    <!-- Modal de Formulário -->
    <div v-if="showForm" class="modal is-active">
      <div class="modal-background" @click="cancelarForm"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            {{ editando ? 'Editar' : 'Nova' }} Configuração
          </p>
          <button class="delete" @click="cancelarForm"></button>
        </header>
        
        <section class="modal-card-body">
          <!-- Informações Básicas -->
          <div class="field">
            <label class="label">Nome do Estabelecimento *</label>
            <div class="control">
              <input 
                class="input" 
                type="text" 
                v-model="formData.nome_estabelecimento"
                placeholder="Ex: Clínica Veterinária PetLife"
                required
              >
            </div>
          </div>

          <!-- Upload de Logo -->
          <div class="field">
            <label class="label">Logo</label>
            <div class="file has-name">
              <label class="file-label">
                <input 
                  class="file-input" 
                  type="file" 
                  accept="image/*"
                  @change="handleLogoUpload"
                >
                <span class="file-cta">
                  <span class="file-icon">
                    <i class="fas fa-upload"></i>
                  </span>
                  <span class="file-label">Escolher logo...</span>
                </span>
                <span class="file-name">
                  {{ logoFile ? logoFile.name : 'Nenhum arquivo selecionado' }}
                </span>
              </label>
            </div>
            <p class="help">Formatos aceitos: PNG, JPG. Tamanho máximo: 2MB</p>
            
            <!-- Preview do logo -->
            <div v-if="logoPreview" class="mt-3">
              <figure class="image is-128x128">
                <img :src="logoPreview" alt="Preview" class="is-rounded">
              </figure>
            </div>
          </div>

          <!-- Paleta de Cores -->
          <div class="field">
            <label class="label">Paleta de Cores</label>
            <div class="columns">
              <div class="column">
                <label class="label is-small">Cor Primária *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_primaria"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_primaria"
                      placeholder="#00d1b2"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
              
              <div class="column">
                <label class="label is-small">Cor Secundária *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_secundaria"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_secundaria"
                      placeholder="#363636"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
            </div>
            
            <div class="columns">
              <div class="column">
                <label class="label is-small">Cor de Destaque *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_accent"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_accent"
                      placeholder="#3273dc"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
              
              <div class="column">
                <label class="label is-small">Cor de Fundo *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_background"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_background"
                      placeholder="#f5f5f5"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Cores de Status e Feedback -->
          <div class="field">
            <label class="label">Cores de Status e Feedback</label>
            <div class="columns">
              <div class="column">
                <label class="label is-small">Cor de Sucesso *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_success"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_success"
                      placeholder="#48c774"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
              
              <div class="column">
                <label class="label is-small">Cor de Erro *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_danger"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_danger"
                      placeholder="#f14668"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
            </div>
            
            <div class="columns">
              <div class="column">
                <label class="label is-small">Cor de Aviso *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_warning"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_warning"
                      placeholder="#ffdd57"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
              
              <div class="column">
                <label class="label is-small">Cor de Informação *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_info"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_info"
                      placeholder="#3298dc"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Cores de Interface -->
          <div class="field">
            <label class="label">Cores de Interface</label>
            <div class="columns">
              <div class="column">
                <label class="label is-small">Cor do Texto *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_texto"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_texto"
                      placeholder="#363636"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
              
              <div class="column">
                <label class="label is-small">Cor das Bordas *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_borda"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_borda"
                      placeholder="#dbdbdb"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
            </div>
            
            <div class="columns">
              <div class="column">
                <label class="label is-small">Cor das Sombras *</label>
                <div class="field has-addons">
                  <div class="control">
                    <input 
                      class="input" 
                      type="color" 
                      v-model="formData.cor_sombra"
                      @input="previewCores"
                    >
                  </div>
                  <div class="control is-expanded">
                    <input 
                      class="input" 
                      type="text" 
                      v-model="formData.cor_sombra"
                      placeholder="#000000"
                      @input="previewCores"
                    >
                  </div>
                </div>
              </div>
              
              <div class="column">
                <!-- Espaço vazio para manter layout -->
              </div>
            </div>
          </div>

          <!-- Informações de Contato -->
          <div class="field">
            <label class="label">Informações de Contato</label>
            
            <div class="field">
              <label class="label is-small">Endereço</label>
              <div class="control">
                <textarea 
                  class="textarea" 
                  v-model="formData.endereco"
                  placeholder="Rua das Flores, 123 - Centro - São Paulo/SP"
                  rows="2"
                ></textarea>
              </div>
            </div>
            
            <div class="columns">
              <div class="column">
                <label class="label is-small">Telefone</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="formData.telefone"
                    placeholder="(11) 99999-9999"
                  >
                </div>
              </div>
              
              <div class="column">
                <label class="label is-small">E-mail</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="email" 
                    v-model="formData.email"
                    placeholder="contato@clinica.com"
                  >
                </div>
              </div>
            </div>
            
            <div class="field">
              <label class="label is-small">Website</label>
              <div class="control">
                <input 
                  class="input" 
                  type="url" 
                  v-model="formData.website"
                  placeholder="https://www.clinica.com"
                >
              </div>
            </div>
          </div>

          <!-- Ativar configuração -->
          <div class="field">
            <div class="control">
              <label class="checkbox">
                <input 
                  type="checkbox" 
                  v-model="formData.ativo"
                >
                Ativar esta configuração imediatamente
              </label>
            </div>
          </div>
        </section>
        
        <footer class="modal-card-foot">
          <button 
            class="button is-success" 
            @click="salvarConfiguracao"
            :disabled="!isFormValid || loading"
          >
            <span v-if="loading" class="loader is-small"></span>
            <span v-else>{{ editando ? 'Atualizar' : 'Criar' }}</span>
          </button>
          <button class="button" @click="cancelarForm">Cancelar</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<style scoped>
.marca-admin {
  padding: 1rem;
}

.color-palette {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.color-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.color-swatch {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.loader {
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3498db;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  display: inline-block;
}

.loader.is-small {
  width: 16px;
  height: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.modal-card {
  max-width: 800px;
  width: 95%;
}

.modal-card-body {
  max-height: 80vh;
  overflow-y: auto;
}

.file-name {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 768px) {
  .columns {
    margin: 0;
  }
  
  .column {
    padding: 0.5rem;
  }
}
</style> 