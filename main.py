import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import os

# Function to open a script based on the selected option
def open_script(option):
    script_folder = "scripts"
    scripts = {
        "Simple Motion": os.path.join(script_folder, "1.py"),
        "Simple Pendulum": os.path.join(script_folder, "2.py"),
        "Gravity": os.path.join(script_folder, "3.py"),
        "Projectile Motion": os.path.join(script_folder, "4.py")
        # Add more options as needed
    }
    if option in scripts:
        script_path = scripts[option]
        try:
            subprocess.Popen(["python", script_path])  # Open script in a new process
            messagebox.showinfo("Script Launched", f"The script '{option}' has been launched successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"The script '{option}' could not be found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while launching '{option}': {str(e)}")

# Create the main application window
root = tk.Tk()
root.title("Physics Visualization")

# Create a frame for better organization with scrollbar
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky="nsew")

# Create a label
label = ttk.Label(frame, text="Select an option for Visualization:", font=("Helvetica", 14))
label.grid(row=0, column=0, columnspan=3, pady=10)

# Create a scrollable list of options
options = ["Simple Motion", "Simple Pendulum", "Gravity", "Projectile Motion"]  # Example options, modify as needed
scrollbar = ttk.Scrollbar(frame, orient="vertical")
option_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=40, height=3, font=("Helvetica", 12))

for option in options:
    option_listbox.insert(tk.END, option)

option_listbox.grid(row=1, column=0, padx=10, pady=5, columnspan=3, sticky="nsew")
scrollbar.grid(row=1, column=3, sticky="ns")
scrollbar.config(command=option_listbox.yview)

# Add icons to buttons using PIL
icon_folder = "icons"
icons = {
    "Simple Motion": os.path.join(icon_folder, "icon1.png"),
    "Simple Pendulum": os.path.join(icon_folder, "icon2.png"),
    "Gravity": os.path.join(icon_folder, "icon3.png"),
    "Projectile Motion": os.path.join(icon_folder, "icon4.png")
    # Add more icons as needed
}

buttons = []
for idx, option in enumerate(options):
    icon_path = icons.get(option, None)
    button_text = option
    if icon_path:
        try:
            pil_image = Image.open(icon_path)
            tk_image = ImageTk.PhotoImage(pil_image)
            button = ttk.Button(frame, text=button_text, image=tk_image, compound="left", command=lambda opt=option: on_button_click(opt))
            button.image = tk_image  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error loading image '{icon_path}': {str(e)}")
            button = ttk.Button(frame, text=button_text, command=lambda opt=option: on_button_click(opt))
    else:
        button = ttk.Button(frame, text=button_text, command=lambda opt=option: on_button_click(opt))
    
    button.grid(row=2 + idx, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    buttons.append(button)

# Function to handle button clicks
def on_button_click(option):
    open_script(option)

# Center the window on the screen
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
root.geometry(f"+{position_right}+{position_down}")

# Run the main loop
root.mainloop()
