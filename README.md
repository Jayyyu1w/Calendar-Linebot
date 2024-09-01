# Calendar-Linebot

## 👁️Overview
This is Linebot to extract event from message and add to google calendar, using flask to build local server, ngrok service to build line webhook URL and llama-cpp-python to run LLM locally.

It is welcome to open issue or pull requests to make this project better.🎉 

## 📖Installation
- To run this project locally, follow this steps:
1. Clone the repository of this project by excuting the following command
```bash
git clone https://github.com/Jayyyu1w/Calendar-Linebot.git
or
git clone git@github.com:Jayyyu1w/Calendar-Linebot.git
```

2. Install the required packages by running the folloeing command:

```bash
pip install -r requirements.txt
```

3. Install [ngrok](https://ngrok.com/)

4. Login [Line Developers](https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2F)

## 🧰Usage
- Add lineapi.txt and put Channel access token in first line, Channel secret in second line.

- Add model and paste model path to llm_extract.py

- Run server.py
```
python server.py
```

- Run ngrok service
```
ngrok http <your local server URL>
```

- Put ngrok URL to Line Bot Webhook URL and add /callback at back
```
<ngrok URL>/callback
```

- All done🤗
