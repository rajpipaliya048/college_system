# Generated by Django 4.2.6 on 2023-10-17 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveBigIntegerField()),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('mobile_number', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=6)),
                ('level_of_education', models.CharField(choices=[('10th pass', '10th pass'), ('12th pass', '12th pass'), ('graduation', 'graduation'), ('post_graduation', 'post_graduation')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
