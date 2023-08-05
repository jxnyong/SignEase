from langTranslate import extract_complete_sentences, translate_text
from model import HandGestureRecogniser
# pip install --upgrade httpx
# pip install --upgrade httpcore
from mongodb import MongoDB
from datetime import datetime
from Text2Speech import speak
from translate import Translator
import cv2 , numpy as np, model
import pyvirtualcam
import PySimpleGUI as sg
import json
from typing import Dict, List
import requests

with open('langConfig.json', 'r') as f:
    data = json.load(f)
    inLANG:str = data["Setting"]["inputLanguage"]
    outLANG:str = data["Setting"]["outputLanguage"]

# def getlang(configFile:str='langConfig.json'):
#     with open(configFile, 'r') as f:
#         data = json.load(f)
#         outLANG:str = data["Setting"]["outputLanguage"]
#     return outLANG

def main(users:str=None):
    cap = cv2.VideoCapture(0)
    recog = HandGestureRecogniser()
    model.__draw__ = (False, False, True)
    sg.theme('DarkBlack1')
    # define the window layout
    layout = [[sg.Image(filename='', key='image')],
                [sg.Combo(['Microphone','Speaker'],default_value='Microphone',key='Output',size=(10, 2),font='Helvetica 14',readonly=True), 
                sg.Button('Record', size=(10, 1), font='Helvetica 14'),
                sg.Button('Stop', size=(10, 1), font='Any 14',visible=False),]]

    # create the window and show it without the plot
    window = sg.Window('Live Subtitling',
                        layout, location=(100, 100), icon='logo.ico')

    recording = False
    with pyvirtualcam.Camera(width=1280, height=800, fps=20, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
        while True:
            event, values = window.read(timeout=20)
            if event == 'Exit' or event == sg.WIN_CLOSED: 
                break
            elif event == 'Record':
                window['Record'].Update(visible=False)
                window['Stop'].Update(visible=True)
                recording = True
            elif event == 'Stop':
                window['Stop'].Update(visible=False)
                window['Record'].Update(visible=True)
                recording = False
            if recording:
                ret, frame = cap.read()
                decoded_image = cv2.imdecode(np.frombuffer(recog.landmarks(frame), np.uint8), cv2.IMREAD_COLOR)
                # cv2.imshow("preview", decoded_image)
                
                with open('transcript.txt', 'r') as f:
                    contents = f.read()
                print(f'{recog.transcript=}\n{contents=}')
                with open('transcript.txt', 'w') as f:
                    if recog.transcript != contents and recog.transcript != '':
                        #implement langTranslate here (but require NLP to function first.)
                        f.write(recog.transcript) #.replace(' ','').lower()
                        speak(recog.lastWord, (True if values['Output'] == 'Microphone' else False), file="speech")
                    else:
                        f.write(contents)
                imgbytes = cv2.imencode('.png', cv2.resize(decoded_image, (600, 400), interpolation=cv2.BORDER_DEFAULT))[1].tobytes()  # ditto
                cam.send(cv2.resize(decoded_image, (1280, 800), interpolation=cv2.BORDER_DEFAULT))
                cam.sleep_until_next_frame()
                window['image'].update(data=imgbytes)
            else:
                img = cv2.imread("cameraDisabled.png")
                # this is faster, shorter and needs less includes
                imgbytes = cv2.imencode('.png', cv2.resize(img, (600, 400), interpolation=cv2.BORDER_DEFAULT))[1].tobytes()
                window['image'].update(data=imgbytes)

    # Release resources/Turning off webcam
    cap.release()
    cv2.destroyAllWindows()

    #read transcript.txt to translate the language and put into translatedText.txt
    # for LiveTranslation
    with open('translatedText.txt', 'w', encoding='utf-8' ) as f:
        target_language = outLANG #language to translate to
        with open('transcript.txt', 'r', encoding='utf-8') as t:
            file_path = "transcript.txt"
            complete_sentences = extract_complete_sentences(file_path)
            separator = ' '  #  separator between the elements of the list
            strCompleteSentences = separator.join(complete_sentences)
        f.write(translate_text(strCompleteSentences))
        

    with open('transcript.txt', 'r') as f: #change transcript.txt to translatedText.txt if needed
        if len(transcript:=f.read())>0:
            db = MongoDB("session", "translations", "users")
            data = {
                "conversation": f"{transcript}",
                "userId": 0, 
                "sessionId": 0, 
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "users": users, 
            }
            db.insert_one("translations", data)