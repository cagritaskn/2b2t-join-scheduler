import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import time
import threading
import pyautogui
import configparser
import os
import pygetwindow as gw
import cv2
import numpy as np
import sys

# Global variable to control the scheduled task
stop_thread = False

# Path for configuration file
config_file = 'settings.ini'

# Load settings from config file
def load_settings():
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if 'SETTINGS' in config:
        hour = config['SETTINGS'].get('hour', '0')
        minute = config['SETTINGS'].get('minute', '0')
        minecraft_path = config['SETTINGS'].get('minecraft_path', '')
        
        hour_entry.insert(0, hour)
        minute_entry.insert(0, minute)

        # Set the minecraft_path if it's present in the config
        if minecraft_path and os.path.isfile(minecraft_path):
            global minecraft_exe_path
            minecraft_exe_path = minecraft_path

# Save settings to config file
def save_settings(hour, minute, minecraft_path=''):
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'hour': hour,
        'minute': minute,
        'minecraft_path': minecraft_path
    }
    
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Function to browse and select Minecraft.exe
def browse_minecraft_exe():
    file_path = filedialog.askopenfilename(
        title="Select Minecraft.exe",
        filetypes=[("Minecraft Executable", "Minecraft.exe")],
        defaultextension="Minecraft.exe"
    )
    
    if file_path and os.path.basename(file_path) == 'Minecraft.exe':
        global minecraft_exe_path
        minecraft_exe_path = file_path
        save_settings(hour_entry.get(), minute_entry.get(), minecraft_exe_path)
    else:
        messagebox.showerror("Error", "Please select a valid Minecraft.exe file.")

# Check if Minecraft.exe exists or needs to be selected
def check_minecraft_exe():
    global minecraft_exe_path
    if not os.path.isfile(minecraft_exe_path):
        if not messagebox.askyesno("Minecraft Not Found", "Minecraft.exe not found. Do you want to select it manually?"):
            app.quit()
        else:
            browse_minecraft_exe()

# Function to get the base path for bundled files
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as a frozen executable
        return sys._MEIPASS
    else:
        # Running as a script
        return os.path.dirname(os.path.abspath(__file__))

