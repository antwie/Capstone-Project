# Generated by Django 3.1.6 on 2021-03-24 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0003_auto_20210324_1043'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='drivers',
            table='Driver',
        ),
        migrations.AlterModelTable(
            name='licenseplate',
            table='licensePlate',
        ),
    ]
