# Generated by Django 3.1.6 on 2021-03-24 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0002_drivers_incedence_licenseplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licenseplate',
            name='crime_case_count',
            field=models.IntegerField(),
        ),
    ]
