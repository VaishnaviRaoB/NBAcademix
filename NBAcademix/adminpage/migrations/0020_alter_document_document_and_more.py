# Generated by Django 5.0.6 on 2024-11-27 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0019_performancechart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='performance_documents/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='original_filename',
            field=models.CharField(max_length=255),
        ),
    ]
