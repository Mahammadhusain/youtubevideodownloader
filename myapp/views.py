from django.shortcuts import render
from pytube import YouTube,Playlist
from pytube.exceptions import VideoUnavailable

# Create your views here.


def HomeView(request):
    check_get_req = True if request.method == "GET" else False
    

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
            print(all_available_qualities)
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
    context = {"check_get_req":check_get_req}
    return render(request, 'single_video.html',context)



def PlaylistView(request):
    # test url   https://www.youtube.com/playlist?list=PLOEofOHYmmAMMjOr5SlTjPKa1J7obAYZj
    context ={}

    if request.method == "POST":
        try:
            playlist_url = request.POST.get('playlist_url')
            resolution = request.POST.get('Resolution')
            print(playlist_url)
            playlist = Playlist(playlist_url)
            videos = playlist.video_urls
            videos_context =[]
            for video in videos:
                try:
                    video_context = single_video_context(video,resolution)
                    videos_context.append(video_context)
                except VideoUnavailable:
                    print(f"The video at {video} is unavailable")
            context["videos_context"]= videos_context
            return render(request, 'play_list.html', context)
        except Exception as e:
            print("Exception",e)
            message = "Could not download the playlist. Please try again later."
            context = {"message": message}
            return render(request, 'play_list.html', context)
    return render(request, 'play_list.html', context)





def single_video_context(url,resolution=""):
# [<Stream: itag="17" mime_type="video/3gpp" res="144p" fps="12fps" vcodec="mp4v.20.3" acodec="mp4a.40.2" progressive="True" type="video">,
#  <Stream: itag="18" mime_type="video/mp4" res="360p" fps="24fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">,
#  <Stream: itag="22" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">, 
#  <Stream: itag="313" mime_type="video/webm" res="2160p" fps="24fps" vcodec="vp9" progressive="False" type="video">, <Stream: itag="271" mime_type="video/webm" res="1440p" fps="24fps" vcodec="vp9" progressive="False" type="video">, <Stream: itag="137" mime_type="video/mp4" res="1080p" fps="24fps" vcodec="avc1.640028" progressive="False" type="video">, <Stream: itag="248" mime_type="video/webm" res="1080p" fps="24fps" vcodec="vp9" progressive="False" type="video">, <Stream: itag="136" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.4d401f" progressive="False" type="video">, <Stream: itag="247" mime_type="video/webm" res="720p" fps="24fps" vcodec="vp9" progressive="False" type="video">, <Stream: itag="135" mime_type="video/mp4" res="480p" fps="24fps" vcodec="avc1.4d401e" progressive="False" type="video">, <Stream: itag="244" mime_type="video/webm" res="480p" fps="24fps" vcodec="vp9" progressive="False" type="video">, <Stream: itag="134" mime_type="video/mp4" res="360p" fps="24fps" vcodec="avc1.4d401e" progressive="False" type="video">, <Stream: itag="243" mime_type="video/webm" res="360p" fps="24fps" vcodec="vp9" progressive="False" type="video">, <Stream: itag="133" mime_type="video/mp4" res="240p" fps="24fps" vcodec="avc1.4d4015" progressive="False" type="video">, <Stream: itag="242" mime_type="video/webm" res="240p" fps="24fps" vcodec="vp9" progressive="False" type="video">, <Stream: itag="160" mime_type="video/mp4" res="144p" fps="24fps" vcodec="avc1.4d400c" progressive="False" type="video">, <Stream: itag="278" mime_type="video/webm" res="144p" fps="24fps" vcodec="vp9" progressive="False" type="video">, <Stream: itag="139" mime_type="audio/mp4" abr="48kbps" acodec="mp4a.40.5" progressive="False" type="audio">, <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">, <Stream: itag="249" mime_type="audio/webm" abr="50kbps" acodec="opus" progressive="False" type="audio">, <Stream: itag="250" mime_type="audio/webm" abr="70kbps" acodec="opus" progressive="False" type="audio">, <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">]
    
    try:
        video_url = YouTube(url)
        author = video_url.author
        publish_date = video_url.publish_date
        channel_url = video_url.channel_url
        description = video_url.description
        # print(video_url.keywords)
        video_title = video_url.title
        video_thumbnail = video_url.thumbnail_url
        all_available_qualities = video_url.streams
        print("resolution",resolution)
        print("next video")
        streams_list = []
        # .filter(progressive=True)
        for i in all_available_qualities:
            # print(vars(i))
            video_details = vars(i)
            if resolution != "" and resolution != None:
                if video_details["resolution"] == resolution:
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
            else:
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
                    })
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
        return context
    except:
        return {}