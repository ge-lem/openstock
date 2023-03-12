# Generated by Django 4.1.4 on 2023-03-12 10:41

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('basic_organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='organization',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='name_unique'),
        ),
    ]