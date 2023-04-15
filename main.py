# import requirements needed
import os
import smtplib
import re

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
import requests

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

API_URL = "https://api-inference.huggingface.co/models/Chetan007/gpt2-sonnet-generators"
headers = {"Authorization": "Bearer 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"}

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
  app = Flask(__name__)
else:
  app = Flask(__name__, static_url_path=base_url + 'static')

app.secret_key = os.urandom(64)


@app.route(f'{base_url}')
def home():
  return render_template('index.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
  return redirect(url_for('results'))


@app.route(f'{base_url}/results/')
def results():
  if 'data' in session:
    data = session['data']
    return render_template('results.html', generated=data)
  else:
    return render_template('results.html', generated=None)


"""
Finish the two functions below to complete the website's backend.
"""


def query(text):
  """
    Can you write a function that sends a prompt to the Hugging Face endpoint and
    returns the model's output as a string?
    """
  payload = {"inputs": text}
  response = requests.post(API_URL, headers=headers, json=payload)
  try:
    q = eval(
      str(response.content)[3:-2].replace("\\n",
                                          " ").replace("\\",
                                                       " "))["generated_text"]
    print(q)
    if not q.endswith('.'):
      q += '.'
  except Exception as e:
    q = e
    q = "I am sorry our creative expert is busy due to traffic, Please try again after some time. Thank you!"
  return q


def process_prompt(prompt):
  processed_prompt = query(prompt)
  return render_template('results.html', generated=processed_prompt)


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
  if request.method == 'POST':
    prompt = request.form['prompt']
    # Process the prompt and return the result
    result = process_prompt(prompt)
    return result
  else:
    return redirect(url_for('home'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port, debug=True)
