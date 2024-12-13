# Generated by Django 5.1 on 2024-12-06 01:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caregiver',
            fields=[
                ('caregiver_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('social_security_number', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True)),
                ('type', models.CharField(choices=[('Familial', 'Familial'), ('Independent', 'Independent')], max_length=25, null=True)),
                ('date_of_hire', models.DateField()),
                ('date_of_termination', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CaregiverCert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('CNA', 'CNA'), ('TEMP', 'TEMP')], max_length=15)),
                ('expiration_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('caregiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care_profiles.caregiver')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('social_security_number', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address_line_1', models.CharField(blank=True, max_length=255, null=True)),
                ('address_line_2', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('medical_history', models.TextField()),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('alternative_id', models.CharField(blank=True, max_length=100, null=True)),
                ('caregiver', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='care_profiles.caregiver')),
            ],
        ),
    ]
