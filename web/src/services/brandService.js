import apiService from './api.js'

class BrandService {
  // Buscar configuração de marca ativa
  async getConfiguracaoAtiva() {
    try {
      return await apiService.get('/brand/ativa/')
    } catch (error) {
      console.error('Erro ao buscar configuração de marca:', error)
      // Retornar configuração padrão em caso de erro
      return {
        nome_estabelecimento: 'AgendaVet',
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
        logo_url: null,
        endereco: '',
        telefone: '',
        email: '',
        website: ''
      }
    }
  }

  // Listar todas as configurações de marca
  async getTodasConfiguracoes() {
    try {
      return await apiService.get('/brand/')
    } catch (error) {
      console.error('Erro ao buscar configurações:', error)
      throw error
    }
  }

  // Criar nova configuração de marca
  async criarConfiguracao(configuracaoData) {
    try {
      return await apiService.post('/brand/', configuracaoData)
    } catch (error) {
      console.error('Erro ao criar configuração:', error)
      throw error
    }
  }

  // Atualizar configuração de marca
  async atualizarConfiguracao(id, configuracaoData) {
    try {
      return await apiService.put(`/brand/${id}/`, configuracaoData)
    } catch (error) {
      console.error('Erro ao atualizar configuração:', error)
      throw error
    }
  }

  // Ativar uma configuração específica
  async ativarConfiguracao(id) {
    try {
      return await apiService.post(`/brand/${id}/ativar/`)
    } catch (error) {
      console.error('Erro ao ativar configuração:', error)
      throw error
    }
  }

  // Deletar configuração de marca
  async deletarConfiguracao(id) {
    try {
      return await apiService.delete(`/brand/${id}/`)
    } catch (error) {
      console.error('Erro ao deletar configuração:', error)
      throw error
    }
  }

  // Upload de logo
  async uploadLogo(id, logoFile) {
    try {
      const formData = new FormData()
      formData.append('logo', logoFile)
      
      // Usar endpoint específico para upload de logo
      return await apiService.patch(`/brand/${id}/upload_logo/`, formData)
    } catch (error) {
      console.error('Erro ao fazer upload do logo:', error)
      throw error
    }
  }

  // Aplicar configuração de marca no CSS
  aplicarTema(configuracao) {
    const root = document.documentElement
    
    // Aplicar cores CSS principais
    root.style.setProperty('--primary-color', configuracao.cor_primaria)
    root.style.setProperty('--secondary-color', configuracao.cor_secundaria)
    root.style.setProperty('--accent-color', configuracao.cor_accent)
    root.style.setProperty('--background-color', configuracao.cor_background)
    
    // Aplicar cores de status e feedback
    root.style.setProperty('--success-color', configuracao.cor_success)
    root.style.setProperty('--danger-color', configuracao.cor_danger)
    root.style.setProperty('--warning-color', configuracao.cor_warning)
    root.style.setProperty('--info-color', configuracao.cor_info)
    
    // Aplicar cores de interface
    root.style.setProperty('--text-color', configuracao.cor_texto)
    root.style.setProperty('--border-color', configuracao.cor_borda)
    root.style.setProperty('--shadow-color', configuracao.cor_sombra)
    
    // Manter compatibilidade com o sistema anterior
    root.style.setProperty('--primary', configuracao.cor_primaria)
    root.style.setProperty('--secondary', configuracao.cor_secundaria)
    root.style.setProperty('--background', configuracao.cor_background)
    root.style.setProperty('--text', configuracao.cor_texto)
    
    // Preview de cores para o formulário
    root.style.setProperty('--preview-primary', configuracao.cor_primaria)
    root.style.setProperty('--preview-secondary', configuracao.cor_secundaria)
    root.style.setProperty('--preview-accent', configuracao.cor_accent)
    root.style.setProperty('--preview-background', configuracao.cor_background)
    root.style.setProperty('--preview-success', configuracao.cor_success)
    root.style.setProperty('--preview-danger', configuracao.cor_danger)
    root.style.setProperty('--preview-warning', configuracao.cor_warning)
    root.style.setProperty('--preview-info', configuracao.cor_info)
    
    // Atualizar título da página
    document.title = configuracao.nome_estabelecimento || 'AgendaVet'
    
    // Atualizar favicon se houver logo
    if (configuracao.logo_url) {
      let favicon = document.querySelector('link[rel="icon"]')
      if (!favicon) {
        favicon = document.createElement('link')
        favicon.rel = 'icon'
        document.head.appendChild(favicon)
      }
      favicon.href = configuracao.logo_url
    }
    
    // Armazenar configuração no localStorage para persistência
    localStorage.setItem('brandConfig', JSON.stringify(configuracao))
  }

  // Carregar configuração salva do localStorage
  carregarTemaLocal() {
    try {
      const configSalva = localStorage.getItem('brandConfig')
      if (configSalva) {
        const configuracao = JSON.parse(configSalva)
        this.aplicarTema(configuracao)
        return configuracao
      }
    } catch (error) {
      console.error('Erro ao carregar tema local:', error)
    }
    return null
  }

  // Validar formato de cor hexadecimal
  validarCorHex(cor) {
    const regex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/
    return regex.test(cor)
  }
}

export default new BrandService() 