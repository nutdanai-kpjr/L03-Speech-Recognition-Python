import streamlit as frontendBuilder
import glob
import json
from podcast_summarize_services import saveTranscript

frontendBuilder.title("🙉 Minute Podcast: Too Long Don't Listen")

json_files = glob.glob("*.json")

episode_id = frontendBuilder.sidebar.text_input("🏓 Give us Episode ID")
button = frontendBuilder.sidebar.button("🐬 Get Episode summary", on_click=saveTranscript, args=(episode_id,))  # type: ignore


def getFormattedTime(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        start_t = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        start_t = f"{minutes:02d}:{seconds:02d}"

    return start_t


if button:
    filename = episode_id + "_chapters.json"
    print(filename)
    with open(filename, "r") as f:
        data = json.load(f)

    chapters = data["chapters"]
    episode_title = data["episode_title"]
    thumbnail = data["thumbnail"]
    podcast_title = data["podcast_title"]
    audio = data["audio_url"]

    frontendBuilder.header(f"{podcast_title} - {episode_title}")
    frontendBuilder.image(thumbnail, width=200)
    frontendBuilder.markdown(f"#### {episode_title}")

    for chp in chapters:
        with frontendBuilder.expander(
            chp["gist"] + " - " + getFormattedTime(chp["start"])
        ):
            chp["summary"]


# run via streamlit run 1_podcast_summarize.py
# Sample Episode ID: 4bdac209399848b4a2e72f68362096da
