from flask import Flask, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)         # Create Flask app first
CORS(app)                     # Then apply CORS

@app.route('/')
def index():
    conn = sqlite3.connect("regs.db")
    cur = conn.cursor()
    cur.execute("SELECT title, last_modified, url FROM documents ORDER BY last_modified DESC LIMIT 10")
    docs = cur.fetchall()
    conn.close()
    return render_template("index.html", docs=docs)

if __name__ == "__main__":
    app.run(debug=True)
