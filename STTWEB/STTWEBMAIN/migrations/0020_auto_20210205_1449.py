# Generated by Django 3.1.3 on 2021-02-05 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STTWEBMAIN', '0019_auto_20210205_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='channels',
            name='top_tags',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='videos',
            name='similar_videos_updated',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 5, 14, 49, 50, 795847)),
        ),
    ]