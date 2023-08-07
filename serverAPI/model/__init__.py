# <---- Action Recognition ---->
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp
try: from . import find
except ImportError: import find
from keras.models import Sequential
from keras.layers import LSTM, Dense
#MediaPipe Holistic. --> For keypoint detection on our hands.
mp_holistic = mp.solutions.holistic 

#MediaPipe Drawing --> For drawing the keypoints on the hands.
mp_drawing = mp.solutions.drawing_utils

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
    # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
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

#find location of files
files = find.__getfiles__(fullpath=True)

#Path for exported data, numpy arrays
# DATA_PATH = os.path.join()
#DATA_PATH = os.path.join('C:/C290 - Special Project/dataset/mp_data')

#Actions that we try to detect
actions = np.array(['please', 'pull', 'test', 'request', 'review', 'change', 'bug', 'fix', 'integrate', 'code', 'commit', 'and'])

#Thirty videos worth of data
no_sequence = 40

#Videos are going to be 30 frames in length
sequence_length = 30

# Model for "im_done.h5"
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662))) #64 LSTM units
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

#Loading the model
MODELNAME = 'action.h5'
model.load_weights(files[MODELNAME]) #if not under direct directory

#holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.5)
threshold = 0.4 #Confidence level. For us to render results on if they past a certain threshold

def predict_action(frames):
    imagesAndResults = [mediapipe_detection(frame, holistic) for frame in frames]
    keypoints = [extract_keypoints(results) for _, results in imagesAndResults]
    res = model.predict(np.expand_dims(keypoints, axis=0))[0]
    print(actions[np.argmax(res)])
    return actions[np.argmax(res)]
if __name__ == "__main__":
    #testing
    #1. New detection variable
    sequence = []
    sentence = []
    predictions = []
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    #Set/Accessing mediapipe model
    while cap.isOpened():
        start = time.perf_counter()
        #Read feed from the webcam. frame = image frmo webcam
        ret, frame = cap.read()

        #Make detection
        image, results = mediapipe_detection(frame, holistic)
        
        #Drawing landmarks
        draw_landmarks(image, results)
        
        #Prediction Logic
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]
        
        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            print(actions[np.argmax(res)])
            predictions.append(np.argmax(res))

            #Visualising the predictions on screen
            if np.unique(predictions[-10:])[0] == np.argmax(res): #Ensuring there are no wrong prediction during transitions
                print(f'{res=}')
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                    else:
                        sentence.append(actions[np.argmax(res)])

                if len(sentence) > 5:
                    sentence = sentence[-5:]

                cv2.rectangle(image, (0,0), (640,40), (245, 117, 16), -1)
                cv2.putText(image, ' '.join(sentence), (3,30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        print(f"time elapsed: {time.perf_counter()-start}")
        #Showing to screen
        cv2.imshow('OpenCV Feed', image)

        # Break the loop on pressing 'q'. 0xFF represents current key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Release resources/Turning off webcam
    cap.release()
    cv2.destroyAllWindows()
                                        