from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from STTWEBMAIN.models import Videos
import os
import sys
import ast
from STTWEBMAIN.vtt_to_txt import get_sub_info


class Command(BaseCommand):

    def handle(self, *args, **options):

        filenames = []
        missing_files = []

        for file in os.listdir('C:\\Programs\\STT\\subs\\vttsubs'):
            filenames.append(file)

        for missing_file in missing_files:
            for filename in filenames:
                if missing_file in filename:
                    sub_info = get_sub_info(filename)
                    video = Videos(video_id = sub_info['video_id'], channel = sub_info['channel'], title = sub_info['title'], date = sub_info['date'], downloaded = 1)
                    video.save()



