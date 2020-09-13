## PEPEQuestBot, or Financial Quest with Oleg, Tinkoff voice assistant

> Solution produced during "Oleg Hackathon" as part of the "Hack Lab" course in Skotech in collaboration with Tinkoff, September 11-13, 2020
>
> Team PEPEtoners: [Ilya Borovik](https://github.com/ilya16), [Vladislav Kniazev](https://github.com/Vladoskn), [Vanessa Skliarova](https://github.com/Vanessik), [Bulat Khabibullin](https://github.com/MrWag2), and [Zakhar Pichugin](https://github.com/zakharpichugin)
>
> [Bot demo](https://youtu.be/AzI5-e4_kXI)

## Installation
1. At first, you need to [create new bot in Telegram](https://core.telegram.org/bots#6-botfather).
2. Install python and venv

You're ready to run bot locally.

## Local run
1. Set up environment variables: `TELEGRAM_BOT_KEY`, `VOICEKIT_API_KEY`, `VOICEKIT_SECRET_KEY`.
   For example, `export TELEGRAM_BOT_KEY=<TOKEN>`
2. Activate virtual environment using `source venv/bin/activate`
3. Run bot `python hackabot/bot.py`

## Deployment
1. If you have not access to some server, you may sign up to some one (for instance, [Heroku](https://www.heroku.com/)).
2. Connect to the server. You may [use ssh](https://phoenixnap.com/kb/ssh-to-connect-to-remote-server-linux-or-windows) to connect.
3. Install Tmux `sudo apt install tmux`
4. Attach to Tmux `tmux attach || tmux new`
5. Clone your repository.
5. Repeat local run steps.