import os
from yt_dlp import YoutubeDL

DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),"videos_yt")
os.makedirs(DIR,exist_ok=True)

def dl(url):
    YoutubeDL({
        'outtmpl':os.path.join(DIR,'%(title)s.%(ext)s'),
        'format':'bestvideo+bestaudio/best',
        'merge_output_format':'mp4',
        'writethumbnail':True,
        'concurrent_fragment_downloads':5,
    }).download([url.strip()])