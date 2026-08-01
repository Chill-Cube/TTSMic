import customtkinter
from gtts import gTTS
import pygame
import time
import os
from virtual_mic import VirtualMic
import threading

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class TTSApp:

    """A tkinter-based text-to-speech application that converts text input to audio playback."""
     
    def __init__(self):
        """Initialise the TTS Application with ui elements

        Creates all necessary GUI elements and sets up the user interface.
        """

        self.root = customtkinter.CTk()
        self.frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.label = customtkinter.CTkLabel(self.frame, text="TTSMic", font=("Arimo", 50))
        self.entry = customtkinter.CTkEntry(self.frame, placeholder_text="Speak your mind", width=400)
        self.button = customtkinter.CTkButton(self.frame, text="Enter", command=self.say_tts)

        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        self.setup_ui()

    def setup_ui(self):
        """Give ui properties and pack it into the root window."""

        self.root.geometry("500x300")
        self.root.title("TTSMic")
        self.root.resizable(False, False) 

        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label.pack()

        self.entry.pack(pady=12)
        self.entry.bind("<Return>", self.say_tts_input)

        self.button.pack(pady=12)

    def check_playback(self, file_name):
        """Loops until the music player isn't playing any music. From there, it deletes the audio file.
        Args:
            file_name (str): Path to the temporary audio file to be deleted
        """

        if pygame.mixer.music.get_busy():
            self.root.after(150, self.check_playback, file_name)
        else:
            pygame.mixer.music.unload()
            os.remove(file_name)

    def say_tts_input(self, event):
        """Calls say_tts from the entry bind.
        
        Args:
            event: The tkinter event object (not used)
        """

        self.say_tts()

    def say_tts(self):
        """Retrieves text in the entry box then turns it into speech in a .mp3 file."""

        if pygame.mixer.music.get_busy(): return # Prevents spamming audio playback

        file_name = f"{time.time()}.mp3"

        tts = gTTS(text=self.entry.get(), lang='en')
        tts.save(file_name)

        mic = VirtualMic()

        def play_to_others():
            mic.play_in_mic(file_name)

        def play_to_self():
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play()

        thread1 = threading.Thread(target=play_to_others) 
        thread2 = threading.Thread(target=play_to_self) 

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        
        pygame.mixer.music.unload()
        os.remove(file_name)
        

    def run(self):
        """Start the main application loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = TTSApp()
    app.run()




        