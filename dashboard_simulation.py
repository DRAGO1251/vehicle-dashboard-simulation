import tkinter as tk
from tkinter import ttk
import random
import pygame
import os

pygame.mixer.init()

def play_sound(filename, loop=False):
    try:
        path = os.path.join("sounds", filename)
        sound = pygame.mixer.Sound(path)
        if loop:
            sound.play(-1)
        else:
            sound.play()
    except Exception as e:
        print(f"Sound error: {e}")

class VehicleDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Dashboard Simulation")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.speed = tk.IntVar()
        self.fuel = 100
        self.temperature = 30
        self.coolant_temp = 30
        self.odometer = 0
        self.engine_on = False
        self.left_blink = False
        self.right_blink = False
        self.left_on = False
        self.right_on = False
        self.hazard_on = False
        self.headlights_on = False
        self.highbeam_on = False
        self.gear = tk.StringVar(value="P")

        self.setup_ui()
        self.update_dashboard()
        self.blink_signals()

    def setup_ui(self):
        tk.Label(self.root, text="VEHICLE DASHBOARD", font=("Helvetica", 20, "bold"), fg="white", bg="black").pack(pady=10)

        # Speed and Gear
        frame = tk.Frame(self.root, bg="black")
        frame.pack()
        tk.Label(frame, text="Speed", fg="white", bg="black").pack()
        ttk.Scale(frame, from_=0, to=180, orient="horizontal", variable=self.speed).pack()

        gear_frame = tk.Frame(self.root, bg="black")
        gear_frame.pack(pady=5)
        tk.Label(gear_frame, text="Gear", fg="white", bg="black").pack(side="left")
        ttk.Combobox(gear_frame, textvariable=self.gear, values=["P", "R", "N", "D", "1", "2", "3"]).pack(side="left")

        # Controls
        ctrl = tk.Frame(self.root, bg="black")
        ctrl.pack(pady=10)

        ttk.Button(ctrl, text="Start Engine", command=self.toggle_engine).grid(row=0, column=0, padx=5)
        ttk.Button(ctrl, text="Left Signal", command=self.toggle_left_signal).grid(row=0, column=1, padx=5)
        ttk.Button(ctrl, text="Right Signal", command=self.toggle_right_signal).grid(row=0, column=2, padx=5)
        ttk.Button(ctrl, text="Refuel", command=self.refuel).grid(row=0, column=3, padx=5)
        ttk.Button(ctrl, text="Toggle Headlights", command=self.toggle_headlights).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(ctrl, text="Toggle High Beams", command=self.toggle_highbeams).grid(row=1, column=1, padx=5)
        ttk.Button(ctrl, text="Toggle Hazards", command=self.toggle_hazards).grid(row=1, column=2, padx=5)

        # Signal indicators
        self.left_signal = tk.Label(self.root, text="←", font=("Helvetica", 18), fg="grey", bg="black")
        self.left_signal.place(x=30, y=20)
        self.right_signal = tk.Label(self.root, text="→", font=("Helvetica", 18), fg="grey", bg="black")
        self.right_signal.place(x=740, y=20)

        # Display
        self.info = {}
        self.display_frame = tk.Frame(self.root, bg="black")
        self.display_frame.pack(pady=10)

        self.add_display("Speed", "0 km/h")
        self.add_display("Fuel", "100%")
        self.add_display("Engine Temp", "30°C")
        self.add_display("Coolant Temp", "30°C")
        self.add_display("Odometer", "0.0 km")
        self.add_display("Status", "OFF")

        self.warning = tk.Label(self.root, text="", fg="red", bg="black", font=("Helvetica", 12, "bold"))
        self.warning.pack()

        self.diagnostics = tk.Label(self.root, text="", fg="lightgreen", bg="black", font=("Courier", 10), justify="left")
        self.diagnostics.pack()

    def add_display(self, key, value):
        frame = tk.Frame(self.display_frame, bg="black")
        frame.pack()
        label = tk.Label(frame, text=f"{key}: ", font=("Helvetica", 12), fg="white", bg="black")
        label.pack(side="left")
        val_label = tk.Label(frame, text=value, font=("Helvetica", 12, "bold"), fg="cyan", bg="black")
        val_label.pack(side="left")
        self.info[key] = val_label

    def toggle_engine(self):
        self.engine_on = not self.engine_on
        self.info["Status"].config(text="ON" if self.engine_on else "OFF", fg="green" if self.engine_on else "grey")
        play_sound("engine_start.wav")
        if not self.engine_on:
            self.speed.set(0)

    def toggle_left_signal(self):
        self.left_blink = not self.left_blink
        play_sound("blinker.wav", loop=self.left_blink or self.hazard_on)
        if not self.left_blink and not self.hazard_on:
            pygame.mixer.stop()

    def toggle_right_signal(self):
        self.right_blink = not self.right_blink
        play_sound("blinker.wav", loop=self.right_blink or self.hazard_on)
        if not self.right_blink and not self.hazard_on:
            pygame.mixer.stop()

    def toggle_hazards(self):
        self.hazard_on = not self.hazard_on
        self.left_blink = self.right_blink = self.hazard_on
        play_sound("blinker.wav", loop=self.hazard_on)
        if not self.hazard_on:
            pygame.mixer.stop()

    def toggle_headlights(self):
        self.headlights_on = not self.headlights_on
        play_sound("headlight_toggle.wav")

    def toggle_highbeams(self):
        self.highbeam_on = not self.highbeam_on
        play_sound("headlight_toggle.wav")

    def refuel(self):
        self.fuel = 100
        play_sound("refuel.wav")

    def update_dashboard(self):
        spd = self.speed.get()
        self.info["Speed"].config(text=f"{int(spd)} km/h")

        if self.engine_on:
            self.odometer += spd / 100
            self.fuel -= spd / 1000
            self.temperature += 0.1 * (spd / 10)
            self.coolant_temp += 0.08 * (spd / 10)
        else:
            self.temperature -= 0.2
            self.coolant_temp -= 0.1

        self.temperature = min(max(self.temperature, 30), 120)
        self.coolant_temp = min(max(self.coolant_temp, 30), 110)
        self.fuel = max(self.fuel, 0)

        self.info["Fuel"].config(text=f"{int(self.fuel)}%", fg="green" if self.fuel > 30 else "orange")
        self.info["Engine Temp"].config(text=f"{int(self.temperature)}°C", fg="red" if self.temperature >= 110 else "blue")
        self.info["Coolant Temp"].config(text=f"{int(self.coolant_temp)}°C", fg="red" if self.coolant_temp >= 100 else "blue")
        self.info["Odometer"].config(text=f"{self.odometer:.1f} km")

        if self.temperature >= 110:
            self.warning.config(text="⚠️ ENGINE OVERHEATING!")
            play_sound("overheat_alarm.wav")
        elif self.fuel <= 10:
            self.warning.config(text="⛽ LOW FUEL WARNING!")
        else:
            self.warning.config(text="")

        diag = "[DIAGNOSTICS]\\n✔️ Engine: OK\\n"
        diag += "⚠️ Battery: Low Voltage\\n" if random.random() < 0.1 else "✔️ Battery: OK\\n"
        diag += "✔️ Brakes: OK\\n"
        self.diagnostics.config(text=diag)

        self.root.after(500, self.update_dashboard)

    def blink_signals(self):
        if self.left_blink:
            self.left_on = not self.left_on
            self.left_signal.config(fg="yellow" if self.left_on else "black")
        else:
            self.left_signal.config(fg="grey")

        if self.right_blink:
            self.right_on = not self.right_on
            self.right_signal.config(fg="yellow" if self.right_on else "black")
        else:
            self.right_signal.config(fg="grey")

        self.root.after(500, self.blink_signals)

if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleDashboard(root)
    root.mainloop()

