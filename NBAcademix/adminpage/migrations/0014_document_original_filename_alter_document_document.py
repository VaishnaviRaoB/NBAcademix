# Generated by Django 5.0.6 on 2024-11-24 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0013_rename_performancedocument_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='original_filename',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='documents/'),
        ),
    ]
