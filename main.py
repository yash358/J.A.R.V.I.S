import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
from datetime import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import psutil
from pygame import mixer
import json
import requests
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        r.energy_threshold = 300
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email', 'password')
    server.sendmail('your email', to, content)
    server.close()


def musiconloop(file, stopper):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play(loops=-1)


    while True:
        input_of_user = input()
        if input_of_user == stopper:
            mixer.music.stop()
            break


if __name__ == "__main__":
    wishMe()
    init_battery = time.time()
    battery_secs = 20
    init_water = time.time()
    # init_eyes = time.time()
    # init_exercise = time.time()
    watersecs = 1*60
    # exsecs = 2*60
    # eyessecs = 10*60
    while True:
        query = takeCommand().lower()

        #battery
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged
        # Logic for executing tasks based on query
        if 'jarvis' in query:
            query = query.replace('jarvis', '')
            query = query.strip()
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.strip()
                print(query)
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open vs code' in query:
                codePath = "C:\\Users\\ASUS\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codePath)

            # elif 'open youtube' in query:
            #     webbrowser.open("www.youtube.com")
            #
            # elif 'open google' in query:
            #     webbrowser.open("www.google.com")
            #
            # elif 'open stackoverflow' in query:
            #     webbrowser.open("www.stackoverflow.com")
            elif 'open' in query:
                web = query.replace('open', '')
                web = web.replace(" ", "")
                webbrowser.open("www." + web + ".com")


            elif 'play music' in query:
                music_dir = 'D:\music'
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))

                # webbrowser.open("https://open.spotify.com/collection/tracks")


            elif 'time' in query:
                strTime = datetime.now().strftime("%H:%M:%S")
                print(strTime)
                speak(f"Sir, the time is {strTime}")



            # elif 'email to yash' in query:
            #     try:
            #         speak("What should I say?")
            #         content = takeCommand()
            #         to = "receiver's email"
            #         sendEmail(to, content)
            #         speak("Email has been sent!")
            #     except Exception as e:
            #         print(e)
            #         speak("Sorry Sir. I am not able to send this email")

            elif 'news' in query:
                speak('News for Today .. ')

                speak('So first news is..')
                url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=22fa274e85764348aa45e21d5c3026d3'
                news = requests.get(url).text
                news_dict = json.loads(news)
                arts = news_dict['articles']
                # n = len(arts)
                n = 5
                i = 0
                for article in arts:
                    time.sleep(1)
                    if i == n - 1:
                        speak("Today's last News is..")
                        print(article['title'])
                        speak(article['title'])
                        break
                    print(article['title'])
                    speak(article['title'])
                    i += 1
                    time.sleep(1)
                    if i != n - 1:
                        speak("Moving to the next news..")

            elif 'exit' in query:
                speak('Thank You Sir. Have a nice day')
                break


        if not plugged and percent < 45:
            if time.time() - init_battery > battery_secs:
                speak(f"Sir Please Charge Your Laptop {percent}% battery remaining")
                init_battery = time.time()

        if time.time() - init_water > watersecs:
            speak('Sir Please Drink Water')
            print("Water Drinking time. Enter 'drank' to stop the alarm.")
            musiconloop('Drink Water And Mind My Business.mp3', 'drank')
            init_water = time.time()

        # if time.time() - init_eyes > eyessecs:
        #     speak('Eye exercise time')
        #     print("Eye exercise time. Enter 'doneeyes' to stop the alarm.")
        #     musiconloop('Open Your Eyes ALARM.mp3', 'doneeyes')
        #     init_eyes = time.time()
        #
        # if time.time() - init_exercise > exsecs:
        #     speak('Physical Activity Time')
        #     print("Physical Activity Time. Enter 'donephy' to stop the alarm.")
        #     musiconloop('Workout Alarm.mp3', 'donephy')
        #     init_exercise = time.time()

