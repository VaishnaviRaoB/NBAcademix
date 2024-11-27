# Generated by Django 5.0.6 on 2024-11-27 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0021_performancechart_avg_sgpa_v_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancechart',
            name='academic_performance_index',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='performancechart',
            name='avg_sgpa_i',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='performancechart',
            name='avg_sgpa_ii',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='performancechart',
            name='avg_sgpa_vii',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='performancechart',
            name='avg_sgpa_viii',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='performancechart',
            name='mean_percentage_successful',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='performancechart',
            name='total_successful_students',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='performancechart',
            name='avg_cgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='performancechart',
            name='detained_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='performancechart',
            name='performance',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminpage.studentperformance'),
        ),
        migrations.AlterField(
            model_name='performancechart',
            name='total_cgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='performancechart',
            name='total_students',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]