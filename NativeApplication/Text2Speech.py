import pyttsx3,os,time, string, random, simpleaudio as sa
from pygame import mixer, _sdl2 as devices
TEMP = "TEMP"

# Initialize mixer with the correct device
# Set the parameter devicename to use the VB-CABLE name from the outputs printed previously.
mixer.init(devicename = "CABLE Input (VB-Audio Virtual Cable)")

# Initialize text to speech
engine = pyttsx3.Engine()

def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def device() -> None:
    # Get available output devices
    mixer.init()
    print("Inputs:", devices.audio.get_audio_device_names(True))
    print("Outputs:", devices.audio.get_audio_device_names(False))
    # [get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))]
    mixer.quit()

def speak(text, microphone:bool=True, *, file:str=get_random_string(6)):
    # Save speech as audio file
    engine.save_to_file(text, f"{TEMP}/{file}.wav")
    engine.runAndWait()
    if microphone:
        # Play the saved audio file
        mixer.music.load(f"{TEMP}/{file}.wav")
        mixer.music.play() # Play it
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        mixer.music.unload()
    else:
        sa.WaveObject.from_wave_file(f"{TEMP}/{file}.wav").play().wait_done()
    os.remove(f"{TEMP}/{file}.wav")
if __name__ == "__main__":
    speak("The quick brown fox jumped over the lazy dog.")
    speak("Testing")