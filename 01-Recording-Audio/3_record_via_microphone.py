import pyaudio
import wave

FRAMES_PER_BUFFER = 6400
FORMAT = pyaudio.paInt16
CHANNELS = 1  # mono
RATE = 32000  # Sample Rate
recorder = pyaudio.PyAudio()

# Start Record
stream = recorder.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER,
)  # Set up the stream config


framesResult = []
recordDuration = 5  # as seconds
print(f" 🎙️ We are recording your voice for {recordDuration} seconds ...")

for i in range(
    0, int(RATE / FRAMES_PER_BUFFER * recordDuration)
):  # Similar to  video recording, we are going to record for 5 seconds
    # Each second have framerate / frames_per_buffer frames (32000 / 6400 = 5 frames)
    # So we are going to record for 5 seconds, 5 * 5 = 25 frames
    data = stream.read(FRAMES_PER_BUFFER)
    framesResult.append(data)


print(" 📝 Saving your voice to record_via_microphone.wav ...")
stream.stop_stream()
stream.close()
recorder.terminate()

# Save the recorded data as a WAV file
waveFile = wave.open("record_via_microphone.wav", "wb")
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(recorder.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b"".join(framesResult))  # Write binary data to the file
waveFile.close()
