# Generated by Django 5.0.6 on 2024-12-18 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0035_remove_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='placementdetails',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]