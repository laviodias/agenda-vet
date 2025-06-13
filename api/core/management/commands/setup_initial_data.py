from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Empresa
from servicos.models import Servico
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
                'telefone': '(11) 99999-9999'
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
        
        # Criar usuário cliente de teste
        cliente_user, created = Usuario.objects.get_or_create(
            username='cliente@email.com',
            defaults={
                'email': 'cliente@email.com',
                'nome': 'Cliente Teste',
                'tipo': 'cliente',
                'telefone': '(11) 99999-9999'
            }
        )
        
        if created:
            cliente_user.set_password('cliente123')
            cliente_user.save()
            self.stdout.write(self.style.SUCCESS('Usuário cliente criado com sucesso'))
        else:
            self.stdout.write('Usuário cliente já existe')
        
        # Criar profissionais
        profissionais_data = [
            {
                'username': 'joao.silva@agendavet.com',
                'email': 'joao.silva@agendavet.com',
                'nome': 'Dr. João Silva',
                'tipo': 'profissional',
                'especialidade': 'Clínico Geral',
                'crmv': 'SP-12345'
            },
            {
                'username': 'maria.santos@agendavet.com',
                'email': 'maria.santos@agendavet.com',
                'nome': 'Dra. Maria Santos',
                'tipo': 'profissional',
                'especialidade': 'Cardiologia',
                'crmv': 'SP-67890'
            },
            {
                'username': 'pedro.costa@agendavet.com',
                'email': 'pedro.costa@agendavet.com',
                'nome': 'Dr. Pedro Costa',
                'tipo': 'profissional',
                'especialidade': 'Ortopedia',
                'crmv': 'SP-11111'
            }
        ]
        
        for prof_data in profissionais_data:
            profissional, created = Usuario.objects.get_or_create(
                username=prof_data['username'],
                defaults=prof_data
            )
            
            if created:
                profissional.set_password('prof123')
                profissional.save()
                self.stdout.write(f'Profissional {profissional.nome} criado com sucesso')
            else:
                self.stdout.write(f'Profissional {profissional.nome} já existe')
        
        # Criar serviços
        servicos_data = [
            {
                'nome': 'Consulta Veterinária',
                'descricao': 'Consulta geral para avaliação da saúde do seu pet',
                'preco': 80.00
            },
            {
                'nome': 'Vacinação',
                'descricao': 'Aplicação de vacinas essenciais',
                'preco': 60.00
            },
            {
                'nome': 'Exame de Sangue',
                'descricao': 'Análise completa do sangue do animal',
                'preco': 120.00
            },
            {
                'nome': 'Banho e Tosa',
                'descricao': 'Higiene e cuidados estéticos',
                'preco': 50.00
            }
        ]
        
        for servico_data in servicos_data:
            servico, created = Servico.objects.get_or_create(
                nome=servico_data['nome'],
                defaults={
                    **servico_data,
                    'empresa': empresa
                }
            )
            
            if created:
                self.stdout.write(f'Serviço {servico.nome} criado com sucesso')
            else:
                self.stdout.write(f'Serviço {servico.nome} já existe')
        
        self.stdout.write(self.style.SUCCESS('Configuração inicial concluída!')) 