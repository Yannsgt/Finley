
import mysql.connector
import hashlib
from cryptography.fernet import Fernet
from CTkListbox import *
import subprocess
import json
import os
from difflib import get_close_matches

import unicodedata
from spellchecker import SpellChecker
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import re


spell = SpellChecker(language='fr')
questions = []
answers = []
Qcount = 0
name = ""
surname = ""
mail = ""
FirstQ = ""

BleuL = '#204186'
BleuM = '#263574'
BleuD = '#1A2C4E'
Blanc = '#FFFFFF'
Noir = '#000000'
Gris = '52575F'
Finley = '60C5EF'