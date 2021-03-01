import sys
import os
import collections
from operator import itemgetter
import time
from os.path import dirname, abspath
import json
from STTWEBMAIN.models import Videos, Channels

STT_dir = dirname(dirname(dirname((abspath(__file__)))))
exclude_directory = STT_dir + '/exclusion'


def replace_words(replaceme):
    with open(os.path.join(exclude_directory, replaceme), encoding="utf8") as replaceFile:
        replace_data = replaceFile.read()
        replace = replace_data.split()
        return set(replace)


def replace_phrase(replaceme):
    with open(os.path.join(exclude_directory, replaceme), encoding="utf8") as replaceFile:
        replace_data = replaceFile.read()
        replace = replace_data.split('\n')
        return set(replace)


def tuple_to_list(most_common_thing):
    most_common_things_list = []
    for instance in most_common_thing:
        add = True
        for sub_instance in instance[:-1]:
            if '’' in sub_instance or '–' in sub_instance or '"' in sub_instance or '—' in sub_instance\
                    or "'" in sub_instance or '[' in sub_instance or ']' in sub_instance or '-' in sub_instance\
                    or '?' in sub_instance:
                add = False
                break
        if add:
            most_common_things_list.append(list(instance))
    return most_common_things_list


def most_common_adjusted(most_common_thing, most_common_thing2):
    most_common_thing2 = most_common_thing2[0:15]
    nw = -1
    for instance in most_common_thing:
        nw += 1
        np = -1
        for instance2 in most_common_thing2:
            np += 1
            if instance[0] in instance2[0]:
                # print(instance, instance2)
                # print(most_common_thing[nw][0] ,most_common_thing[nw][1])
                most_common_thing[nw][1] -= instance2[1]
                # print(most_common_thing[nw][0], most_common_thing[nw][1])
                # print('------------')
    return most_common_thing


def filter_by_number(list, n):
    new_list = []
    for item in list:
        if item[1] >= n:
            new_list.append(item)
    return new_list


# def combine_continued_tags(list):  # Work in progress. coming soon TM
#     new_list = []
#     combined_list = []
#     if len(list) != 0:
#         old_item = list[0]
#         for item in list[1:]:
#             if old_item[0].split()[-3] == item[0].split()[2] and old_item[0].split()[-2] == item[0].split()[1] \
#                     and old_item[0].split()[-1] == item[0].split()[0]:
#                 combined_string = old_item[0]
#                 for item2 in item[0].split()[2:]:
#                     combined_string += item2 + ' '
#                 combined_list.append(combined_string)
#             else:
#                 new_list.append(item)
#             old_item = item
#         print(combined_list)
#         print(new_list)


