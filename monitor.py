import os
import requests
import datetime

# ========== CONFIG ==========
WEBSITE_URL = "https://vonwayforex.com"
DISCORD_WEBHOOK = "https://discordapp.com/api/webhooks/1410541592430772266/ODhT3mnYipnNrkOade63Zgy3200thAddKErKuS5wTJoLIjUQdJBWDpmXuY025UQMvVjo"
TELEGRAM_BOT_TOKEN = "8038370188:AAHOK5rVTvhADOmsSUebac3hmZeShqT8K1w"
TELEGRAM_CHAT_ID = "-1002947694522"

# Log file (same folder as this script)
LOG_FILE = os.path.join(os.path.dirname(__file__), "website_log.txt")

# Make sure folder exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# ========== FUNCTIONS ==========
def write_log(message: str):
    """Write a message to the log file with timestamp (GMT+8)."""
    gmt8 = datetime.timezone(datetime.timedelta(hours=8))
    timestamp = datetime.datetime.now(gmt8).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def send_telegram(message: str):
    """Send alert to Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=5,
        )
        response.raise_for_status()
    except Exception as e:
        write_log(f"Telegram send failed: {e}")


# def send_discord(message: str):
#     """Send alert to Discord webhook."""
#     try:
#         response = requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=5)
#         response.raise_for_status()
#     except Exception as e:
#         write_log(f"Discord send failed: {e}")


def check_site():
    """Check website status and log/send alerts."""
    try:
        response = requests.get(WEBSITE_URL, timeout=10)

        gmt8 = datetime.timezone(datetime.timedelta(hours=8))
        timestamp = datetime.datetime.now(gmt8).strftime("%Y-%m-%d %H:%M:%S")

        if response.status_code == 200:
            message = f"✅ Website Vonway is UP , {timestamp}"
        else:
            message = f"⚠️ Website DOWN (Status: {response.status_code}), {timestamp}"

        write_log(message)
        send_telegram(message)
        # send_discord(message)

    except Exception as e:
        gmt8 = datetime.timezone(datetime.timedelta(hours=8))
        timestamp = datetime.datetime.now(gmt8).strftime("%Y-%m-%d %H:%M:%S")
        message = f"❌ ERROR checking website: {e}, {timestamp}"
        write_log(message)
        send_telegram(message)
        # send_discord(message)


# ========== MAIN ==========
if __name__ == "__main__":
    check_site()
    print("✅ Website monitor check finished. Log saved to:", LOG_FILE)
