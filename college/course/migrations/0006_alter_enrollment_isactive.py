# Generated by Django 4.2.6 on 2023-10-23 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_enrollment_isactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='isactive',
            field=models.BooleanField(default=True),
        ),
    ]
