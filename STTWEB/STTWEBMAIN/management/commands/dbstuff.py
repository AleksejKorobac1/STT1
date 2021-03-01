from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from STTWEBMAIN.models import Videos
import os
import sys
import time
import subprocess


def printline(response):
    i = 0
    while True:
        line = response[i:i + 13]
        if line == '':
            break
        print(line[:-2])
        #f.write(line[:-2] + os.linesep)
        i += 13


class Command(BaseCommand):
    videos = Videos.objects.all()
    infolist = []
    # for video in videos:
    #     print(id)
    #     video.video_id = id
    #     video.save()
    files = []
    ids = []
    for file in os.listdir(VttSubDirectory):
        attributes = file[12:].split('п')
        ids.append(file[:11])
        if Videos.objects.filter(video_id = file[:11]).first():
            video = Videos.objects.filter(video_id = file[:11]).first()
            #q = Videos(video_id = file[:11], channel = attributes[0], title = attributes[1], date = attributes[2].replace('.en.vtt', ''))
            video.title = attributes[1]
            video.channel = attributes[0]
            video.date = attributes[2].replace('.en.vtt', '')
            video.downloaded = 1
            video.save()
    #
    #
    #
    #     file.save()

    # response1 = str(
    #     subprocess.Popen(["youtube-dl", "--ignore-errors", "--get-id", Playlist], stdout=subprocess.PIPE).communicate())
    #
    # response1 = response1[3:-8]
    # printline(response1)

    t1 = time.time()
    print(t1-t0)

    def handle(self, *args, **options):
        self.stdout.write('This was extremely simple!!!')