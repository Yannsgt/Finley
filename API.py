#Imports
from flask import Flask, render_template, request, redirect, url_for, session,send_file,jsonify
import functions,variables

# Initialisation de l'API
app = Flask(__name__)
app.secret_key = 'TEST'

#Suite des imports

# import mysql.connector
# import hashlib
# from cryptography.fernet import Fernet
# from CTkListbox import *
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

from datetime import datetime




#Variables:___________________________________ START

global mailUP
global nameUP
global surnameUP
global demandeUP
global questionsUP
global reponsesUP
global Qcount

mailUP = ""
nameUP = ""
surnameUP = ""
demandeUP = ""
questionsUP = []
reponsesUP = []
Qcount = 0

#Variables___________________________________ END





# Gestion Knowledge_Base____________________________________________________________________________________________________________ START
#Récupération de la BDD de Finley
def load_knowledge_base(file_path: str) -> dict:
    full_path = os.path.abspath(file_path)
    with open(full_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data

# Initialisation de la BDD de Finley dans une variable
knowledge_base = load_knowledge_base('knowledge_base.json')

# Sauvegarde d'une donnée dans la BDD de Finley
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)



#BDD Clients:
#Ajout:
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

#Vérification:
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



#BDD Log:
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

# Gestion Knowledge_Base____________________________________________________________________________________________________________ END







#Gestion des BDD pour les questions et réponses problématiques______________________________________________________________________ START

