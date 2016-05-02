# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 22:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import login.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_name', models.CharField(max_length=100)),
                ('album_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=login.models.images_path)),
                ('thumbnail', models.ImageField(editable=False, upload_to=login.models.thumbnail)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Album')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('email', models.EmailField(default='foo@gmail.com', max_length=200)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User'),
        ),
    ]