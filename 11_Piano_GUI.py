import tkinter as tk
from tkinter import messagebox
import pygame
import os
import time

pygame.mixer.init()

SOUND_PATH = "C:/Users/USUARIO/Desktop/Python/Python_Code/"
default_bpm = 120
note_durations = {
    "Whole": 4.0,
    "Half": 2.0,
    "Quarter": 1.0,
    "Eighth": 0.5,
    "Sixteenth": 0.25
}

# Initialize 4 measure slots
measures = [[] for _ in range(4)]
current_measure = 0


def play_sound(note):
    try:
        full_path = os.path.join(SOUND_PATH, f"{note}.wav")
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error loading sound file for {note}: {e}")


# Add note to current measure with duration
def add_note_to_measure(note, duration):
    if len(measures[current_measure]) < 4:
        measures[current_measure].append((note, duration))
        sequence_display.insert(tk.END, f"Measure {current_measure + 1}: {note} ({duration})\n")
    else:
        tk.messagebox.showinfo("Limit reached", "Each measure can only have 4 beats.")


# Play the recorded sequence based on BPM and the selected measure order
def play_sequence():
    bpm = int(bpm_entry.get())
    beat_duration = 60 / bpm

    # Get the order of measures and play accordingly
    measure_order = [int(m) - 1 for m in measure_order_entry.get().split(",") if m.isdigit()]

    for measure_index in measure_order:
        for note, duration in measures[measure_index]:
            play_sound(note)
            time.sleep(duration * beat_duration)


# Select measure to add notes
def select_measure(index):
    global current_measure
    current_measure = index
    sequence_display.insert(tk.END, f"\n--Selected Measure {current_measure + 1}--\n")


# Create main Tkinter window
root = tk.Tk()
root.title("Piano with Measure Recorder")

# Define notes and colors
notes = ["C", "D", "E", "F", "G", "A", "B", "C5"]
colors = ["white"] * len(notes)

# Create piano buttons
for i, note in enumerate(notes):
    color = colors[i]
    button = tk.Button(root, text=note, width=5, height=10, bg=color,
                       command=lambda n=note: add_note_to_measure(n, note_durations[note_type.get()]))
    button.grid(row=0, column=i)

# Select note type for each note added
note_type_label = tk.Label(root, text="Select Note Type:")
note_type_label.grid(row=1, column=0, columnspan=2, sticky="w")
note_type = tk.StringVar(value="Quarter")
note_type_menu = tk.OptionMenu(root, note_type, *note_durations.keys())
note_type_menu.grid(row=1, column=2)

# BPM entry to control speed
bpm_label = tk.Label(root, text="BPM:")
bpm_label.grid(row=2, column=0, sticky="w")
bpm_entry = tk.Entry(root, width=5)
bpm_entry.insert(0, str(default_bpm))
bpm_entry.grid(row=2, column=1, sticky="w")

# Display sequence of notes
sequence_display = tk.Text(root, height=10, width=40)
sequence_display.grid(row=3, column=0, columnspan=8)

# Buttons to select measure slots
for i in range(4):
    measure_button = tk.Button(root, text=f"Measure {i + 1}", command=lambda i=i: select_measure(i))
    measure_button.grid(row=1, column=4 + i)

# Input for the order of measures to play
measure_order_label = tk.Label(root, text="Measure Order (e.g., 1,2,3,4):")
measure_order_label.grid(row=4, column=0, columnspan=2, sticky="w")
measure_order_entry = tk.Entry(root, width=10)
measure_order_entry.insert(0, "1,2,3,4")
measure_order_entry.grid(row=4, column=2)

# Button to play the sequence
play_button = tk.Button(root, text="Play Sequence", command=play_sequence)
play_button.grid(row=5, column=0, columnspan=4)

# Run the Tkinter main loop
root.mainloop()
