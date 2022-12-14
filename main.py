from pprint import pprint
from functions.online_ops import OPENWEATHER_APP_ID
from functions.os_ops import open_camera, open_cmd, open_discord, open_notepad, open_calculator
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email
import requests
import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
from utils import opening_text

USERNAME = config('USER')
BOTNAME = config('BOTNAME')
STATE_CODE = 'WI'
COUNTRY_CODE = 'US'
CITY_NAME = 'MIDDLETON'

engine = pyttsx3.init('sapi5')

# set rate
engine.setProperty('rate', 190)

# set volume
engine.setProperty('volume', 1.0)

# set voice (male)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


def greet_user():
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good Afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")


def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-us')
        if not 'exit' in query or 'stop' in query or 'done' in query or 'thanks' in query or 'thank you' in query or 'no' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak(f"Good night {USERNAME}, take care!")
            else:
                speak(f"Have a good day {USERNAME}!")
            exit()
    except Exception:
        speak("Sorry, I could not understand. Could you please say that again?")
        query = 'None'
    return query


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(
                f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do you want to search on Google?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send an email" in query:
            speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email sir.")
            else:
                speak(
                    "Something went wrong while I was sending the mail. Please check the error logs.")

        elif 'joke' in query:
            speak(f"Hope you like this one.")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Here's some advice for you.")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen.")
            pprint(advice)

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines.")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            speak("What location would you like to view the weather for?")
            weather_location = take_user_input().lower()
            # city = requests.get(
            # f"http://api.openweathermap.org/geo/1.0/direct?q={CITY_NAME},{STATE_CODE},{COUNTRY_CODE}&limit={1}&appid={OPENWEATHER_APP_ID}").text
            #ip_address = find_my_ip()
            #city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            city = 'Middleton'
            state = 'US'

            print(city)

            speak(f"Getting weather report for your city {city}, {state}")
            weather, temperature, feels_like = get_weather_report(
                city, state)
            speak(
                f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report shows it is {weather}")
            speak("For your convenience, I am printing it on the screen.")
            print(
                f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
        speak("Is there anything else I can do for you?")
