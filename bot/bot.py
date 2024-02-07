from openai import OpenAI
import telebot

import sqlite3

from mysecrets import config
from utils import clean_code


TELEGRAM_TOKEN = config.bot_api_key
OPENAI_API_KEY = config.openai_api_key

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def secretize_hint(hint, n):
    hint = hint.split('\n')
    for i in range(len(hint)):
        hint[i] = f'||{hint[i]}||'
    hint = f"Подсказка {n}:\n" + '\n'.join(hint)
    
    return hint

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Поришли мне задачку, я дам тебе подсказки.")
    
# main function
@bot.message_handler(func=lambda message: True)
def explain_code(message):
    text = message.text
    
    # cache
    #conn = sqlite3.connect(config.cache_dir + 'code_explanations.db')
    #cursor = conn.cursor()
    # Check if the code is already in the database
    #cursor.execute("SELECT explanation FROM explanations WHERE code = ?", (code,))
    #explanation = cursor.fetchone()
    
    explanation = None
    
    if explanation:
        bot.reply_to(message, explanation[0])
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant skilled in explaining olympiad programming tasks who speaks russian language and provides useful links for resources when its is needed. You should give 3 levels of hints: Hint 1: (easy hint), Hint2: (medium hint), Hint 3: (full hint). If a certain algorithm is needed, state the name of it in the Hint 2. Also provide code in Hint 3. Format the output like this: Hint 1: ... Hint 2: ... Hint 3: ... ."},
                    {"role": "user", "content": f"Помоги с решением этой задачи:\n\n{text}"}
                ]
            )
            explanation = response.choices[0].message.content
            
            for c in ['_', '`', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' ]:
                explanation = explanation.replace(c, f'\\{c}')
            
            hint1 = explanation[explanation.find("Hint 1:"):explanation.find("Hint 2:")]
            hint1 = secretize_hint(hint1, 1)
            
            hint2 = explanation[explanation.find("Hint 2:"):explanation.find("Hint 3:")]
            hint2 = secretize_hint(hint2, 2)
            
            hint3 = explanation[explanation.find("Hint 3:"):]
            hint3 = secretize_hint(hint3, 3)
            
            all_hints = '\n\n'.join([hint1, hint2, hint3])
            
            # Insert the new code and explanation into the database
            #cursor.execute("INSERT INTO explanations (code, explanation) VALUES (?, ?)", (code, explanation))
            #conn.commit()
            try:
                bot.reply_to(message, hint1, parse_mode='MarkdownV2')
            except:
                print(hint1)
            try:
                bot.reply_to(message, hint2, parse_mode='MarkdownV2')
            except:
                print(hint2)
            try:
                bot.reply_to(message, hint3, parse_mode='MarkdownV2')
            except:
                print(hint3)
            
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
        

bot.infinity_polling()

