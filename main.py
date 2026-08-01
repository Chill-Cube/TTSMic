import customtkinter
from gtts import gTTS
import pygame
import time
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

pygame.mixer.init()

def say_tts(event):
    file_name = f"{time.time()}.mp3"

    tts = gTTS(text=entry.get(), lang='en')
    tts.save(file_name)
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()

    check_playback(file_name)


def check_playback(file_name):
    if pygame.mixer.music.get_busy():
        root.after(150, check_playback, file_name)
    else:
        pygame.mixer.music.unload()
        os.remove(file_name)

root = customtkinter.CTk()
root.geometry("500x300")
root.title("TTSMic")
root.resizable(False, False) 

frame = customtkinter.CTkFrame(root, fg_color="transparent")
frame.place(relx=0.5, rely=0.5, anchor="center")

label = customtkinter.CTkLabel(frame, text="TTSMic", font=("Arimo", 50))
label.pack()

entry = customtkinter.CTkEntry(frame, placeholder_text="Speak your mind", width=400)
entry.pack(pady=12)
entry.bind("<Return>", say_tts)

button = customtkinter.CTkButton(frame, text="Enter", command=say_tts)
button.pack(pady=12)

root.mainloop()