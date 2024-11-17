import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal
import asyncio
import threading
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import pyautogui

class Bridge(QObject):
    talkEngine = pyttsx3.init()
    talkEngine.setProperty('voice', talkEngine.getProperty('voices')[1].id)
    talkEngine.setProperty('rate', 145)
    showApp = Signal(bool)
    
    def speak(self,text):
        self.talkEngine.say(text)
        self.talkEngine.runAndWait()

    @Slot()
    def on(self):
        global listen
        print("ON")
        listen = True
        threading.Thread(target=run_async_task, daemon=True).start()
        self.speak("Listening now!")

    @Slot()
    def off(self):
        global listen
        listen = False
        print("OFF")

    @Slot()
    def show_win(self,a):
        self.showApp.emit(a)

listen = False
typeModeOn = False
bridge = Bridge()
async def run():
    while listen:
        listenSpeech()
        await asyncio.sleep(1)

def listenSpeech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('...\n')
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            if listen:
                print('wait...\n')
                query = r.recognize_google(audio, language='en-in')
                print(f">>|{query}|\n")
                asyncio.create_task(execute(query))
        except Exception as e:
            print("Rejecting noice...")

def google_search(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
def open_settings():
    os.system('start ms-settings:')
def typeText(text):
    if text=='full stop':
        pyautogui.typewrite(". ", interval=0)
        return
    pyautogui.typewrite(text, interval=0.1)

async def execute(speech):
    global typeModeOn
    if typeModeOn:
        if speech=='stop':
            typeModeOn=False
            bridge.speak('Stopped typing')
            return
        typeText(speech)
    if speech=="show yourself":
        print("show")
        bridge.show_win(True)
    elif speech=='hide yourself':
        print('hide')
        bridge.show_win(False)
    elif speech=='type for me':
        typeModeOn=True
        bridge.speak('Ready to type')
        print('typing')

    else:
        speech=speech.lower()
        if 'time' in speech:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            bridge.speak(f"It's {strTime}")
        elif 'search' in speech:
            speech=speech.replace('search','')
            print(speech)
            google_search(speech)
        elif 'open' or 'show' or 'start' in speech:
            if 'youtube' in speech:
                webbrowser.open('https://www.youtube.com')
            elif 'email' in speech:
                webbrowser.open('https://www.gmail.com')
            elif 'facebook' in speech:
                webbrowser.open('https://www.facebook.com')
            elif 'computer settings' in speech:
                open_settings()
            elif 'notepad' in speech:
                os.system('notepad.exe')
            else:
                print("nothing")

def start_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

def run_async_task():
    asyncio.run(run())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop_thread = threading.Thread(target=start_loop, daemon=True)
    loop_thread.start()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('bridge', bridge)
    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