def add_question_to_database(database_path, new_question_text):
    try:
        # Load existing JSON data from the database file
        with open(database_path, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize with an empty dictionary
        json_data = {}

    # Create or update the "Questions" array with the new question
    if "Questions" in json_data:
        json_data["Questions"].append({"text": new_question_text})
    else:
        json_data["Questions"] = [{"text": new_question_text}]

    # Write the updated JSON data back to the database file
    with open(database_path, 'w') as file:
        json.dump(json_data, file, indent=2)

def add_answer_to_database(question, answer, file_path):
    # Read the existing data from the JSON file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create a new structure
        data = {"qa_pairs": []}
    except json.JSONDecodeError:
        # If the file is empty or corrupted, create a new structure
        data = {"qa_pairs": []}

    # Check if the question-answer pair already exists in the list
    for existing_pair in data['qa_pairs']:
        if existing_pair['question'] == question and existing_pair['answer'] == answer:
            return f'Question-Answer pair already exists: {question} - {answer}'

    # Add the new question-answer pair to the list
    data['qa_pairs'].append({"question": question, "answer": answer})
    
    # Write the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    return f'Question-Answer pair added: {question} - {answer}'


#Gestion des BDD pour les questions et réponses problématiques______________________________________________________________________ END








#Vérification DATA _________________________________________________________________________________________________________________ START

# Fonctions pour vérifier l'orthographe
def check_spelling(text):
    misspelled = variables.spell.unknown(text.split())
    corrected_text = text
    for word in misspelled:
        suggestion = variables.spell.correction(word)
        if suggestion is not None:
            corrected_text = corrected_text.replace(word, suggestion)
    return corrected_text

#Vérification DATA _________________________________________________________________________________________________________________ END








# Gestion des Réponses:______________________________________________________________________________________________________________ START

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

# Gestion des Réponses:______________________________________________________________________________________________________________ END









# Gestion des Emails:________________________________________________________________________________________________________________ START

def send_emailToDFL_with_questions_and_answers(name, surname, mail, msg, questions, answers, phone):
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
    html_content = f"<h1><strong>Recapitulatif de Finley avec {name} {surname}</strong></h1>"
    html_content += f"<p><strong>Email:</strong> {mail}</p>"
    html_content += f"<p><strong>Téléphone:</strong> {phone}</p>"
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
    sender_email = "thomas.quintana@hotmail.com"  # Update with sender's email
    receiver_email = mail  # Update with user's email retrieved from the form
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "thomas.quintana@hotmail.com"
    smtp_password = "conan74"

    if receiver_email and questions and answers:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Récapitulatif de votre conversation avec Finley"
        message["From"] = sender_email
        message["To"] = receiver_email

        # HTML content of the email
        # html_content = "<img id="Finley" src="{{ url_for('static', filename='img/Finley.png') }}" alt="Finley Image">"
        html_content = f"<h1>Cher(e) {surname} {name}</h1>"
        html_content += "<h2>Votre conversation avec Finley:</h2>"
        html_content += "<p><strong>Vos questions et leurs réponses:</strong></p>"
        for question, answer in zip(questions, answers):
            html_content += "<hr>"
            html_content += f"<p><strong> - Question:</strong> {question}</p>"
            html_content += f"<p><strong> - Réponse:</strong> {answer}</p>"
            html_content += "<hr>"
        html_content+= "<p>Pour toute question supplémentaire n'hésitez pas à nous contacter via: support@dynamic-finances.com</p>"
        html_content += "<p>Cordialement</p>"
        html_content += "<p>L'équipe DFL<p>"

        # Attach HTML content to the email
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("An email has been sent to the client")
    else:
        print("Error: Invalid email address")

# Gestion des Emails:________________________________________________________________________________________________________________ END


# Vérification Connexion: ___________________________________________________________________________________________________________ START

def validate_email(address):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    match = re.match(pattern, address)
    print("Match object:", match)  # Debug print statement
    return match

def login(mail, name, surname):
    print("Email entered:", mail)  # Debug print statement
    if validate_email(mail):
        if does_client_exist(name, surname, mail, "log_base.json"):
            pass
        else:
            add_new_client(name, surname, mail, r"log_base.json")
        return render_template('Chat.html')
    else:
        print("login_error: login failed")
        return redirect(url_for('launch_Finley'))

# Vérification Connexion: ___________________________________________________________________________________________________________ END








#ROUTES:_____________________________________________ START

#TEST.html:
@app.route('/',methods=['POST','GET'])
def test():
    return render_template('TEST.html')
@app.route('/launch_Finley',methods=['POST','GET'])
def launch():
    return render_template('Login.html')

@app.route('/Conn_Finley',methods=['POST','GET'])
def connect_to_chat():
    global nameUP
    global mailUP
    global demandeUP
    session['mail'] = request.form.get('email')
    session['name'] = request.form.get('prénom')
    session['surname'] = request.form.get('nom')
    session['demande'] = request.form.get('demande')
    mailUP = session.get('mail')
    print("Connexion mail: "+session.get('mail')+"\n")
    nameUP = session.get('name')
    print("Connexion name: "+session.get('name')+"\n")
    surnameUP = session.get('surname')
    print("Connexion surname: "+session.get('surname')+"\n")
    demandeUP = session.get('demande')
    print("Connexion demande: "+demandeUP+"\n")
    return login(session.get('mail'),session.get('name'),session.get('surname'))

#----------------------

#Chat.html:
@app.route('/Finley',methods=['POST'])
def Finley():
    user_question = request.json.get('user_question')
    global Qcount
    Qcount+=1
    corrected_input = check_spelling(user_question)
    best_match = find_best_match(corrected_input, [q["question"] for q in knowledge_base["questions"]])
    if best_match:
        bot_response = get_answer_for_question(best_match, knowledge_base)
        print("questionsUP:", len(questionsUP), "\n")
        questionsUP.append(user_question)
        print("questionsUP:", len(questionsUP), "\n")
        print("questionsUP:", len(reponsesUP), "\n")
        reponsesUP.append(bot_response)
        print("questionsUP:", len(reponsesUP), "\n")
    else:
        bot_response = "Je n’ai pas la réponse à votre question. Veuillez la reformuler ou nous contacter directement."
        add_question_to_database(r"questions_base.json",user_question)
        print("questionsUP:", len(questionsUP), "\n")
        questionsUP.append(user_question)
        print("questionsUP:", len(questionsUP), "\n")
        print("questionsUP:", len(reponsesUP), "\n")
        reponsesUP.append(bot_response)
        print("questionsUP:", len(reponsesUP), "\n")
    return jsonify({'bot_response': bot_response})

@app.route('/Contact',methods=['POST','GET'])
def contact():
    return render_template('Contact.html')

@app.route('/getDemandeUP', methods=['GET'])
def get_demandeUP():
    global demandeUP
    return jsonify({"demandeUP": demandeUP})

#----------------------

#Contact.html:
@app.route('/EnvoieADFL',methods=['POST','GET'])
def sendMail():
    msg = request.form.get('message')
    phone = request.form.get('phone')
    send_emailToDFL_with_questions_and_answers(session.get('name'), session.get('surname'), session.get('mail'), msg, questionsUP, reponsesUP, phone)
    return render_template('Satisfaction.html')

#----------------------

#Satisfaction.html:
@app.route('/QuitNoted',methods=['POST'])
def quitNoted():
    global Qcount
    global questionsUP
    global reponsesUP
    questions = variables.questions
    answers = variables.answers
    grade = request.form.get('ratingValue')
    print(f"Received rating: {grade}")
    update_database(session.get('name'), session.get('surname'), session.get('mail'), Qcount, "quit", int(grade),r"log_base.json")
    send_email_with_questions_and_answers(session.get('name'), session.get('surname'), session.get('mail'), questionsUP, reponsesUP)
    Qcount = 0
    questionsUP = []
    reponsesUP = []
    return redirect('/launch_Finley')

@app.route('/NoteBad',methods=['POST'])
def Bad():
    note = request.json.get('rep')
    print("note= ",note,"\n")
    add_answer_to_database(note,r"answer_base.json")
    return 'Bad note received: ' + note

@app.route('/NoteGood',methods=['POST'])
def Good():
    note = request.json.get('note')
    return 'Good note received: '+note

#----------------------

#General:
# @app.route('/image')
# def get_image():
#     # Replace 'image.jpg' with the path to your image file
#     return send_file('\img\Finley.png', mimetype='image/png')

@app.route('/Quit',methods=['POST','GET'])
def quit():
    return render_template('Satisfaction.html')

@app.route('/QuitNoContact',methods=['POST','GET'])
def QuitNoContact():
    return render_template('quit.html')
#ROUTES:_____________________________________________ END


#####Lancement de l'API#####
if __name__ == '__main__':
    app.run()
