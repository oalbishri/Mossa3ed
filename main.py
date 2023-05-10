import requests
import json
from flask import Flask, request, render_template

app = Flask(__name__)

API_ENDPOINT = "https://experimental.willow.vectara.io/v1/chat/completions"

HEADERS = {
    'Content-Type': 'application/json',
    'customer-id': '4199489844',
    'x-api-key': 'XXXXX'
}

def get_vectara_data(complaint):
    url = "https://api.vectara.io/v1/query"

    payload = json.dumps({
        "query": [
            {
                "query": complaint,
                "numResults": 5,
                "corpusKey": [
                    {
                        "customerId": 0,
                        "corpusId": 2
                    }
                ]
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'customer-id': 'XXXXX',
        'x-api-key': 'XXXXXX'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def sendQus(com, additional_info):
    prompt = ("This bot is a customer service agent for a company called Five Seasons which is a company that specialized in optical and selling glasses. The company has different branches. In the reply the bot should be welcoming but not greeting the costumer using the Islamic greets unless the costumer use it. The bot will receive the customer's complaint in text form, analyze it, and respond with an apologetic and friendly tone in the Saudi Najdi dialect. Please provide a solution to the customer's issue with detailed steps based on the information the customer has provided in the following complaint. Make sure the reply is in the Saudi Najdi dialect and use emojis when necessary. Also, make sure the reply is consistent with the Saudi culture and sounds like Saudis. If needed provide like a to-do-list to the costumer. Also please depends first on the information provided to CHatgpt through Vectara API:\n\n"
            "Complaint: {}\n\nsummarize and add this Additional info: {}\n\nSuggested reply in the Saudi Najdi dialect. This reply should be very concise and to the poin. Be welcoming but do not greet with the Islamic greet if the costumer did not greet you with that:".format(com, additional_info))
    
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": com
            }
        ]
    }
    json_body = json.dumps(body)
    res = requests.post(url=API_ENDPOINT, data=json_body, headers=HEADERS)
    response_list = json.loads(res.text)
    response_text = response_list['choices'][0]['message']['content']
    return response_text.strip()

@app.route('/send_question', methods=['POST'])
def send_question():
    complaint = request.form.get('complaint')

    if complaint:
        vectara_data = get_vectara_data(complaint)
        response = sendQus(complaint, vectara_data)
        return render_template('form.html', response=response, complaint=complaint)
    else:
        return "Invalid input data", 400

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