def generate_tags(txt_sub_file_name):

    txt_time_sub_directory = os.path.join(STT_dir, 'subs/txt_time_subs/')

    replace = replace_words('words.txt')
    replace2 = replace_words('words2.txt')
    replace3 = replace_words('words3.txt')
    # replace4 = replace_words('words4.txt')
    replace2_y = replace_words('words2y.txt')
    replace3_z = replace_words('words3z.txt')
    replace3_x = replace_words('words3x.txt')
    # replace4_x = replace_words('words4x.txt')
    # replace4_zz = replace_words('words4zz.txt')

    replace_phrase2 = replace_phrase('phrases2.txt')
    replace_phrase3 = replace_phrase('phrases3.txt')
    # replace_phrase4 = replace_phrase('phrases4.txt')
    # replace_part_phrase4 = replace_phrase('partofphrase4.txt')
    # replace4_yz = replace_phrase('words4yz.txt')
    # replace4_xy = replace_phrase('words4xy.txt')

    with open(os.path.join(txt_time_sub_directory, txt_sub_file_name[:11] + '.en.txt'), encoding="utf8") as f:
        data = f.read()
        data = data.replace(':', '').replace(',', '').replace('.', '').replace('- [', '').replace(']', '')
        datasplit = data.split()
        datasplit = [x.lower() for x in datasplit if not x.startswith('0')]

    i = 1
    j = 0

    words = []
    phrases2 = []
    phrases3 = []
    # phrases4 = []

    for word in datasplit:
        try:
            #word = (datasplit[j])
            phrase2 = (datasplit[i], datasplit[i+1])
            phrase3 = (datasplit[j-1], datasplit[j], datasplit[j+1])
            #phrase4 = (datasplit[j], datasplit[j+1], datasplit[j+2], datasplit[j+3])
            words.append(word)
            phrases2.append(phrase2)
            phrases3.append(phrase3)
            #phrases4.append(phrase4)
            i += 1
            j += 1

        except IndexError:
            break

    phrases3_new = []
    for phrase3 in phrases3:
        x, y, z = phrase3
        if x not in replace3 and y not in replace3 and z not in replace3:
            phrases3_new.append(phrase3)

    phrases2_new = []
    for phrase2 in phrases2:
        x, y = phrase2
        if x not in replace2 and y not in replace2:
            phrases2_new.append(phrase2)

    words_clean = []
    phrases2_clean = []
    phrases3_clean = []
    #phrases4_clean = []

    for word in words:
        x = word
        # if x.lower() not in replace:
        #     words_clean.append(x)
        if x not in replace:
            words_clean.append(x)

    for phrase in phrases2_new:
        x, y = phrase
        xy = (x + ' ' + y)
        # if x.lower() not in replace2 and y.lower() not in replace2 and y.lower() not in replace2_y \
        #         and xy.lower() not in replace_phrase2:
        #     phrases2_clean.append(xy)
        if y not in replace2_y \
                and xy not in replace_phrase2:
            phrases2_clean.append(xy)

    for phrase in phrases3_new:
        x, y, z = phrase
        xy = (x + ' ' + y)
        yz = (y + ' ' + z)
        xyz = (x + ' ' + y + ' ' + z)
        # if x.lower() not in replace3 and x.lower() not in replace3_x and y.lower() not in replace3 and z.lower() not in replace3 \
        #         and z.lower() not in replace3_z and xyz.lower() not in replace_phrase3 \
        #         and xy.lower() not in replace_phrase2 and yz.lower() not in replace_phrase2 \
        #         and xy != yz and xy != xyz:
        #     phrases3_clean.append(xyz)
        if x not in replace3_x \
                and z not in replace3_z and xyz not in replace_phrase3 \
                and xy not in replace_phrase2 and yz not in replace_phrase2 \
                and xy != yz and xy != xyz:
            phrases3_clean.append(xyz)

    # for phrase in phrases4:
    #     x, y, z, zz = phrase
    #     xy = (x + ' ' + y)
    #     yz = (y + ' ' + z)
    #     zzz = (z + ' ' + zz)
    #     xyzzz = (x + ' ' + y + ' ' + z + ' ' + zz)
    #     if x.lower() not in replace4 and x.lower() not in replace4_x and y.lower() not in replace4 and z.lower() not in replace4\
    #             and zz.lower() not in replace4 and zz.lower() not in replace4_zz and xyzzz.lower() not in replace_phrase4 \
    #             and xy.lower() not in replace_part_phrase4 and yz.lower() not in replace_part_phrase4 and zzz.lower() not in replace_part_phrase4\
    #             and yz.lower() not in replace4_yz and xy.lower() not in replace4_xy and x != y and y != z:
    #         phrases4_clean.append(xyzzz)

    most_common_words = collections.Counter(words_clean).most_common(100)
    most_common_phrases2 = collections.Counter(phrases2_clean).most_common(100)
    most_common_phrases3 = collections.Counter(phrases3_clean).most_common(100)
    # most_common_phrases4 = collections.Counter(phrases4_clean).most_common(100)

    most_common_words_list = tuple_to_list(most_common_words)
    most_common_phrases2_list = tuple_to_list(most_common_phrases2)
    most_common_phrases3_list = tuple_to_list(most_common_phrases3)

    most_common_words_list = most_common_adjusted(most_common_words_list, most_common_phrases2_list)
    most_common_phrases2_list = most_common_adjusted(most_common_phrases2_list, most_common_phrases3_list)
    # most_common_phrases3_list = most_common_adjusted(most_common_phrases3_list, most_common_phrases4)

    most_common_words_list = sorted(most_common_words_list,key=itemgetter(1), reverse=True)
    most_common_phrases2_list = sorted(most_common_phrases2_list, key=itemgetter(1), reverse=True)
    most_common_phrases3_list = sorted(most_common_phrases3_list, key=itemgetter(1), reverse=True)

    most_common_words_list = filter_by_number(most_common_words_list, 3)
    most_common_phrases2_list = filter_by_number(most_common_phrases2_list, 3)
    most_common_phrases3_list = filter_by_number(most_common_phrases3_list, 3)
    # most_common_phrases4 = filter_by_number(most_common_phrases4, 3)

    # result = {'ones': most_common_words_list[0:7], 'twos': most_common_phrases2_list[0:7],
    #            'threes': most_common_phrases3_list[0:5], 'fours': most_common_phrases4[0:5]}
    result = most_common_words_list[0:10] + most_common_phrases2_list[0:6] + most_common_phrases3_list[0:3]

    return json.dumps(result)


