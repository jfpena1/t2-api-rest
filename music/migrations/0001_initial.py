# Generated by Django 3.2 on 2021-04-20 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=50)),
                ('artist_url', models.CharField(max_length=50)),
                ('tracks', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('albums', models.CharField(max_length=50)),
                ('tracks', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('duration', models.IntegerField()),
                ('times_played', models.IntegerField()),
                ('artist_url', models.CharField(max_length=50)),
                ('album_url', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.artist')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.artist'),
        ),
    ]
