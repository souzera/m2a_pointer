# Generated by Django 5.1.4 on 2025-01-02 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointer', '0004_alter_ponto_entrada_alter_ponto_saida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ponto',
            name='entrada',
            field=models.TimeField(auto_created=True, auto_now=True),
        ),
    ]
