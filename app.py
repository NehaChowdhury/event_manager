from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            name TEXT, 
            email TEXT, 
            event TEXT
        )
    """)
    con.commit()
    con.close()

# Initialize DB on startup
with app.app_context():
    init_db()

# Home page
@app.route('/')
def home():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM events")
    events = cur.fetchall()
    con.close()
    return render_template("index.html", events=events)

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event = request.form['event']

        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO registrations VALUES (?,?,?)", (name, email, event))
        con.commit()
        con.close()
        return redirect('/')

    return render_template("register.html")

# Admin page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']

        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO events (title, date) VALUES (?,?)", (title, date))
        con.commit()
        con.close()
        return redirect('/')

    return render_template("admin.html")

# Edit Event
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        cur.execute("UPDATE events SET title=?, date=? WHERE id=?", (title, date, id))
        con.commit()
        con.close()
        return redirect('/')
    
    cur.execute("SELECT * FROM events WHERE id=?", (id,))
    event = cur.fetchone()
    con.close()
    return render_template("edit.html", event=event)

# Delete Event
@app.route('/delete/<int:id>')
def delete(id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM events WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
