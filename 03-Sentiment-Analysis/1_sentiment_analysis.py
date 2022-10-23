import json
from youtube_downloader_services import getVideoInfo, getAudioUrl
from sentiment_analysis_services import saveTranscript

videoUrl = "https://www.youtube.com/watch?v=oiIpn3Ud034"  # (TechLead Iphone 13 Review)


def saveVideoSentiments(url):
    print("Step 1 : Get Video Info via Youtube Downloader")
    video_info = getVideoInfo(url)
    url = getAudioUrl(video_info)
    if type(video_info) is dict and url:
        title = "result"
        saveTranscript(url, title, sentiment_analysis=True)
        return title


if __name__ == "__main__":
    # resultUrl = saveVideoSentiments(videoUrl)
    # print(resultUrl)
    with open("result_sentiments.json", "r") as f:
        data = json.load(f)

    positives = []
    negatives = []
    neutrals = []
    for result in data:
        text = result["text"]
        if result["sentiment"] == "POSITIVE":
            positives.append(text)
        elif result["sentiment"] == "NEGATIVE":
            negatives.append(text)
        else:
            neutrals.append(text)

    totalPositive = len(positives)
    totalNegative = len(negatives)
    totalNeutral = len(neutrals)

    print("Num positives:", totalPositive)
    print("Num negatives:", totalNegative)
    print("Num neutrals:", totalNeutral)

    # ignore neutrals here
    r = totalPositive / (totalPositive + totalNegative)
    print(f"Positive ratio: {r:.3f}")
