import youtube_dl
from youtube_dl.utils import DownloadError

youtubeDownloader = youtube_dl.YoutubeDL()

videoUrl = "https://www.youtube.com/watch?v=oiIpn3Ud034"  # (TechLead Iphone 13 Review)


def getVideoInfo(url):
    with youtubeDownloader:
        try:
            result = youtubeDownloader.extract_info(url, download=False)
        except DownloadError:
            return None
    # In case if url is a playlist we pick the first video
    if type(result) is dict and "entries" in result:
        video = result["entries"][0]
    else:
        # Just a video
        video = result
    return video


def getAudioUrl(video):
    for f in video["formats"]:
        if f["ext"] == "m4a":
            return f["url"]


if __name__ == "__main__":
    video_info = getVideoInfo(videoUrl)
    url = getAudioUrl(video_info)
    print(url)
