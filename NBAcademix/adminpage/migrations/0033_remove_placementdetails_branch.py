# Generated by Django 5.0.6 on 2024-12-12 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0032_higherstudy_higherstudydocument'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placementdetails',
            name='branch',
        ),
    ]
