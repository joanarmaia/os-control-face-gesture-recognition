
import face_recognition
import cv2
import numpy as np
import os
import time
import pyttsx3



countU = 0
countJ = 0

# Get video
webcam = cv2.VideoCapture(0)

# Load my picture
joana_image = face_recognition.load_image_file("./images/faces/joana/00000.png")
joana_face_encoding = face_recognition.face_encodings(joana_image)[0]

# Get my face and my name
known_face_encodings = [joana_face_encoding]
known_face_names = ["Joana"]

# variables
face_locations = []
face_encodings = []

# Initial Greeting
engine = pyttsx3.init()
voice_num = 0
text_to_say1 = "Welcome to your Personal Assistance Service! I'm ProjectV, but you can call me 'Vee' "
text_to_say2 = "Please step in front of the camera for biometric scan!"
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[voice_num].id)
engine.say(text_to_say1)
time.sleep(3)
engine.say(text_to_say2)
engine.runAndWait()

process_this_frame = True

flagJ = False
flagU = False

while True:

    # Grab a single frame of video
    ret, frame = webcam.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for my face
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"


            # If it's my face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                countJ +=1

                if name == "Joana" and flagJ == False and countJ > 8:
                    # Joana Greeting
                    engine = pyttsx3.init()
                    voice_num = 0
                    text_to_say1 = "Biometric Scan accepted!"
                    text_to_say2 = "Hello Joana! It is a pleasure to see you! Initializing GestureCommand controls !"
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[voice_num].id)
                    engine.say(text_to_say1)
                    engine.say(text_to_say2)
                    engine.runAndWait()
                    #os.system("start https://www.youtube.com/watch?v=Nk7S7D0CQOY")

                    webcam.release()
                    cv2.destroyAllWindows()

                    os.system("conda activate face_recog && python C:/Users/joana/IRONHACK/Projects/final/src/gesture_recognition.py")
                    flagJ = True


            if name != "Joana":
                name = "Unknown"
                countU += 1

            if name != "Joana" and flagU == False and countU >= 5:
                # Unknown Face
                engine = pyttsx3.init()
                voice_num = 0
                text_to_say1 = "Unknown face detected"
                text_to_say2 = "Sorry, you are not Joana. You don't have access to GestureCommand controls!"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.say(text_to_say2)
                engine.runAndWait()
                flagU = True


            face_names.append(name)
                

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the faces
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)



    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
webcam.release()
cv2.destroyAllWindows()