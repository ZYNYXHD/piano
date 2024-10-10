import cv2
import mediapipe as mp
import pygame

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Initialize Pygame and load piano sounds
pygame.init()
key_sounds = {
    "C": pygame.mixer.Sound("sounds/C.wav"),
    "C#": pygame.mixer.Sound("sounds/C#.wav"),
    "D": pygame.mixer.Sound("sounds/D.wav"),
    "D#": pygame.mixer.Sound("sounds/D#.wav"),
    "E": pygame.mixer.Sound("sounds/E.wav"),
    "F": pygame.mixer.Sound("sounds/F.wav"),
    "F#": pygame.mixer.Sound("sounds/F#.wav"),
    "G": pygame.mixer.Sound("sounds/G.wav"),
    "G#": pygame.mixer.Sound("sounds/G#.wav"),
    "A": pygame.mixer.Sound("sounds/A.wav"),
    "A#": pygame.mixer.Sound("sounds/A#.wav"),
    "B": pygame.mixer.Sound("sounds/B.wav")
}

def play_piano_sound(key):
    """Plays the sound corresponding to the piano key."""
    if key in key_sounds:
        key_sounds[key].play()

def get_piano_key(x):
    """Maps the x-coordinate of the hand to a piano key."""
    if 0.0 <= x < 0.083:
        return "C"
    elif 0.083 <= x < 0.167:
        return "C#"
    elif 0.167 <= x < 0.25:
        return "D"
    elif 0.25 <= x < 0.333:
        return "D#"
    elif 0.333 <= x < 0.417:
        return "E"
    elif 0.417 <= x < 0.5:
        return "F"
    elif 0.5 <= x < 0.583:
        return "F#"
    elif 0.583 <= x < 0.667:
        return "G"
    elif 0.667 <= x < 0.75:
        return "G#"
    elif 0.75 <= x < 0.833:
        return "A"
    elif 0.833 <= x < 0.917:
        return "A#"
    elif 0.917 <= x <= 1.0:
        return "B"

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the x-coordinate of the tip of the index finger (landmark 8)
            x = hand_landmarks.landmark[8].x

            # Map x to a piano key
            key = get_piano_key(x)
            if key:
                play_piano_sound(key)

    # Display the resulting frame
    cv2.imshow("Virtual Piano", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to quit
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
