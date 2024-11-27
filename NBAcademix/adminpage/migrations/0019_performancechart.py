# Generated by Django 5.0.6 on 2024-11-27 03:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0018_achievement_achievementdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chart_image', models.TextField(blank=True, null=True)),
                ('avg_cgpa', models.FloatField(null=True)),
                ('avg_sgpa_iii', models.FloatField(null=True)),
                ('avg_sgpa_iv', models.FloatField(null=True)),
                ('total_students', models.IntegerField(default=0)),
                ('total_cgpa', models.FloatField(null=True)),
                ('detained_count', models.IntegerField(default=0)),
                ('performance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='performance_chart', to='adminpage.studentperformance')),
            ],
        ),
    ]