import cv2, pickle, asyncio
import mediapipe as mp
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,  Dropout
try: from . import find
except ImportError: import find
MODELNAME:str = "asl_letters.h5"

#MediaPipe Hands --> For keypoint detection on our hands.
mp_hands = mp.solutions.hands

#MediaPipe Drawing --> For drawing the keypoints on the hands.
mp_drawing = mp.solutions.drawing_utils

try: data_dict = pickle.load(open('./serverAPI/model/data.pickle', 'rb'))
except FileNotFoundError: data_dict = pickle.load(open(find.__getfiles__(fullpath=True)['data.pickle'], 'rb'))
data = np.asarray(data_dict['data'])

labels = np.asarray(data_dict['labels'])
labels = np.unique(labels)
model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(len(data[0]),)))
model.add(Dense(265, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(labels), activation='softmax'))

try: model.load_weights(f'./serverAPI/model/{MODELNAME}')
except FileNotFoundError: model.load_weights(find.__getfiles__(fullpath=True)[MODELNAME])
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.4, max_num_hands=1)

def mediapipe_detection(image, model) -> tuple:
    #Converting colour (OpenCV default channel format is BGR)
    image =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    #Process the frame and get hand landmarks. Make predictation using Mediapipe for detection.
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results
def extract_keypoints(results):
    data_aux = []
    x_ = []
    y_ = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

    return data_aux

async def predict(frame) -> str:
    image, results = mediapipe_detection(frame, hands)
    class_label = 'Blank'
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:   
        # Extract keypoints from the hand landmarks
        # keypoints = extract_keypoints(results)
        keypoints = np.array(extract_keypoints(results)).reshape(1, -1) 
        
        # Make prediction
        pred = model.predict(keypoints)
        class_label = labels[np.argmax(pred)]
    return class_label

async def predictions(frames):
    if len(frames) != 5:  raise ResourceWarning(f"Number of frames recieved not expected: {len(frames)}frames")
    tasks = [predict(frame) for frame in frames[::2]]
    return await asyncio.gather(*tasks)

def draw_landmarks(image, results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)