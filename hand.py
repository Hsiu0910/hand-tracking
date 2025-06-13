import cv2
import mediapipe as mp
import time
import numpy as np
import collections

# Open camera
cap = cv2.VideoCapture(0)

# Specify MediaPipe model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Drawing utilities
mpDraw = mp.solutions.drawing_utils

# Change landmark and connection styles
handLmStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)

# Time calculation
pTime = 0
cTime = 0

# Define fingertip IDs
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20

# All fingertip IDs
ALL_FINGER_TIPS = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
FINGER_NAMES = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

# Note mapping - Left pinky is Do, and so on
NOTE_NAMES = {
    "Left_20": "Do (C)",   # Left pinky
    "Left_16": "Re (D)",   # Left ring
    "Left_12": "Mi (E)",   # Left middle
    "Left_8": "Fa (F)",    # Left index
    "Left_4": "Sol (G)",   # Left thumb
    "Right_4": "La (A)",   # Right thumb
    "Right_8": "Ti (B)",   # Right index
    "Right_12": "Do' (C')",# Right middle
    "Right_16": "Re' (D')",# Right ring
    "Right_20": "Mi' (E')" # Right pinky
}

# Baseline position tracking for each hand-finger combination
finger_baseline = {}
for hand in ["Left", "Right"]:
    for finger_id in ALL_FINGER_TIPS:
        finger_baseline[f"{hand}_{finger_id}"] = 1.0  # Initialize at bottom of screen

# Record pressed state for each finger
fingers_pressed = {}
last_trigger_time = {}
for hand in ["Left", "Right"]:
    for finger_id in ALL_FINGER_TIPS:
        key = f"{hand}_{finger_id}"
        fingers_pressed[key] = False
        last_trigger_time[key] = 0

# Define threshold values for each finger type
FINGER_THRESHOLDS = {
    THUMB_TIP: 0.05,    # Thumb
    INDEX_TIP: 0.072,   # Index
    MIDDLE_TIP: 0.072,  # Middle
    RING_TIP: 0.060,    # Ring
    PINKY_TIP: 0.076    # Pinky
}

# Individual distance thresholds for each hand-finger combination
distance_thresholds = {}
for hand in ["Left", "Right"]:
    for finger_id in ALL_FINGER_TIPS:
        # Use specific threshold values for each finger type
        distance_thresholds[f"{hand}_{finger_id}"] = FINGER_THRESHOLDS[finger_id]

# Other parameters
TRIGGER_COOLDOWN = 0.5           # Trigger cooldown time
VISUAL_FEEDBACK_DURATION = 0.3   # Visual feedback duration
BASELINE_UPDATE_RATE = 0.05      # Rate to update baseline (higher = faster adaptation)

# Debug mode
DEBUG_MODE = True
# Currently selected hand and finger
SELECTED_HAND = "Left"
SELECTED_FINGER = INDEX_TIP

