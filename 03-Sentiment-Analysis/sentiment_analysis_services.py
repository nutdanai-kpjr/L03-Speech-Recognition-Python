import requests
import time
import json
from secret_api_key import ASSEMBLY_AI_API_KEY


# Similar to 02-Speech-To-Text\speech_to_text_services.py but we are also apply the sentiment analysis on top of it.

# uploadUrl = "https://api.assemblyai.com/v2/upload"
transcriptUrl = "https://api.assemblyai.com/v2/transcript"

headers_auth_only = {"authorization": ASSEMBLY_AI_API_KEY}

headers = {"authorization": ASSEMBLY_AI_API_KEY, "content-type": "application/json"}

CHUNK_SIZE = 5_242_880  # 5MB


# def upload(filename):
#     def readFile(filename):
#         with open(filename, "rb") as f:
#             while True:
#                 data = f.read(CHUNK_SIZE)
#                 if not data:
#                     break
#                 yield data

#     uploadResponse = requests.post(
#         uploadUrl, headers=headers_auth_only, data=readFile(filename)
#     )
#     print("Step 1 : Upload file")
#     return uploadResponse.json()["upload_url"]
#  We don't need the upload function anymore because we are going to use the audio url that we extract via youtube_downloader service instead.


def transcribe(audio_url, sentiment_analysis):

    transcriptRequest = {
        "audio_url": audio_url,
        "sentiment_analysis": sentiment_analysis,
    }

    transcriptResponse = requests.post(
        transcriptUrl, json=transcriptRequest, headers=headers
    )
    print("Step 2 : Transcribe")
    if sentiment_analysis:
        print("Step 2.1 : Applying Sentiment Analysis")
    return transcriptResponse.json()["id"]


def poll(transcript_id):
    pollingUrl = transcriptUrl + "/" + transcript_id
    pollingResponse = requests.get(pollingUrl, headers=headers)
    return pollingResponse.json()


def getTranscriptionResultUrl(url, sentiment_analysis):
    transcribeId = transcribe(url, sentiment_analysis)
    print("Step 3 : Wait for result")
    while True:
        data = poll(transcribeId)  # keep polling until the status is "completed"
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]

        print("waiting for 30 seconds")
        time.sleep(30)


def saveTranscript(url, title, sentiment_analysis=False):
    data, error = getTranscriptionResultUrl(url, sentiment_analysis)

    if data:

        filename = title + ".txt"
        with open(filename, "w") as f:
            f.write(data["text"])
        if sentiment_analysis:
            filename = title + "_sentiments.json"
            with open(filename, "w") as f:
                sentiments = data["sentiment_analysis_results"]
                json.dump(sentiments, f, indent=4)
        print("Transcript saved")
    elif error:
        print("Error!!!", error)
