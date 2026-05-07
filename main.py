from flask import Flask, render_template, request, jsonify
import preprocessing
from recommendation import get_recommendations
from chatbot import chatbot
from spell_checker import spell_checker

app = Flask(__name__)

preprocessing.preprocessing()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Recommendation route
@app.route('/query/<query>', methods=['GET'])
def about(query):
    query = spell_checker(query)
    recommendations = get_recommendations(query=query)
    return recommendations

# chatbot route
@app.route('/chatbot', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    reply = chatbot(messages)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)