# Create window
cv2.namedWindow('Virtual Piano - Separate Hand Settings', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Virtual Piano - Separate Hand Settings', 1280, 720)

def get_finger_name(finger_id):
    """Get finger name from finger ID"""
    index = ALL_FINGER_TIPS.index(finger_id)
    return FINGER_NAMES[index]

def get_current_selection_key():
    """Get the key for the currently selected hand-finger combination"""
    return f"{SELECTED_HAND}_{SELECTED_FINGER}"

while True:
    ret, img = cap.read()
    if not ret:
        break
    
    # Horizontal flip
    img = cv2.flip(img, 1)
    
    # Convert BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process image
    result = hands.process(imgRGB)
    
    # Get window dimensions
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    
    # Display debug info
    if DEBUG_MODE:
        cv2.putText(img, "Press 'D': toggle debug, '+'/'-': adjust threshold", 
                    (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display thresholds for all fingers of both hands
        y_pos = 120
        
        # Current selection key
        current_key = get_current_selection_key()
        
        # Left hand thresholds
        cv2.putText(img, "LEFT HAND:", (30, y_pos), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        y_pos += 30
        
        for finger_id in ALL_FINGER_TIPS:
            key = f"Left_{finger_id}"
            color = (255, 0, 255) if key == current_key else (0, 0, 255)
            name = get_finger_name(finger_id)
            threshold = distance_thresholds[key]
            cv2.putText(img, f"L-{name}: {threshold:.3f}", (30, y_pos), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y_pos += 25
        
        y_pos += 10
        # Right hand thresholds
        cv2.putText(img, "RIGHT HAND:", (30, y_pos), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        y_pos += 30
        
        for finger_id in ALL_FINGER_TIPS:
            key = f"Right_{finger_id}"
            color = (255, 0, 255) if key == current_key else (0, 0, 255)
            name = get_finger_name(finger_id)
            threshold = distance_thresholds[key]
            cv2.putText(img, f"R-{name}: {threshold:.3f}", (30, y_pos), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y_pos += 25
        
        # Display instructions
        y_pos += 10
        cv2.putText(img, f"Selected: {SELECTED_HAND} {get_finger_name(SELECTED_FINGER)}", 
                  (30, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        y_pos += 30
        
        cv2.putText(img, "Use L/R to switch hands, 1-5 for fingers", (30, y_pos), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        y_pos += 30
        cv2.putText(img, "+: increase threshold, -: decrease threshold", (30, y_pos), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Display key instructions
    cv2.putText(img, "Press 'Q' to quit", (imgWidth - 200, 30), 
              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Hand detection results
    if result.multi_hand_landmarks:
        # Identify left/right hands
        handedness_list = []
        if result.multi_handedness:
            for hand_idx, hand_info in enumerate(result.multi_handedness):
                handedness = hand_info.classification[0].label
                handedness_list.append(handedness)
        
        for idx, handLms in enumerate(result.multi_hand_landmarks):
            # Get current hand type (left/right)
            if idx < len(handedness_list):
                current_hand = handedness_list[idx]
            else:
                current_hand = "Unknown"
            
            # Draw hand landmarks
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmStyle, handConStyle)
            
            # Check each fingertip
            for finger_id in ALL_FINGER_TIPS:
                lm = handLms.landmark[finger_id]
                xPos = int(lm.x * imgWidth)
                yPos = int(lm.y * imgHeight)
                
                # Create hand-finger combination key
                finger_key = f"{current_hand}_{finger_id}"
                
                # Update baseline (lowest y value = highest position)
                # Use a sliding update to adapt to hand movement
                current_y = lm.y
                if finger_key in finger_baseline:
                    if current_y < finger_baseline[finger_key]:
                        # Immediately update if position is higher than baseline
                        finger_baseline[finger_key] = current_y
                    else:
                        # Slowly adapt baseline to current position
                        finger_baseline[finger_key] = finger_baseline[finger_key] * (1 - BASELINE_UPDATE_RATE) + current_y * BASELINE_UPDATE_RATE
                else:
                    finger_baseline[finger_key] = current_y
                
                # Calculate downward distance from baseline
                distance = current_y - finger_baseline[finger_key]
                
                # Display distance (debug)
                if DEBUG_MODE:
                    # Magnify for display
                    display_distance = distance * 100
                    cv2.putText(img, f"{display_distance:.1f}", (xPos + 10, yPos - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    
                    # Draw baseline position
                    baseline_y = int(finger_baseline[finger_key] * imgHeight)
                    cv2.line(img, (xPos - 30, baseline_y), (xPos + 30, baseline_y), (0, 255, 255), 2)
                
                # Mark all fingertips (normal size)
                cv2.circle(img, (xPos, yPos), 5, (0, 255, 0), cv2.FILLED)
                
                # Check if distance exceeds threshold
                # Use hand-specific threshold
                if finger_key in distance_thresholds:
                    current_threshold = distance_thresholds[finger_key]
                else:
                    current_threshold = 0.05  # Default if not found
                
                if distance > current_threshold:
                    current_time = time.time()
                    
                    # Check cooldown to avoid rapid triggers
                    if current_time - last_trigger_time.get(finger_key, 0) > TRIGGER_COOLDOWN:
                        fingers_pressed[finger_key] = True
                        last_trigger_time[finger_key] = current_time
                        
                        # Press feedback - large text on screen
                        note_name = NOTE_NAMES.get(finger_key, "Unknown")
                        cv2.putText(img, f"PLAYED: {note_name}", (imgWidth//2 - 200, imgHeight//2),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                        
                        # Add UART command to NUC140 here
                        print(f"Note {note_name} played by {current_hand} finger {finger_id}")
                
                # If finger is in pressed state, draw blue circle
                if fingers_pressed.get(finger_key, False):
                    # Large blue circle
                    cv2.circle(img, (xPos, yPos), 25, (255, 0, 0), cv2.FILLED)
                    # Inner white circle (for visibility)
                    cv2.circle(img, (xPos, yPos), 15, (255, 255, 255), cv2.FILLED)
                    
                    # Display note name
                    note_name = NOTE_NAMES.get(finger_key, "")
                    cv2.putText(img, note_name, (xPos-25, yPos-25), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                
                # Reset fingers not continuously pressed
                if fingers_pressed.get(finger_key, False) and time.time() - last_trigger_time.get(finger_key, 0) > VISUAL_FEEDBACK_DURATION:
                    fingers_pressed[finger_key] = False
                    
                # Draw threshold line
                if DEBUG_MODE:
                    threshold_y = int((finger_baseline[finger_key] + current_threshold) * imgHeight)
                    cv2.line(img, (xPos - 15, threshold_y), (xPos + 15, threshold_y), (255, 0, 255), 2)
            
            # Display hand type
            wrist_x = int(handLms.landmark[0].x * imgWidth)
            wrist_y = int(handLms.landmark[0].y * imgHeight)
            cv2.putText(img, current_hand, (wrist_x-20, wrist_y-20), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Display image
    cv2.imshow('Virtual Piano - Separate Hand Settings', img)
    
    key = cv2.waitKey(1) 
    if key == ord('q'):
        break
    elif key == ord('d'):
        DEBUG_MODE = not DEBUG_MODE
        print(f"Debug mode: {'ON' if DEBUG_MODE else 'OFF'}")
    elif key == ord('+') or key == ord('='):  # Increase threshold (less sensitive)
        current_key = get_current_selection_key()
        distance_thresholds[current_key] *= 1.2  # REVERSED: multiply to increase
        print(f"{SELECTED_HAND} {get_finger_name(SELECTED_FINGER)} threshold increased: {distance_thresholds[current_key]:.3f}")
    elif key == ord('-') or key == ord('_'):  # Decrease threshold (more sensitive)
        current_key = get_current_selection_key()
        distance_thresholds[current_key] /= 1.2  # REVERSED: divide to decrease
        print(f"{SELECTED_HAND} {get_finger_name(SELECTED_FINGER)} threshold decreased: {distance_thresholds[current_key]:.3f}")
    elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:  # Select different finger
        finger_index = int(chr(key)) - 1  # Convert key to index (0-4)
        SELECTED_FINGER = ALL_FINGER_TIPS[finger_index]
        print(f"Selected finger: {SELECTED_HAND} {get_finger_name(SELECTED_FINGER)}")
    elif key == ord('l') or key == ord('L'):  # Select left hand
        SELECTED_HAND = "Left"
        print(f"Selected hand: {SELECTED_HAND}")
    elif key == ord('r') or key == ord('R'):  # Select right hand
        SELECTED_HAND = "Right"
        print(f"Selected hand: {SELECTED_HAND}")
    elif key == ord('c'):  # Reset baselines
        for hand in ["Left", "Right"]:
            for finger_id in ALL_FINGER_TIPS:
                finger_baseline[f"{hand}_{finger_id}"] = 1.0
        print("Baselines reset")

cap.release()
cv2.destroyAllWindows()