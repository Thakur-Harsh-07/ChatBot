from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Directly assign the API key
GEMINI_API_KEY = "AIzaSyCNRwnYlh2wujfZ1Nmy-1LV8hQWn4Fah_Y"
genai.configure(api_key=GEMINI_API_KEY)

# Mental health solutions for common topics
mental_health_solutions = {
    "anxiety": {
        "response": "It sounds like you're feeling anxious. One technique that might help is the 4-7-8 breathing exercise: breathe in for 4 seconds, hold for 7 seconds, and breathe out for 8 seconds. Let's try it together.",
        "coping_strategy": "Breathe in deeply... hold... now breathe out slowly. Repeat this a few times to calm your mind."
    },
    "stress": {
        "response": "Stress can be overwhelming. Consider taking a short break or going for a walk to clear your mind. Practicing mindfulness can help you stay in the present moment.",
        "coping_strategy": "Try closing your eyes for a moment. Focus on your breathing, noticing each inhale and exhale. When you're ready, slowly open your eyes."
    },
    "depression": {
        "response": "I'm really sorry you're feeling this way. Please remember you're not alone. Talking to someone you trust can help. If you ever feel too overwhelmed, reaching out to a therapist could be a great step.",
        "coping_strategy": "I suggest writing down your thoughts and feelings. Sometimes, journaling can help organize the chaos in your mind. You're valued and important."
    },
    "stressed": {
        "response": "Stress can be overwhelming. Consider taking a short break or going for a walk to clear your mind. Practicing mindfulness can help you stay in the present moment.",
        "coping_strategy": "Try closing your eyes for a moment. Focus on your breathing, noticing each inhale and exhale. When you're ready, slowly open your eyes."
    },
    "depressed": {
        "response": "I'm really sorry you're feeling this way. Please remember you're not alone. Talking to someone you trust can help. If you ever feel too overwhelmed, reaching out to a therapist could be a great step.",
        "coping_strategy": "I suggest writing down your thoughts and feelings. Sometimes, journaling can help organize the chaos in your mind. You're valued and important."
    }
}

# Function to simulate word-by-word response
def word_by_word_response(text):
    response = ""
    for word in text.split():
        response += word + " "
        time.sleep(0.3)  # Simulate typing delay
        yield response.strip()

# Function to detect mental health issues and provide solutions
def detect_mental_health(user_message):
    for keyword, solution in mental_health_solutions.items():
        if keyword in user_message.lower():
            return solution
    return None

# Function to generate content via Gemini API
def call_gemini_api(user_message):
    # Check for mental health keywords and provide solutions
    mental_health_response = detect_mental_health(user_message)
    if mental_health_response:
        return mental_health_response['response'] + " " + mental_health_response['coping_strategy']
    
    # If no mental health keyword matched, generate a more general response
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error: Could not connect to Gemini API."

# Route to serve the chatbot interface
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Show user message for tracking
    print(f"User message: {user_message}")
    
    # Call Gemini API or get mental health response
    bot_response = call_gemini_api(user_message)

    # Prepare word-by-word response
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)







