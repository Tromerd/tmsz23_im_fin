# Generated by Django 3.0.4 on 2020-04-18 20:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('url', models.URLField(max_length=256, verbose_name='Kinogo URL')),
                ('description', models.TextField(blank=True, max_length=2048, verbose_name='Description')),
                ('poster', models.ImageField(blank=True, default=None, null=True, upload_to='image/film_app/posters/', verbose_name='Poster')),
                ('year', models.CharField(blank=True, default=None, max_length=24, null=True, verbose_name='Year')),
                ('duration', models.CharField(blank=True, max_length=256, verbose_name='Duration')),
                ('genres', models.CharField(blank=True, max_length=512, verbose_name='Genres')),
            ],
            options={
                'verbose_name': 'Film',
                'verbose_name_plural': 'Films',
                'ordering': ('title', 'year', 'duration'),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Date')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('text', models.TextField(max_length=10112, verbose_name='Text')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='film_app.Film')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ('film', 'user'),
            },
        ),
        migrations.CreateModel(
            name='Screenshots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(blank=True, default=None, null=True, upload_to='image/film_app/screens/', verbose_name='Screenshot')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='film_app.Film')),
            ],
            options={
                'verbose_name': 'Screenshot',
                'verbose_name_plural': 'Screenshots',
            },
        ),
        migrations.CreateModel(
            name='ReviewLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='film_app.Review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
