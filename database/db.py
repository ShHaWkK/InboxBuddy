import sqlite3

def connect():
    conn = sqlite3.connect("inboxbuddy.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            body TEXT,
            summary TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    return conn

def save_mail(mail, summary=None, response=None):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO mails (sender, subject, body, summary, response)
        VALUES (?, ?, ?, ?, ?)
    ''', (mail["from"], mail["subject"], mail["body"], summary, response))
    conn.commit()
    conn.close()
