import apiService from './api.js'

class PublicService {
  // Buscar serviços disponíveis
  async getServicos() {
    try {
      return await apiService.get('/servicos')
    } catch (error) {
      console.error('Erro ao buscar serviços:', error)
      // Retornar dados mockados em caso de erro
      return [
        {
          id: 1,
          nome: 'Consulta Veterinária',
          descricao: 'Consulta geral para avaliação da saúde do seu pet',
          preco: 80.00,
          duracao: 30
        },
        {
          id: 2,
          nome: 'Vacinação',
          descricao: 'Aplicação de vacinas essenciais',
          preco: 60.00,
          duracao: 15
        },
        {
          id: 3,
          nome: 'Exame de Sangue',
          descricao: 'Análise completa do sangue do animal',
          preco: 120.00,
          duracao: 45
        },
        {
          id: 4,
          nome: 'Banho e Tosa',
          descricao: 'Higiene e cuidados estéticos',
          preco: 50.00,
          duracao: 60
        }
      ]
    }
  }

  // Buscar profissionais
  async getProfissionais() {
    try {
      return await apiService.get('/profissionais')
    } catch (error) {
      console.error('Erro ao buscar profissionais:', error)
      // Retornar dados mockados em caso de erro
      return [
        {
          id: 1,
          nome: 'Dr. João Silva',
          especialidade: 'Clínico Geral',
          crmv: 'SP-12345',
          foto: null
        },
        {
          id: 2,
          nome: 'Dra. Maria Santos',
          especialidade: 'Cardiologia',
          crmv: 'SP-67890',
          foto: null
        },
        {
          id: 3,
          nome: 'Dr. Pedro Costa',
          especialidade: 'Ortopedia',
          crmv: 'SP-11111',
          foto: null
        }
      ]
    }
  }

  // Buscar horários de funcionamento
  async getHorariosFuncionamento() {
    try {
      return await apiService.get('/horarios-funcionamento')
    } catch (error) {
      console.error('Erro ao buscar horários:', error)
      // Retornar dados mockados em caso de erro
      return {
        segunda: { inicio: '08:00', fim: '18:00', aberto: true },
        terca: { inicio: '08:00', fim: '18:00', aberto: true },
        quarta: { inicio: '08:00', fim: '18:00', aberto: true },
        quinta: { inicio: '08:00', fim: '18:00', aberto: true },
        sexta: { inicio: '08:00', fim: '18:00', aberto: true },
        sabado: { inicio: '08:00', fim: '12:00', aberto: true },
        domingo: { inicio: '00:00', fim: '00:00', aberto: false }
      }
    }
  }

  // Buscar informações da clínica
  async getInfoClinica() {
    try {
      return await apiService.get('/clinica/info')
    } catch (error) {
      console.error('Erro ao buscar informações da clínica:', error)
      // Retornar dados mockados em caso de erro
      return {
        nome: 'AgendaVet',
        endereco: 'Rua das Flores, 123 - Centro',
        telefone: '(11) 99999-9999',
        email: 'contato@agendavet.com',
        descricao: 'Clínica veterinária especializada no cuidado e bem-estar dos seus pets.',
        sobre: 'Com mais de 10 anos de experiência, nossa clínica oferece atendimento de qualidade com profissionais especializados e equipamentos modernos.'
      }
    }
  }
}

export default new PublicService() 