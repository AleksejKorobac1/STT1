# Generated by Django 3.1.3 on 2021-01-25 14:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STTWEBMAIN', '0015_auto_20201125_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='searches',
            name='channel',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='videos',
            name='similar_videos_updated',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 25, 16, 34, 16, 221343)),
        ),
    ]
