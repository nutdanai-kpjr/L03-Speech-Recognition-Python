import wave
import numpy as np
import matplotlib.pyplot as plt

# read mono audio file that we created in wave_experiment.py
wavFile = wave.open("new_file.wav", "r")

frameRate = wavFile.getframerate()
totalFrames = wavFile.getnframes()
totalTime = totalFrames / frameRate
signalWave = wavFile.readframes(totalFrames)
signalArray = np.frombuffer(signalWave, dtype=np.int16)  # For mono
# For stereo: singal Array is double the size of frames because it has 2 channels
# leftChannel = signal_array[0::2]  [0,2,4,6,8]
# rightChannel = signal_array[1::2]  [1,3,5,7,9]
print("Framerate:", frameRate)
print("Total Frames:", totalFrames)
print("Total Time:", totalTime)
print("Signal Array Shape:", signalArray.shape)

times = np.linspace(0, totalFrames / frameRate, num=totalFrames)  # start, stop, num

# Plot 1:  Audio signal
plt.figure(figsize=(12, 5))
plt.plot(times, signalArray)
plt.title("new_file.wav Audio")
plt.ylabel("Signal Value")
plt.xlabel("Time (s)")
plt.xlim(0, totalTime)
plt.show()

# Plot 2:  Spectrogram: a visual representation of the spectrum of frequencies of a signal as it varies with time.
plt.figure(figsize=(12, 5))
plt.specgram(
    signalArray, Fs=frameRate, vmin=-20, vmax=50  # type: ignore -> (suppresses error)
)  # vmin and vmax are the min and max values for the color scale
plt.title("new_file.wav Left Channel")
plt.ylabel("Frequency (Hz)")
plt.xlabel("Time (s)")
plt.xlim(0, totalTime)
plt.colorbar()
plt.show()
