import tkinter as tk
from threading import Thread, Event
import pyautogui
import time
import random

class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Mover")
        self.root.configure(bg="#2e2e2e")
        
        # Status display screen
        self.status_frame = tk.Frame(root, bg="green", width=200, height=50)
        self.status_frame.pack(pady=20, padx=20, fill=tk.BOTH)
        self.status_label = tk.Label(self.status_frame, 
                                   text="STATUS: STOPPED", 
                                   font=("Arial", 12, "bold"), 
                                   bg="green", 
                                   fg="white")
        self.status_label.pack(expand=True)
        
        # Control buttons
        self.button_frame = tk.Frame(root, bg="#2e2e2e")
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, 
                                    text="Start", 
                                    command=self.start_mouse_movement, 
                                    width=15,
                                    bg="#4CAF50",
                                    fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(self.button_frame, 
                                   text="Stop", 
                                   command=self.stop_mouse_movement, 
                                   width=15,
                                   bg="#f44336",
                                   fg="white",
                                   state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=5)

        # Thread control
        self.stop_event = Event()
        self.thread = None

        # Hotkey bindings
        self.root.bind("<F9>", lambda event: self.start_mouse_movement())
        self.root.bind("<F10>", lambda event: self.stop_mouse_movement())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_status(self, running):
        """Update the status display and buttons"""
        color = "green" if running else "red"
        text = "STATUS: RUNNING" if running else "STATUS: STOPPED"
        self.status_label.config(text=text, bg=color)
        self.status_frame.config(bg=color)
        
        self.start_button.config(state=tk.NORMAL if not running else tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL if running else tk.DISABLED)

    def random_movement(self):
        """Generate random smooth mouse movements"""
        screen_w, screen_h = pyautogui.size()
        while not self.stop_event.is_set():
            end_x = random.randint(0, screen_w)
            end_y = random.randint(0, screen_h)
            
            duration = random.uniform(0.5, 2.0)
            steps = int(duration * 10)
            
            for _ in range(steps):
                if self.stop_event.is_set():
                    return
                pyautogui.moveRel(
                    (end_x - pyautogui.position().x)/steps,
                    (end_y - pyautogui.position().y)/steps,
                    duration=duration/steps
                )
            
            pause_time = random.uniform(5, 15)
            start_time = time.time()
            while (time.time() - start_time) < pause_time:
                if self.stop_event.is_set():
                    return
                time.sleep(0.1)

    def start_mouse_movement(self):
        """Start the movement thread"""
        if self.thread and self.thread.is_alive():
            return
        
        self.stop_event.clear()
        self.thread = Thread(target=self.random_movement, daemon=True)
        self.thread.start()
        self.update_status(True)

    def stop_mouse_movement(self):
        """Signal the thread to stop"""
        self.stop_event.set()
        self.update_status(False)

    def on_close(self):
        """Handle window closing"""
        self.stop_mouse_movement()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()