# Generated by Django 4.2.6 on 2023-10-23 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_remove_enrollment_fees_course_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='html_input',
            field=models.TextField(null=True),
        ),
    ]