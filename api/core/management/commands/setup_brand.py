from django.core.management.base import BaseCommand
from core.models import ConfiguracaoBrand


class Command(BaseCommand):
    help = 'Cria uma configuração de marca padrão'

    def add_arguments(self, parser):
        parser.add_argument(
            '--nome',
            type=str,
            default='AgendaVet',
            help='Nome do estabelecimento',
        )
        parser.add_argument(
            '--cor-primaria',
            type=str,
            default='#00d1b2',
            help='Cor primária em hexadecimal',
        )
        parser.add_argument(
            '--cor-secundaria',
            type=str,
            default='#363636',
            help='Cor secundária em hexadecimal',
        )

    def handle(self, *args, **options):
        # Verificar se já existe uma configuração ativa
        config_existente = ConfiguracaoBrand.objects.filter(ativo=True).first()
        
        if config_existente:
            self.stdout.write(
                self.style.WARNING(f'Já existe uma configuração ativa: {config_existente.nome_estabelecimento}')
            )
            return

        # Criar nova configuração
        config = ConfiguracaoBrand.objects.create(
            nome_estabelecimento=options['nome'],
            cor_primaria=options['cor_primaria'],
            cor_secundaria=options['cor_secundaria'],
            cor_accent='#3273dc',
            cor_background='#f5f5f5',
            ativo=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Configuração de marca criada com sucesso: {config.nome_estabelecimento}'
            )
        ) 