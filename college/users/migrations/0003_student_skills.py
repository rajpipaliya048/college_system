# Generated by Django 4.2.6 on 2023-11-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_requestlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='skills',
            field=models.TextField(null=True),
        ),
    ]
