# Generated by Django 4.1.4 on 2023-01-08 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_invitations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
