#!/bin/python3

import os
import sys
from pytube import YouTube
from pytube.innertube import _default_clients
import re

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


def downloadYouTube(videourl, path):
    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        print(f'Download progress: {percentage_of_completion:.2f}%')

    yt = YouTube(videourl, on_progress_callback=on_progress)
    yt = (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)


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
