from datetime import datetime

def alert_feed(title, url):
    print(f"NEW: {title} - {url}")
    # Log the alert to a file
    with open("alerts.log", "a") as f:
        f.write(f"[{datetime.now()}] NEW: {title} - {url}\n")
