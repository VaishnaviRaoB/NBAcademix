# Generated by Django 5.0.6 on 2024-11-24 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0011_performancedocument_studentperformance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentdocument',
            name='batch',
        ),
        migrations.DeleteModel(
            name='StudentBatch',
        ),
        migrations.DeleteModel(
            name='AcademicYear',
        ),
        migrations.DeleteModel(
            name='StudentDocument',
        ),
    ]