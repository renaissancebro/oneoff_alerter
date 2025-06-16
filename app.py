from flask import Flask, render_template, redirect, url_for
import sqlite3
from flask_cors import CORS
from reg_alert import run_reg_check

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    conn = sqlite3.connect("regs.db")
    cur = conn.cursor()
    cur.execute("SELECT title, last_modified, url FROM documents ORDER BY last_modified DESC LIMIT 10")
    docs = cur.fetchall()
    conn.close()
    return render_template("index.html", docs=docs)

@app.route('/check')
def check_route():
    run_reg_check()  # triggers scraping and alert logic
    return redirect(url_for('index'))  # redirect to homepage/dashboard

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
