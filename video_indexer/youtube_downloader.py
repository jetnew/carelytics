"""
youtube_downloader.py notes:
- May occasionally have errors. Just re-run.
- Caches to prevent duplicate downloading of videos.
"""

from pytube import YouTube


def download_youtube(video_url, videoname='0'):
    if check_cache(video_url):
        print(f"youtube_downloader.py: Video already exists.")
        return
    else:
        # print(f"youtube_downloader.py: Downloading \"{videoname}\".")
        append_cache(video_url)
    yt = YouTube(video_url)
    yt.streams \
        .filter(progressive=True, file_extension='mp4') \
        .order_by('resolution')[-1] \
        .download(output_path='videos',
                  filename=videoname)


# Cache prevents downloading of duplicate videos from similar search terms
def append_cache(text, cachefile="video_indexer/downloaded.txt"):
    """Append the text to a cache file"""
    with open(cachefile, "a") as f:
        f.write(text+'\n')

def read_cache(cachefile="video_indexer/downloaded.txt"):
    """Return the list of text from cache file"""
    with open(cachefile, 'r') as f:
        cache = [video_id.strip() for video_id in f]
    return cache

def check_cache(text, cachefile="video_indexer/downloaded.txt"):
    """Check if cachefile contains given text"""
    cache = read_cache(cachefile)
    return text in cache