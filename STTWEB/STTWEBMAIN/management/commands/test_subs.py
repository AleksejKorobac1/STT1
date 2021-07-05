from django.core.management.base import BaseCommand, CommandError
import os
from os.path import dirname, abspath


class Command(BaseCommand):

    def handle(self, *args, **options):
        STT_dir = dirname(dirname(dirname(dirname(dirname((abspath(__file__)))))))
        vtt_sub_directory = os.path.join(STT_dir, 'subs/vttsubs')
        txt_time_sub_directory = os.path.join(STT_dir, 'subs/txt_time_subs')

        error_list_1 = []
        error_list_2 = []
        error_list_3 = []
        error_list_4 = []
        errors_list = []
        continue_prompt = True

        n = 0
        for file in os.listdir(txt_time_sub_directory):
            with open(os.path.join(txt_time_sub_directory, file)) as txt_time_file:
                i = -1
                for line in txt_time_file:
                    i += 1
                    if not line.startswith('0'):
                        error_list_1.append((file, i))
                        n += 1
        print("[1] Number of subs that don't start with timecode:", n)

        n = 0
        for file in os.listdir(txt_time_sub_directory):
            with open(os.path.join(txt_time_sub_directory, file)) as txt_time_file:
                i = -1
                for line in txt_time_file:
                    i += 1
                    # if not line.startswith('0'):
                    if '00:' in line[8:]:
                        error_list_2.append((file, i))
                        n += 1
        print('[2] Number of subs with 00 in the line: ', n)

        n = 0
        for file in os.listdir(txt_time_sub_directory):
            with open(os.path.join(txt_time_sub_directory, file)) as txt_time_file:
                i = -1
                for line in txt_time_file:
                    i += 1
                    # if not line.startswith('0'):
                    if line[8] != ' ':
                        n += 1
                        error_list_3.append((file, i))

        print('[3] Number of subs with no space after timecode: ', n)

        n = 0
        for file in os.listdir(txt_time_sub_directory):
            with open(os.path.join(txt_time_sub_directory, file)) as txt_time_file:
                i = -1
                for line in txt_time_file:
                    i += 1
                    if line.startswith('000'):
                        n += 1
                        error_list_4.append((file, i))

        print('[4] Number of subs that start with 000: ', n)

        errors_list.append(error_list_1)
        errors_list.append(error_list_2)
        errors_list.append(error_list_3)
        errors_list.append(error_list_4)

        while continue_prompt:
            error_code = int(input('View error:  '))
            if error_code == 0:
                break
            else:
                print(errors_list[error_code-1])

