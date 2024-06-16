from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'assets/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para uploads

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def save_img(file) :
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return filepath

# Rota principal para carregar o mapa
@app.route('/')
def index():
    map_data = load_map_data()
    return render_template('index.html', map_data=map_data)

# Rota para receber os dados do mapa e salvá-los em um arquivo
@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()

    with open('map_data.json', 'w') as f:
        json.dump(data, f)

    return 'Data saved successfully!'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/assets/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Verifique se o arquivo foi submetido
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new Icon</title>
    <h1>Upload new Icon</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



# Função para carregar os dados do mapa
def load_map_data():
    if os.path.exists('map_data.json'):
        with open('map_data.json', 'r') as f:
            map_data = json.load(f)
        return map_data
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

