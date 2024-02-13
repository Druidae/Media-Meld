import yt_dlp
import os

from django.shortcuts import render
from django.http import FileResponse

from .forms import MediaMeldForms


def get_info(request):
    if request.method == "GET":
        form = MediaMeldForms()

        context = {"form": form}

        return render(
            request=request,
            template_name="media_app/index_media_meld.html",
            context=context,
        )
    if request.method == "POST":
        form = MediaMeldForms(request.POST)
        url = request.POST.get("title", "")

        if url:
            try:
                options = {"simulate": True, "quiet": True}

                ydl = yt_dlp.YoutubeDL(options)
                video_info = ydl.extract_info(url=url)
                # video_json_info = json.dumps(video_info)

                formats = video_info.get("formats", None)
                v_formats = []
                a_format = {"format_id": "default"}
                best_audio_size = 0

                for video_format in formats:
                    if (
                        video_format["protocol"] == "https"
                        and video_format["resolution"] != "audio only"
                        and video_format["ext"] != "webm"
                    ):
                        v_formats.append(video_format)
                        # v_formats.append(
                        #     f"{video_format['format_id']}({video_format['resolution']})"
                        # )

                for audio_format in formats:
                    if audio_format["ext"] == "m4a":
                        if audio_format["filesize"] > best_audio_size:
                            a_format = audio_format
                            # a_format = f"{audio_format['ext']}({audio_format['resolution']})"

                video_data = {
                    "url": url,
                    "title": video_info.get("title", None),
                    "thumbnail": video_info.get("thumbnail", None),
                    "v_formats": v_formats,
                    "a_format": a_format,
                }

                context = {"form": form, "video_data": video_data}

                return render(
                    request=request,
                    template_name="media_app/index_media_meld.html",
                    context=context,
                )
            except Exception as _ex:
                context = {"form": form, "error_message": "Check your URl please!"}
                print(_ex)

                return render(
                    request=request,
                    template_name="media_app/index_media_meld.html",
                    context=context,
                )


def download_video(request):
    url = request.POST.get("url", "")
    select_video_format = request.POST.get("select_video", "")
    audio = request.POST.get("audio", "")

    if audio != "default":
        options = {
            "format": f"{select_video_format}+{audio}",
            # 'outtmpl': f'data/{select_video_format}'
        }
    else:
        options = {
            "format": f"{select_video_format}",
            # 'outtmpl': f'data/{select_video_format}'
        }

    ydl = yt_dlp.YoutubeDL(options)
    video = ydl.extract_info(url=url)
    file_name = ydl.prepare_filename(video)
    video_file = open(file_name, "rb")
    os.remove(file_name)

    return FileResponse(video_file, as_attachment=True)
