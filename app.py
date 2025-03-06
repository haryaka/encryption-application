from flask import Flask, request, render_template, send_file
import os
from encryption import encrypt_file, decrypt_file  # Import encryption functions

app = Flask(__name__)

# Storage paths
UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = 'encrypted_files'
DECRYPTED_FOLDER = 'decrypted_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    method = request.form['method']
    key = request.form['key']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        encrypted_path = encrypt_file(filepath, method, key)
        return send_file(encrypted_path, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    file = request.files['file']
    method = request.form['method']
    key = request.form['key']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        decrypted_path = decrypt_file(filepath, method, key)
        return send_file(decrypted_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
