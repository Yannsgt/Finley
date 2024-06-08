import tkinter as tk
from PIL import Image, ImageTk

# Create the Tkinter root window
root = tk.Tk()

# Load the image file
try:
    image = Image.open(r"C:\Users\thoma\Desktop\Finley.png")
    title_image = ImageTk.PhotoImage(image)
except FileNotFoundError:
    print("Image file not found")
    exit()

# Create the label with the image
title_label = tk.Label(
    master=root,
    image=title_image,
    text="Veuillez remplir ces champs pour accéder à la discussion.",
    compound=tk.LEFT,
    font=("Roboto", 24),
    bg="#204186",
    fg="#FFFFFF"
)
title_label.pack(pady=12, padx=10)

# Start the Tkinter event loop
root.mainloop()
