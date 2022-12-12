
# Importing libraries ---------------------------------------------------------------------------
import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque
import os
import pyttsx3
import time
from datetime import datetime
import speech_recognition as sr
import cv2 as cv
import numpy as np
import mediapipe as mp
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlalchemy as alch
from getpass import getpass
from dotenv import load_dotenv
import pymysql
from imutils.video import VideoStream
import imutils
import plotly.express as px
import pandas as pd

from gesture_classifier import KeyPointClassifier
from gesture_recognition_functions import *


# Sytem Speech Settings -------------------------------------------------------------------------
engine = pyttsx3.init()
voice_num = 0


# Counters for detection pause ------------------------------------------------------------------
count0 = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0

# Command line arguments ------------------------------------------------------------------------
args = get_args()

video_device = args.device
video_width = args.width
video_height = args.height

use_static_image_mode = args.use_static_image_mode
min_detection_confidence = args.min_detection_confidence
min_tracking_confidence = args.min_tracking_confidence

use_rectangle = True

# Camera preparation ----------------------------------------------------------------------------
video = cv.VideoCapture(video_device)
video.set(cv.CAP_PROP_FRAME_WIDTH, video_width)
video.set(cv.CAP_PROP_FRAME_HEIGHT, video_height)

# Loading mediapipe and the model ---------------------------------------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=use_static_image_mode,
    max_num_hands=1, 
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence,
)

gesture_classifier = KeyPointClassifier()

# Get gesture names -----------------------------------------------------------------------------
with open('data/gestures_names.csv', encoding='utf-8-sig') as f:
    gestures_names = csv.reader(f)
    gestures_names = [row[0] for row in gestures_names]


# VIDEO RECOGNITION -----------------------------------------------------------------------------

mode = 0 # set to normal video mode

# Initial Greeting ------------------------------------------------------------------------------
text_to_say1 = "You have now access to Gesture Command Controls!"
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[voice_num].id)
engine.say(text_to_say1)
engine.runAndWait()

