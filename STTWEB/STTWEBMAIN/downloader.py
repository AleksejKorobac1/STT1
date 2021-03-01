import subprocess
import time
import os
from os.path import dirname, abspath
from STTWEBMAIN.models import Videos, Searches, Channels
from STTWEBMAIN.tagging import generate_tags, generate_similar_by_tags
from STTWEBMAIN.vtt_to_txt_test import get_sub_info, convert_subtitle
from STTWEBMAIN.search import video_search
from datetime import datetime
import ast
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager


def download_subtitles(video_id):

    downloaded = 0
    STT_dir = dirname(dirname(dirname((abspath(__file__)))))
    vtt_sub_directory = os.path.join(STT_dir, 'subs/vttsubs')
    save_location = vtt_sub_directory + '/%(id)s╬%(uploader)s╬%(title)s╬%(upload_date)s'
    response = str(subprocess.Popen(
        ["youtube-dl", "-o", save_location,
         "--ignore-errors", "--write-auto-sub", "--skip-download", video_id],  # '--cookies', 'C:/Users/HOME/Downloads/cookies.txt'
        stdout=subprocess.PIPE).communicate())
    for file in os.listdir(vtt_sub_directory):

        if video_id in file:
            downloaded = file

    return downloaded


def add_video_to_db(video_id, response):
    downloaded = 1
    video_info = get_sub_info(response)
    title = video_info['title']
    date = video_info['date']
    channel = video_info['channel']

    x = threading.Thread(target=add_channel, args=(video_id, channel))
    x.start()

    convert_subtitle(response)
    tags = generate_tags(response)
    video = Videos(downloaded=downloaded, video_id=video_id, title=title, date=date, channel=channel, tags=tags)
    video.save()
    video.similar_videos = generate_similar_by_tags(video_id)
    video.similar_videos_updated = datetime.now().replace(microsecond=0)
    video.save()
    add_video_to_search(video_id)


def add_video_to_search(video_id):
    searches = Searches.objects.all()
    video = Videos.objects.filter(video_id=video_id).first()
    for search in searches:
        current_search = video_search(video_id + '.en.txt', search.search)
        if current_search > 0:
            search_results = ast.literal_eval(search.result)
            new_results = [video_id, current_search, video.date, video.title]
            search_results.append(new_results)
            search.result = search_results
            # search.save()


def add_channel(video_id, channel):
    if not Channels.objects.filter(channel_name=channel).first():
        t0 = time.time()
        PATH = "C:/Users/HOME/Desktop/STTLEX/STTWEB/geckodriver.exe"
        print('-----------------------------------------------------------no')
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get('https://www.youtube.com/results?search_query=' + channel)
        time.sleep(5)
        # profile_img_url = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div/div/div/div/div/ytd-video-secondary-info-renderer/div/div/ytd-video-owner-renderer/a/yt-img-shadow/img").get_attribute("src")
        profile_img_url = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div/ytd-item-section-renderer/div/ytd-channel-renderer/div/div/a/div/yt-img-shadow/img").get_attribute("src")
        q = Channels(channel_name=channel, profile_img=profile_img_url)
        print(profile_img_url)
        q.save()
        print(time.time()-t0)
        driver.quit()