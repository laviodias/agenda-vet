from django.contrib import admin
from .models import Usuario, ConfiguracaoBrand


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'tipo_usuario', 'is_active', 'date_joined']
    list_filter = ['tipo_usuario', 'is_active', 'date_joined']
    search_fields = ['nome', 'email']
    ordering = ['-date_joined']


@admin.register(ConfiguracaoBrand)
class ConfiguracaoBrandAdmin(admin.ModelAdmin):
    list_display = ['nome_estabelecimento', 'ativo', 'atualizado_em']
    list_filter = ['ativo', 'criado_em', 'atualizado_em']
    search_fields = ['nome_estabelecimento']
    ordering = ['-atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_estabelecimento', 'logo', 'ativo')
        }),
        ('Paleta de Cores', {
            'fields': ('cor_primaria', 'cor_secundaria', 'cor_accent', 'cor_background'),
            'classes': ('collapse',)
        }),
        ('Informações de Contato', {
            'fields': ('endereco', 'telefone', 'email', 'website'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Garantir que apenas uma configuração esteja ativa
        """
        if obj.ativo:
            ConfiguracaoBrand.objects.filter(ativo=True).update(ativo=False)
        super().save_model(request, obj, form, change)