def generate_similar_by_tags(video_id):
    tags_all = []
    suggested_ranking = {}

    videos = Videos.objects.filter(downloaded=1).all()
    tags = json.loads(Videos.objects.filter(video_id=video_id).first().tags)

    for video in videos:
        video_tags_full = [video.video_id]
        video_tags = json.loads(video.tags)
        for tag in video_tags:
            video_tags_full.append(tag[0])
            video_tags_full.append(tag[1])
        tags_all.append(video_tags_full)

    for tag in tags:
        for video_tag in tags_all:
            if tag[0] in video_tag:
                if tag[1] < video_tag[video_tag.index(tag[0])+1]:
                    tag_value = tag[1]
                else:
                    tag_value = video_tag[video_tag.index(tag[0])+1]
                n = len(tag[0].split())
                if video_tag[0] in suggested_ranking:
                    if n == 3:
                        suggested_ranking[video_tag[0]] += tag_value * 3
                    elif n == 2:
                        suggested_ranking[video_tag[0]] += tag_value * 2
                    else:
                        suggested_ranking[video_tag[0]] += tag_value
                else:
                    if n == 3:
                        suggested_ranking[video_tag[0]] = tag_value * 3
                    elif n == 2:
                        suggested_ranking[video_tag[0]] = tag_value * 2
                    else:
                        suggested_ranking[video_tag[0]] = tag_value

    suggested_ranking = {k: v for k, v in sorted(suggested_ranking.items(), key=lambda item: item[1])}
    similar_videos = list(reversed(list(suggested_ranking)))

    if len(suggested_ranking) >= 10:
        similar_videos = similar_videos[1:11]
    else:
        similar_videos = similar_videos[1:len(similar_videos)]
    matched = []
    for similar_video in similar_videos:
        similar_tags = json.loads(Videos.objects.filter(video_id=similar_video).first().tags)
        matched_video = [similar_video]
        for tag in tags:
            for similar_tag in similar_tags:
                if tag[0] == similar_tag[0]:
                    matched_video.append(similar_tag)
        matched.append(matched_video)

    return json.dumps(matched)


def calculate_top_tags(channel):  # db object
    tags_all = {}
    videos = Videos.objects.filter(channel=channel.channel_name, downloaded=1).all()
    video_count = videos.count()
    print(video_count)
    for video in videos:
        if 'D&D' not in video.title:
            for tag in json.loads(video.tags):
                if tag[0].lower() in tags_all:
                    tags_all[tag[0].lower()] += tag[1]
                else:
                    tags_all[tag[0].lower()] = tag[1]

    tags_all = {k: v for k, v in sorted(tags_all.items(), key=lambda item: item[1])}
    top_tags = []

    for i in range(0, len(tags_all)):
        # top_tags.append([list(tags_all.keys())[i], list(tags_all.values())[i]/video_count])
        top_tags.append(list(tags_all.keys())[i])
    top_tags = list(reversed(top_tags))

    # downloaded_videos = len(Videos.objects.filter(downloaded=1))
    # total_videos = len(Videos.objects.all())
    # search = Searches.objects.all().order_by('-times_searched')
    # i = -1
    # top_search = []
    # for search in search[0:5]:
    #     top_search.append([search.search, search.times_searched])

    chan = channel
    chan.top_tags = json.dumps(top_tags[:10])
    chan.save()
