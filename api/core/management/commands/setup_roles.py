from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Role, Permission, RolePermission, Usuario, UserRole


class Command(BaseCommand):
    help = 'Setup inicial de roles e permissões do sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Remove todos os roles e permissões existentes antes de criar novos',
        )
        parser.add_argument(
            '--assign-superuser',
            action='store_true',
            help='Atribui role de admin para todos os superusuários existentes',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando setup de roles e permissões...'))

        with transaction.atomic():
            if options['reset']:
                self.stdout.write('Removendo roles e permissões existentes...')
                UserRole.objects.all().delete()
                RolePermission.objects.all().delete()
                Role.objects.all().delete()
                Permission.objects.all().delete()

            # Criar permissões
            self.create_permissions()
            
            # Criar roles
            self.create_roles()
            
            # Atribuir permissões aos roles
            self.assign_permissions_to_roles()
            
            # Atribuir roles aos superusuários se solicitado
            if options['assign_superuser']:
                self.assign_admin_role_to_superusers()

        self.stdout.write(self.style.SUCCESS('Setup de roles e permissões concluído com sucesso!'))

    def create_permissions(self):
        """Criar todas as permissões do sistema"""
        self.stdout.write('Criando permissões...')
        
        permissions_data = [
            # Usuários
            ('usuarios', 'create', 'Criar novos usuários'),
            ('usuarios', 'read', 'Visualizar dados dos usuários'),
            ('usuarios', 'update', 'Editar dados dos usuários'),
            ('usuarios', 'delete', 'Excluir usuários'),
            ('usuarios', 'list', 'Listar todos os usuários'),
            ('usuarios', 'manage', 'Gerenciar usuários completamente'),
            
            # Agendamentos
            ('agendamentos', 'create', 'Criar novos agendamentos'),
            ('agendamentos', 'read', 'Visualizar agendamentos'),
            ('agendamentos', 'update', 'Editar agendamentos'),
            ('agendamentos', 'delete', 'Cancelar agendamentos'),
            ('agendamentos', 'list', 'Listar todos os agendamentos'),
            ('agendamentos', 'manage', 'Gerenciar agenda e disponibilidade'),
            
            # Animais
            ('animais', 'create', 'Registrar novos animais'),
            ('animais', 'read', 'Visualizar dados dos animais'),
            ('animais', 'update', 'Editar dados dos animais'),
            ('animais', 'delete', 'Excluir registros de animais'),
            ('animais', 'list', 'Listar todos os animais'),
            ('animais', 'manage', 'Gerenciar cadastro de animais'),
            
            # Serviços
            ('servicos', 'create', 'Criar novos serviços'),
            ('servicos', 'read', 'Visualizar serviços'),
            ('servicos', 'update', 'Editar serviços'),
            ('servicos', 'delete', 'Excluir serviços'),
            ('servicos', 'list', 'Listar todos os serviços'),
            ('servicos', 'manage', 'Gerenciar catálogo de serviços'),
            
            # Configurações
            ('configuracoes', 'read', 'Visualizar configurações'),
            ('configuracoes', 'update', 'Editar configurações'),
            ('configuracoes', 'manage', 'Gerenciar configurações do sistema'),
            
            # Relatórios
            ('relatorios', 'read', 'Visualizar relatórios'),
            ('relatorios', 'create', 'Gerar relatórios'),
            ('relatorios', 'manage', 'Gerenciar relatórios'),
            
            # Marca/Branding
            ('brand', 'read', 'Visualizar configurações de marca'),
            ('brand', 'create', 'Criar configurações de marca'),
            ('brand', 'update', 'Editar configurações de marca'),
            ('brand', 'delete', 'Excluir configurações de marca'),
            ('brand', 'manage', 'Gerenciar marca e identidade visual'),
        ]

        for resource, action, description in permissions_data:
            permission, created = Permission.objects.get_or_create(
                resource=resource,
                action=action,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'  ✓ Criada permissão: {permission}')

    def create_roles(self):
        """Criar roles do sistema"""
        self.stdout.write('Criando roles...')
        
        roles_data = [
            (
                'admin',
                'Administrador',
                'Acesso total ao sistema. Pode gerenciar usuários, configurações e todos os recursos.'
            ),
            (
                'veterinario',
                'Veterinário',
                'Profissional veterinário. Pode gerenciar agendamentos, animais e serviços.'
            ),
            (
                'recepcionista',
                'Recepcionista',
                'Funcionário da recepção. Pode gerenciar agendamentos e visualizar informações básicas.'
            ),
            (
                'cliente',
                'Cliente',
                'Cliente da clínica. Pode agendar serviços e visualizar seus próprios dados.'
            ),
        ]

        for name, display_name, description in roles_data:
            role, created = Role.objects.get_or_create(
                name=name,
                defaults={
                    'display_name': display_name,
                    'description': description,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ Criado role: {role}')

    def assign_permissions_to_roles(self):
        """Atribuir permissões aos roles"""
        self.stdout.write('Atribuindo permissões aos roles...')

        # Administrador - todas as permissões
        admin_role = Role.objects.get(name='admin')
        all_permissions = Permission.objects.all()
        for permission in all_permissions:
            RolePermission.objects.get_or_create(
                role=admin_role,
                permission=permission
            )
        self.stdout.write(f'  ✓ Admin: {all_permissions.count()} permissões')

        # Veterinário - permissões de gestão clínica
        vet_role = Role.objects.get(name='veterinario')
        vet_permissions = Permission.objects.filter(
            resource__in=['agendamentos', 'animais', 'servicos'],
            action__in=['create', 'read', 'update', 'list', 'manage']
        )
        for permission in vet_permissions:
            RolePermission.objects.get_or_create(
                role=vet_role,
                permission=permission
            )
        self.stdout.write(f'  ✓ Veterinário: {vet_permissions.count()} permissões')

        # Recepcionista - permissões de atendimento
        recep_role = Role.objects.get(name='recepcionista')
        recep_permissions = Permission.objects.filter(
            resource__in=['agendamentos', 'animais', 'usuarios'],
            action__in=['create', 'read', 'update', 'list']
        )
        for permission in recep_permissions:
            RolePermission.objects.get_or_create(
                role=recep_role,
                permission=permission
            )
        self.stdout.write(f'  ✓ Recepcionista: {recep_permissions.count()} permissões')

        # Cliente - permissões básicas
        client_role = Role.objects.get(name='cliente')
        client_permissions = Permission.objects.filter(
            resource__in=['agendamentos', 'animais'],
            action__in=['create', 'read']
        )
        for permission in client_permissions:
            RolePermission.objects.get_or_create(
                role=client_role,
                permission=permission
            )
        self.stdout.write(f'  ✓ Cliente: {client_permissions.count()} permissões')

    def assign_admin_role_to_superusers(self):
        """Atribuir role de admin para superusuários"""
        self.stdout.write('Atribuindo role de admin para superusuários...')
        
        admin_role = Role.objects.get(name='admin')
        superusers = Usuario.objects.filter(is_superuser=True)
        
        for user in superusers:
            user_role, created = UserRole.objects.get_or_create(
                user=user,
                role=admin_role,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'  ✓ Role admin atribuído para: {user.nome}')
            else:
                self.stdout.write(f'  - {user.nome} já possui role admin')

    def migrate_existing_users(self):
        """Migrar usuários existentes para o sistema de roles"""
        self.stdout.write('Migrando usuários existentes...')
        
        # Mapear tipos de usuário para roles
        tipo_to_role = {
            'admin': 'admin',
            'veterinario': 'veterinario',
            'cliente': 'cliente',
        }
        
        for user in Usuario.objects.all():
            # Pular se já tem roles atribuídos
            if user.user_roles.exists():
                continue
                
            # Determinar role baseado no tipo_usuario
            role_name = tipo_to_role.get(user.tipo_usuario, 'cliente')
            
            try:
                role = Role.objects.get(name=role_name)
                UserRole.objects.create(
                    user=user,
                    role=role,
                    is_active=True
                )
                self.stdout.write(f'  ✓ {user.nome} → {role.display_name}')
            except Role.DoesNotExist:
                self.stdout.write(f'  ✗ Role {role_name} não encontrado para {user.nome}') 