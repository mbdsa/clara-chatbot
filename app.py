from flask import Flask, render_template, request, jsonify
import json
import os
from dotenv import load_dotenv
import openai

from difflib import get_close_matches

app = Flask(__name__)

# Charger les variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Charger la FAQ
try:
    with open('faq.json', 'r', encoding='utf-8') as f:
        faq_data = json.load(f)
except Exception as e:
    print(f"Erreur lors du chargement de la FAQ : {e}")
    faq_data = []

# Recherche améliorée dans la FAQ
def find_answer(user_input):
    user_input = user_input.lower()
    questions = [item['question'].lower() for item in faq_data]
    match = get_close_matches(user_input, questions, n=1, cutoff=0.6)

    if match:
        for item in faq_data:
            if item['question'].lower() == match[0]:
                return item['answer']
    return None

# Fallback : Utiliser OpenAI si la FAQ n'a pas de réponse
def ask_openai(question):
    try:
        response = openai.ChatCompletion.create(

            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es Clara, coach en nutrition. Réponds de façon professionnelle et utile, "
                        "sans dire bonjour ni répéter ta présentation. "
                        "Va directement à l’essentiel en lien avec la question posée."
                    )
                },
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erreur API OpenAI : {e}")
        return "Je ne suis pas certaine de la réponse. Vous pouvez me contacter par e-mail ou via le formulaire si besoin."


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get("message", "")

    response = find_answer(user_input)

    if not response:
        response = ask_openai(user_input)

    return jsonify({ "answer": response })

if __name__ == '__main__':
    app.run(debug=True)
