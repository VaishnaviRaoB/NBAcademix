# Generated by Django 5.0.6 on 2024-11-24 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0012_remove_studentdocument_batch_delete_studentbatch_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PerformanceDocument',
            new_name='Document',
        ),
    ]
