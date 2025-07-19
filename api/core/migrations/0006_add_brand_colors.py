from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_unify_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaobrand',
            name='cor_success',
            field=models.CharField(
                default='#48c774',
                help_text='Cor de sucesso/confirmação em formato hexadecimal (ex: #48c774)',
                max_length=7
            ),
        ),
        migrations.AddField(
            model_name='configuracaobrand',
            name='cor_danger',
            field=models.CharField(
                default='#f14668',
                help_text='Cor de erro/negação em formato hexadecimal (ex: #f14668)',
                max_length=7
            ),
        ),
        migrations.AddField(
            model_name='configuracaobrand',
            name='cor_warning',
            field=models.CharField(
                default='#ffdd57',
                help_text='Cor de aviso em formato hexadecimal (ex: #ffdd57)',
                max_length=7
            ),
        ),
        migrations.AddField(
            model_name='configuracaobrand',
            name='cor_info',
            field=models.CharField(
                default='#3298dc',
                help_text='Cor de informação em formato hexadecimal (ex: #3298dc)',
                max_length=7
            ),
        ),
        migrations.AddField(
            model_name='configuracaobrand',
            name='cor_texto',
            field=models.CharField(
                default='#363636',
                help_text='Cor principal do texto em formato hexadecimal (ex: #363636)',
                max_length=7
            ),
        ),
        migrations.AddField(
            model_name='configuracaobrand',
            name='cor_borda',
            field=models.CharField(
                default='#dbdbdb',
                help_text='Cor das bordas em formato hexadecimal (ex: #dbdbdb)',
                max_length=7
            ),
        ),
        migrations.AddField(
            model_name='configuracaobrand',
            name='cor_sombra',
            field=models.CharField(
                default='#000000',
                help_text='Cor das sombras em formato hexadecimal (ex: #000000)',
                max_length=7
            ),
        ),
    ] 