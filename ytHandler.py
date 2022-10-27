from __future__ import unicode_literals

# Youtube Download
from youtubesearchpython import VideosSearch, Video
import youtube_dl

# Convert audio files to .wav
import subprocess

# Clear the console before the main func start
import os

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

def YtDownload(vidLink):
    """Download the audio from the video link given by the user

    Args:
        vidLink (str): Link of the youtube video
    """
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = vidLink,download=False
    )
    filename = f"/Music/{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
        'quiet':True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("\nDownload complete !")

def FileConverter(fileName):
    """Converts the file given in arg from .mp3 to .wav

    Args:
        fileName (str): Name of the file to convert (must be in the Music directory)
    """
    filePath = os.path.abspath(f'./Music/{fileName}.mp3')
    outputPath = os.path.abspath('./Music')
    path_to_ffmpeg_exe = r'C:\\FFmpeg\\bin\\ffmpeg.exe'

    #Convert the file
    subprocess.call([path_to_ffmpeg_exe, '-i',
     filePath, #Input
      os.path.join(outputPath, str(fileName + ".wav"))]) #Output

    #Delete the old file
    os.remove(filePath)

def YtHandler(convertToWav=True):
    """Main function of the module, handles all relations with youtube, from searching to downloading the audio
       and converting the file to .wav

    Args:
        convertToWav (bool, optional): Is the file must be converted ?. Defaults to True.
    """
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
        YtDownload(vidLink)
        if convertToWav:
            FileConverter(vidTitle)

if __name__=='__main__':
    YtHandler()


"""
pip install ffmpeg
pip install youtube_dl
pip install youtube-search-python
"""