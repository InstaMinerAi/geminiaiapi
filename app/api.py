import google.generativeai as genai
import json

from fastapi import FastAPI

app = FastAPI()

genai.configure(api_key="AIzaSyBKjGn82XbYabudH5CIeS1lNupOFys3Wf4")

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

def send_and_recieve(message, history):
    # Set up the model
    generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens":  200,
    }
    
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    for n in range(3):
      try:
        convo = model.start_chat(history=json.loads(history))
        convo.send_message(str(message))
        return convo.last.text
      except Exception as e:
        print("Error:", e)
        if n == 3:
          return "Uh oh! looks like something went wrong, our support team will contact you shortly"
        continue
    return "Uh oh! looks like something went wrong, our support team will contact you shortly"

@app.get("/{message}/{history}")
def send(message, history):
  response = send_and_recieve(message, (history))
  return response