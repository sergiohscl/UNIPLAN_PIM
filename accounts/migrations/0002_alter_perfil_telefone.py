# Generated by Django 5.0.4 on 2024-10-05 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='telefone',
            field=models.CharField(max_length=19),
        ),
    ]
