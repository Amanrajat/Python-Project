
import datetime
from random import random
import pyttsx3
import speech_recognition as sr
import webbrowser
from plyer import notification
import pyautogui 
import time
import os
import psutil
import wikipedia
import pywhatkit as pwk
import mtranslate
import pygame
# import yt_dlp
import subprocess
# import mpv

mpv_process = None
mpv_socket = "/tmp/mpvsocket"

def speak(audio):
    # function to make the assistant speak
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty("rate", 150)
    engine.say(audio)
    engine.runAndWait()

def command():
    content = ""
    while content == "":
        """ Function to recognize voice commands """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Adjusting for background noise... Please wait.")
            r.adjust_for_ambient_noise(source, duration=2)  # Helps with noisy environments
            
            print("Say something...")
            r.energy_threshold = 800  # Adjust sensitivity to voice
            r.pause_threshold = 0.5  # Adjust pause time (allows brief pauses)
            audio = r.listen(source, phrase_time_limit=15)  # Listens for up to 15 seconds

        try:
            print("Processing...")
            content = r.recognize_google(audio, language='en-in')
            print("You said: " + content)
            return content.lower()
        except Exception as e:
            print("Please try again.....")


# """ Closes an application by its process name """
def close_application(app_name):
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if app_name.lower() in process.info["name"].lower():
            os.kill(process.info["pid"], 9)  # Force kill the process
            speak(f"Closing {app_name}")
            print(f"Closing {app_name}...")
            return
    speak(f"Could not find {app_name} running.")
    print(f"Could not find {app_name} running.")            

# """ Function to take a screenshot """
def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"screenshot_{timestamp}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_name)
    speak("Screenshot taken and saved as " + screenshot_name)
    print("Screenshot saved as:", screenshot_name)

# Keep asking for input until valid speech is detected
def main_process():
    while True:
        request = command()
        if not request:
            continue
# start 
        if "hello jarvis" in request:
            print("You said........... : ", request)
            print("Welcome, how can I help you?")
            speak("Welcome, how can I help you?")
# play any music 
        elif "play music" in request:
            request = request.replace("jarvis ", "")
            request = request.replace("play music ", "")
            webbrowser.open("https://www.youtube.com/results?search_query=" + request)
               
#check current time
        elif "current time" in request:    
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is : "+ str(now_time))
            print("Current time is : "+ str(now_time))
#check today date 
        elif "today date" in request:    
            now_date = datetime.datetime.now().strftime("%d-%m-%Y")  
            speak("Today's date is: " + now_date)  
            print("Today's date is:", now_date)
#add any new task in the file  
        elif "new task" in request:
            task = request.replace("new task", "") 
            task = task.strip()
            if task != "":
                speak("Adding task: " + task)
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")
# read any task using txt file
        elif "speak task" in request:
            try:
                with open("todo.txt", "r") as file:
                    tasks = file.read().strip()
                if tasks:
                    speak("Your tasks for today are: " + tasks)
                    print("Your tasks:", tasks)
                else:
                    speak("No tasks found.")
            except FileNotFoundError:
                speak("No task list found.")

#show txt notification    
        elif "show work" in request:
            try:
                with open("todo.txt", "r") as file:
                    tasks = file.read().strip()
                if tasks:
                    notification.notify(
                        title="Today's Work",
                        message=tasks,
                        timeout=10
                    )
                else:
                    speak("No tasks found.")
            except FileNotFoundError:
                speak("No task list found.")
#open any file & application 
        elif "open" in request:
            app_name = request.replace("open", "").strip()
            if app_name:  
                pyautogui.press("super")   
                pyautogui.typewrite(app_name)
                pyautogui.sleep(2)
                pyautogui.press("enter")
                speak("Opening " + app_name)
            else:
                speak("Please specify an application to open.")
# screenshot
        elif "screenshot" in request:
            take_screenshot() 
# close any file and application
        elif "close" in request:
            app_name = request.replace("close", "").strip()
            if app_name:
                close_application(app_name)
            else:
               speak("Please specify an application to close.") 
               
#search any wiki content  
        elif "wikipedia" in request:
            request = request.replace("hey jarvis", "")
            request = request.replace("search wikipedia", "")
            print(request) 
            # wikipedia.set_lang("hi") 
            result = wikipedia.summary(request, sentences=10)  
            print(result) 
            speak(result)
# search any content with the help of jarvis
        elif "search google" in request:
            request = request.replace("jarvis ", "")
            request = request.replace("search google ", "")
            webbrowser.open("https://www.google.com/search?q=" + request)
#whatsapp msg 
        elif "send whatsapp" in request:
            pwk.sendwhatmsg("+917238844900", "Hi, how are you?", 1, 25, 30)
#send email
        elif "send email" in request:
            pwk.send_mail("amansrivastava072@gmail.com",
                           user_config.gmail_password,
                          "hello" ,
                          "hello, how are you",
                          "amanofficial072@gmail.com"
                          )
            speak("Email sent")

if __name__ == "__main__":
    main_process()

