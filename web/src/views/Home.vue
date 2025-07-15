<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AgendamentoForm from '../components/AgendamentoForm.vue';
import publicService from '../services/publicService.js'
import { useBrand } from '../composables/useBrand.js'

const router = useRouter()
const { brandConfig } = useBrand()

const servicos = ref([])
const profissionais = ref([])
const horariosFuncionamento = ref({})
const infoClinica = ref(null)

const loading = ref(true)
const loadingProfissionais = ref(true)
const loadingHorarios = ref(true)
const loadingInfo = ref(true)

const formatarDia = (dia) => {
  const dias = {
    segunda: 'Segunda-feira',
    terca: 'Terça-feira',
    quarta: 'Quarta-feira',
    quinta: 'Quinta-feira',
    sexta: 'Sexta-feira',
    sabado: 'Sábado',
    domingo: 'Domingo'
  }
  return dias[dia] || dia
}

const carregarDados = async () => {
  try {
    // Carregar dados em paralelo
    const [servicosData, profissionaisData, horariosData, infoData] = await Promise.all([
      publicService.getServicos(),
      publicService.getProfissionais(),
      publicService.getHorariosFuncionamento(),
      publicService.getInfoClinica()
    ])

    servicos.value = servicosData
    profissionais.value = profissionaisData
    horariosFuncionamento.value = horariosData
    infoClinica.value = infoData

  } catch (error) {
    console.error('Erro ao carregar dados da página inicial:', error)
  } finally {
    loading.value = false
    loadingProfissionais.value = false
    loadingHorarios.value = false
    loadingInfo.value = false
  }
}

onMounted(() => {
  carregarDados()
})

const goToAuth = () => {
  router.push('/auth')
}
</script>

