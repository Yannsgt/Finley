import customtkinter
import mysql.connector
import hashlib
from cryptography.fernet import Fernet
from CTkListbox import *
import subprocess
import json
import os
from difflib import get_close_matches
import tkinter as tk 
from tkinter import Tk, Frame, Scrollbar, Text, Entry, Button, END, Toplevel, Label
import unicodedata
from spellchecker import SpellChecker
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import re
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import Canvas, Entry, Button, Text, Frame

import functions
import variables

# image = Image.open(r"C:\Users\thoma\Desktop\Finley.png")
# title_image = ImageTk.PhotoImage(image)

root = tk.Tk()
root.configure(bg="#1A2C4E")  # Set background color of root window
#root.title("")
title_label = tk.Label(
    master=root,
    # image=title_image,
    text="Veuillez remplir ces champs pour accéder à la discussion.",
    compound=tk.LEFT,
    font=("Roboto", 24),
    bg="#1A2C4E",
    fg="#FFFFFF"
)
title_label.pack(pady=12, padx=10)

functions.make_full_screen(root)
root.bind("<Escape>", lambda event: functions.exit_fullscreen(root))

frame = tk.Frame(master=root,bg=variables.Blanc)
frame.pack(fill = "both", expand=True)

# label = tk.Label(master=frame, font=("Roboto",24))
# label.pack(pady=12, padx=10)

entry1 = functions.PlaceholderEntry(frame,"Prénom",bg=variables.BleuD, fg=variables.Blanc)
entry1.pack(padx=12,pady=10,anchor='center')

entry2 = functions.PlaceholderEntry(frame,"Nom",bg=variables.BleuD, fg=variables.Blanc)
entry2.pack(padx=12,pady=10,anchor='center')

entry3 = functions.PlaceholderEntry(frame,"Email",bg=variables.BleuD, fg=variables.Blanc)
entry3.pack(padx=12,pady=10,anchor='center')

demande = functions.PlaceholderText(frame, placeholder="Votre Demande", bg=variables.BleuD, fg='#FFFFFF', wrap='word', yscrollcommand=Scrollbar.set)
demande.pack(padx=12,pady=10,anchor='center')

error_label = tk.Label(frame, textvariable="", fg="red")

button = tk.Button(master=demande, text="Acceder", command=lambda: functions.login(root,entry3.get(), entry1.get(), entry2.get(),entry3,error_label))
button.place(relx=1.0, rely=1.0, anchor='se')

error_label.pack(anchor='center')

root.mainloop()