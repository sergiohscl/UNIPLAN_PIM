# Generated by Django 5.0.4 on 2024-10-03 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(max_length=100)),
                ('icone', models.ImageField(blank=True, null=True, upload_to='icones')),
            ],
        ),
        migrations.CreateModel(
            name='PerfilDoctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=100)),
                ('crm', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('perfil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.perfil')),
                ('specialty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctors.specialties')),
            ],
        ),
        migrations.CreateModel(
            name='AvailableDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('scheduled', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.perfildoctor')),
            ],
        ),
    ]
