# Generated by Django 3.1.6 on 2021-03-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0008_incedence_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='incedence',
            name='accuracy_score',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
