# PortalQuiz
Challenge yourself with our Winter Quiz bot! This bot was made by the Portal Development team as an entry to Top.gg’s 2021 Winter Hackathon and won the prize for Most Consistent. Start the quiz with the `/quiz` command and challenge your friends to get the highest score! To end a game early, run the `/endgame` command.

~~[Invite the bot here.](https://top.gg/bot/871981757531050064)~~

## EOL Notice
This project is no longer maintained and the bot has been taken offline due to general lack of interest. The source code is available for educational purpose and self-hosting. Support will not be provided for self-hosting.

## Hosting
Clone the repository
```bash
git clone https://github.com/PortalDiscordDevelopment/PortalQuiz.git
```
Install the dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -Ur requirements.txt
```

Follow the directions in `.env.example` and `config.example.py` to set up your environment variables and configuration.

Run the bot
```bash
python3 bot.py
```