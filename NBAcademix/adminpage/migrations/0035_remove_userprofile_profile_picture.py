# Generated by Django 5.0.6 on 2024-12-13 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0034_userprofile_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
    ]
