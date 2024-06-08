from flask import Flask, render_template, request, jsonify

import spacy

app = Flask(__name__)

# Load the English language model
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    # Get the text from the request
    text = request.form['text']
    
    # Process the text with SpaCy
    doc = nlp(text)
    
    # Extract entities from the text
    entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
    
    # Return the entities as JSON
    return jsonify(entities)

if __name__ == '__main__':
    app.run(debug=True)
