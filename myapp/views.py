from django.shortcuts import render
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

# Create your views here.


def HomeView(request):

    if request.method == "POST":
        try:
            video_url = YouTube(request.POST.get('video_url'))

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
                        'resolution_int' : int(video_details['resolution'][:-1]) if video_details['resolution'] else None,
                        # 'is_4k' : int(video_details['resolution'][:-1]) >= 2160 if video_details['resolution'] is not None else False,
                        'abr': video_details['abr'],
                    }
                )

            # print(streams_list)
                # print(int(video_details['resolution'][:-1]) if video_details['resolution'] else None)
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
            return render(request, 'single_video.html', context)
        except:
            print("***********")
            return render(request, 'single_video.html')
    return render(request, 'single_video.html')


def PlaylistView(request):
    context = {}
    return render(request, 'play_list.html', context)