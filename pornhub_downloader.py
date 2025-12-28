import os
from yt_dlp import YoutubeDL

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos_pornhub")
os.makedirs(DIR, exist_ok=True)

def dl(url):
    YoutubeDL({
        'outtmpl': os.path.join(DIR, '%(title)s.%(ext)s'),
        'format': 'best',
        'writethumbnail': True,
        'concurrent_fragment_downloads': 5,
    }).download([url.strip()])

def main():
    print("PornHub Downloader")
    print(f"Folder: {DIR}\n")
    while True:
        url = input("URL (or 'exit'): ").strip()
        if url.lower() in {"exit"}:
            break
        if url:
            print(f"Downloading: {url}")
            try:
                dl(url)
                print("Done\n")
            except Exception as e:
                print(f"Error: {e}\n")
        if input("Another video? (y/n): ").strip().lower() not in {"y", "yes", ""}:
            break

if __name__ == "__main__":
    main()