# Generated by Django 3.2.16 on 2024-12-11 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0027_higherstudy_higherstudydocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='higherstudy',
            name='year',
            field=models.CharField(max_length=20),
        ),
    ]
