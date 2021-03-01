from django.core.management.base import BaseCommand, CommandError
from STTWEBMAIN.tagging import generate_similar_by_tags
from STTWEBMAIN.models import Videos
from datetime import datetime, timedelta
from progress.bar import Bar


class Command(BaseCommand):

    def handle(self, *args, **options):

        video_ids = []
        tenmin = timedelta(seconds=1)
        videos = Videos.objects.filter(downloaded=1).all()
        for video in videos:
            video_ids.append(video.video_id)
        bar = Bar('    Tagging', max=len(video_ids))
        for video_id in video_ids:
            print(' ', video_id)
            video = Videos.objects.filter(video_id=video_id).first()
            if datetime.now() - video.similar_videos_updated.replace(tzinfo=None) > tenmin:
                similar_videos = generate_similar_by_tags(video_id)
                video.similar_videos_updated = datetime.now().replace(microsecond=0)
                video.similar_videos = similar_videos
                video.save()
            bar.next()
        bar.finish()



