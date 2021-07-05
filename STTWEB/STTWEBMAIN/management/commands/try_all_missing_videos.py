from django.core.management.base import BaseCommand, CommandError
from STTWEBMAIN.tagging import generate_tags
from STTWEBMAIN.models import Videos, Searches
from STTWEBMAIN.downloader import download_subtitles
from STTWEBMAIN.vtt_to_txt_test import convert_subtitle, get_sub_info
from STTWEBMAIN.tagging import generate_tags, generate_similar_by_tags
from STTWEBMAIN.search import video_deep_search, video_search
import time
import ast
from datetime import datetime, timedelta


class Command(BaseCommand):

    def handle(self, *args, **options):

        videos = Videos.objects.filter(downloaded=0).order_by('-id')
        oneday = timedelta(hours=24)
        video_ids = []

        for video in videos:
            video_ids.append(video.video_id)

        for video_id in video_ids:
            print(video_id)
            video = Videos.objects.filter(video_id=video_id).first()
            if datetime.now() - video.subtitles_checked.replace(tzinfo=None) > oneday:
                print('24h have passed. Checking')
                response = download_subtitles(video_id)
                if response != 0:
                    print('Subtitles downloaded')
                    # video = Videos.objects.filter(video_id=response[:11]).first()
                    video.downloaded = 1
                    video_info = get_sub_info(response)
                    video.title = video_info['title']
                    video.date = video_info['date']
                    video.channel = video_info['channel']
                    convert_subtitle(response)
                    tags_list = generate_tags(response)
                    video.tags = tags_list['ones']
                    video.tags_2 = tags_list['twos']
                    video.tags_3 = tags_list['threes']
                    video.tags_4 = tags_list['fours']
                    video.save()
                    video.similar_videos = generate_similar_by_tags(video_id)
                    video.similar_videos_updated = datetime.now().replace(microsecond=0)

                    searches = Searches.objects.all()
                    for search in searches:
                        current_search = video_search(video_id + '.en.txt', search.search)
                        if current_search > 0:
                            search_results = ast.literal_eval(search.result)
                            new_results = [video_id, current_search, video.date, video.title]
                            search_results.append(new_results)
                            search.result = search_results
                            search.save()
            else:
                print("24h haven't passed since check")

            video.subtitles_checked = datetime.now().replace(microsecond=0)
            video.save()
            time.sleep(120)
