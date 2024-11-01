import tkinter as tk
import pygame
import os

pygame.mixer.init()

SOUND_PATH = "C:/Users/USUARIO/Desktop/Python/Python_Code/"

def play_sound(note):
    try:
        full_path = os.path.join(SOUND_PATH, f"{note}.wav")
        print(f"Loading: {full_path}")  # Debugging print
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error loading sound file for {note}: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Piano")

# Define notes and colors
notes = ["C", "D", "E", "F", "G", "A", "B", "C5"]
colors = ["white", "white", "white", "white", "white", "white", "white", "white"]

# Create piano buttons
for i, note in enumerate(notes):
    color = colors[i]
    button = tk.Button(root, text=note, width=5, height=10, bg=color, command=lambda n=note: play_sound(n))
    button.grid(row=0, column=i)

# Run the Tkinter main loop
root.mainloop()
