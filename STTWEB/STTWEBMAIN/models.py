from django.db import models
from datetime import datetime


class Videos(models.Model):
    video_id = models.CharField(max_length=11, default='')
    downloaded = models.IntegerField(default=0)
    title = models.CharField(max_length=150, default='')
    date = models.CharField(max_length=10, default='')
    channel = models.CharField(max_length=30, default='')
    tags = models.CharField(max_length=1000, default='')
    similar_videos = models.CharField(max_length=1000, default='')
    similar_videos_updated = models.DateTimeField(default=datetime.now())
    subtitles_checked = models.DateTimeField(default='2010-01-01 12:00:00')


class Searches(models.Model):
    search = models.CharField(max_length=100, default='')
    result = models.CharField(max_length=1000, default='')
    times_searched = models.IntegerField(default=0)
    channel = models.CharField(max_length=100, default='')


class Stats(models.Model):
    channel = models.CharField(max_length=30, default='')
    total_videos = models.IntegerField(default=0)
    downloaded_videos = models.IntegerField(default=0)
    top_tags = models.CharField(max_length=1000, default='')
    top_search = models.CharField(max_length=1000, default='')


class Channels(models.Model):
    channel_name = models.CharField(max_length=30, default='')
    profile_img = models.CharField(max_length=100, default='')
    managed = models.IntegerField(default=0)
    top_tags = models.CharField(max_length=1000, default='')