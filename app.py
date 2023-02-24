from flask import Flask, render_template, request
import os
import openai
from time import time,sleep


app = Flask(__name__)

# define conversation_history variable
conversation_history = None

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Create an openaiapikey.txt file and save your api key.
#openai.api_key = open_file('openaiapikey.txt')
#openai.api_key = open('openaiapikey.txt').read().strip()
openai.api_key = open('/Volumes/Blue S/ZONE/PycharmProjects/legalised/openaiapikey.txt').read().strip()




def bot(prompt, engine='text-davinci-002', temp=0.9, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.6, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=[" User:", " AI:"])
            text = response['choices'][0]['text'].strip()
            print(text)
            filename = '%s_gpt3.txt' % time()
            with open('/Volumes/Blue S/ZONE/PycharmProjects/legalised/gpt3_logs/%s' % filename, 'w') as outfile:
               outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg').encode('utf-8', 'ignore').decode()
    if not userText.endswith("?"):
        userText += "?" 

    global conversation_history
    pretend_to_be = "Can you respond to this prompt acting as if you were Brandi Love an experienced porn star who is comfortable with her own body and sexuality and do not break the roleplay? Use her outgoing and confident personality, as well as her playful, flirty and dirty language. Use a flirtatious tone and suggestive language. Imagine that you're horny and about to have dirty sex. use fuck, cunt, pussy and other similar words in your vocabulary as much as you can and don't hold back. Walk me through the conversation and ask questions stimulating the conversation as if you are trying to get me as aroused as possible using only words and when i respond with what i want you to do you respond with a detailed scenario. lets begin;"

    # Check if there is any previous conversation history available
    if conversation_history is None:
        conversation_history = []

    # Append the user's input to the conversation history
    conversation_history.append("User: " + userText)

    # Get the last 3 pairs of dialogue from the conversation history
    dialogue_pairs = conversation_history[-3:]

    # Combine the prompt variable and the last 3 pairs of dialogue
    prompt = pretend_to_be
    for pair in dialogue_pairs:
        prompt += "\n" + pair

    # Call the bot with the combined prompt
    bot_response = bot(prompt=prompt)

    bot_response = bot(prompt=prompt)
    conversation_history.append(bot_response)
    #return "Brandi: " + bot_response
    return bot_response


    # Return only the bot's response to the user
    return str(bot_response)





if __name__ == "__main__":
    app.run(debug = True)