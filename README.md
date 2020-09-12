# Installation
1. At first, you need to [create new bot in Telegram](https://core.telegram.org/bots#6-botfather).
2. Install python and venv
3. Install [poetry](https://python-poetry.org/docs/#installation)
4. Install dependencies with `poetry install`

You're ready to run bot locally.

# Local run
1. Set up environment variable `TELEGRAM_BOT_KEY`.
   For example, `export TELEGRAM_BOT_KEY=<youy_token>`
2. Activate environment `poetry shell`
3. Run bot `python hackabot\telegram.py`

# Deployment
1. If you have not access to some server, you may sign up to some one (for instance, [Heroku](https://www.heroku.com/)).
2. Connect to the server. You may [use ssh](https://phoenixnap.com/kb/ssh-to-connect-to-remote-server-linux-or-windows) to connect.
3. Install Tmux `sudo apt install tmux`
4. Attach to Tmux `tmux attach || tmux new`
5. Clone your repository.
5. Repeat local run steps.

# Chitchat
To use chitchat service, try to run the next script:
```python
import requests

if __name__ == '__main__':
    resp = requests.post(
        'https://chitchat-vc.tinkoff.ru/?key=d812744d7bb10f374df9faa10a146ebf',
        json={'text': 'Привет', 'user_id': 'some_user'}
    )
    print(resp.status_code, resp.text)
```

# Tests
We recommend to write [smoke-tests](https://en.wikipedia.org/wiki/Smoke_testing_(software)) for your solutions. We wrote some tests to make this process more clear for you
