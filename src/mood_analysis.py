
#importing libraries
import pandas as pd
from getpass import getpass
from dotenv import load_dotenv
import sqlalchemy as alch
import os
import numpy as np
import re
import random
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from datetime import datetime
import pyttsx3

# GRAPH ---------------------------------------------------------------------------------------------

# Connecting to SQL
load_dotenv()
password = os.getenv('sql_password')
dbName = "mood"
connectionData=f"mysql+pymysql://root:{password}@localhost/{dbName}"
engine = alch.create_engine(connectionData)

# Getting dataframe
mood = pd.read_sql_query('SELECT * FROM entries', engine) 
#print(mood)


# AVERAGE (MONTH)-------------------------------------------------------------------------------------------

# Getting months from database
datepoints = []
for date in mood.date:
    datepoints.append(date[5:7])
mood['month']=datepoints


# current date
nowtoday = datetime.now()
nowtoday = str(nowtoday)
month = nowtoday[5:7]

# entries for current month
monthly_mood = mood.loc[mood['month'] == month]

# current month average mood
avg = np.mean(monthly_mood.sentiment)

scale = 0
if avg <-0.8:
    scale = 0
elif avg>=-0.8 and avg<-0.6:
    scale = 1
elif avg>=-0.6 and avg<-0.4:
    scale = 2
elif avg>=-0.4 and avg<-0.2:
    scale = 3
if avg>=-0.2 and avg<0:
    scale = 4
elif avg == 0:
    scale = 5
elif avg>0 and avg<0.2:
    scale = 6
elif avg>=0.2 and avg<0.4:
    scale = 7
elif avg>=0.4 and avg<0.6:
    scale = 8
elif avg>=0.6 and avg<0.8:
    scale = 9
elif avg >= 0.8:
    scale = 10
    
# AVERAGE (ALL)-------------------------------------------------------------------------------------------

avgall = np.mean(mood.sentiment)

scale2 = 0
if avgall <-0.8:
    scale2 = 0
elif avgall>=-0.8 and avgall<-0.6:
    scale2 = 1
elif avgall>=-0.6 and avgall<-0.4:
    scale2 = 2
elif avgall>=-0.4 and avgall<-0.2:
    scale2 = 3
if avgall>=-0.2 and avgall<0:
    scale2 = 4
elif avgall == 0:
    scale2 = 5
elif avgall>0 and avgall<0.2:
    scale2 = 6
elif avgall>=0.2 and avgall<0.4:
    scale2 = 7
elif avgall>=0.4 and avgall<0.6:
    scale2 = 8
elif avgall>=0.6 and avgall<0.8:
    scale2 = 9
elif avgall >= 0.8:
    scale2 = 10

# 'V' SPEAKING -------------------------------------------------------------------------------------------

engine = pyttsx3.init()
voice_num = 0
text_to_say0 = f"The average of your mood this month was {scale} out of 10"
text_to_say1 = f"The average of all of your mood entries is {scale2} out of 10"
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[voice_num].id)
engine.say(text_to_say0)
engine.say(text_to_say1)
engine.runAndWait()

fig = px.bar(mood, x='date', y="sentiment", title="Sentiment Analysis of user's mood over time", hover_data=['text'])
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(hovermode="x unified")

fig.show()




