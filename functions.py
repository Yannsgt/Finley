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
from datetime import datetime
from tkinter import ttk
from tkinter import Canvas, Entry, Button, Text, Frame

import variables
import tkinter as tk

class PlaceholderText(tk.Text):
    def __init__(self, master=None, placeholder="", placeholder_color='#FFFFFF', bg=None, fg=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.bg = bg
        self.fg = fg
        self.default_fg_color = fg if fg else self.cget('fg')

        if self.bg:
            self.config(bg=self.bg)
        if self.fg:
            self.config(fg=self.fg)

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert("1.0", self.placeholder)
        self.tag_configure("placeholder", foreground=self.placeholder_color)
        self.tag_add("placeholder", "1.0", "end")

    def on_focus_in(self, event):
        if self.get("1.0", "end-1c") == self.placeholder:
            self.delete("1.0", "end")
            self.config(foreground=fg)


    def on_focus_out(self, event):
        if not self.get("1.0", "end-1c").strip():
            self.put_placeholder()

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color='#FFFFFF', bg=None, fg=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = variables.Blanc
        self.bg = bg
        self.fg = fg
        self.default_fg_color = fg if fg else self.cget('fg')  # Use existing foreground color if not provided
        

        # Configure background color
        if self.bg:
            print("Background color: "+bg)
            self.config(bg=self.bg)
        if self.fg:
            print("Texte color: "+fg)
            self.config(fg=self.fg)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def on_focus_in(self, event):
        if self['fg'] == self.placeholder_color:
            self.delete(0, "end")
            self['fg'] = self.default_fg_color

    def on_focus_out(self, event):
        if not self.get():
            self.put_placeholder()


def make_full_screen(root1):
    screen_width = root1.winfo_screenwidth()
    screen_height = root1.winfo_screenheight()
    root1.overrideredirect(True)
    
    root1.geometry(f"{screen_width}x{screen_height}+0+0")
    root1.focus_force()

def exit_fullscreen(root2):
        print("Exiting full-screen mode")
        root2.overrideredirect(False)
        root2.geometry("500x350")
        root2.update_idletasks()  # Update the window to ensure changes take effect

def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return self.create_polygon(points, **kwargs, smooth=True)


def draw_user_bubble(canvas, x, y, width, height, text):
    x1, y1 = x, y
    x2, y2 = x + width, y + height
    radius = 10

    # Draw the main rectangle
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill='light blue')
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill='light blue')

    # Draw the rounded corners
    canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, style='pieslice', fill='light blue')
    canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, style='pieslice', fill='light blue')
    canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, style='pieslice', fill='light blue')
    canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, style='pieslice', fill='light blue')

    # Draw the text inside the user's message bubble
    canvas.create_text(x1 + 10, y1 + 10, anchor='nw', text=text, width=width - 20, fill='black')


def draw_bot_bubble(canvas, x, y, width, height, text):
    x1, y1 = x, y
    x2, y2 = x + width, y + height
    radius = 10

    # Draw the main rectangle
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill='light blue')
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill='light blue')

    # Draw the rounded corners
    canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, style='pieslice', fill='light blue')
    canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, style='pieslice', fill='light blue')
    canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, style='pieslice', fill='light blue')
    canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, style='pieslice', fill='light blue')

    # Draw the text inside the user's message bubble
    canvas.create_text(x1 + 10, y1 + 10, anchor='nw', text=text, width=width - 20, fill='black')


# Gestion Knowledge_Base
# Fonction permettant de récupérer la Base de Donnée de Finley
def load_knowledge_base(file_path: str) -> dict:
    full_path = os.path.abspath(file_path)
    with open(full_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data

knowledge_base = load_knowledge_base('knowledge_base.json')

# Fonction permettant d'ajouter une donnée dans la Base de Donnée de Finley
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)



def add_new_client(name, surname, mail, database_path):
    # Connexion à la BDD
    with open(database_path, 'r') as file:
        database = json.load(file)

    # Vérification de l'éxistence du client en BDD
    for client in database['clients']:
        if client['mail'] == mail:
            print("Client already exists in the database.")
            return

    # Création des Données du client dans la BDD
    new_client = {
        "name": name,
        "surname": surname,
        "mail": mail,
        "chatbot_data": {
            "average_questions_per_session": 0,
            "total_sessions": {
                "weekly": 0,
                "monthly": 0,
                "trimester": 0
            },
            "quit_method": "",
            "average_grade": {
                "weekly": 0,
                "monthly": 0,
                "trimester": 0
            }
        }
    }

    # Ajout des Données
    database['clients'].append(new_client)

    # Sauvegarde des Données
    with open(database_path, 'w') as file:
        json.dump(database, file, indent=2)
    print("Client ajouté à la BDD")



