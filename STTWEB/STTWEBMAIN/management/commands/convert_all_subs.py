from django.core.management.base import BaseCommand, CommandError
from STTWEBMAIN.vtt_to_txt_test import convert_subtitle
import os
import time
from os.path import dirname, abspath
from progress.bar import Bar


class Command(BaseCommand):

    def handle(self, *args, **options):
        i = 0
        STT_dir = dirname(dirname(dirname(dirname(dirname((abspath(__file__)))))))
        vtt_sub_directory = os.path.join(STT_dir, 'subs/vttsubs')
        txt_time_sub_directory = os.path.join(STT_dir, 'subs/txt_time_subs')

        t0 = time.time()
        for file in os.listdir(vtt_sub_directory):
            i += 1

        print(vtt_sub_directory)
        bar = Bar('Converting', max=i)
        for file in os.listdir(vtt_sub_directory):
            convert_subtitle(file)
            bar.next()
        bar.finish()
        print(time.time() - t0)
