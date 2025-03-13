import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import winsound


class PomodoroTimer:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x400")
        self.root.config(bg="#f0f0f0")
        
        # Timer variables
        self.fiftyMin = tk.IntVar(value=0)
        self.work_time = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 15 * 60

        self.current_time = self.work_time
        self.timer_running = False
        self.timer_paused = False
        self.pomodoro_count = 0

        self.setup_gui()

    def setup_gui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=20)

        # Timer label
        self.timer_label = ttk.Label(
            self.main_frame,
            font=("Helvetica", 48)
        )
        self.timer_label.pack(pady=20)
        self.timer_label.config(text="25:00")
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="Work Time",
            font=("Helvetica", 14)
        )
        self.status_label.pack(pady=10)

        self.minuteCheckbox = tk.Checkbutton(self.main_frame, text="50+10",font=("Helvetica", 12),
            variable=self.fiftyMin, onvalue=1, offvalue=0, command=self.update_times)
        self.minuteCheckbox.pack(pady=10, padx=10)

        # Buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=20)

        # Start button
        self.start_button = ttk.Button(
            self.button_frame,
            text="Start",
            command=self.start_timer
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Pause button
        self.pause_button = ttk.Button(
            self.button_frame,
            text="Pause",
            command=self.pause_timer
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        self.reset_button = ttk.Button(
            self.button_frame,
            text="Reset",
            command=self.reset_timer
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Counter label
        self.counter_label = ttk.Label(
            self.main_frame,
            text="Pomodoros: 0",
            font=("Helvetica", 12)
        )
        self.counter_label.pack(pady=10)

    def update_times(self):
        if self.fiftyMin.get() == 1:
            self.work_time = 50 * 60
            self.short_break = 10 * 60
            self.long_break = 30 * 60
            self.timer_label.config(text="50:00")
        else:
            self.work_time = 25 * 60
            self.short_break = 5 * 60
            self.long_break = 15 * 60
            self.timer_label.config(text="25:00")
        self.reset_timer()

    def update_timer(self):
        if self.timer_running and not self.timer_paused:
            if self.current_time > 0:
                minutes = self.current_time // 60
                seconds = self.current_time % 60
                self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.current_time -= 1
                self.root.after(1000, self.update_timer)
                self.root.title(f"{minutes:02d}:{seconds:02d}")
            else:
                self.timer_complete()


    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
        elif self.timer_paused:
            self.timer_paused = False
            self.update_timer()

    def pause_timer(self):
        self.timer_paused = True
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.root.title(f"Paused - {minutes:02d}:{seconds:02d}")

    def reset_timer(self):
        self.timer_running = False
        self.timer_paused = False
        self.current_time = self.work_time
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        self.status_label.config(text="Work Time")
        self.root.title(f"Pomodoro Timer")


    def timer_complete(self):
        winsound.Beep(1000, 1000)  # Beep sound when timer completes
        if self.status_label["text"] == "Work Time":
            self.pomodoro_count += 1
            self.counter_label.config(text=f"Pomodoros: {self.pomodoro_count}")
            
            if self.pomodoro_count % 4 == 0:
                self.current_time = self.long_break
                self.status_label.config(text="Long Break")
                self.root.title("Long Break")
            else:
                self.current_time = self.short_break
                self.status_label.config(text="Short Break")
                self.root.title("Short Break")
        else:
            self.current_time = self.work_time
            self.status_label.config(text="Work Time")
        
        self.timer_running = False
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        self.root.title(f"Pomodoro Timer")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
