import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pywhatkit

engine = pyttsx3.init()
listener = sr.Recognizer()

def talk(text):
    engine.say(text)
    engine.runAndWait()

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
    elif "exit" in command:
        talk("Goodbye!")
        exit()
    else:
        talk("I didn't understand that command")

while True:
    run_assistant()