def does_client_exist(name, surname, mail, database_path):
    # Load the database
    with open(database_path, 'r') as file:
        database = json.load(file)

    # Check if any client matches the provided name, surname, and mail
    for client in database['clients']:
        if client['name'] == name and client['surname'] == surname and client['mail'] == mail:
            return True

    # If no client matches, return False
    return False



def update_database(name, surname, mail, questions_per_session, quit_method, grade, database_path):
    # Load the existing database
    print("Loading database from:", database_path)
    with open(database_path, 'r') as file:
        database = json.load(file)

    # Find the client in the database
    client_index = None
    for i, client in enumerate(database['clients']):
        if client['mail'] == mail:
            print("Client found in the database.")
            client_index = i
            break

    if client_index is not None:
        # Update the client's data
        client = database['clients'][client_index]

        # Update total sessions
        now = datetime.now()
        current_week = now.strftime("%V")

        client['chatbot_data']['total_sessions']['weekly'] += 1

        # Calculate new average questions per session
        total_sessions = sum(client['chatbot_data']['total_sessions'].values())
        total_questions = client['chatbot_data']['average_questions_per_session'] * total_sessions
        total_sessions += 1
        total_questions += questions_per_session
        new_average_questions_per_session = total_questions / total_sessions

        # Update average questions per session
        client['chatbot_data']['average_questions_per_session'] = new_average_questions_per_session

        # Update quit method
        client['chatbot_data']['quit_method'] = quit_method

        # Calculate new average grade
        for period in ['weekly', 'monthly']:
            total_grades = client['chatbot_data']['average_grade'][period] * (total_sessions - 1)
            total_grades += grade
            new_average_grade = total_grades / total_sessions
            client['chatbot_data']['average_grade'][period] = new_average_grade

        # Save the updated database
        with open(database_path, 'w') as file:
            json.dump(database, file, indent=2)
        print("Database updated successfully!")
    else:
        print("Client not found in the database.")


def check_spelling(text):
    misspelled = variables.spell.unknown(text.split())
    corrected_text = text
    for word in misspelled:
        suggestion = variables.spell.correction(word)
        if suggestion is not None:
            corrected_text = corrected_text.replace(word, suggestion)
    return corrected_text

# Recherche de la réponse la plus appropriée
def find_best_match(user_question: str, questions: list) -> str:
    
    matches = get_close_matches(user_question, questions, n=2, cutoff=0.6)

    if not matches:
        return None

    if len(matches) == 1 and get_close_matches(user_question, questions, n=1, cutoff=0.6)[0] == matches[0]:
        return matches[0]

    max_cutoff_match = max(matches, key=lambda match: get_close_matches(match, questions, n=1, cutoff=0.6))
    return max_cutoff_match

# Récupération de la réponse
def get_answer_for_question(question: str, knowledge_base: dict) -> str:
    for item in knowledge_base["questions"]:
        if item["question"] == question:
            return item["answer"]
    return None

def send_emailToDFL_with_questions_and_answers(name, surname, mail, msg, questions, answers):
    sender_email = "thomas.quintana@hotmail.com" #mettre le mail de DFL ou Finley
    receiver_email = "thomas.quintana@hotmail.com" # ici pour le test, a remplacer par le mail de DFL (ou Antoine)
    smtp_server = "smtp.office365.com" #Changer vers le type de mail de DFL ou Finley
    smtp_port = 587
    smtp_username = "thomas.quintana@hotmail.com" #mettre le mail de DFL ou Finley
    smtp_password = "conan74" #mettre le code du mail de DFL ou Finley

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Dernière conversation avec Finley de {surname} {name}"
    message["From"] = sender_email
    message["To"] = receiver_email

    # HTML du mail
    html_content = f"<h1><strong>Recap de Finley avec {name} {surname}</strong></h1>"
    html_content += f"<p><strong>Mail:</strong> {mail}</p>"
    html_content += f"<p><strong>Message de {name} {surname}:</strong> {msg}\n</p>"
    html_content += "<p><strong>Questions et Réponses:</strong></p>"
    for question, answer in zip(questions, answers):
        html_content += "<hr>"
        html_content += f"<p><strong> - Question:</strong> {question}</p>"
        html_content += f"<p><strong> - Réponse:</strong> {answer}</p>"
        html_content += "<hr>"

    # Ajout de l'HTML au mail
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Un email à été envoyé à DFL")


