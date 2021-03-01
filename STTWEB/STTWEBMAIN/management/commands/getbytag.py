from django.core.management.base import BaseCommand, CommandError
from STTWEBMAIN.tagging import generate_tags
from STTWEBMAIN.models import Videos
import os
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        t0 = time.time()
        videos = Videos.objects.filter(downloaded=1)
        print(videos)
        print(time.time() - t0)

