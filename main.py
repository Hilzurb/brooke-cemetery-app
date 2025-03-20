from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os

app = Flask(__name__)
CSV_FILE = 'cemetery_data.csv'
PASSWORD_VIEW = 'Brooke'  
PASSWORD_ADD = '26070'  

def initialize_csv():
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
        
