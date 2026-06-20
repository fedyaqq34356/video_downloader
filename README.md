# Video Downloader

Download videos from YouTube, TikTok, Instagram, Twitter/X, Twitch, and PornHub.

## Requirements

```bash
pip install yt-dlp PyQt6
```

## Usage

```bash
python main.py
```

Select platform, paste URL, click Download.

## Features

- Multi-platform support
- Custom save directory
- Progress tracking
- Thumbnail download
- Playlist support (YouTube)

## Structure

```
main.py                  # GUI application
youtube_downloader.py    # YouTube module
tiktok_downloader.py     # TikTok module
instagram_downloader.py  # Instagram module
twitter_downloader.py    # Twitter/X module
twitch_downloader.py     # Twitch module
pornhub_downloader.py    # PornHub module
icons/                   # Platform icons
```

## Output

Videos save to `videos_{platform}/` by default.

## License

GNU General Public License v3.0