# Generated by Django 3.1.2 on 2020-10-15 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STTWEBMAIN', '0005_videos_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='title',
            field=models.CharField(default='', max_length=150),
        ),
    ]