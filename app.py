# app.py
import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Get Gemini API key from environment variables
GEMINI_KEY = os.getenv('GEMINI_KEY')

# --- API Endpoint for Gemini Text Generation ---
@app.route('/generate-text', methods=['POST'])
def generate_text():
    """
    Handles POST requests to generate text using the Gemini API.
    Expects a JSON body with a 'prompt' key.
    """
    if not GEMINI_KEY:
        return jsonify({"error": "GEMINI_KEY not set in environment variables."}), 500

    # Get JSON data from the request body
    data = request.get_json()

    # Check if 'prompt' is present in the request data
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body."}), 400

    prompt = data['prompt']

    # Gemini API configuration
    base_url = 'https://generativelanguage.googleapis.com/v1beta'
    models_url = f'{base_url}/models/gemini-2.0-flash'
    url = f'{models_url}:generateContent?key={GEMINI_KEY}'
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Payload for the Gemini API request
    gemini_data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        # Make the request to the Gemini API
        response = requests.post(url, headers=headers, json=gemini_data)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Parse the JSON response from Gemini
        gemini_response = response.json()

        # Extract the generated text
        if gemini_response and 'candidates' in gemini_response and \
           len(gemini_response['candidates']) > 0 and \
           'content' in gemini_response['candidates'][0] and \
           'parts' in gemini_response['candidates'][0]['content'] and \
           len(gemini_response['candidates'][0]['content']['parts']) > 0 and \
           'text' in gemini_response['candidates'][0]['content']['parts'][0]:
            
            generated_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"generated_text": generated_text}), 200
        else:
            return jsonify({"error": "Unexpected response format from Gemini API.", "details": gemini_response}), 500

    except requests.exceptions.RequestException as e:
        # Handle network or HTTP-related errors from requests library
        return jsonify({"error": f"Error connecting to Gemini API: {e}", "details": str(response.text if 'response' in locals() else '')}), 500
    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

# --- Health Check Endpoint ---
@app.route('/health', methods=['GET'])
def health_check():
    """Simple endpoint to check if the server is running."""
    return jsonify({"status": "running", "message": "API server is healthy!"}), 200

# --- Run the Flask app ---
if __name__ == '__main__':
    # You can change the port as needed
    app.run(debug=True, port=5000)