# Function to locate and click on a button using image recognition
def click_button(image_name):
    base_path = get_base_path()
    image_path = os.path.join(base_path, image_name)
    screen = pyautogui.screenshot()
    screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    button_img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Convert both images to grayscale
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
    button_gray = cv2.cvtColor(button_img, cv2.COLOR_BGR2GRAY)

    # Use adaptive thresholding to improve recognition
    screen_threshold = cv2.adaptiveThreshold(screen_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    button_threshold = cv2.adaptiveThreshold(button_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Match template and find all the matching locations
    result = cv2.matchTemplate(screen_threshold, button_threshold, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Only click if the best match confidence is above a certain threshold (e.g., 0.7)
    if max_val >= 0.7:
        # Calculate the center of the best matching location
        best_match = (max_loc[0] + button_img.shape[1] // 2, max_loc[1] + button_img.shape[0] // 2)
        pyautogui.click(best_match)
        return True

    return False

# Launching Minecraft
def start_minecraft():
    global stop_thread
    try:
        # Check if Minecraft is already running
        minecraft_window = None
        for window in gw.getWindowsWithTitle('Minecraft Launcher'):
            if 'Minecraft Launcher' in window.title:
                minecraft_window = window
                break
        
        if minecraft_window:
            # Bring the Minecraft window to the foreground
            minecraft_window.activate()
            minecraft_window.maximize()
        else:
            # Minecraft is not running
            if minecraft_exe_path and os.path.isfile(minecraft_exe_path):
                subprocess.Popen(minecraft_exe_path)
                time.sleep(10)  # Wait for Minecraft to launch
            else:
                messagebox.showerror("Launcher Not Found", "Minecraft.exe not found. Please configure the correct path.")
                stop_thread = True
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while launching Minecraft: {e}")
        stop_thread = True

# Automation
def join_server():
    global stop_thread
    status_label.config(text=f"Running the automation...", fg="green", bg="black")
    time.sleep(20)  # Wait for Minecraft to load

    # Click on the "Play" button
    if click_button("play_button.png"):
        print("Clicked Play button.")
    else:
        print("Play button not found.")

    time.sleep(90)

    # Click on the "Multiplayer" button
    if click_button("multiplayer_button.png"):
        print("Clicked Multiplayer button.")
    else:
        print("Multiplayer button not found.")

    time.sleep(3)

    # Click on the "Direct Connect" button
    if click_button("direct_connect_button.png"):
        print("Clicked Direct Connect button.")
    else:
        print("Direct Connect button not found.")

    time.sleep(3)
    pyautogui.hotkey('ctrl', 'a')  # Select All
    time.sleep(3)

    pyautogui.write(server_address)  # IP
    time.sleep(3)
    pyautogui.press('enter')  # Connect
    time.sleep(3)
    stop_thread = True
    status_label.config(text=f"Joined the server successfully.", fg="green", bg="black")

    while not stop_thread:
        time.sleep(1)  # Keep the thread alive

# Function to start Minecraft and join server
def scheduled_start():
    global stop_thread

    try:
        target_hour = int(hour_entry.get())
        target_minute = int(minute_entry.get())
    except ValueError:
        stop_thread = True
        messagebox.showerror("Error", "Invalid hour and minute input.")
        status_label.config(text="Inactive", fg="white", bg="black")
        toggle_button.config(text="Activate")
        return

    # Validate the hour and minute values
    if target_hour < 0 or target_hour > 23 or target_minute < 0 or target_minute > 59:
        stop_thread = True
        messagebox.showerror("Error", "Invalid hour and minute input.")
        status_label.config(text="Inactive", fg="white", bg="black")
        toggle_button.config(text="Activate")
        return

    # Format hour and minute with leading zero if necessary
    formatted_hour = f"{target_hour:02}"
    formatted_minute = f"{target_minute:02}"

    messagebox.showinfo("Info", f"Minecraft will start at {formatted_hour}:{formatted_minute}.")
    
    # Save the settings
    save_settings(formatted_hour, formatted_minute, minecraft_exe_path)

    while not stop_thread:
        current_time = time.localtime()
        if (current_time.tm_hour == target_hour and
            current_time.tm_min == target_minute):
            start_minecraft()
            join_server()
            break
        # Check every second to see if we need to stop
        time.sleep(1)
    
    # Update status label if the thread exits
    if not stop_thread:
        status_label.config(text="Inactive", fg="white", bg="black")
        toggle_button.config(text="Activate")

def update_status_with_dots(selected_hour, selected_minute):
    global stop_thread
    dots = ""
    while not stop_thread:
        formatted_hour = f"{int(selected_hour):02}"
        formatted_minute = f"{int(selected_minute):02}"
        status_label.config(text=f"Active ({formatted_hour}:{formatted_minute}){dots}", fg="green")
        dots = "." * ((len(dots) + 1) % 4)  # Cycle through 0 to 3 dots
        time.sleep(1)  # Wait for 1 second before updating

def toggle_activation():
    global stop_thread
    if toggle_button.cget("text") == "Activate":
        stop_thread = False
        selected_hour = hour_entry.get()
        selected_minute = minute_entry.get()
        toggle_button.config(text="Deactivate")

        # Start the loading animation in a new thread
        threading.Thread(target=update_status_with_dots, args=(selected_hour, selected_minute)).start()
        thread = threading.Thread(target=scheduled_start)
        thread.start()
    else:
        if messagebox.askyesno("Confirm Deactivation", "Are you sure you want to deactivate?"):
            stop_thread = True
            status_label.config(text="Deactivated", fg="red", bg="black")
            toggle_button.config(text="Activate")

# Quit function with confirmation dialog
def quit_application():
    global stop_thread
    if messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?"):
        # Stop the thread
        stop_thread = True
        os._exit(0)

# Validate only numeric input for hour and minute
def validate_numeric_input(P):
    if len(P) > 2:
        return False
    if P.isdigit() or P == "":
        return True
    return False

# Format hour and minute with leading zero if necessary
def format_entry(event):
    value = event.widget.get()
    if len(value) == 1 and value.isdigit():
        event.widget.delete(0, tk.END)
        event.widget.insert(0, f"0{value}")

# GUI setup
app = tk.Tk()
app.title("2B2T Join Scheduler")
app.geometry("300x230")  # Make the app window bigger
app.configure(background='black')
app.resizable(False, False)
app.iconbitmap(os.path.join(get_base_path(), 'icon.ico'))

# Default Minecraft path
minecraft_exe_path = "C:\\XboxGames\\Minecraft Launcher\\Content\\Minecraft.exe"
server_address = "2b2t.org"

# Validation
vcmd = (app.register(validate_numeric_input), '%P')

# Hour and minute entries
tk.Label(app, text="Hour:", fg="white", bg="black", font=("Arial", 10, "bold")).pack(pady=(10, 0))
hour_entry = tk.Entry(app, validate='key', validatecommand=vcmd, fg="white", bg="black", font=("Arial", 10, "bold"), justify='center', width=5)
hour_entry.pack(pady=(0, 10))
hour_entry.bind("<FocusOut>", format_entry)

tk.Label(app, text="Minute:", fg="white", bg="black", font=("Arial", 10, "bold")).pack(pady=(5, 0))
minute_entry = tk.Entry(app, validate='key', validatecommand=vcmd, fg="white", bg="black", font=("Arial", 10, "bold"), justify='center', width=5)
minute_entry.pack(pady=(0, 5))
minute_entry.bind("<FocusOut>", format_entry)

# Load settings when the app starts
load_settings()

# Check for Minecraft.exe when the app starts
check_minecraft_exe()

# Toggle button for activation/deactivation
toggle_button = tk.Button(app, text="Activate", command=toggle_activation, font=("Arial", 10, "bold"))
toggle_button.pack(pady=(10, 5))

# Status label
status_label = tk.Label(app, text="Inactive", fg="white", bg="black", font=("Arial", 10, "bold"))
status_label.pack(pady=(0, 5))

# Quit button
quit_button = tk.Button(app, text="Quit", command=quit_application, font=("Arial", 10, "bold"))
quit_button.pack(pady=(0, 0))

app.mainloop()
