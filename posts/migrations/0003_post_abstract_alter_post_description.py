# Generated by Django 4.1.4 on 2023-10-17 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_rename_isrequest_post_is_request_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='abstract',
            field=models.TextField(blank=True, default='Texte apparaissant sur la page de recherche.'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, default="Texte apparaissant que quand on clique sur l'annonce.\n"),
        ),
    ]
