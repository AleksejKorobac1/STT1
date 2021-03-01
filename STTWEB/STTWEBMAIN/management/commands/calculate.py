from django.core.management.base import BaseCommand, CommandError
from STTWEBMAIN.tagging import generate_tags, calculate_top_tags
from STTWEBMAIN.models import Videos, Stats, Searches, Channels
import os
import time
import requests
import random
import ast
import json
from operator import itemgetter


class Command(BaseCommand):

    def handle(self, *args, **options):
        channels = Channels.objects.filter()
        for channel in channels:
            calculate_top_tags(channel)
