# Generated by Django 5.2 on 2025-04-30 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0012_remove_cliente_prazocontrato_cliente_przcontrato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='przcontrato',
        ),
    ]
