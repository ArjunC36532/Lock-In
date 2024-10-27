import datetime
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import openai
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
links = []

with app.app_context():
        db.create_all()

openai.api_key = os.getenv('API_KEY')
 
@app.route('/')
def index():
    return render_template('index.html')  # updated to match new layout

@app.route('/quiz-and-learn')
def quiz_and_learn():
    return render_template('quiz-and-learn.html')

@app.route('/learn', methods=['POST'])
def learn_topic():
    topic = request.json.get("topic", "")
    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    chatgpt_response = get_chatgpt_response(topic)
    return jsonify({"response": chatgpt_response})

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    topic = request.json.get("topic", "")
    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    quiz_data = generate_quiz_questions(topic)
    return jsonify({"questions": quiz_data})

def get_chatgpt_response(topic):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Teach me about {topic}."}
        ],
        max_tokens=100,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()

def generate_quiz_questions(topic):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert quiz creator."},
            {"role": "user", "content": f"Generate 5 detailed, multiple-choice quiz questions about '{topic}' with correct answers labeled A-D."}
        ],
        max_tokens=500,
        temperature=0.7,
    )

    quiz_text = response.choices[0].message['content'].strip().split("\n\n")
    questions = []

    for quiz in quiz_text:
        lines = quiz.split("\n")
        question = lines[0]
        options = lines[1:5]
        correct_answer = "A"  # Default to "A" if parsing fails; adjust parsing as needed.

        questions.append({
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        })

    return questions

@app.route('/setup', methods=['POST','GET'])
def setup():
    if request.method == 'POST':
        link = request.form['link']
        links.append(link)
        return render_template('setup.html', links=links)

    else:
        return render_template('setup.html', links=links)  # Render the setup template
    
@app.route('/delete_last_link', methods=['POST'])
def delete_last_link():
    if links:
        links.pop()  # Remove the last link
    return render_template('setup.html', links=links)

@app.route('/start', methods=['POST'])
def start():
    # Placeholder for future functionality
    return render_template('start.html', links = links)

@app.route('/timer')
def lock_In_timer():
    return render_template('timer_scrn.html')

if __name__ == "__main__":
    app.run(debug=True)
