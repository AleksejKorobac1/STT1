from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from STTWEBMAIN.models import Videos
import os
import sys
import time
import subprocess


class Command(BaseCommand):

    def handle(self, *args, **options):
        t0 = time.time()
        playlist = 'PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4'
        response1 = str(subprocess.Popen(
            ["youtube-dl", "--ignore-errors", "--get-id", playlist, '--force-ipv4'],
            stdout=subprocess.PIPE).communicate())
        list = response1[3:-10].split('\\n')
        for item in list:
            if not Videos.objects.filter(video_id=item).first():
                q = Videos(video_id=item, downloaded=0)
                q.save()
