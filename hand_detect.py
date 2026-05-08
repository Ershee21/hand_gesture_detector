# Import OpenCV library
# Used for webcam access and drawing on screen
import cv2

#Import MediaPipe library for hand detection and gesture recognition
#used forhandtracking and gesture recognition
import mediapipe as mp

#import custom functions for gesture recognition
from gesture_utils import get_finger_states, detect_gesture

#acccess mediapipe hands solution
mp_hands = mp.solutions.hands

#used for drawing hand landmarks and connections on the webcam feed
mp_drawing = mp.solutions.drawing_utils

#create hand detection object with specified parameters
hands = mp_hands.Hands(
    static_image_mode=False,  
    max_num_hands=1, #one hand only
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

#open webcam
#0 = default cam
cap = cv2.VideoCapture(0)

#infinite loop for webcam frames
while True:

    #read frame from webcam
    ret, frame = cap.read()
    if not ret:  #camera failes loop stops
        break

    frame = cv2.flip(frame, 1) #mirror image for natural interaction
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convert BGR to RGB for mediapipe processing (SINCE MEDIAPIPE REQUIRED RGB (RED GREEN BLUE)FORMAT)
    results = hands.process(rgb_frame) #PROCESS FRAME AND DETECT HANDS

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks( #draw hand landmarks and connections on the webcam feed
                frame, #draw on webcam frame
                hand_landmarks,  #hand landmarks detected by mediapipe
                mp_hands.HAND_CONNECTIONS #predefined connections between hand landmarks in mediapipe
            )

            fingers = get_finger_states(hand_landmarks) #gets finger states (open or closed) using the custom function from gesture_utils.py
            gesture = detect_gesture(fingers)  #from the gesture_utils.py file to detect gestures

            #Draw text on the webcam screen
            cv2.putText(
                frame,  #frame where text will be displayed
                gesture, #text to display
                (50, 80), #position of text on screen (x,y) 
                cv2.FONT_HERSHEY_SIMPLEX, #font style
                1.5, #font size
                (0, 255, 0), #text color (green in BGR format) (blue, green, red)
                3 #thickness of text
            )

    cv2.imshow("Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()