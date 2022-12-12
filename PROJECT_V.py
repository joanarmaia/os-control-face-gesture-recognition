
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import imutils
import os

myimage = "images/aesthetic/interface1.png"

interface = tk.Tk()
interface.geometry("531x531+200+50")
interface.title("PROJECT'V' - O.S. Personal Assistant")
interface.resizable(width=False, height=False)
background = tk.PhotoImage(file=myimage)
background1 = tk.Label(interface, image=background).place(x=0, y=0)

# Colors
button_color = "#ffffff"

#command
def openProgram ():
    os.system("conda activate face_recog && python src/program.py")

def openREADME():
    os.system("start https://github.com/joanarmaia/final/blob/main/README.md")

# Buttons
button1 = tk.Button(interface, text="START", bg=button_color, fg='#000000', relief="flat", cursor="hand2", command = openProgram,width=9, height=1, font=("Bahnschrift Light", 16))
button1.place(x=220, y=243)

button2 = tk.Button(interface, text="?", bg=button_color, fg='#000000', relief="flat", cursor="hand2", command = openREADME, width=2, height=1, font=("Bahnschrift Light", 15))
button2.place(x=472, y=472)


interface.mainloop()