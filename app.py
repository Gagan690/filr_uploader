from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
# from flask_ngrok import run_with_ngrok
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Allowed extensions
ALLOWED_EXTENSIONS = {'jpg', 'pdf', 'mp4', 'docx'}

# Set upload folder inside /static/uploads
UPLOAD_FOLDER = Path(__file__).parent / 'static' / 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy login credentials
users = {
    'gagan': 'password123',
    'admin': 'admin123'
}

# Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('upload'))
        else:
            flash('Invalid Credentials. Try again.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            username = session['username']
            date_str = datetime.now().strftime('%Y_%m_%d')
            ext = file.filename.rsplit('.', 1)[1].lower()

            # Build the path: /static/uploads/<date>/<username_date>/<filetype>/
            upload_path = app.config['UPLOAD_FOLDER'] / date_str / f"{username}_{date_str}" / ext
            upload_path.mkdir(parents=True, exist_ok=True)

            filename = secure_filename(file.filename)
            file.save(upload_path / filename)

            flash('File uploaded successfully!')
            return redirect(url_for('upload'))

        else:
            flash('Invalid file type.')
            return redirect(url_for('upload'))

    return render_template('upload.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# For running locally
if __name__ == '__main__':
    # run_with_ngrok(app)  # Add this line to enable ngrok
    app.run()
