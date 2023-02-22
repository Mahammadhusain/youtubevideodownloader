from django.shortcuts import render
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

# Create your views here.


def HomeView(request):

    try:
        video_url = YouTube('https://www.youtube.com/watch?v=P98-VNuu85c')

        author = video_url.author
        publish_date = video_url.publish_date
        channel_url = video_url.channel_url
        description = video_url.description
        # print(video_url.keywords)
        
        video_title = video_url.title
        video_thumbnail = video_url.thumbnail_url
        all_available_qualities = video_url.streams

        streams_list = []
        # .filter(progressive=True)
        for i in all_available_qualities:
            # print(vars(i))
            video_details = vars(i)
            streams_list.append(
                {
                    'file_type': video_details['type'],
                    'mime_type': video_details['mime_type'],
                    'download_url': video_details['url'],
                    'video_quality': video_details['subtype'],
                    'filesize_mb': video_details['_filesize_mb'],
                    'file_type': video_details['type'],
                    'filesize_gb': video_details['_filesize_gb'],
                    'resolution': video_details['resolution'],
                    'abr': video_details['abr'],
                }
            )

        # print(streams_list)
        context = {
            'video_title': video_title,
            'video_thumbnail': video_thumbnail,
            'streams_list':streams_list,
            # -------------------------
            'author':author,
            'publish_date':publish_date,
            'channel_url':channel_url,
            'description':description,
        }
        return render(request, 'index.html', context)
    except:
        print("***********")
        return render(request, 'index.html')
