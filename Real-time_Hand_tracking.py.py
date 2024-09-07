import cv2
import mediapipe as mp
import numpy as np

# Initialize mediapipe hand tracker
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize the drawing canvas
canvas = None

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Flip the frame horizontally for natural movement
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Convert the frame to RGB (as mediapipe works with RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and get hand landmarks
    result = hands.process(rgb_frame)
    
    # Create a canvas to draw lines
    if canvas is None:
        canvas = np.zeros_like(frame)
    
    # Check if hands are detected
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Extract landmark for the tip of the index finger (landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            
            # Convert the normalized landmark position to pixel values
            x = int(index_finger_tip.x * width)
            y = int(index_finger_tip.y * height)
            
            # Draw a circle at the tip of the index finger
            cv2.circle(frame, (x, y), 10, (255, 0, 0), cv2.FILLED)
            
            # Draw a line from the last position to the new position
            if 'last_position' in locals():
                cv2.line(canvas, last_position, (x, y), (0, 255, 0), 5)
            
            # Update the last known position
            last_position = (x, y)
    
    # Combine the original frame with the canvas
    frame_with_line = cv2.add(frame, canvas)
    
    # Show the frame with lines
    cv2.imshow("Hand Tracking", frame_with_line)
    
    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()
