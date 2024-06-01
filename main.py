import requests
from bs4 import BeautifulSoup as bs
from moviepy.editor import VideoFileClip
import argparse
import os
import json
from datetime import datetime


session = requests.session()    # Start session


def get_video_link(url):
    content = session.get(url).content
    soup = bs(content, "lxml")
    data_json = json.loads(soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"}).text)

    video_link = data_json["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]["video"]["playAddr"]

    return video_link


def get_mp4(video_link, file_name):
    # Create mp4 file
    content = session.get(video_link).content
    with open(f"{file_name}.mp4", "wb") as file:
        file.write(content)


def get_mp3(video_link, file_name):
    # Create mp4 file
    content = session.get(video_link).content
    with open(f"{file_name}.mp4", "wb") as file:
        file.write(content)

    #From mp4 to mp3 file
    with VideoFileClip(f"{file_name}.mp4") as video_clip:
        with video_clip.audio as audio_clip:
            audio_clip.write_audiofile(f"{file_name}.mp3")

    # Remove old mp4 file
    os.remove(f"{file_name}.mp4")


if __name__ == "__main__":
    # Get argparse params
    parser = argparse.ArgumentParser()

    parser.add_argument("url", type=str, help="Tik Tok video link")
    parser.add_argument("format", type=str, help="Downloadable content format | mp4 | mp3 |")
    parser.add_argument("-n", "--name", type=str, default=datetime.now().strftime('%Y-%m-%d_%H%M%S%f'), help="File name")

    args = parser.parse_args()

    # Set params
    video_link = get_video_link(args.url)
    format = args.format
    file_name = args.name

    # mp4 or mp3
    if format == "mp4":
        get_mp4(video_link, file_name)

    elif format == "mp3":
        get_mp3(video_link, file_name)