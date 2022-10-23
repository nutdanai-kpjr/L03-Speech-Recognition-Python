from speech_to_text_services import *

filename = "sample_short.mp3"
audioUrl = upload(filename)

saveTranscript(audioUrl, "result_sample_short")

# Audio file ref : https://www.effortlessenglishpage.com/p/mp3-free-download.html
