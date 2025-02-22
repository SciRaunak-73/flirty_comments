from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import random

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load flirty comments from text files
with open("flirty_comments_english.txt", "r", encoding="utf-8") as f:
    english_comments = f.readlines()
with open("flirty_comments_hindi.txt", "r", encoding="utf-8") as f:
    hindi_comments = f.readlines()

def get_random_comment():
    return random.choice(english_comments + hindi_comments).strip()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            comment = get_random_comment()
            return render_template('index.html', comment=comment, image_url=url_for('uploaded_file', filename=file.filename))
    return render_template('index.html', comment=None, image_url=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Serve HTML template
@app.route('/index.html')
def index_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
