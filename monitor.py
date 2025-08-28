import requests
import datetime


#config
WEBSITE_URL = "https://vonwayforex.com"
DISCORD_WEBHOOK = "https://discordapp.com/api/webhooks/1410541592430772266/ODhT3mnYipnNrkOade63Zgy3200thAddKErKuS5wTJoLIjUQdJBWDpmXuY025UQMvVjo"
TELEGRAM_BOT_TOKEN = "8038370188:AAHOK5rVTvhADOmsSUebac3hmZeShqT8K1w"
TELEGRAM_CHAT_ID = "-1002947694522"

LOG_FILE = r"C:\Users\mirol\OneDrive\Desktop\logwebsite\test_log.txt"

def send_discord(message:str):
    data = {
        "content":message
    }
    try:
        response = requests.post(DISCORD_WEBHOOK,json=data,timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        write_log("failed",e)
        

def write_log(message:str):
    """Write a message to the log file with timestamp"""
    gmt8 = datetime.timezone(datetime.timedelta(hours=8))
    timestamp = datetime.datetime.now(gmt8).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE,"a",encoding="utf-8") as f:f.write(line)


def send_telegram(message:str):
    """Send alert to telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=5
        )
        print("Response:", response.text)
    except Exception as e:
        write_log("failed",e)


def check_site():
    try:
        response = requests.get(WEBSITE_URL, timeout=10)

        if response.status_code == 200:
            gmt8 = datetime.timezone(datetime.timedelta(hours=8))
            timestamp = datetime.datetime.now(gmt8).strftime("%Y-%m-%d %H:%M:%S")
            message = f"✅ Website Vonway is UP , {timestamp}"
            write_log(message)
            send_telegram(message)
            send_discord(message)
        else:
            message = f"⚠️ Website DOWN: Website Vonway (Status: {response.status_code}),{timestamp}"
            write_log(message)
            send_telegram(message)
            send_discord(message)

    except Exception as e:
        gmt8 = datetime.timezone(datetime.timedelta(hours=8))
        timestamp = datetime.datetime.now(gmt8).strftime("%Y-%m-%d %H:%M:%S")
        message = f"❌ ERROR: Website Vonway ({e}),{timestamp}"
        write_log(message)
        send_telegram(message)
        send_discord(message)


if __name__== "__main__":
    check_site()
    print("✅ Website monitor check finished")
    

