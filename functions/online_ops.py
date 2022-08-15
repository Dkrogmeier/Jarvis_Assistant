from ipaddress import ip_address
from shutil import ExecError
import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')
NEWS_API_KEY = config('NEWS_API_KEY')
OPENWEATHER_APP_ID = config('OPENWEATHER_APP_ID')
TMDB_API_KEY = config("TMDB_API_KEY")


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def play_on_youtube(video):
    kit.playonyt(video)


def play_on_spotify(song):
    pass


def search_on_google(query):
    kit.search(query)


def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def get_weather_report(city, state):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={OPENWEATHER_APP_ID}&units=imperial").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}°F", f"{feels_like}°F"


def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]


def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


def calender():
    """This returns google calender events for current day"""
    pass


def todo():
    """This returns to-do list for current day"""
    pass


def add_todo():
    """This adds elements to a to-do list for current day"""
    pass


def delete_todo():
    """This deletes elements from a to-do list for current day"""
    pass