def send_email_with_questions_and_answers(name, surname, mail, questions, answers):
        print("____________________________________________________________________________________________ "+mail)
        sender_email = "thomas.quintana@hotmail.com" #mettre le mail de DFL ou Finley
        receiver_email = mail
        print(receiver_email)
        smtp_server = "smtp.office365.com" #Changer vers le type de mail de DFL ou Finley
        smtp_port = 587
        smtp_username = "thomas.quintana@hotmail.com" #mettre le mail de DFL ou Finley
        smtp_password = "conan74" #mettre le code du mail de DFL ou Finley

        message = MIMEMultipart("alternative")
        message["Subject"] = f"Votre dernière conversation avec finley"
        message["From"] = sender_email
        message["To"] = receiver_email

        # HTML du mail
        html_content = f"<h1><strong>Votre Conversation:</strong></h1>"
        html_content += "<p><strong>Questions et Réponses:</strong></p>"
        for question, answer in zip(questions, answers):
            html_content += "<hr>"
            html_content += f"<p><strong> - Question:</strong> {question}</p>"
            html_content += f"<p><strong> - Réponse:</strong> {answer}</p>"
            html_content += "<hr>"

        # Ajout de l'HTML au mail
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Un email à été envoyé au Client")


def on_enter_pressed(input_field,user_dialog,bot_dialog,contact_button,affichBubles,event=None):
    variables.Qcount += 1
    user_input = input_field.get()
    input_field.delete(0, END)
    if user_input:
        if user_input.lower() == 'quit':
            send_email_with_questions_and_answers(variables.name, variables.surname, variables.mail, message_entry.get("1.0", tk.END), variables.questions, variables.answers)
            variables.myroot.quit()
        else:
            corr_input = check_spelling(user_input)
            user_dialog.config(state='normal')
            user_dialog.insert(END, 'Vous: ' + user_input + '\n')
            user_dialog.config(state='disabled')
            draw_user_bubble(affichBubles,10,10,50,30, user_input)

            best_match = find_best_match(corr_input, [q["question"] for q in knowledge_base["questions"]])
            if best_match:
                answer = get_answer_for_question(best_match, knowledge_base)
                if answer:
                    # Message de Finley pendant sa recherche d'une réponse
                    bot_dialog.config(state='normal')
                    bot_dialog.insert(END, 'Finley: Réponse en cours . . .\n')
                    bot_dialog.config(state='disabled')

                    # Réponse de Finley
                    bot_dialog.config(state='normal')
                    bot_dialog.insert(END, 'Finley: ' + answer + '\n')
                    bot_dialog.config(state='disabled')
                    draw_bot_bubble(affichBubles,10,50,50,30,answer)

                    variables.questions.append(user_input)
                    variables.answers.append(answer)

                    # Suppression du message de la recherche de réponse
                    bot_dialog.config(state='normal')
                    bot_dialog.delete('end - 3 lines', 'end - 2 lines')
                    bot_dialog.config(state='disabled')
                else:
                    print("Error: No Answers")
                    bot_dialog.config(state='normal')
                    bot_dialog.insert(END, 'Finley: Je n’ai pas la réponse à votre question. Veuillez la reformuler ou nous contacter directement.\n')
                    bot_dialog.config(state='disabled')
                    questions.append(user_input)
                    variables.answers.append("Réponse introuvable")
                    # Afficher le bouton "Contacter"
                    contact_button.pack(side='left', padx=5, pady=5)
            else:
                print("Error: best_match Not functionning")
                bot_dialog.config(state='normal')
                bot_dialog.insert(END, 'Finley: Je n’ai pas la réponse à votre question. Veuillez la reformuler ou nous contacter directement.\n')
                bot_dialog.config(state='disabled')
                variables.questions.append(user_input)
                variables.answers.append("Réponse introuvable")
                contact_button.pack(side='left', padx=5, pady=5)
    else:
        print("User input is empty. Ignoring.")
    
        
     

# Fonction pour afficher la fenêtre de contact
def open_contact_window(root):
    contact_window = Toplevel(root)
    contact_window.configure(bg=variables.BleuD)
    contact_window.title("Contactez-nous")
    contact_window.geometry("400x300")

    contact_label = Label(contact_window, text="Remplissez le formulaire ci-dessous pour nous contacter:",bg=variables.BleuD, fg=variables.Blanc)
    contact_label.pack(pady=10)

    # Ajoutez ici les champs du formulaire de contact (nom, email, message, etc.)

    tk.Label(contact_window, text="Message:",bg=variables.BleuD,fg=variables.Blanc).pack()
    message_entry = PlaceholderText(contact_window, "Laissez un message içi", bg=variables.BleuD,fg=variables.Blanc, height=5)
    message_entry.pack()

    Tel = PlaceholderEntry(contact_window,"Telephone (facultatif)",text="Telephone",bg=variables.BleuD,fg=variables.Blanc)
    Tel.pack()
    # Send button
    send_button = Button(master = contact_window, text="Envoyer", bg=variables.BleuD,fg=variables.Blanc,command=lambda: send_emailToDFL_with_questions_and_answers(variables.name, variables.surname, variables.mail, message_entry.get("1.0", END), variables.questions, variables.answers))
    send_button.pack()


