# Generated by Django 5.2 on 2025-04-25 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0003_rename_interesses_cliente_observacoes_cliente_apto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='imgcnh',
            field=models.ImageField(upload_to=''),
        ),
    ]
