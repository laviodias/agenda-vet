from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta, time
from core.models import Empresa, ConfiguracaoBrand, Role, Permission, RolePermission, UserRole
from servicos.models import Servico
from animais.models import Animal
from agendamentos.models import Agendamento
from usuarios.models import Usuario

User = get_user_model()

class Command(BaseCommand):
    help = 'Configura dados iniciais da aplicação'

    def handle(self, *args, **options):
        self.stdout.write('Configurando dados iniciais...')
        
        # Criar empresa padrão
        empresa, created = Empresa.objects.get_or_create(
            nome='AgendaVet',
            defaults={
                'cnpj': '00.000.000/0001-00',
                'endereco': 'Rua das Flores, 123 - Centro',
                'telefone': '(11) 99999-9999',
                'email': 'contato@agendavet.com',
                'descricao': 'Clínica veterinária especializada no cuidado e bem-estar dos seus pets.',
                'sobre': 'Com mais de 10 anos de experiência, nossa clínica oferece atendimento de qualidade com profissionais especializados e equipamentos modernos.'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Empresa criada com sucesso'))
        else:
            self.stdout.write('Empresa já existe')
        
        # Criar usuário admin
        admin_user, created = Usuario.objects.get_or_create(
            username='admin@agendavet.com',
            defaults={
                'email': 'admin@agendavet.com',
                'nome': 'Administrador',
                'tipo': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Usuário admin criado com sucesso'))
        else:
            self.stdout.write('Usuário admin já existe')

        # Atribuir role de admin ao usuário admin
        try:
            admin_role = Role.objects.get(name='admin')
            UserRole.objects.get_or_create(user=admin_user, role=admin_role, defaults={'is_active': True})
            self.stdout.write(self.style.SUCCESS('Role admin atribuído ao usuário admin'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao atribuir role admin: {e}'))
        
        # Criar usuários clientes de teste
        clientes_data = [
            {
                'username': 'cliente@email.com',
                'email': 'cliente@email.com',
                'nome': 'Cliente Teste',
                'tipo': 'cliente',
                'telefone': '(11) 99999-9999'
            },
            {
                'username': 'maria.silva@email.com',
                'email': 'maria.silva@email.com',
                'nome': 'Maria Silva',
                'tipo': 'cliente',
                'telefone': '(11) 88888-8888'
            },
            {
                'username': 'carlos.santos@email.com',
                'email': 'carlos.santos@email.com',
                'nome': 'Carlos Santos',
                'tipo': 'cliente',
                'telefone': '(11) 77777-7777'
            }
        ]
        
        clientes_criados = []
        for cliente_data in clientes_data:
            cliente, created = Usuario.objects.get_or_create(
                username=cliente_data['username'],
                defaults=cliente_data
            )
            
            if created:
                cliente.set_password('cliente123')
                cliente.save()
                clientes_criados.append(cliente)
                self.stdout.write(f'Cliente {cliente.nome} criado com sucesso')
            else:
                clientes_criados.append(cliente)
                self.stdout.write(f'Cliente {cliente.nome} já existe')
        
        # Criar profissionais
        profissionais_data = [
            {
                'username': 'joao.silva@agendavet.com',
                'email': 'joao.silva@agendavet.com',
                'nome': 'Dr. João Silva',
                'tipo': 'profissional',
                'especialidade': 'Clínico Geral',
                'crmv': 'SP-12345',
                'telefone': '(11) 11111-1111'
            },
            {
                'username': 'maria.santos@agendavet.com',
                'email': 'maria.santos@agendavet.com',
                'nome': 'Dra. Maria Santos',
                'tipo': 'profissional',
                'especialidade': 'Cardiologia',
                'crmv': 'SP-67890',
                'telefone': '(11) 22222-2222'
            },
            {
                'username': 'pedro.costa@agendavet.com',
                'email': 'pedro.costa@agendavet.com',
                'nome': 'Dr. Pedro Costa',
                'tipo': 'profissional',
                'especialidade': 'Ortopedia',
                'crmv': 'SP-11111',
                'telefone': '(11) 33333-3333'
            },
            {
                'username': 'ana.oliveira@agendavet.com',
                'email': 'ana.oliveira@agendavet.com',
                'nome': 'Dra. Ana Oliveira',
                'tipo': 'profissional',
                'especialidade': 'Dermatologia',
                'crmv': 'SP-44444',
                'telefone': '(11) 44444-4444'
            }
        ]
        
        profissionais_criados = []
        for prof_data in profissionais_data:
            profissional, created = Usuario.objects.get_or_create(
                username=prof_data['username'],
                defaults=prof_data
            )
            
            if created:
                profissional.set_password('prof123')
                profissional.save()
                profissionais_criados.append(profissional)
                self.stdout.write(f'Profissional {profissional.nome} criado com sucesso')
            else:
                profissionais_criados.append(profissional)
                self.stdout.write(f'Profissional {profissional.nome} já existe')
        
        # Criar serviços
        servicos_data = [
            {
                'nome': 'Consulta Veterinária',
                'descricao': 'Consulta geral para avaliação da saúde do seu pet',
                'preco': 80.00,
                'duracao': 30
            },
            {
                'nome': 'Vacinação',
                'descricao': 'Aplicação de vacinas essenciais',
                'preco': 60.00,
                'duracao': 15
            },
            {
                'nome': 'Exame de Sangue',
                'descricao': 'Análise completa do sangue do animal',
                'preco': 120.00,
                'duracao': 45
            },
            {
                'nome': 'Banho e Tosa',
                'descricao': 'Higiene e cuidados estéticos',
                'preco': 50.00,
                'duracao': 60
            },
            {
                'nome': 'Cirurgia',
                'descricao': 'Procedimentos cirúrgicos diversos',
                'preco': 500.00,
                'duracao': 120
            },
            {
                'nome': 'Radiografia',
                'descricao': 'Exame de imagem para diagnóstico',
                'preco': 150.00,
                'duracao': 30
            },
            {
                'nome': 'Ultrassom',
                'descricao': 'Exame de ultrassonografia',
                'preco': 200.00,
                'duracao': 45
            },
            {
                'nome': 'Emergência',
                'descricao': 'Atendimento de emergência 24h',
                'preco': 300.00,
                'duracao': 60
            }
        ]
        
        servicos_criados = []
        for servico_data in servicos_data:
            servico, created = Servico.objects.get_or_create(
                nome=servico_data['nome'],
                defaults={
                    **servico_data,
                    'empresa': empresa
                }
            )
            
            if created:
                servicos_criados.append(servico)
                self.stdout.write(f'Serviço {servico.nome} criado com sucesso')
            else:
                servicos_criados.append(servico)
                self.stdout.write(f'Serviço {servico.nome} já existe')
        
        # Criar animais para os clientes
        animais_data = [
            {
                'nome': 'Rex',
                'especie': 'Cão',
                'raca': 'Labrador',
                'data_nascimento': '2020-03-15',
                'peso': 25.5,
                'observacoes': 'Cão muito dócil e brincalhão'
            },
            {
                'nome': 'Luna',
                'especie': 'Gato',
                'raca': 'Persa',
                'data_nascimento': '2021-07-20',
                'peso': 4.2,
                'observacoes': 'Gata tranquila, gosta de carinho'
            },
            {
                'nome': 'Thor',
                'especie': 'Cão',
                'raca': 'Pastor Alemão',
                'data_nascimento': '2019-11-10',
                'peso': 35.0,
                'observacoes': 'Cão protetor e inteligente'
            },
            {
                'nome': 'Mia',
                'especie': 'Gato',
                'raca': 'Siamês',
                'data_nascimento': '2022-01-05',
                'peso': 3.8,
                'observacoes': 'Gata curiosa e ativa'
            },
            {
                'nome': 'Buddy',
                'especie': 'Cão',
                'raca': 'Golden Retriever',
                'data_nascimento': '2020-09-12',
                'peso': 28.0,
                'observacoes': 'Cão muito amigável com crianças'
            }
        ]
        
        animais_criados = []
        for i, animal_data in enumerate(animais_data):
            animal, created = Animal.objects.get_or_create(
                nome=animal_data['nome'],
                dono=clientes_criados[i % len(clientes_criados)],  # Usar módulo para distribuir entre os clientes
                defaults={
                    **animal_data,
                    'empresa': empresa
                }
            )
            
            if created:
                animais_criados.append(animal)
                self.stdout.write(f'Animal {animal.nome} criado com sucesso')
            else:
                animais_criados.append(animal)
                self.stdout.write(f'Animal {animal.nome} já existe')
        
        # Criar agendamentos de exemplo
        self.stdout.write('Criando agendamentos de exemplo...')
        
        # Verificar se já existem agendamentos
        if Agendamento.objects.exists():
            self.stdout.write('Agendamentos já existem, pulando criação...')
        else:
            # Criar agendamentos para os próximos dias
            data_atual = timezone.now().date()
            agendamentos_exemplo = [
                {
                    'data_hora': data_atual + timedelta(days=1, hours=9),
                    'servico': servicos_criados[0],  # Consulta
                    'animal': animais_criados[0],    # Rex
                    'cliente': clientes_criados[0]  # Cliente Teste
                },
                {
                    'data_hora': data_atual + timedelta(days=2, hours=14),
                    'servico': servicos_criados[1],  # Vacinação
                    'animal': animais_criados[1],    # Luna
                    'cliente': clientes_criados[1]  # Maria Silva
                },
                {
                    'data_hora': data_atual + timedelta(days=3, hours=10),
                    'servico': servicos_criados[2],  # Exame de Sangue
                    'animal': animais_criados[2],    # Thor
                    'cliente': clientes_criados[2]  # Carlos Santos
                },
                {
                    'data_hora': data_atual + timedelta(days=4, hours=15),
                    'servico': servicos_criados[3],  # Banho e Tosa
                    'animal': animais_criados[3],    # Mia
                    'cliente': clientes_criados[0]  # Cliente Teste
                },
                {
                    'data_hora': data_atual + timedelta(days=5, hours=11),
                    'servico': servicos_criados[0],  # Consulta
                    'animal': animais_criados[4],    # Buddy
                    'cliente': clientes_criados[1]  # Maria Silva
                }
            ]
            
            for agendamento_data in agendamentos_exemplo:
                # Usar get_or_create com tratamento de exceção para evitar duplicatas
                try:
                    agendamento, created = Agendamento.objects.get_or_create(
                        empresa=empresa,
                        data_hora=agendamento_data['data_hora'],
                        animal=agendamento_data['animal'],
                        defaults=agendamento_data
                    )
                    
                    if created:
                        self.stdout.write(f'Agendamento criado: {agendamento.animal.nome} - {agendamento.servico.nome} - {agendamento.data_hora}')
                    else:
                        self.stdout.write(f'Agendamento já existe: {agendamento.animal.nome} - {agendamento.servico.nome} - {agendamento.data_hora}')
                except Exception as e:
                    # Se houver erro de constraint única, apenas ignorar
                    self.stdout.write(f'Agendamento já existe (erro ignorado): {agendamento_data["animal"].nome} - {agendamento_data["servico"].nome} - {agendamento_data["data_hora"]}')
        
        self.stdout.write(self.style.SUCCESS('Configuração inicial concluída!')) 