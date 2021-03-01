from django.core.management.base import BaseCommand, CommandError
from STTWEBMAIN.tagging import generate_tags
from STTWEBMAIN.models import Videos
import os
import time
from progress.bar import Bar
from os.path import dirname, abspath


class Command(BaseCommand):

    def handle(self, *args, **options):

        t0 = time.time()
        file_list = []
        j = 0
        i = 0
        STT_dir = dirname(dirname(dirname(dirname(dirname((abspath(__file__)))))))
        txt_time_sub_directory = os.path.join(STT_dir, 'subs/txt_time_subs/')
        # try:
        for file in os.listdir(txt_time_sub_directory):
            i += 1
            file_list.append(file)
        bar = Bar('    Tagging', max=i)
        for file in file_list:
            j += 1
            try:
                tags_list = generate_tags(file[:-7])
                video = Videos.objects.filter(video_id=file[:-7]).first()
                video.tags = tags_list
                video.save()
                bar.next()
            except AttributeError:
                print(file)
                pass
        bar.finish()

        print('Total time: ', time.time()- t0)
        # except AttributeError:
        #     print(file)





