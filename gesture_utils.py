def get_finger_states(hand_landmarks):
    tips = [4, 8, 12, 16, 20]  #landmark indices for fingertips in mediapipe (nasa net sya sa picture)
    fingers = [] #list to store finger states (1 for open, 0 for closed)

    # Thumb 
    #since thumbs moves sideways thats why we use x coordinates to determine if its open or closed
    #if the x coordinate of the thumb tip (landmark 4) is less than the x coordinate of the joint below it (landmark 3) then the thumb is open (1), otherwise its closed (0)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers 
    #for the other fingers we compare the y coordinates of the fingertip with the y coordinates of the joint two landmarks below it (tip - 2) to determine if the finger is open or closed
    for tip in tips[1:]: #Loop through all fingertip IDs except the first one (starts from the index 1)
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def detect_gesture(fingers):

    if fingers == [1, 1, 1, 1, 1]:
        return "Open Palm"

    elif fingers == [0, 0, 0, 0, 0]:
        return "Fist"

    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace"

    elif fingers == [0, 1, 0, 0, 0]:
        return "Pointing"
    
    elif fingers == [1, 0, 0, 0, 0]:
        return "Thumbs Up"
    elif fingers == [0, 1, 1, 1, 1]:
        return "Four"
    elif fingers == [1, 1, 0, 0, 1]:
        return "Rock"

    return "Unknown"