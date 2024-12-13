# Generated by Django 5.1 on 2024-12-06 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care_profiles', '0004_task_type_patientevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='careplantask',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='careplantask',
            name='time_spent',
        ),
        migrations.AddField(
            model_name='careplantask',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='careplantask',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='careplantask',
            name='day_of_week',
            field=models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='careplantask',
            name='frequency',
            field=models.CharField(choices=[('Once', 'Once'), ('Daily', 'Daily'), ('Weekly', 'Weekly')], default='Daily', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='careplantask',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='CarePlanTaskEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date_time', models.DateTimeField()),
                ('is_completed', models.BooleanField(default=False)),
                ('time_spent', models.DurationField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('care_plan_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='care_profiles.careplantask')),
            ],
        ),
    ]
