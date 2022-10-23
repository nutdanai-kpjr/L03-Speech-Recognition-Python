from pydub import AudioSegment  # Don't forget to install ffmpeg


wavAudio = AudioSegment.from_wav("sample.wav")


wavAudio = wavAudio - 6  # Decrease Volume by 6dB
wavAudio = wavAudio * 3  # Repeat Audio 3 times
wavAudio = wavAudio.fade_in(2000)  # Fade in 2 seconds
wavAudio = wavAudio.fade_out(2000)  # Fade out 2 seconds

wavAudio.export("sample.mp3", format="mp3")
