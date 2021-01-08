from flask import Flask, render_template, url_for, request, send_from_directory, flash
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from flask import request, redirect
from werkzeug.utils import secure_filename
import os
from skimage import io
from skimage.transform import resize, rotate

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = "Your_secret_string"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
  region_options = ['East', 'South', 'Midwest', 'West', 'Pacific Coast', 'Desert']
  season_options = ['Spring', 'Summer', 'Fall', 'Winter']
  return render_template('home.html', region_options=region_options, season_options=season_options)


@app.route('/pictures', methods=['POST','GET'])
def pictures():
    region_id = request.form['region']
    season_id = request.form['season']
    return render_template('pictures.html', season_id=season_id, region_id=region_id, url=f'./static/images/region{region_id}season{season_id}.png', image=image)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/uploader', methods=['POST','GET'])
def uploader():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return render_template('/uploader.html')
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return render_template('/uploader.html')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        test_data = io.imread('static/uploads/'+filename)
        resize(test_data,(300,200,3))
        # Load model
        model_name = 'mymodel_43/'
        model = tf.keras.models.load_model('models/'+model_name)

        # Predict on user input
        prediction = np.argmax(model.predict(test_data))

        target_names=['Benign Plants', 'Poison Ivy', 'Poison Oak']

        # Index target names at prediction value
        for name in target_names[prediction]:
            predicted_name = name
        return render_template('/uploader.html',filename=filename)
  else:
    return render_template('/uploader.html')

@app.route('/results', methods=['POST'])
def results():
    return render_template('results.html', prediction=predicted_name, image=f'./static/uploads/'+filename)

if __name__ == '__main__':
  app.run()