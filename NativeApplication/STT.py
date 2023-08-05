#import libraries
import os, io,  whisper, torch
import speech_recognition as sr
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

#parameters
DEFAULT_SETTINGS = {
    'model': 'tiny', #'base.en',
    'threshold': 1000,
    'record timeout': 2,
    'sample rate': 32000,
}

#whisper model
MODEL = whisper.load_model(DEFAULT_SETTINGS['model'])

#set up microphone as audio source
SOURCE = sr.Microphone(sample_rate=DEFAULT_SETTINGS['sample rate'])


class CloseGUI(StopIteration):
    pass
#speech recognition, contains the functions of speech recognition
class SpeechRecognition:
    
    #initializes the attributes/settings based on DEFAULT_SETTINGS
    def __init__(self, *, SETTINGS=DEFAULT_SETTINGS):
        #tracks most recent audio data
        self.phrase_time = None
        self.last_sample = bytes()

        #store audio data received from mic
        self.data_queue = Queue()

        #from SpeechRoognizer
        #create instance
        self.recorder = sr.Recognizer()

        #minimum voice activity needed to considered as speech
        self.recorder.energy_threshold = SETTINGS['threshold']

        #prevent "auto adjustment" of threshold
        self.recorder.dynamic_energy_threshold = False

        #time to wait before ending recording
        self.record_timeout = SETTINGS['record timeout']

        #tempfile to store the audio data
        self.temp_file = NamedTemporaryFile().name
        #store the recognize words from speech
        self.transcription = ['']
        #audio source for recording
        self.source = SOURCE

    #when audio data is received from mic
    def record_callback(self, _, audio: sr.AudioData) -> None:
        #raw data
        data = audio.get_raw_data()
        #queue the data
        self.data_queue.put(data)

    #starts the speech recognition
    def start(self):
        with self.source:
            #adjust the mic according to the ambient noise
            self.recorder.adjust_for_ambient_noise(self.source)

        #starts mic recording
        self.recorder.listen_in_background(
            self.source,
            #calls record_callback when there is audio data
            self.record_callback,
            phrase_time_limit=self.record_timeout
        )

        #perform audio data processing
        while True:
            try:
                #perform if not empty
                if not self.data_queue.empty():
                    #checks if data_queue is not empty
                    while not self.data_queue.empty():
                        #receive the audio data and append the audio data
                        data = self.data_queue.get()
                        self.last_sample += data

                    #create instance, AudioData class
                    audio_data = sr.AudioData(
                        #parameters
                        self.last_sample,
                        self.source.SAMPLE_RATE,
                        self.source.SAMPLE_WIDTH
                    )

                    #convert audio data in WAV
                    wav_data = io.BytesIO(audio_data.get_wav_data()).read()

                    #open the temp file to write the WAV audio data into
                    with open(self.temp_file, 'w+b') as f:
                        f.write(wav_data)

                    #Whisper to transcribe the wavfile
                    result = MODEL.transcribe(
                        self.temp_file,
                        fp16=torch.cuda.is_available()
                    )
                    
                    # os.system('cls' if os.name == 'nt' else 'clear')
                    #print by individual words
                    text = result['text'].strip()
                    with open('subtitles.txt', 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(result['text'].strip())
                    
                    sleep(0.25)

            #end process when keyboard interrupt
            except KeyboardInterrupt:
                break
#run the code
if __name__ == "__main__":
    speech_recognition = SpeechRecognition()
    
    print('recording')
    speech_recognition.start()