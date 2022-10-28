from __future__ import unicode_literals

# Youtube Download
from youtubesearchpython import VideosSearch, Video
import youtube_dl

# Convert audio files to .wav
import subprocess

# Clear the console before the main func start
import os

# Import pip modules
import pkg_resources
import sys

def pipInit():
    required = {"ffmpeg", "youtube_dl", "youtube-search-python"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

def YtSearch(userInput = None):
    """This function returns the link and title of the first video found on youtube

    Args:
        userInput (str, optional): Title of the video searched by the user. Defaults to None.

    Returns:
        (str, str): The video link and title
    """
    if userInput:
        search = VideosSearch(userInput, limit = 1)
    else:
        search = VideosSearch(str(input()), limit = 1)

    result = dict(search.result())

    vidLink = result['result'][0]['link']
    vidTitle = result['result'][0]['title']

    return vidLink, vidTitle

def YtDownload(vidLink, path):
    """Download the audio from the video link given by the user

    Args:
        vidLink (str): Link of the youtube video
    """
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = vidLink,download=False
    )
    filename = f"{path}/{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
        'quiet':True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("\nDownload complete !")

def FileConverter(fileName, path):
    """Converts the file given in arg from .mp3 to .wav

    Args:
        fileName (str): Name of the file to convert (must be in the Music directory)
    """
    filePath = os.path.abspath(f'{path}/{fileName}.mp3')
    outputPath = os.path.abspath(path)
    path_to_ffmpeg_exe = r'C:\\FFmpeg\\bin\\ffmpeg.exe'

    #Convert the file
    subprocess.call([path_to_ffmpeg_exe, '-i',
     filePath, #Input
      os.path.join(outputPath, str(fileName + ".wav"))]) #Output

    #Delete the old file
    os.remove(filePath)

def YtHandler(path = "./Music", convertToWav=True, pipInitialize=False):
    """Main function of the module, handles all relations with youtube, from searching to downloading the audio
       and converting the file to .wav

    Args:
        path (str, optional): The path where the file will be downloaded. Defaults to "./Music".
        convertToWav (bool, optional): Is the file must be converted ?. Defaults to True.
        pipInitialize (bool, optional): Should the program initialize pip packages ? . Defaults to False.

    """
    if pipInitialize:
        pipInit()

    os.system('cls')
    userInput = str(input("What is the name/link of the video you want to download ? : "))

    #Case if the user input is the link of the video
    if userInput[:32] == 'https://www.youtube.com/watch?v=':
        videoInfo = dict(Video.getInfo(userInput))
        vidLink = videoInfo['link']
        vidTitle = videoInfo['title']
    else:
        vidLink, vidTitle = YtSearch(userInput)

    rep = str(input(f"\nDo you want to download: {vidTitle} ?\n"))

    if rep in ['y', 'Y', 'Yes', 'yes']:
        print("Downloading...\n")
        YtDownload(vidLink, path)
        if convertToWav:
            FileConverter(vidTitle, path)

if __name__=='__main__':
    YtHandler(convertToWav=False)


"""
pip install -U ffmpeg youtube_dl youtube-search-python
"""