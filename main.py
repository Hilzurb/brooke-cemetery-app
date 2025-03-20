from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
import requests

app = Flask(__name__)
CSV_FILE = 'cemetery_data.csv'
PASSWORD_VIEW = 'Brooke'  
PASSWORD_ADD = '26070'  

GITHUB_CSV_URL = 'https://raw.githubusercontent.com/hilzurbuch/brooke-cemetery-app/main/cemetery_data.csv'

def fetch_csv_from_github():
    try:
        response = requests.get(GITHUB_CSV_URL)
        response.raise_for_status()
        with open(CSV_FILE, 'w') as file:
            file.write(response.text)
        print("✅ CSV fetched successfully from GitHub.")
    except Exception as e:
        print(f"⚠️ Error fetching CSV from GitHub: {e}")
        # If fetching fails, create an empty CSV to avoid crashing
        if not os.path.exists(CSV_FILE):
            df = pd.DataFrame(columns=['Name', 'DOB', 'DOD', 'STONE', 'SECTION', 'LOT', 'NOTES', 'DIRECTION'])
            df.to_csv(CSV_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD_VIEW:
            return redirect(url_for('home'))
        else:
            return "<h2>Incorrect password. Go back and try again.</h2>"
    return '''<h1>Brooke Cemetery Login</h1>
    <form method="POST">
        <input type="password" name="password" placeholder="Enter password">
        <button type="submit">Login</button>
    </form>'''

@app.route('/home')
def home():
    return '''
    <h1>Brooke Cemetery Database</h1>
    <p>Serving the historic rural cemetery of Wellsburg, WV — established 1857</p>
    <h2>Search Entries</h2>
    <form action="/search" method="POST">
        <input name="Name" placeholder="Name">
        <input name="DOB" placeholder="DOB">
        <input name="SECTION" placeholder="Section">
        <input name="LOT" placeholder="Lot">
        <button type="submit">Search</button>
    </form>
    <h2>Add New Entry (Password Required)</h2>
    <form action="/add" method="POST">
        <input type="password" name="add_password" placeholder="Add Entry Password">
        <input name="Name" placeholder="Name" required>
        <input name="DOB" placeholder="DOB">
        <input name="DOD" placeholder="DOD">
        <input name="STONE" placeholder="Stone">
        <input name="SECTION" placeholder="Section">
        <input name="LOT" placeholder="Lot">
        <input name="NOTES" placeholder="Notes">
        <input name="DIRECTION" placeholder="Direction">
        <button type="submit">Add Entry</button>
    </form>
    <h2>Download All Records</h2>
    <a

