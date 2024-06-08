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
from tkinter import Canvas, Entry, Button, Text, Frame

spell = SpellChecker(language='fr')
questions = []
answers = []
Qcount = 0
name = ""
surname = ""
mail = ""
FirstQ = ""
myroot = customtkinter.CTk()
BleuL = '#204186'
BleuM = '#263574'
BleuD = '#1A2C4E'
Blanc = '#FFFFFF'
Noir = '#000000'
Gris = '52575F'
Finley = '60C5EF'