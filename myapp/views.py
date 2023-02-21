from django.shortcuts import render
from pytube import YouTube

# Create your views here.


def HomeView(request):

    video_url = YouTube('https://www.youtube.com/watch?v=XhEw22gxiEI')

    video_title = video_url.title
    video_thumbnail = video_url.thumbnail_url
    all_available_qualities = video_url.streams

    streams_list = []

    for i in all_available_qualities:
        video_details = vars(i)
        streams_list.append(
            {
                'file_type': video_details['type'],
                'mime_type': video_details['mime_type'],
                'download_url': video_details['url'],
                'video_quality': video_details['subtype'],
                'filesize_mb': video_details['_filesize_mb'],
                'filesize_gb': video_details['_filesize_gb'],
                'resolution': video_details['resolution'],
            }
        )
    print(streams_list)
    context = {
        'video_title': video_title,
        'video_thumbnail': video_thumbnail,
    }
    return render(request, 'index.html', context)
