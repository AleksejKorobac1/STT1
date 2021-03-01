from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from STTWEBMAIN.models import Videos
import time
import subprocess


class Command(BaseCommand):

    def handle(self, *args, **options):
        playlist = ''

        response1 = str(subprocess.Popen(
            ["youtube-dl", "--ignore-errors", "--get-id", playlist, '--playlist-start', '1', '--playlist-end', '10'],
            stdout=subprocess.PIPE).communicate())

        list = response1[3:-10].split('\\n')

        for item in list:
            print(item)
