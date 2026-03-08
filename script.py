import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pywhatkit
import random

engine = pyttsx3.init()
listener = sr.Recognizer()

responses = [
    "I'm ready, sir.",
    "How can I help you?",
    "Yes, tell me your command.",
    "At your service!"
]

def talk(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        talk("Good morning!")
    elif hour < 18:
        talk("Good afternoon!")
    else:
        talk("Good evening!")
    talk(random.choice(responses))

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            return command
    except:
        return ""

def run_assistant():
    command = take_command()
    if not command:
        return

    print(f"Command: {command}")

    if "open youtube" in command:
        talk("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open chrome" in command:
        talk("Opening Chrome")
        os.system("open -a 'Google Chrome'" if os.name == "posix" else "start chrome")
    elif "play" in command:
        song = command.replace("play", "")
        talk(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        talk(f"The time is {now}")
    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        talk(f"Today's date is {today}")
    elif "who are you" in command or "your name" in command:
        talk("I am your advanced assistant, at your service!")
    elif "exit" in command or "quit" in command:
        talk("Goodbye! Have a nice day.")
        exit()
    else:
        talk("I didn't understand that. Can you repeat?")

greet_user()

while True:
    run_assistant()