while True:

    # Press ESC to stop program -----------------------------------------------------------------
    key = cv.waitKey(10)
    if key == 27:  # ESC
        break

    number, mode = select_mode(key, mode)

    # Camera capture ----------------------------------------------------------------------------
    ret, image = video.read()
    if not ret:
        break
    image = cv.flip(image, 1)  # Mirror image
    debug_image = copy.deepcopy(image)

    # Detecting hands ---------------------------------------------------------------------------
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB) #convert to color

    image.flags.writeable = False
    results = hands.process(image) 
    image.flags.writeable = True


    if results.multi_hand_landmarks is not None:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                results.multi_handedness):
            # Bounding box calculation
            rectangle = calculate_rectangle(debug_image, hand_landmarks)
            # Landmark calculation
            landmark_list = calculate_each_landmark(debug_image, hand_landmarks)

            # Conversion to relative coordinates / normalized coordinates
            pre_processed_landmark_list = pre_process_landmark(landmark_list)

            # Write to the dataset file
            logging_csv(number, mode, pre_processed_landmark_list)


            # Hand sign classification
            hand_sign_id = gesture_classifier(pre_processed_landmark_list)

            # Counters
            if hand_sign_id == 0:
                count0 += 1
            if hand_sign_id == 1:
                count1 += 1
            if hand_sign_id == 2:
                count2 += 1
            if hand_sign_id == 3:
                count3 += 1
            if hand_sign_id == 4:
                count4 += 1
            if hand_sign_id == 5:
                count5 += 1
            if hand_sign_id == 6:
                count6 += 1
            if hand_sign_id == 7:
                count7 += 1
            if hand_sign_id == 8:
                count8 +=1 
            if hand_sign_id == 9:
                count9 += 1

            # Drawing rectangle/landmarks/gesture name
            debug_image = draw_rectangle(use_rectangle, debug_image, rectangle)
            debug_image = draw_landmarks(debug_image, landmark_list)
            debug_image = draw_info_text(
                debug_image,
                rectangle,
                gestures_names[hand_sign_id])

            # Flags for stopping command 
            flag0 = False
            flag1 = False
            flag2 = False
            flag3 = False
            flag4 = False 
            flag5 = False
            flag6 = False
            flag7 = False
            flag8 = False
            flag9 = False

            # OPEN YOUTUBE 
            if hand_sign_id == 0 and flag0 == False and count0 >=15:
                text_to_say1 = "Opening YouTube"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.runAndWait()
                os.system("start https://www.youtube.com/")
                os.system("timeout 3")
                flag0 = True
                count0 = 0
        
            # OPEN GITHUB
            if hand_sign_id == 1 and flag1 == False and count1 >=15:
                text_to_say1 = "Opening GitHub!"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.runAndWait()
                os.system("start https://github.com/")
                os.system("timeout 3")
                flag1 = True
                count1 = 0

                text_to_say2 = "If you're going to work on something, don't forget to commit regularly!"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say2)
                engine.runAndWait()


            # OPEN WORD DOCUMENT
            if hand_sign_id == 2 and flag2 == False and count2 >=15:
                text_to_say1 = "Opening new Word Document!"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.runAndWait()
                os.system("type nul > new_document.docx")
                os.system("start new_document.docx")
                os.system("timeout 2")

                flag2 = True
                count2 = 0

            # OPEN LINKEDIN
            if hand_sign_id == 3 and flag3 == False and count3 >=15:
                text_to_say1 = "Opening LinkedIn!"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.runAndWait()
                os.system("start https://www.linkedin.com/home")
                os.system("timeout 3")
                flag3 = True
                count3 = 0

            # OPEN EXCEL
            if hand_sign_id == 4 and flag4 == False and count4 >= 15:
                text_to_say1 = "Opening new Excel Sheet!"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.runAndWait()
                #os.system("type nul >  new_sheet.xlsx")
                os.system("start new_sheet.xlsx")
                os.system("timeout 3")
                flag4 = True
                count4 = 0

            # OPEN NETFLIX
            if hand_sign_id == 5 and flag5 == False and count5 >= 15:
                
                now = datetime.now()
                current_time = int(now.strftime("%H"))

                text_to_say0 = "Opening Netflix!"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say0)
                engine.runAndWait()
                os.system("start https://www.netflix.com/browse")
                os.system("timeout 2")
                
                if current_time >= 8 and current_time < 12:
                    text_to_say1 = f"It's {current_time} in the morning! Shouldn't you be working?"
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[voice_num].id)
                    engine.say(text_to_say1)
                    engine.runAndWait()

                if current_time >= 14 and current_time <= 18:
                    text_to_say2 = "It's the middle of the afternoon! Shouldn't you be working?"
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[voice_num].id)
                    engine.say(text_to_say2)
                    engine.runAndWait()
                
                if current_time >= 23 or (current_time >= 0 and current_time <= 4):
                    text_to_say3 = "It's a bit late... Are you sure you should be watching Netflix right now?"
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[voice_num].id)
                    engine.say(text_to_say3)
                    engine.runAndWait()
            

                flag5 = True
                count5 = 0

            # Open Spotify
            if hand_sign_id == 6 and flag6 == False and count6 >= 15:
                text_to_say1 = "Opening Spotify!"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.runAndWait()
                os.system("start https://open.spotify.com/")
                os.system("timeout 3")
                flag3 = True
                count3 = 0
        

            # JOURNALING    
            if hand_sign_id == 8 and flag8 == False and count8 >=15:
                text_to_say1 = "How are you today Joana? I'm Listening! But only for 10 seconds"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.runAndWait()

                r = sr.Recognizer()
                def SpeakText(command):
                    # Initialize the engine
                    engine = pyttsx3.init()
                    engine.say(command)
                    engine.runAndWait()
                with sr.Microphone() as source2:
                    r.adjust_for_ambient_noise(source2, duration=0.2)
                    audio2 = r.record(source2, duration = 10)
                    mytext = r.recognize_google(audio2)
                
                print(mytext)
                flag8 = True
                count8 = 0

                # Sentiment Analysis
                sia = SentimentIntensityAnalyzer()
                mysentiment = sia.polarity_scores(mytext)
                mysentiment = list(mysentiment.values())[3]
                mysentiment = float(mysentiment)

                if mysentiment < 0:
                    text_to_say2 = "I'm sorry to hear that. Remember everything is temporary and soon you'll be okay again"
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[voice_num].id)
                    engine.say(text_to_say2)
                    engine.runAndWait()
                
                if mysentiment > 0:
                    text_to_say3 = "I'm so happy you are having a good day!"
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[voice_num].id)
                    engine.say(text_to_say3)
                    engine.runAndWait()

                text_to_say4 = "On a scale of 0 to 10, with 10 being super happy, how are you feeling?"
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say4)
                engine.runAndWait()
                
                r = sr.Recognizer()
                def SpeakText(command):
                    # Initialize the engine
                    engine = pyttsx3.init()
                    engine.say(command)
                    engine.runAndWait()
                with sr.Microphone() as source2:
                    r.adjust_for_ambient_noise(source2, duration=0.2)
                    audio3 = r.record(source2, duration = 5)
                    scalemood = r.recognize_google(audio3)
                
                scalemood = int(scalemood)

                print(scalemood)

                # Getting date and time
                nowtoday = datetime.now()
                nowtoday = str(nowtoday)
                nowtoday = nowtoday[:16]

                print(nowtoday)

                # Loading entries to sql
                load_dotenv()
                password = os.getenv('sql_password')
                dbName = "mood"
                connectionData=f"mysql+pymysql://root:{password}@localhost/{dbName}"
                engine = alch.create_engine(connectionData)
                engine.execute(f'''
                INSERT INTO entries(date, text, scale, sentiment) VALUES('{nowtoday}', "{mytext}", {scalemood}, {mysentiment})''')
                

                text_to_say5 = "Your mood was loaded successfully to the database!"
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say5)
                engine.runAndWait()

            # OPEN RECORDS
            if hand_sign_id == 7 and flag7 == False and count7 >= 15:
                text_to_say1 = "Opening Mood Records!"
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.runAndWait()
                #os.system("conda activate face_recog && python src/mood_analysis.py")
                
                # Connecting to SQL
                load_dotenv()
                password = os.getenv('sql_password')
                dbName = "mood"
                connectionData=f"mysql+pymysql://root:{password}@localhost/{dbName}"
                engine = alch.create_engine(connectionData)
                # Getting dataframe
                mood = pd.read_sql_query('SELECT * FROM entries', engine)
                fig = px.bar(mood, x='date', y="sentiment", title="Sentiment Analysis of user's mood over time", hover_data=['text'])
                fig.update_xaxes(rangeslider_visible=True)
                fig.update_layout(hovermode="x unified")
                fig.show()

                os.system("timeout 3")

                flag4 = True
                count4 = 0                
                

            # STOP PROGRAM
            if hand_sign_id == 9 and flag9 == False and count9 >= 20:
                flag9 = True
                
                video.release()
                cv.destroyAllWindows()

                text_to_say1 = "ProjectV is now terminated!"
                text_to_say2 = "Goodbye Joana! Hope to see you soon"
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[voice_num].id)
                engine.say(text_to_say1)
                engine.say(text_to_say2)
                engine.runAndWait()
                count9 = 0

                  

    debug_image = draw_info(debug_image, mode, number)


    # SHOW SCREEN --------------------------------------------------------------------------
    cv.imshow('Hand Gesture Recognition', debug_image)

video.release()
cv.destroyAllWindows()
