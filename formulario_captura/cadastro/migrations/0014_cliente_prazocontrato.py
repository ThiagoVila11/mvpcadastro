# Generated by Django 5.2 on 2025-04-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0013_remove_cliente_przcontrato'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='prazocontrato',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
