from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os
import logging

app = Flask(__name__)
# CORS(app)l
@app.route('/')
def home():
    return render_template('/index.html')



# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv("API_KEY")

if api_key is None:
    raise ValueError("OpenAI API key not found in environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Store chat history in-memory (for demonstration purposes)
chat_history = []

# Route to handle GPT-3 requests
@app.route("/gpt-request", methods=["POST"])
def gpt_request():
    try:
        data = request.get_json()

        # Construct the conversation format for GPT-3 input
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            *chat_history,
            {"role": "user", "content": data["user_input"]},
        ]

        # Make API call to GPT-3
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Process and append GPT-3 response to chat history
        output = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": output})

        return jsonify({"success": True, "output": output})

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred."})

# if __name__ == "__main__":
#     app.run(debug=True)