def UserPage(root,Pseudo, Qcount, name, surname, mail):
    root.withdraw()
    chat = tk.Tk()
    chat.title("ChatBot")

    make_full_screen(chat)
    chat.bind("<Escape>", lambda event: exit_fullscreen(chat))

    # afk_detector = AFKDetector()
    # afk_detector.check_afk_status()
    def on_close():
        variables.myroot.withdraw()  # Hide the main window
        note_window = Toplevel(variables.myroot)  # Create a new window for the note selection
        note_window.title("NOTE")
        def handle_button_click(note,Qcount,name,surname,mail,questions,answers):
            print("Selected note:", note)
            note_window.destroy()  # Close the note selection window
            send_email_with_questions_and_answers(variables.name, variables.surname, variables.mail, variables.questions, variables.answers)
            # Display a thanks message
            bot_dialog.config(state='normal')
            bot_dialog.insert(END, 'Finley: Merci pour votre retour!\n')
            bot_dialog.config(state='disabled')
            if note == "Bad":
                grade = 1
            elif note == "Neutral":
                grade = 2
            else: 
                grade = 3
            update_database(variables.name, variables.surname, variables.mail, variables.Qcount, "quit", grade,r"C:\xampp\htdocs\AI\AI_Test\Chatbot_DFL\Versions_Finley\log_base.json")
            chat.withdraw()
        
        bad_button = tk.Button(note_window, text="Bad", command=lambda: handle_button_click("Bad",variables.Qcount,variables.name,variables.surname,variables.mail,variables.questions,variables.answers))
        bad_button.pack(pady=5)

        neutral_button = tk.Button(note_window, text="Neutral", command=lambda: handle_button_click("Neutral",variables.Qcount,variables.name,variables.surname,variables.mail,variables.questions,variables.answers))
        neutral_button.pack(pady=5)

        good_button = tk.Button(note_window, text="Good", command=lambda: handle_button_click("Good",variables.Qcount,variables.name,variables.surname,mail,variables.questions,variables.answers))
        good_button.pack(pady=5)

    frame = tk.Frame(master=chat)
    frame.pack(pady=5)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')

    user_dialog = Text(frame, width=50, height=15, wrap='word', yscrollcommand=scrollbar.set)
    user_dialog.pack(side='right')

    bot_dialog = Text(frame, width=50, height=15, wrap='word', yscrollcommand=scrollbar.set)
    bot_dialog.pack(side='left')

    affichBubles = Canvas(frame, width=50, height=50, bg='light gray', bd=0, highlightthickness=0)
    affichBubles.pack(side='left')

    scrollbar.config(command=bot_dialog.yview)

    input_frame = Frame(chat)
    input_frame.pack(pady=5)

    input_field = Entry(input_frame, width=50)
    input_field.pack(side='left', padx=5)
    input_field.bind("<Return>", lambda event : on_enter_pressed(input_field))

    # Bouton "Contacter"
    contact_button = tk.Button(input_frame, text="Contacter", command=lambda: open_contact_window(variables.myroot))

    send_button = tk.Button(input_frame, text="Envoyer", command=lambda: on_enter_pressed(input_field,user_dialog,bot_dialog,contact_button,affichBubles))
    send_button.pack(side='right', padx=5)

    # Call check_afk_status to start checking AFK status
    # check_afk_status()

    chat.protocol("WM_DELETE_WINDOW", on_close)  # Call on_close when the window is closed

    chat.mainloop()



def validate_email(address):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    match = re.match(pattern, address)
    print("Match object:", match)  # Debug print statement
    return match

def login(root, mail, name, surname, entry3, error_label):
    variables.name = name
    variables.surname = surname
    variables.mail = mail
    variables.myroot = root
    print("Email entered:", mail)  # Debug print statement
    if validate_email(mail) and name!=None and surname!=None:
        error_label.config(text="")
        if does_client_exist(name, surname, mail, r"C:\xampp\htdocs\AI\AI_Test\Chatbot_DFL\Versions_Finley\log_base.json"):
            pass
        else:
            add_new_client(name, surname, mail, r"C:\xampp\htdocs\AI\AI_Test\Chatbot_DFL\Versions_Finley\log_base.json")
        UserPage(variables.myroot, surname, variables.Qcount, name, surname, mail)
    else:
        # Clear the email entry field
        entry3.delete(0, 'end')
        # Display error message below the email entry field
        error_label.config(text="Email invalide. Veuillez entrer un email valide.")




