import speech_recognition as sr
import webbrowser
import pyttsx3
import subprocess
import os
import requests
from win10toast import ToastNotifier
from datetime import date
import keyboard
import time
import sys

engine = pyttsx3.init()
engine.setProperty('volume', 0.05)
engine.setProperty('rate', 190)

def recognise(msg="Powiedz coś"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(msg)
        audio = r.listen(source)
        try:
            recognised_text = r.recognize_google(audio, language="pl-PL")
            print("Powiedziałeś: " + recognised_text)
            return recognised_text.lower()
        except sr.UnknownValueError:
            print("Nie mogłem zrozumieć co powiedziałeś") 
            return None
        except sr.RequestError as e:
            print("ERROR", e)
            return None

def get_weather(city_name):
    api_key = "7f65d64dd758ebad7126c5e51b282423"
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    complete_url = base_url + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    x = response.json()
    
    if x["cod"] != "404":
        y = x["main"]
        temp = y["temp"]
        temp_odcz = y["feels_like"]
        cisnienie = y["pressure"]
        wilgot = y["humidity"]

        today = date.today().strftime("%d %B %Y")
        toaster = ToastNotifier()
        toaster.show_toast("Pogoda dzisiaj (" + today + ") w " + city_name,
                           "Temperatura: " + str(round(temp - 273.15)) + "°C" +
                            "\nOdzuwalna: " + str(round(temp_odcz - 273.15)) + "°C" +
                            "\nCiśnienie: " + str(cisnienie) + "hPa" +
                            "\nWilgotność: " + str(wilgot) + "%",
                            duration=10)
    else:
        print("Nie znaleziono miasta!")

text = recognise()
if text:
    word_list = text.split(" ")  
    if ("otwórz" in text and word_list[0] == "otwórz") or ("uruchom" in text and word_list[0] == "uruchom"): 
        if "przeglądarkę" in text: 
            engine.say("Otwieram przeglądarkę") 
            engine.runAndWait()
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get('chrome').open_new_tab("http://www.google.com")
        
        elif "discorda" in text: 
            engine.say("Otwieram Discorda")
            engine.runAndWait()
            path = os.path.expanduser("~") + "\\AppData\\Local\\Discord\\app-1.0.9152\\Discord.exe"
            subprocess.call([path])
            sys.exit()

    elif "jaka jest pogoda" in text: 
        engine.say("Podaj nazwę miasta")
        engine.runAndWait()
        city_name = recognise("Powiedz nazwę miasta")
        if city_name:
            get_weather(city_name)
        else:
            engine.say("Nie rozumiem, powiedz jeszcze raz")
            engine.runAndWait()
    
    elif "wyslij maila" in text or "wyslij e-mail" in text: 
        if "bez adresata" in text:
            webbrowser.open_new_tab("mailto:")    
        else:
            engine.say("Podaj adres email")
            engine.runAndWait()
            adresat = recognise("Do kogo chcesz wysłać email? (powiedz \"nie\" jeśli nie chcesz podawać)")
            if adresat and adresat.lower() != "nie":
                adresat = adresat.replace(" ", "").lower()
                engine.say("Podaj temat maila")
                engine.runAndWait()
                temat = recognise("Podaj temat maila")
                engine.say("Podaj treść maila")
                engine.runAndWait()
                tresc = recognise("Podaj treść maila")
                mailto_link = f"mailto:{adresat}?subject={temat}&body={tresc}"
                webbrowser.open_new_tab(mailto_link)
                time.sleep(10)  
                keyboard.press_and_release("ctrl+enter")
            else:
                engine.say("Nie podano adresata")
                engine.runAndWait()
    
    elif "wyszukaj w google" in text:
        engine.say("Co mam wyszukać?")
        engine.runAndWait()
        search = recognise("Co mam wyszukać?")
        if search:
            webbrowser.open_new_tab(f"http://www.google.com/search?q={search}")
        else:
            engine.say("Nie rozumiem, powiedz jeszcze raz")
            engine.runAndWait()