import json
import requests
import time
from secret_api_key import ASSEMBLY_AI_API_KEY, LISTEN_NOTES_API_KEY


transcriptUrl = "https://api.assemblyai.com/v2/transcript"
headers_assembly_ai_auth_only = {"authorization": ASSEMBLY_AI_API_KEY}
headers_assembly_ai = {
    "authorization": ASSEMBLY_AI_API_KEY,
    "content-type": "application/json",
}


listenNotesEpisodeUrl = "https://listen-api.listennotes.com/api/v2/episodes"
headers_listennotes = {
    "X-ListenAPI-Key": LISTEN_NOTES_API_KEY,
}

CHUNK_SIZE = 5_242_880  # 5MB


def getEpisodeAudioUrl(episode_id):
    url = listenNotesEpisodeUrl + "/" + episode_id
    response = requests.request("GET", url, headers=headers_listennotes)
    data = response.json()
    episode_title = data["title"]
    thumbnail = data["thumbnail"]
    podcast_title = data["podcast"]["title"]
    audio_url = data["audio"]
    print("Step 1 : Get Audio URL of Podcast From ListenNotes")
    return audio_url, thumbnail, podcast_title, episode_title


def transcribe(audio_url, auto_chapters):
    transcriptRequest = {"audio_url": audio_url, "auto_chapters": auto_chapters}
    transcriptResponse = requests.post(
        transcriptUrl, json=transcriptRequest, headers=headers_assembly_ai
    )
    print("Step 2 : Transcribe")
    return transcriptResponse.json()["id"]


def poll(transcript_id):
    pollingUrl = transcriptUrl + "/" + transcript_id
    pollingResponse = requests.get(pollingUrl, headers=headers_assembly_ai)
    return pollingResponse.json()


def getTranscriptionResultUrl(url, auto_chapters):
    transcribeId = transcribe(url, auto_chapters)
    print("Step 3 : Wait for result")
    while True:
        data = poll(transcribeId)  # keep polling until the status is "completed"
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]

        print("waiting for 60 seconds")
        time.sleep(60)


def saveTranscript(episode_id):
    audio_url, thumbnail, podcast_title, episode_title = getEpisodeAudioUrl(episode_id)

    data, error = getTranscriptionResultUrl(audio_url, auto_chapters=True)

    if data:
        filename = episode_id + ".txt"
        with open(filename, "w") as f:
            f.write(data["text"])
        filename = episode_id + "_chapters.json"
        with open(filename, "w") as f:
            chapters = data["chapters"]

            data = {"chapters": chapters}
            data["audio_url"] = audio_url
            data["thumbnail"] = thumbnail
            data["podcast_title"] = podcast_title
            data["episode_title"] = episode_title

            json.dump(data, f, indent=4)
            print("Transcript saved")
            return True
    elif error:
        print("Error!!!", error)
