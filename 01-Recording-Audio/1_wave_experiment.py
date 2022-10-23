# Type of Audio

# .mp3 Lossy Audio Compression
# .flac Lossless Audio Compression
# .wav Uncompressed Audio

# Audio Signal Parameters
# - number of channels (Number of sources of Audio)
# - sample width:
# - framerate/sample_rate : Quality of Audio
# - number of frames : Length of Audio
# - values of a frame : Amplitude of Audio

import wave


waveFile = wave.open("sample.wav", "rb")  # "rb" means read binary

# Print Params
print("Total Channels", waveFile.getnchannels())  # 1
print("Sample width", waveFile.getsampwidth())  # 2
print("Frame rate.", waveFile.getframerate())  # 16000
print("Total frames", waveFile.getnframes())  # 16000
print(
    "Parameters:", waveFile.getparams()
)  # (1, 2, 16000, 16000, 'NONE', 'not compressed')

# Calculate Duration
duration = waveFile.getnframes() / waveFile.getframerate()
print("Duration:", duration)  # 1.0

# Read Frames
wavFrames = waveFile.readframes(waveFile.getnframes())
waveFile.close()

# Write new wave file
frameRate = 16000.0  # hertz
numberOfChannels = 1  # mono
sampleWidth = 2  # 2 bytes

newWaveFileWrite = wave.open("new_file.wav", "wb")
newWaveFileWrite.setnchannels(numberOfChannels)
newWaveFileWrite.setsampwidth(sampleWidth)
newWaveFileWrite.setframerate(frameRate)
newWaveFileWrite.writeframes(wavFrames)
newWaveFileWrite.close()

newWaveFileRead = wave.open("new_file.wav", "rb")
print("Total Channels", newWaveFileRead.getnchannels())  # 1
print("Sample width", newWaveFileRead.getsampwidth())  # 2
print("Frame rate.", newWaveFileRead.getframerate())  # 16000
print("Total frames", newWaveFileRead.getnframes())  # 16000
newWaveFileRead.close()
