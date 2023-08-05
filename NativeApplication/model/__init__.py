import mediapipe as mp
from keras.models import Sequential
from keras.layers import Dense, LSTM
import cv2, numpy as np
import asyncio
try: from . import find
except ImportError: import find
try: from . import gestures
except ImportError: import gestures
MODELNAME:str = 'refined_action.h5' # change this as needed
actions = np.array(['bye', 'day', 'hello', 'help', 'how', 'i', 'iloveyou', 'morning', 'my', 'need', 'no', 'please', 'thanks', 'time', 'what', 'when', 'where', 'who', 'why', 'yes', 'you'])
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662))) #64 LSTM units
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

__draw__ = (True, True, True)

try: model.load_weights(f'./serverAPI/model/{MODELNAME}')
except FileNotFoundError: model.load_weights(find.__getfiles__(fullpath=True)[MODELNAME]) #if not under direct directory

#MediaPipe Holistic. --> For keypoint detection on our hands.
mp_holistic = mp.solutions.holistic 
#MediaPipe Drawing --> For drawing the keypoints on the hands.
mp_drawing = mp.solutions.drawing_utils
holistic = mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.5)     

def mediapipe_detection(image, model):
    #Converting colour (OpenCV default channel format is BGR)
    image =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    #Process the frame and get hand landmarks. Make predictation using Mediapipe for detection.
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results
#Default colouring and size for the landmarks
def draw_landmarks(image, results):
    if __draw__[0]:
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
    if __draw__[1]:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    if __draw__[2]:
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
#Each keypoints/landmark has 3 or 4 values (e.g, res.x, res.y ....)
def extract_keypoints(results):
    #Arrays for values of landmark/keypoints in face
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3) #In this case, there are 486 landmarks with 3 values, res x, res y ad res z.
    #Arrays for values of landmark/keypoints in pose
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    #Arrays for values of landmark/keypoints in left-hand
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    #Arrays for values of landmark/keypoints in right-hand
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([face, pose, lh, rh])

class HandGestureRecogniser():
    def __init__(self, *, threshold:int=0.5) -> None:
        self.sequence:list = []
        self.sentence:list = []
        self.predictions:list = []
        self.frames:list = []
        self.threshold = threshold
    
    async def predict(self):
        return model.predict(np.expand_dims(self.sequence, axis=0))[0]
    async def gather(self):
        tasks = [self.predict(), gestures.predictions(self.frames)]
        results = await asyncio.gather(*tasks)
        return results
    def predict_action(self):
        pred = None
        res, res2 = asyncio.run(self.gather())
        self.predictions.append(np.argmax(res))
        self.predictions = self.predictions[-10:]
        if res[np.argmax(res)] > self.threshold:
            if np.unique(self.predictions)[0] != np.argmax(res): #inverted from chris
                pred = actions[np.argmax(res)]
        if all(element == res2[0] for element in res2) and res2[0] != 'Blank':
            pred = res2[0]
        if pred:
            if len(self.sentence) > 0:
                if pred != self.sentence[-1]:
                    self.sentence.append(pred)
            else:
                self.sentence.append(pred)
    def landmarks(self, frame):
        #Make detection
        image, results = mediapipe_detection(frame, holistic)
        #Drawing landmarks
        draw_landmarks(image, results)
        #Prediction Logic
        keypoints = extract_keypoints(results)
        self.frames.append(frame)
        self.sequence.append(keypoints)
        self.sequence = self.sequence[-30:]
        self.frames = self.frames[-5:]
        if len(self.sequence) == 30:
            self.predict_action()
        reti, frame = cv2.imencode(".jpg", image)
        return frame.tobytes()
    @property
    def transcript(self) -> str:
        return ' '.join(self.sentence)
    @property
    def lastWord(self) -> str:
        return self.sentence[-1:]
    def __repr__(self) -> str:
        return ' '.join(self.sentence)
__all__ = ['HandGestureRecogniser',]