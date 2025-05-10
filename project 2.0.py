import os
import uuid
import threading
import tkinter as tk
from tkinter import ttk
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from deep_translator import GoogleTranslator
import webbrowser

# Create an instance of Tkinter frame or window
win = tk.Tk()

# Set the geometry of tkinter frame
win.geometry("700x450")
win.title("Real-Time Voice🎙️ Translator🔊")

# Load icon
try:
    icon = tk.PhotoImage(file="icon.png")
    win.iconphoto(False, icon)
except Exception as e:
    print(f"Icon not loaded: {e}")

# Create labels and text boxes for the recognized and translated text
input_label = tk.Label(win, text="Recognized Text ⮯")
input_label.pack()
input_text = tk.Text(win, height=5, width=50)
input_text.pack()

output_label = tk.Label(win, text="Translated Text ⮯")
output_label.pack()
output_text = tk.Text(win, height=5, width=50)
output_text.pack()

# Blank space for layout
tk.Label(win, text="").pack()

# Create a dictionary of language names and codes
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "French": "fr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Punjabi": "pa"
}

language_names = list(language_codes.keys())

# Create dropdown menus for the input and output languages
input_lang_label = tk.Label(win, text="Select Input Language:")
input_lang_label.pack()

input_lang = ttk.Combobox(win, values=language_names)
input_lang.set("English")  # Default value
input_lang.pack()

down_arrow = tk.Label(win, text="▼")
down_arrow.pack()

output_lang_label = tk.Label(win, text="Select Output Language:")
output_lang_label.pack()

output_lang = ttk.Combobox(win, values=language_names)
output_lang.set("English")  # Default value
output_lang.pack()

# Blank space for layout
tk.Label(win, text="").pack()

keep_running = False

# Define the translation and audio functions
def update_translation():
    global keep_running

    if keep_running:
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Speak Now!")
                audio = r.listen(source)

            speech_text = r.recognize_google(audio)
            input_text.insert(tk.END, f"{speech_text}\n")

            input_language_code = language_codes.get(input_lang.get(), "auto")
            output_language_code = language_codes.get(output_lang.get(), "en")
            
            translated_text = GoogleTranslator(
                source=input_language_code,
                target=output_language_code
            ).translate(text=speech_text)
            
            voice = gTTS(translated_text, lang=output_language_code)
            unique_filename = f"voice_{uuid.uuid4().hex}.mp3"
            voice.save(unique_filename)
            
            playsound(unique_filename)
            os.remove(unique_filename)

            output_text.insert(tk.END, translated_text + "\n")

        except sr.UnknownValueError:
            output_text.insert(tk.END, "Could not understand!\n")
        except sr.RequestError:
            output_text.insert(tk.END, "Could not request results from Google Speech API.\n")
        except Exception as e:
            output_text.insert(tk.END, f"Error: {e}\n")

        win.after(100, update_translation)

def run_translator():
    global keep_running
    if not keep_running:
        keep_running = True
        threading.Thread(target=update_translation, daemon=True).start()

def kill_execution():
    global keep_running
    keep_running = False

def open_about_page():
    about_window = tk.Toplevel()
    about_window.title("About")
    about_window.iconphoto(False, icon)

    github_link = ttk.Label(
        about_window, 
        text="github.com/tharun/real-time-voice-translator", 
        foreground="blue", 
        cursor="hand2"
    )
    github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/tharun/real-time-voice-translator"))
    github_link.pack()

    about_text = tk.Text(about_window, height=10, width=50)
    about_text.insert("1.0", """
    A machine learning project that translates voice from one language to another in real time while preserving the tone and emotion of the speaker. Outputs the result in MP3 format. Choose input and output languages from the dropdown menu and start the translation!
    """)
    about_text.pack()

    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack()

# Create buttons for the GUI
run_button = tk.Button(win, text="Start Translation", command=run_translator)
run_button.place(relx=0.25, rely=0.9, anchor="c")

kill_button = tk.Button(win, text="Kill Execution", command=kill_execution)
kill_button.place(relx=0.5, rely=0.9, anchor="c")

about_button = tk.Button(win, text="About this project", command=open_about_page)
about_button.place(relx=0.75, rely=0.9, anchor="c")

# Run the Tkinter event loop
win.mainloop()
