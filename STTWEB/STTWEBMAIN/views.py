from django.shortcuts import render
from .models import Videos, Searches, Stats, Channels
from .search import video_deep_search, video_search_all_test, video_deep_search_details
from .downloader import add_video_to_db, download_subtitles
from .tagging import calculate_top_tags
import time
import ast
from .util import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import redirect
import requests
import json


def search(request):
    if len(request.GET.get('video_search')) > 2:
        search = request.GET.get('video_search')
        videos = Videos.objects.filter(downloaded=1).all()
        redirect_to = False

        if 'youtube.com' in search:
            search = search.split('v=')[1].split('&')[0]
            if Videos.objects.filter(video_id=search):
                redirect_to = search
            if redirect_to:
                return redirect('/detailed?video_id=' + redirect_to)
            else:
                url = 'http://127.0.0.1:8000/download_subs'
                data = {
                    'video_id': search
                }
                x = requests.post(url, data=data)
                print('-----------------------------')
                print(x)
                if json.loads(x.text)['downloaded'] == 1:
                    return redirect('/detailed?video_id=' + search)
                else:
                    return redirect('/')

        exclude = []
        sort_by = request.GET.get('sort_by')
        date_selection = [convert_date(request.GET.get('date_start')), convert_date(request.GET.get('date_end'))]
        videos_list = []

        for video in videos:  # Reading and appending tags from DB
            videos_list.append(video.video_id)
            videos_list.append(video.tags)

        if sort_by == 'date':
            search_results = sorted(video_search_all_test(search, 'all'),
                                    key=sort_results_by_date, reverse=True)
        else:
            search_results = sorted(video_search_all_test(search, 'all'),
                                    key=sort_results_by_occurrences, reverse=True)

        if request.GET.get('exclude_dnd'):
            exclude.append(request.GET.get('exclude_dnd'))

        search_results = exclude_from_results(search_results, exclude)
        search_results_number_total = 0  # Number of times search term was used across all videos
        search_results_number = len(search_results)  # Number of videos in which search term appears
        for result in search_results:  # Appending tags to results
            if int(date_selection[0]) <= int(result[2]) <= int(date_selection[1]):
                search_results_number_total += result[1]
                result_id_in_videos_list = videos_list.index(result[0])
                result.append(ast.literal_eval(videos_list[result_id_in_videos_list + 1])[:10])
                try:
                    result.append(Channels.objects.filter(channel_name=result[4]).first().profile_img)
                except AttributeError:
                    print('att', result[4])
                    pass
            else:
                search_results.remove(result)

        page = request.GET.get('page', 1)
        paginator = Paginator(search_results, 25)
        search_results = paginator.page(page)

        context = {
            'date_start': request.GET.get('date_start'),
            'date_end': request.GET.get('date_end'),
            'search': search,
            'sorted_by': request.GET.get('sort_by'),
            'search_results': search_results,
            # 'search_results_number': search_results_number,
            'search_results_number_total': search_results_number_total,
            # 'exclude': exclude
        }

    else:
        context = {'len_error': 'Search request too short'}
    return render(request, 'search.html', context=context)


def detailed(request):
    if request.method == "GET":
        similar_videos_full = []
        video_id = request.GET.get('video_id')
        video = Videos.objects.filter(video_id=video_id).first()
        similar_videos = json.loads(video.similar_videos)
        search_detailed_tags = json.loads(video.tags)

        for similar_vid in similar_videos:
            similar_video = Videos.objects.filter(video_id=similar_vid[0]).first()
            similar_video_channel = similar_video.channel
            similar_videos_full.append([similar_vid[0], similar_video.title, similar_vid[1],
                                        similar_vid[2:], similar_video.date, similar_video_channel])

        if request.GET.get('search'):
            search = request.GET.get('search')
            results = video_deep_search(video.video_id + '.en.txt', search)
            results.insert(0, video_id)

            if len(results) != 0:
                search_detailed = video_deep_search_details(results)
                search_detailed = mark_frequent_results(search_detailed)
            else:
                search_detailed = 'llll'

        context = {
            'search': request.GET.get('search'),
            'video_id': video_id,
            'search_detailed_tags': search_detailed_tags,
            'date_start': request.GET.get('date_start'),
            'date_end': request.GET.get('date_end'),
            'sorted_by': request.GET.get('sort_by'),
            'title': video.title,
            'similar_videos': similar_videos_full
        }
        if request.GET.get('search'):
            context['search_detailed'] = search_detailed

        return render(request, 'detailed.html', context=context)


def index(request):
    channels = Channels.objects.filter(managed=1)

    context = {
        'channels': channels
    }
    return render(request, 'home.html', context=context)


def get_data(request):
    search = request.GET.get('search')

    if len(search) > 2:
        try:
            search = search.split('|')[1][1:]
        except IndexError:
            pass
        video_id = request.GET.get('video_id')
        results = video_deep_search(video_id+'.en.txt', search)

        results.insert(0, video_id)
        search_detailed = video_deep_search_details(results)
        search_detailed = mark_frequent_results(search_detailed)
        context = {
            'search_detailed': search_detailed,
            'search': search,
            'video_id': video_id
        }
    else:
        context = {

        }

    return render(request, 'results.html', context)


@csrf_exempt
def download_subs(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        response = download_subtitles(video_id)
        downloaded = 0
        if response != 0:
            add_video_to_db(video_id, response)
            downloaded = 1

        return JsonResponse(data={'downloaded': downloaded})


def channel(request, channel_name):

    latest_video = Videos.objects.filter(channel=channel_name).last().title
    videos = Videos.objects.filter(channel=channel_name)
    channel = Channels.objects.filter(channel_name=channel_name).first()

    if not channel.top_tags:
        calculate_top_tags(channel)

    profile_image = channel.profile_img
    channel.top_tags = json.loads(channel.top_tags)
    subbed_videos = videos.filter(downloaded=1).count()
    context = {
        'video': latest_video,
        'channel': channel,
        'profile_image': profile_image,
        'subbed_videos': subbed_videos
    }
    if channel.managed == 1:
        total_videos = videos.count()
        context['total_videos'] = total_videos
    return render(request, 'channel.html', context)