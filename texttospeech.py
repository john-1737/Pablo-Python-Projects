"""Text To Speech Talker, by Al Sweigart al@inventwithpython.com
An example program using the text-to-speech features of the pyttsx3
module.
View this code at https://nostarch.com/big-book-small-python-projects
Tags: tiny, beginner"""

import sys
from tkinter import messagebox, simpledialog

try:
    import pyttsx3
except ImportError:
    messagebox.showwarning(message='''The pyttsx3 module needs to be installed to run thisprogram. On Windows, open a Command Prompt and run:
pip install pyttsx3
On macOS and Linux, open a Terminal and run:
pip3 install pyttsx3''')
    sys.exit()

tts = pyttsx3.init()  # Initialize the TTS engine.

messagebox.showinfo(message='''Welcome to Text To Speech Talker!
Text-to-speech using the pyttsx3 module, which in turn uses
the NSSpeechSynthesizer (on macOS), SAPI5 (on Windows), or
eSpeak (on Linux) speech engines.
Inspired by Al Sweigart's Text To Speech Talker.''')

while True:
    text = simpledialog.askstring('Text To Speech Talker', 'Enter the text to speak, or press Cancel to quit.')

    if text == '':
        sys.exit()

    tts.say(text)  # Add some text for the TTS engine to say.
    tts.runAndWait()  # Make the TTS engine say it.
