# Generated by Django 5.2 on 2025-05-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0014_cliente_prazocontrato'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='vrunidade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
