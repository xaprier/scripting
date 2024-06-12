#!/bin/python3

import os
import sys
from pytube import YouTube
from pytube.innertube import _default_clients
import re

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


def sanitize_filename(filename):
    # Replace spaces with underscores and remove special characters
    return re.sub(r"[^\w\-_\.\(\)]", "_", filename)


def downloadYouTube(videourl, path):
    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        print(f"Download progress: {percentage_of_completion:.2f}%")

    yt = YouTube(videourl, on_progress_callback=on_progress)

    # Select the highest resolution video stream
    video_stream = (
        yt.streams.filter(file_extension="mp4", only_video=True)
        .order_by("resolution")
        .desc()
        .first()
    )
    # Select the highest quality audio stream
    audio_stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()

    if not os.path.exists(path):
        os.makedirs(path)

    # Sanitize the title for the filename
    sanitized_title = sanitize_filename(yt.title)

    # Download the video stream
    video_path = video_stream.download(output_path=path, filename="video.mp4")
    # Download the audio stream
    audio_path = audio_stream.download(output_path=path, filename="audio.mp4")

    # Merge video and audio using ffmpeg (requires ffmpeg to be installed)
    output_path = os.path.join(path, sanitized_title + ".mp4")
    os.system(
        f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental "{output_path}"'
    )

    # Clean up temporary files
    os.remove(video_path)
    os.remove(audio_path)

    # Print information about the downloaded video
    print(f"Title: {yt.title}")
    print(f"Author: {yt.author}")
    print(f"Length: {yt.length} seconds")
    print(f"Views: {yt.views}")
    print(f"Resolution: {video_stream.resolution}")
    print(f"Filesize: {os.path.getsize(output_path) / (1024 * 1024):.2f} MB")
    print(f"Path: {output_path}")


def print_help():
    help_message = """
    Usage: python youtube.py <URL> <Path>

    <URL>  : The URL of the YouTube video to download.
    <Path> : The directory path where the video will be saved.

    Example:
    python script.py https://www.youtube.com/watch?v=jCJ3rWRhRtU /home/xaprier/Videos/Hidamari
    """
    print(help_message)


def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r"^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$"
    )
    return youtube_regex.match(url)


def main():
    if len(sys.argv) < 3 or "--help" in sys.argv:
        print_help()
        return

    videourl = sys.argv[1]
    path = sys.argv[2]

    if not is_valid_youtube_url(videourl):
        print("Error: The provided URL is not a valid YouTube URL.")
        print_help()
        return

    if not videourl or not path:
        print_help()
        return

    downloadYouTube(videourl, path)


if __name__ == "__main__":
    main()
