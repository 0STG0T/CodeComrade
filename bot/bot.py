from openai import OpenAI
import telebot

import sqlite3

from mysecrets import config
from utils import clean_code


TELEGRAM_TOKEN = config.bot_api_key
OPENAI_API_KEY = config.openai_api_key

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi! Send me some code, and I'll try to explain it.")
    
# main function
@bot.message_handler(func=lambda message: True)
def explain_code(message):
    code = clean_code(message.text)
    
    # cache
    conn = sqlite3.connect(config.cache_dir + 'code_explanations.db')
    cursor = conn.cursor()
    # Check if the code is already in the database
    cursor.execute("SELECT explanation FROM explanations WHERE code = ?", (code,))
    explanation = cursor.fetchone()
    
    if explanation:
        bot.reply_to(message, explanation[0])
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant skilled in explaining programming code who speaks russian language and provides useful links for resources when its is needed."},
                    {"role": "user", "content": f"Обьясни этот код:\n\n{code}"}
                ]
            )
            explanation = response.choices[0].message.content
            
            # Insert the new code and explanation into the database
            cursor.execute("INSERT INTO explanations (code, explanation) VALUES (?, ?)", (code, explanation))
            conn.commit()
            
            bot.reply_to(message, explanation)
            
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
        

bot.infinity_polling()

