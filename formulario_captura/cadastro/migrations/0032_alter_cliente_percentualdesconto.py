# Generated by Django 5.2 on 2025-05-14 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0031_cliente_datainiciodesconto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='percentualdesconto',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, verbose_name='Percentual de desconto'),
        ),
    ]
