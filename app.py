from flask import Flask, render_template, request, g
from flask import redirect, url_for, abort
import sqlite3

app = Flask(__name__)

def get_message_db():
    try:
        return g.message_db
    except AttributeError:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cursor = g.message_db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                          id INTEGER PRIMARY KEY,
                          handle TEXT,
                          message TEXT)''')
        g.message_db.commit()
        return g.message_db

def insert_message(request):
    message = request.form['message']
    handle = request.form['handle']
    
    db = get_message_db()
    cursor = db.cursor()
    SQL_query = "INSERT INTO messages (handle, message) VALUES (?, ?)"
    cursor.execute(SQL_query, (handle, message))
    
    db.commit()
    db.close()

def random_messages(n):
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('''SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT ?''', (n,))
    messages = cursor.fetchall()
    db.close()
    return messages

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        insert_message(request)
        appreciation = "Thanks for Submitting!"
        return render_template('submit.html', appreciation = appreciation)
    else:
        return render_template('submit.html')

@app.route('/view')
def view():
    messages = random_messages(5)
    return render_template('view.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
