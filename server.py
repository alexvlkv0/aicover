import os
from flask import Flask, request, redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename
import aicover

UPLOAD_FOLDER = os.path.join(os.getcwd(),'audio')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/upload", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        data = ' '.join(request.args).split('-')
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], f'queue\\{filename}')
            file.save(path)
            ai = aicover.Cover()
            for version in ai.cover(data[0],data[1],data[2],data[3], app.config['UPLOAD_FOLDER']):
                os.rename(version[0], os.path.join(app.config['UPLOAD_FOLDER'], f'result\\version{version[1]}'))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)