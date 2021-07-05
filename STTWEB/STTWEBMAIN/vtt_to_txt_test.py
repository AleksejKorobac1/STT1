import os
import sys
import time
import zlib
from os.path import dirname, abspath

# File is called test but it's not actually a test. This is the main file and I'm just lazy.


def get_correction_list(exclude_directory, file):
    with open(os.path.join(exclude_directory, file)) as correction:
        correctionList = []
        for line in correction:
            line = line[:-1]
            correctionList.append(line.split(','))
    return correctionList


STT_dir = dirname(dirname(dirname((abspath(__file__)))))
exclude_directory = STT_dir + '/subs'
vtt_sub_directory = os.path.join(STT_dir, 'subs/vttsubs')
txt_time_sub_directory = os.path.join(STT_dir, 'subs/txt_time_subs')
compressed_sub_directory = os.path.join(STT_dir, 'subs/compressed_subs')
correction_list = get_correction_list(exclude_directory, 'corrections.txt')


def convert_subtitle(filename):
    txt_file = open(os.path.join(txt_time_sub_directory, filename[:11] + '.en.txt'), 'w', encoding="utf8")  # creates the .txt file
    with open(os.path.join(vtt_sub_directory, filename), encoding="utf8") as vtt_file:
        i = 1
        text = []
        for line in vtt_file:
            if len(line) > 2 and '<' not in line and '[Music]' not in line and '[Laughter]' not in line\
                    and '[Applause]' not in line:
                text.append(line)                  # Deletes empty lines, lines with <c> format, [Applause] etc.

    text2 = []

    for i in range(len(text)-2):         # Deletes consecutive timestamp lines
        if text[i].startswith('0'):
            if text[i+1].startswith('0'):
                pass
            else:
                text2.append(text[i][:8] + '\n')
        else:
            text2.append(text[i])

    text = text2[3:]

    text2 = []
    previous = 1
    current = 1

    for line in text:
        try:
            if text[previous] == text[current]:
                if not text[current+1].startswith('0'):  # If two text lines next to each other combine them
                    if text[current-1].startswith('0'):  # Finding the previous timestamp
                        timestamp = current-1
                    else:
                        timestamp = current
                        while not text[timestamp].startswith('0'):
                            timestamp -= 1
                    text2.append(text[timestamp])
                    text2.append(text[current].replace('\n', ' ') + text[current+1])
                    current += 1
                    previous = current
                    while text[previous].startswith('0') or text[previous] == text[current]:  # Find the next text line
                        previous += 1
                    current = previous
                current += 1
                while text[current].startswith('0'):  # Find the next text line
                    current += 1
            else:
                if text[previous - 1].startswith('0'):
                    timestamp = previous - 1
                else:
                    timestamp = previous
                    while not text[timestamp].startswith('0'):
                        timestamp -= 1
                text2.append(text[timestamp])
                text2.append(text[previous])
                previous = current
        except IndexError:
            break

    text = text2
    text2 = []
    i = 0

    for line in text:       # Combines three text lines into one with one timestamp
        try:
            final = text[i].replace('\n', ' ') + text[i+1].replace('\n', ' ') + text[i+3].replace('\n', ' ') + text[i+5]
            i += 6
            text2.append(final)
        except IndexError:
            pass

    for line in text2:
        txt_file.write(line)

    # Making corrections
    txt_file = open(os.path.join(txt_time_sub_directory, filename[:11] + '.en.txt'), 'r', encoding="utf8")
    txt_file_old_data = txt_file.read()
    txt_file.close()
    txt_file = open(os.path.join(txt_time_sub_directory, filename[:11] + '.en.txt'), 'w', encoding="utf8")
    for correction_item in correction_list:
        for instance in correction_item[1:]:
            txt_file_old_data = txt_file_old_data.replace(instance, correction_item[0])

    txt_file.write(txt_file_old_data)
    compress_sub(filename)


def get_sub_info(file):
    attributes = file[12:].split('╬')
    video_id = file[:11]
    channel = attributes[0]
    title = attributes[1]
    date = attributes[2].replace('.en.vtt', '')
    video_info = {'video_id': video_id, 'channel': channel, 'title': title, 'date': date}
    return video_info


def compress_sub(file):
    f = open(os.path.join(vtt_sub_directory, file), 'r', encoding='utf-8')
    data = f.read()
    f.close()

    f = open(os.path.join(compressed_sub_directory, file), 'wb')
    data = zlib.compress(data.encode('utf8'))
    f.write(data)
    f.close()