<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero is-primary is-bold">
      <div class="hero-body">
        <div class="container">
          <div class="columns is-vcentered">
            <div class="column is-6">
              <!-- Logo e nome da clínica -->
              <div class="clinic-branding mb-4">
                <div v-if="brandConfig?.logo_url" class="clinic-logo mb-3">
                  <figure class="image is-96x96">
                    <img :src="brandConfig.logo_url" :alt="brandConfig.nome_estabelecimento" class="is-rounded">
                  </figure>
                </div>
                <h1 class="title is-1 has-text-white clinic-name">
                  {{ brandConfig?.nome_estabelecimento || 'AgendaVet' }}
                </h1>
              </div>
              
              <h2 class="title is-3 has-text-white">
                Cuidado especial para seu pet
              </h2>
              <p class="subtitle is-5 has-text-white-ter">
                Agende consultas veterinárias de forma simples e rápida. 
                Cuidamos da saúde do seu melhor amigo com carinho e profissionalismo.
              </p>
              <div class="buttons">
                <router-link to="/auth" class="button is-white is-medium">
                  <span class="icon">
                    <i class="fas fa-calendar-plus"></i>
                  </span>
                  <span>Agendar Consulta</span>
                </router-link>
                <a href="#servicos" class="button is-outlined is-white is-medium">
                  <span class="icon">
                    <i class="fas fa-stethoscope"></i>
                  </span>
                  <span>Nossos Serviços</span>
                </a>
              </div>
            </div>
            <div class="column is-6 has-text-centered">
              <div class="hero-image">
                <i class="fas fa-paw" style="font-size: 8rem; color: rgba(255,255,255,0.3);"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Serviços Section -->
    <section id="servicos" class="section">
      <div class="container">
        <div class="has-text-centered mb-6">
          <h2 class="title is-3">Nossos Serviços</h2>
          <p class="subtitle is-5 has-text-grey">
            Oferecemos uma ampla gama de serviços veterinários para cuidar do seu pet
          </p>
        </div>

        <div v-if="loading" class="has-text-centered">
          <div class="loader"></div>
          <p class="mt-3">Carregando serviços...</p>
        </div>

        <div v-else class="columns is-multiline">
          <div 
            v-for="servico in servicos" 
            :key="servico.id" 
            class="column is-4"
          >
            <div class="card service-card">
              <div class="card-content">
                <div class="service-icon has-text-centered mb-4">
                  <i class="fas fa-stethoscope" style="font-size: 3rem; color: #3273dc;"></i>
                </div>
                <h3 class="title is-4 has-text-centered">{{ servico.nome }}</h3>
                <p class="has-text-grey has-text-centered mb-4">
                  {{ servico.descricao }}
                </p>
                <div class="service-details has-text-centered">
                  <div class="price">
                    <span class="has-text-primary has-text-weight-bold">
                      R$ {{ servico.preco.toFixed(2) }}
                    </span>
                  </div>
                  <div class="duration has-text-grey">
                    <small>{{ servico.duracao }} minutos</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Profissionais Section -->
    <section class="section has-background-light">
      <div class="container">
        <div class="has-text-centered mb-6">
          <h2 class="title is-3">Nossa Equipe</h2>
          <p class="subtitle is-5 has-text-grey">
            Profissionais especializados e dedicados ao cuidado dos seus pets
          </p>
        </div>

        <div v-if="loadingProfissionais" class="has-text-centered">
          <div class="loader"></div>
          <p class="mt-3">Carregando profissionais...</p>
        </div>

        <div v-else class="columns is-multiline">
          <div 
            v-for="profissional in profissionais" 
            :key="profissional.id" 
            class="column is-4"
          >
            <div class="card professional-card">
              <div class="card-content has-text-centered">
                <div class="professional-avatar mb-4">
                  <figure class="image is-128x128 is-inline-block">
                    <img 
                      v-if="profissional.foto" 
                      :src="profissional.foto" 
                      :alt="profissional.nome"
                      class="is-rounded"
                    >
                    <div v-else class="avatar-placeholder is-rounded">
                      <i class="fas fa-user-md" style="font-size: 3rem; color: #ccc;"></i>
                    </div>
                  </figure>
                </div>
                <h3 class="title is-4">{{ profissional.nome }}</h3>
                <p class="subtitle is-6 has-text-grey">{{ profissional.especialidade }}</p>
                <p class="has-text-grey-light is-size-7">CRMV: {{ profissional.crmv }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Horários Section -->
    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-6">
            <h2 class="title is-3">Horários de Funcionamento</h2>
            <p class="subtitle is-5 has-text-grey mb-5">
              Estamos sempre prontos para atender você e seu pet
            </p>

            <div v-if="loadingHorarios" class="has-text-centered">
              <div class="loader"></div>
              <p class="mt-3">Carregando horários...</p>
            </div>

            <div v-else class="horarios-list">
              <div 
                v-for="(horario, dia) in horariosFuncionamento" 
                :key="dia"
                class="horario-item"
              >
                <div class="dia">{{ formatarDia(dia) }}</div>
                <div class="horario" :class="{ 'fechado': !horario.aberto }">
                  <span v-if="horario.aberto">
                    {{ horario.inicio }} - {{ horario.fim }}
                  </span>
                  <span v-else class="has-text-danger">Fechado</span>
                </div>
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="info-card">
              <h3 class="title is-4">Informações de Contato</h3>
              
              <div v-if="loadingInfo" class="has-text-centered">
                <div class="loader"></div>
                <p class="mt-3">Carregando informações...</p>
              </div>

              <div v-else class="contact-info">
                <!-- Usar dados da configuração de marca se disponíveis, senão usar dados da clínica -->
                <div v-if="brandConfig?.endereco || infoClinica?.endereco" class="contact-item">
                  <span class="icon has-text-primary">
                    <i class="fas fa-map-marker-alt"></i>
                  </span>
                  <span>{{ brandConfig?.endereco || infoClinica?.endereco }}</span>
                </div>
                
                <div v-if="brandConfig?.telefone || infoClinica?.telefone" class="contact-item">
                  <span class="icon has-text-primary">
                    <i class="fas fa-phone"></i>
                  </span>
                  <span>{{ brandConfig?.telefone || infoClinica?.telefone }}</span>
                </div>
                
                <div v-if="brandConfig?.email || infoClinica?.email" class="contact-item">
                  <span class="icon has-text-primary">
                    <i class="fas fa-envelope"></i>
                  </span>
                  <span>{{ brandConfig?.email || infoClinica?.email }}</span>
                </div>
                
                <div v-if="brandConfig?.website" class="contact-item">
                  <span class="icon has-text-primary">
                    <i class="fas fa-globe"></i>
                  </span>
                  <a :href="brandConfig.website" target="_blank" class="has-text-primary">
                    {{ brandConfig.website }}
                  </a>
                </div>
              </div>

              <div class="mt-5">
                <router-link to="/auth" class="button is-primary is-fullwidth">
                  <span class="icon">
                    <i class="fas fa-calendar-plus"></i>
                  </span>
                  <span>Agendar Consulta</span>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
  <AgendamentoForm />
</template>

<style scoped>
.hero {
  background: linear-gradient(135deg, var(--primary-color, #3273dc) 0%, var(--accent-color, #209cee) 100%);
  min-height: 60vh;
  display: flex;
  align-items: center;
}

.clinic-branding {
  text-align: center;
}

.clinic-logo {
  display: flex;
  justify-content: center;
}

.clinic-logo img {
  border: 3px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.clinic-name {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  margin-bottom: 0.5rem !important;
}

.hero-image {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.service-card {
  height: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.professional-card {
  height: 100%;
  transition: transform 0.3s ease;
  border-radius: 12px;
}

.professional-card:hover {
  transform: translateY(-5px);
}

.avatar-placeholder {
  width: 128px;
  height: 128px;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #e0e0e0;
}

.horarios-list {
  max-width: 400px;
}

.horario-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.horario-item:last-child {
  border-bottom: none;
}

.dia {
  font-weight: 600;
  color: #333;
}

.horario {
  color: #3273dc;
  font-weight: 500;
}

.horario.fechado {
  color: #ff3860;
}

.info-card {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 12px;
  height: 100%;
}

.contact-info {
  margin-top: 1.5rem;
}

.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  gap: 0.75rem;
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3273dc;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .hero {
    min-height: 50vh;
  }
  
  .hero .title {
    font-size: 1.75rem;
  }
  
  .hero .subtitle {
    font-size: 1.1rem;
  }
}
</style> 