from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
DB_PATH = 'db/patients.db'

def init_db():
    os.makedirs('db', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            disease TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_charts(df):
    os.makedirs('static', exist_ok=True)

    # Pie chart: Disease distribution
    plt.figure(figsize=(4,4))
    df['disease'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, shadow=True)
    plt.ylabel('')
    plt.title('Disease Distribution')
    plt.tight_layout()
    plt.savefig('static/disease_pie.png')
    plt.close()

    # Bar chart: Avg age by gender
    plt.figure(figsize=(5,4))
    df.groupby('gender')['age'].mean().plot(kind='bar', color=['skyblue', 'salmon', 'orange'])
    plt.title('Average Age by Gender')
    plt.ylabel('Average Age')
    plt.tight_layout()
    plt.savefig('static/age_gender_bar.png')
    plt.close()

    # Bar chart: Gender count
    plt.figure(figsize=(5,4))
    df['gender'].value_counts().plot(kind='bar', color=['skyblue', 'salmon', 'orange'])
    plt.title('Patient Count by Gender')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('static/gender_count_bar.png')
    plt.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)",
                  (name, age, gender, disease))
        conn.commit()
        conn.close()
        return redirect('/')

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()

    if not df.empty:
        generate_charts(df)

    return render_template('index.html', patients=df.values, has_data=not df.empty)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
DB_PATH = 'db/patients.db'

def init_db():
    os.makedirs('db', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            disease TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_charts(df):
    os.makedirs('static', exist_ok=True)

    # Pie chart: Disease distribution
    plt.figure(figsize=(4,4))
    df['disease'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, shadow=True)
    plt.ylabel('')
    plt.title('Disease Distribution')
    plt.tight_layout()
    plt.savefig('static/disease_pie.png')
    plt.close()

    # Bar chart: Avg age by gender
    plt.figure(figsize=(5,4))
    df.groupby('gender')['age'].mean().plot(kind='bar', color=['skyblue', 'salmon', 'orange'])
    plt.title('Average Age by Gender')
    plt.ylabel('Average Age')
    plt.tight_layout()
    plt.savefig('static/age_gender_bar.png')
    plt.close()

    # Bar chart: Gender count
    plt.figure(figsize=(5,4))
    df['gender'].value_counts().plot(kind='bar', color=['skyblue', 'salmon', 'orange'])
    plt.title('Patient Count by Gender')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('static/gender_count_bar.png')
    plt.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)",
                  (name, age, gender, disease))
        conn.commit()
        conn.close()
        return redirect('/')

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()

    if not df.empty:
        generate_charts(df)

    return render_template('index.html', patients=df.values, has_data=not df.empty)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
