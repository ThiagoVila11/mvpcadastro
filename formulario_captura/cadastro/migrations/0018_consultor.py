# Generated by Django 5.2 on 2025-05-06 20:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0017_cliente_apartamento_cliente_condominio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultorNome', models.CharField(blank=True, max_length=120, verbose_name='Nome')),
                ('consultorEmail', models.EmailField(help_text='Exemplo: usuario@provedor.com', max_length=255, unique=True, validators=[django.core.validators.EmailValidator(message='Digite um e-mail válido')], verbose_name='E-mail')),
                ('consultorTelefone', models.CharField(blank=True, null=True, verbose_name='Telefone')),
                ('consultorDataInicio', models.DateField(blank=True, null=True, verbose_name='Data de Início')),
                ('consultorAtivoInativo', models.CharField(choices=[('A', 'Ativo(a)'), ('I', 'Inativo(a)')], default='A', max_length=1, null=True, verbose_name='Ativo/Inativo')),
            ],
        ),
    ]
