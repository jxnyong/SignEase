#!/usr/bin/env python
from langTranslate import translate_text, extract_complete_sentences
from mongodb import MongoDB
from datetime import datetime
import PySimpleGUI as sg
import cv2, pyvirtualcam
import threading, io,  whisper, torch, json, numpy as np
from PIL import ImageFont, ImageDraw, Image
import speech_recognition as sr
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
flag = False

with open('langConfig.json', 'r') as f:
    #https://www.alchemysoftware.com/livedocs/ezscript/Topics/Catalyst/Language.htm
    data = json.load(f)
    inLANG:str = data["Setting"]["inputLanguage"]
    outLANG:str = data["Setting"]["outputLanguage"]
    OPTIONS = data['Options']
    FONT = cv2.FONT_HERSHEY_PLAIN if outLANG == "En" else data["Languages"][outLANG]

#parameters
DEFAULT_SETTINGS = {
    'model': f'tiny{".en" if outLANG == "En" else ""}',
    'threshold': 1000,
    'record timeout': 2,
    'sample rate': 32000,
}
#whisper model
MODEL = whisper.load_model(DEFAULT_SETTINGS['model'])

#set up microphone as audio source
SOURCE = sr.Microphone(sample_rate=DEFAULT_SETTINGS['sample rate'])
class StopIterationGUI(StopIteration):
    pass
#speech recognition, contains the functions of speech recognition
class SpeechRecognition:
    def __init__(self, SETTINGS=DEFAULT_SETTINGS, *, verbose:bool=False):
        self._stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.phrase_time = None
        self.last_sample = bytes()
        self.data_queue = Queue()
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = SETTINGS['threshold']
        self.recorder.dynamic_energy_threshold = False
        self.record_timeout = SETTINGS['record timeout']
        self.temp_file = NamedTemporaryFile(delete=False).name
        self.source = SOURCE
        self._verbose = verbose
    @property
    def stop_event(self):
        return self._stop_event
    def record_callback(self, _, audio: sr.AudioData):
        data = audio.get_raw_data()
        self.data_queue.put(data)
    def start(self):
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)
        self.recorder.listen_in_background(
            self.source,
            self.record_callback,
            phrase_time_limit=self.record_timeout
        )
        while not self.stop_event.is_set():
            try:
                self.pause_event.wait()
                if not self.data_queue.empty():
                    while not self.data_queue.empty():
                        data = self.data_queue.get()
                        self.last_sample += data
                    audio_data = sr.AudioData(
                        self.last_sample,
                        self.source.SAMPLE_RATE,
                        self.source.SAMPLE_WIDTH
                    )
                    wav_data = io.BytesIO(audio_data.get_wav_data()).read()
                    with open(self.temp_file, 'w+b') as f:
                        f.write(wav_data)
                    result = MODEL.transcribe(
                        self.temp_file,
                        language = inLANG,
                        fp16=torch.cuda.is_available(),
                    )
                    text = result['text'].strip()
                    with open('subtitles.txt', 'w', encoding="utf-8") as f:
                        if inLANG != outLANG:f.write(translate_text(text))
                        else: f.write(text)
                    if self._verbose:
                        print(text)
                    sleep(0.25)
            except KeyboardInterrupt:
                break

def readTranscript(words:int, *, file='subtitles.txt') -> str:
    with open(file, 'r', encoding='utf-8') as f:
        if outLANG == 'En':
            return " ".join(f.read().split(" ")[-words:])
        return " ".join(f.read()[-words:])
        
def putText(frame, text, *, coordinates:tuple=(100,660), font = cv2.FONT_HERSHEY_PLAIN, color:tuple=(0,0,0)):
    thickness = 2
    if isinstance(font, int):
        return cv2.putText(frame, text, coordinates, font, 2, color, thickness, cv2.LINE_AA)
    #if not english
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(frame_pil)
    font = ImageFont.truetype(font, 45)
    draw.text(coordinates, text, font=font, fill=color)
    return cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)


def main(user:str=None, callback:callable=None):
    speech_recognisor = SpeechRecognition(verbose=True)
    sg.theme('DarkBlack1')
    # define the window layout
    layout = [[sg.Image(filename='', key='image')],
              [sg.Button('Record', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Helvetica 14', visible=False),]]

    # create the window and show it without the plot
    window = sg.Window('Live Subtitling',
                       layout, location=(100, 100), icon='logo.ico')
    
    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    speechRecogniser_thread = threading.Thread(target=speech_recognisor.start)
    speechRecogniser_thread.start()
    recording = False
    settings_window_open = False
    with pyvirtualcam.Camera(width=1280, height=800, fps=20, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
        while True:
            event, values = window.read(timeout=20)
            if event == 'Exit' or event == sg.WIN_CLOSED:
                if callback:
                    callback(user)
                speech_recognisor.stop_event.set()
                speechRecogniser_thread.join()
                
                return
            elif event == 'Record':
                speech_recognisor.pause_event.set()
                window['Stop'].Update(visible=True)
                window['Record'].Update(visible=False)
                recording = True
            elif event == 'Stop':
                speech_recognisor.pause_event.clear()
                window['Stop'].Update(visible=False)
                window['Record'].Update(visible=True)
                recording = False
            
            if recording:
                ret, frame = cap.read()
                frame = cv2.resize(frame, (1280, 800), interpolation=cv2.BORDER_DEFAULT)
                frame = cv2.flip(frame, 1)
                if (transcript:=readTranscript(11)):
                    frame = putText(frame,transcript, color=(255,255,255), font= FONT)
                imgbytes = cv2.imencode('.png', cv2.resize(frame, (600, 400), interpolation=cv2.BORDER_DEFAULT))[1].tobytes()  # ditto
                # frame = cv2.flip(frame, 1)
                cam.send(frame)
                cam.sleep_until_next_frame()
                window['image'].update(data=imgbytes)
            else:
                img = cv2.imread("cameraDisabled.png")
                # this is faster, shorter and needs less includes
                imgbytes = cv2.imencode('.png', cv2.resize(img, (600, 400), interpolation=cv2.BORDER_DEFAULT))[1].tobytes()
                window['image'].update(data=imgbytes)
    cv2.destroyAllWindows()
    if len(transcript:=readTranscript(-0))>0:
        db = MongoDB("session", "translations", "users")
        data = {
            "conversation": f"{transcript}",
            "userId": 0, 
            "sessionId": 0, 
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "user": user, 
        }
        db.insert_one("translations", data)
        
if __name__ == "__main__":
    main()