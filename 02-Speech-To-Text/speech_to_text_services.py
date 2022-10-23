import requests
import time
from secret_api_key import ASSEMBLY_AI_API_KEY


uploadUrl = "https://api.assemblyai.com/v2/upload"
transcriptUrl = "https://api.assemblyai.com/v2/transcript"

headers_auth_only = {"authorization": ASSEMBLY_AI_API_KEY}

headers = {"authorization": ASSEMBLY_AI_API_KEY, "content-type": "application/json"}

CHUNK_SIZE = 5_242_880  # 5MB

# How it works
# 1. Upload the audio file to AssemblyAI (We will get a audio URL)
# 2. Use the audio URL to send a transcription request to AssemblyAI
# 3. Poll the transcription request until the status is "completed"
# 4. Save the transcript to a text file


def upload(filename):
    def readFile(filename):
        with open(filename, "rb") as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    uploadResponse = requests.post(
        uploadUrl, headers=headers_auth_only, data=readFile(filename)
    )
    print("Step 1 : Upload file")
    return uploadResponse.json()["upload_url"]


def transcribe(audio_url):

    transcriptRequest = {"audio_url": audio_url}

    transcriptResponse = requests.post(
        transcriptUrl, json=transcriptRequest, headers=headers
    )
    print("Step 2 : Transcribe")
    return transcriptResponse.json()["id"]


def poll(transcript_id):
    pollingUrl = transcriptUrl + "/" + transcript_id
    pollingResponse = requests.get(pollingUrl, headers=headers)
    return pollingResponse.json()


def getTranscriptionResultUrl(url):
    transcribeId = transcribe(url)
    print("Step 3 : Wait for result")
    while True:
        data = poll(transcribeId)  # keep polling until the status is "completed"
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]

        print("waiting for 30 seconds")  # wait for 30 seconds before polling again
        time.sleep(30)


def saveTranscript(url, title):
    data, error = getTranscriptionResultUrl(url)

    if data:
        filename = title + ".txt"
        with open(filename, "w") as f:
            f.write(data["text"])
        print("Transcript saved")
    elif error:
        print("Error!!!", error)


if __name__ == "__main__":
    filename = "sample_short.mp3"
    audioUrl = upload(filename)

    saveTranscript(audioUrl, "result_sample_short")
