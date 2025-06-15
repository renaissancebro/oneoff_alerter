# reg_alert.py

import os
import requests
import sqlite3
from dotenv import load_dotenv
from alert_feed import alert_feed

# === SETUP ===
load_dotenv()
API_KEY = os.getenv("API_KEY")
DB_PATH = "regs.db"

# === DB INIT ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        title TEXT,
        last_modified TEXT,
        url TEXT
    )
    """)
    conn.commit()
    return conn, cur

# === API CALL ===
def get_documents(keyword="solar", limit=5):
    params = {
        "api_key": API_KEY,
        "filter[searchTerm]": keyword,
        "page[size]": limit,
        "sort": "-lastModifiedDate"
    }
    res = requests.get("https://api.regulations.gov/v4/documents", params=params)
    res.raise_for_status()
    return res.json().get("data", [])

# === MAIN LOGIC ===
def update_and_alert(docs, cur, conn):
    for doc in docs:
        doc_id = doc["id"]
        attrs = doc["attributes"]
        title = attrs["title"]
        last_mod = attrs.get("lastModifiedDate")
        url = f"https://www.regulations.gov/document/{doc_id}"

        cur.execute("SELECT last_modified FROM documents WHERE id = ?", (doc_id,))
        row = cur.fetchone()

        if not row:
            print(f"[NEW] {title}\n🔗 {url}\n")
            cur.execute("INSERT INTO documents VALUES (?, ?, ?, ?)", (doc_id, title, last_mod, url))
            alert_feed(title, url)

        elif row[0] != last_mod:
            print(f"[UPDATED] {title}\n🔗 {url}\n(last mod changed)\n")
            cur.execute("UPDATE documents SET last_modified = ?, title = ? WHERE id = ?", (last_mod, title, doc_id))
            alert_feed(title, url)

    conn.commit()

# === ENTRYPOINT ===
if __name__ == "__main__":
    conn, cur = init_db()
    documents = get_documents(keyword="solar", limit=10)
    update_and_alert(documents, cur, conn)
