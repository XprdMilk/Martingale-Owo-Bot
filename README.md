# OwO Bot Martingale Farmer

An automated, hands-free coinflip script for the Discord OwO Bot using the Martingale betting strategy.

### Features
* **Live Dashboard:** Displays current bankroll, net profit, and countdown timers directly in the console.
* **Captcha Detection:** Instantly stops sending commands and plays a loud siren if a captcha is detected.
* **Auto-Cash Check:** Periodically checks your balance automatically to keep the terminal dashboard updated.

### Installation
1. Install the requirements: `pip install -r requirements.txt`
2. Rename `.env.example` to `.env` and paste your Discord User Token and Target Channel ID inside.
3. Run the script: `python mart2.py`
4. Type `.start` in the designated Discord channel.

### Disclaimer
Using self-bots violates Discord's Terms of Service. Use this script at your own risk. Furthermore, the Martingale strategy does not guarantee infinite profit; a long enough losing streak will wipe out your bankroll. Walk away while you are in the green!