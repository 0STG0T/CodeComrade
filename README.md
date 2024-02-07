<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="./images/logo.webp" alt="Bot logo"></a>
</p>

<h3 align="center">CodeComrade</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-inactive-red.svg)]()
[![Platform](https://img.shields.io/badge/platform-telegram-blue.svg)](https://t.me/code_comrade_bot)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](/LICENSE)

</div>

---

<p align="center">A real friend won't let you cheat!<br>🤖<br>
CodeComrade - a TG bot that helps students by providing helpful hints for different problems, but not giving out the whole solution to copy.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Demo / Working](#demo)
- [How it works](#working)
- [Usage](#usage)
- [Deploying your own bot](#deployment)
- [TODO](../TODO.md)
- [Acknowledgements](#acknowledgement)

## 🧐 About <a name = "about"></a>
<b>Problem:</b><br>
<pre>
  When solving problems, many people have problems, sometimes a person does not understand where to start a solution. In such circumstances, cheating or mindless copying of the solution often occurs. Thus, a person does not learn and forgets the solution over time, instead of learning how to solve this problem.
</pre>
  <br>
<b>Solution:</b><br>
<pre>
  A telegram bot that gives hints and leads to a solution without giving a complete solution.
</pre>

## 🎥 Demo / Working <a name = "demo"></a>

![Responce with secrets](./images/demo1.png)

![Unleashing secrts](./images/demo2.png)

## 💭 How it works <a name = "working"></a>
<b>1. Getting responce from OpenAI:</b>
<pre>
response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant skilled in explaining olympiad programming tasks who speaks russian language and provides useful links for resources when its is needed. You should give 3 levels of hints: Hint 1: (easy hint), Hint2: (medium hint), Hint 3: (full hint). If a certain algorithm is needed, state the name of it in the Hint 2. Also provide code in Hint 3. Format the output like this: Hint 1: ... Hint 2: ... Hint 3: ... ."},
                    {"role": "user", "content": f"Помоги с решением этой задачи:\n\n{text}"}
                ]
      )
</pre>
<b>2. Formatting telegram output:</b>
<pre>
def secretize_hint(hint, n):
    hint = hint.split('\n')
    for i in range(len(hint)):
        hint[i] = f'||{hint[i]}||'
    hint = f"Подсказка {n}:\n" + '\n'.join(hint)
    
    return hint
  
for c in ['_', '`', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' ]:
                explanation = explanation.replace(c, f'\\{c}')

hint1 = explanation[explanation.find("Hint 1:"):explanation.find("Hint 2:")]
            hint1 = secretize_hint(hint1, 1)
</pre>

## 🎈 Usage <a name = "usage"></a>

@code_comrade_bot

Just send it a problem.

The bot will then give you 3 hints in secrets.

## 🚀 Deploying your own bot <a name = "deployment"></a>

<pre>
1. Install all packages used in the project.
2. Pass your API keys to mysecrets.py
3. RUN bot.py
</pre>

## ⛏️ Built Using <a name = "built_using"></a>

- OpenAI API
- BotFather
- Telebot
- Python

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

Project paper and presentaion in russian: [link](./АкмаевА_11А%202.zip)