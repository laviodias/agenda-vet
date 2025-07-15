import { ref, onMounted } from 'vue'
import brandService from '../services/brandService.js'

const brandConfig = ref(null)
const isLoading = ref(false)

export function useBrand() {
  // Carregar configuração de marca
  const loadBrandConfig = async () => {
    isLoading.value = true
    try {
      const config = await brandService.getConfiguracaoAtiva()
      brandConfig.value = config
      
      // Aplicar tema automaticamente
      if (config) {
        brandService.aplicarTema(config)
      }
      
      return config
    } catch (error) {
      console.error('Erro ao carregar configuração de marca:', error)
      
      // Tentar carregar do localStorage como fallback
      const localConfig = brandService.carregarTemaLocal()
      if (localConfig) {
        brandConfig.value = localConfig
        return localConfig
      }
      
      // Se nada funcionar, usar configuração padrão
      const defaultConfig = {
        nome_estabelecimento: 'AgendaVet',
        cor_primaria: '#00d1b2',
        cor_secundaria: '#363636',
        cor_accent: '#3273dc',
        cor_background: '#f5f5f5',
        logo_url: null
      }
      brandConfig.value = defaultConfig
      brandService.aplicarTema(defaultConfig)
      return defaultConfig
    } finally {
      isLoading.value = false
    }
  }

  // Atualizar configuração de marca
  const updateBrandConfig = (newConfig) => {
    brandConfig.value = newConfig
    brandService.aplicarTema(newConfig)
  }

  // Inicializar na primeira chamada
  onMounted(() => {
    if (!brandConfig.value) {
      loadBrandConfig()
    }
  })

  return {
    brandConfig,
    isLoading,
    loadBrandConfig,
    updateBrandConfig
  }
} 