# Generated by Django 3.1.2 on 2020-11-18 11:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STTWEBMAIN', '0011_stats_top_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='similar_videos',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='videos',
            name='similar_videos_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 18, 13, 1, 45, 867835)),
        ),
    ]