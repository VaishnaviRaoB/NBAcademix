# Generated by Django 5.0.6 on 2024-12-19 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0038_offerletter_original_filename'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='placementdetails',
            index=models.Index(fields=['name'], name='adminpage_p_name_7039a0_idx'),
        ),
        migrations.AddIndex(
            model_name='placementdetails',
            index=models.Index(fields=['usn'], name='adminpage_p_usn_b81809_idx'),
        ),
        migrations.AddIndex(
            model_name='placementdetails',
            index=models.Index(fields=['company_name'], name='adminpage_p_company_a31b9d_idx'),
        ),
        migrations.AddIndex(
            model_name='placementdetails',
            index=models.Index(fields=['passout_year'], name='adminpage_p_passout_0665db_idx'),
        ),
    ]
