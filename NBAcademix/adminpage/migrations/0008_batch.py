# Generated by Django 5.0.6 on 2024-11-14 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0007_remove_studentfile_batch_delete_batchyear_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
    ]
