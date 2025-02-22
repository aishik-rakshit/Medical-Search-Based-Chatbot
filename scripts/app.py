from flask import Flask, request, jsonify, render_template
from chatbot import generate_response
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

conversation_history = []
context_message = ("As a medical chatbot, I am here to provide accurate and reliable information "
                   "exclusively about medical needs. It is very important to check the previous search context "
                   "to determine if new information is required. If more information is needed, the chatbot should "
                   "respond with: 'I need more information.'")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get('query')
    
    response = generate_response(user_query, conversation_history, context_message)
    conversation_history.append({"role": "user", "content": user_query})
    conversation_history.append({"role": "assistant", "content": response})

    return jsonify({"response": response})

if __name__ == '__main__':
    logging.info("Starting Flask web app...")
    app.run(debug=True)
