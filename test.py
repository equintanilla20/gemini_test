import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY')

def main():
    print('test')
    # Change curl command to Python code
    base_url = 'https://generativelanguage.googleapis.com/v1beta'
    models_url = f'{base_url}/models/gemini-2.0-flash'
    url = f'{models_url}:generateContent?key={GEMINI_KEY}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "How many contestants are in Love Island USA season 7?"
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Response:", response.json()['candidates'][0]['content']['parts'][0]['text'])
    else:
        print("Error:", response.status_code, response.text)
    
    
if __name__ == '__main__':
    main()
    