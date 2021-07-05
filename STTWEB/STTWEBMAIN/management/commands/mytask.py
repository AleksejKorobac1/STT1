from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from STTWEBMAIN.models import Videos
from STTWEBMAIN.search import video_search_all_test, video_deep_search
from STTWEBMAIN.tagging import generate_tags
from STTWEBMAIN.tagging import generate_similar_by_tags
from STTWEBMAIN.downloader import add_video_to_search, add_channel
import os
import time
import sys


class Command(BaseCommand):

    def handle(self, *args, **options):
        add_channel('Ethoslab')




        pass
