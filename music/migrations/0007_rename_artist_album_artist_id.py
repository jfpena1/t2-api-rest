# Generated by Django 3.2 on 2021-04-23 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_rename_artist_id_album_artist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='artist',
            new_name='artist_id',
        ),
    ]
