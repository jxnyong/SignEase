import pyvirtualcam
import cv2
def readTranscript(words:int, *, file='subtitles.txt') -> str:
    with open(file, 'r', encoding='utf-8') as f:
        return " ".join(f.read().split(" ")[-words:])

def putText(frame, text, *, coordinates:tuple=(100,660), font = cv2.FONT_HERSHEY_PLAIN, color:tuple=(0,0,0)):
    fontScale = 2
    thickness = 2
    return cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)

cap = cv2.VideoCapture(0)
with pyvirtualcam.Camera(width=1280, height=800, fps=20, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
    while True:
        ret_val, frame = cap.read()
        frame = cv2.resize(frame, (1280, 800), interpolation=cv2.BORDER_DEFAULT)
        frame = cv2.flip(frame, 1)
        frame = putText(frame,readTranscript(11), color=(255,255,255))
        # cv2.imshow('Subtitling preview', cv2.resize(frame, (1000, 625), interpolation=cv2.BORDER_DEFAULT))
        frame = cv2.flip(frame, 1)
        cam.send(frame)
        cam.sleep_until_next_frame()
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()