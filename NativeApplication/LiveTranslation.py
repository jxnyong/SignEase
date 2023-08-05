from model import HandGestureRecogniser
from Text2Speech import speak
import cv2, numpy as np, model
import pyvirtualcam
cap = cv2.VideoCapture(0)
recog = HandGestureRecogniser()
model.__draw__ = (False, False, True)
with pyvirtualcam.Camera(width=1280, height=800, fps=20, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
    while cap.isOpened():
        #Read feed from the webcam. frame = image
        ret, frame = cap.read()
        decoded_image = cv2.imdecode(np.frombuffer(recog.landmarks(frame), np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("preview", decoded_image)
        with open('transcript.txt', 'r') as f:
            contents = f.read()
        print(f'{recog.transcript=}\n{contents=}')
        with open('transcript.txt', 'w') as f:
            if recog.transcript != contents and recog.transcript != '':
                f.write(recog.transcript)
                speak(recog.lastWord, file="speech")
            else:
                f.write(contents)
        # Break the loop on pressing 'q'. 0xFF represents current key
        cam.send(cv2.resize(decoded_image, (1280, 800), interpolation=cv2.BORDER_DEFAULT))
        cam.sleep_until_next_frame()
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release resources/Turning off webcam
cap.release()
cv2.destroyAllWindows()