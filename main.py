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
        # Create an empty CSV if fetch fails
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
    <a href="/download">Download CSV</a>
    '''

@app.route('/search', methods=['POST'])
def search():
    df = pd.read_csv(CSV_FILE)
    query = request.form
    results = df.copy()

    for field in ['Name', 'DOB', 'SECTION', 'LOT']:
        if query[field]:
            results = results[results[field].astype(str).str.contains(query[field], case=False, na=False)]

    return results.to_html()

@app.route('/add', methods=['POST'])
def add():
    add_password = request.form.get('add_password')
    if add_password != PASSWORD_ADD:
        return "<h2>Incorrect add-entry password. Go back and try again.</h2>"

    new_entry = {
        'Name': request.form['Name'],
        'DOB': request.form['DOB'],
        'DOD': request.form['DOD'],
        'STONE': request.form['STONE'],
        'SECTION': request.form['SECTION'],
        'LOT': request.form['LOT'],
        'NOTES': request.form['NOTES'],
        'DIRECTION': request.form['DIRECTION']
    }
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return redirect(url_for('home'))

@app.route('/download')
def download():
    return send_file(CSV_FILE, as_attachment=True)

if __name__ == '__main__':
    fetch_csv_from_github()
    app.run(host='0.0.0.0', port=81)
