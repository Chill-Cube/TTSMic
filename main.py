import customtkinter
from gtts import gTTS
import pygame
import time
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

pygame.mixer.init()

class TTSMicApp:

    """A class handling TTS UI, Input and local Output. """
     
    def __init__(self):
        """Initialises ui elements"""

        self.root = customtkinter.CTk()
        self.frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.label = customtkinter.CTkLabel(self.frame, text="TTSMic", font=("Arimo", 50))
        self.entry = customtkinter.CTkEntry(self.frame, placeholder_text="Speak your mind", width=400)
        self.button = customtkinter.CTkButton(self.frame, text="Enter", command=self.say_tts)

        self.setup_ui()

    def setup_ui(self):
        """Give ui properties and pack it into the root"""

        self.root.geometry("500x300")
        self.root.title("TTSMic")
        self.root.resizable(False, False) 

        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label.pack()

        self.entry.pack(pady=12)
        self.entry.bind("<Return>", self.say_tts_input)

        self.button.pack(pady=12)

    def check_playback(self, file_name):
        """Loops until the music player isn't playing any music. From there, it deletes the audio file."""

        if pygame.mixer.music.get_busy():
            self.root.after(150, self.check_playback, file_name)
        else:
            pygame.mixer.music.unload()
            os.remove(file_name)

    def say_tts_input(self, event):
        """Calls say_tts from the entry bind."""

        self.say_tts()

    def say_tts(self):
        """Retrieves text in the entry box then turns it into speech in a .mp3 file."""

        if pygame.mixer.music.get_busy(): return # Prevents spam

        file_name = f"{time.time()}.mp3"

        tts = gTTS(text=self.entry.get(), lang='en')
        tts.save(file_name)
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()

        self.check_playback(file_name) # Start check loop


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TTSMicApp()
    app.run()




        