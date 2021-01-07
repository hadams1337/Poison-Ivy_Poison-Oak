from flask import Flask, render_template, url_for, request
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from flask import request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello():
  return 'Hello, World!'

@app.route('/')
def home():
  region_options = ['East', 'South', 'Midwest', 'West', 'Pacific Coast', 'Desert']
  season_options = ['Spring', 'Summer', 'Fall', 'Winter']
  return render_template('home.html', region_options=region_options, season_options=season_options)



@app.route('/pictures', methods=['POST', "GET"])
def graphs():
    region = request.form['region']
    season = request.form['season']

    return render_template('pictures.html', season_id=season_id, region_id=region_id, url=f'./static/images/region{region_id}season{season_id}.png', image=image)

@app.route('/uploader', methods=['POST', 'GET'])
def upload_image():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("uploader.html")

@app.route('/results', methods=['POST', 'GET'])
def results():
    test_data = upload_image()

    # Load model
    filename = 'mymodel_43/'
    model = tf.keras.models.load_model('models/filename')

    # Predict on user input
    prediction = np.argmax(model.predict(test_data))

    target_names=['Benign Plants', 'Poison Ivy', 'Poison Oak']

    # Index target names at prediction value
    for name in target_names[prediction]:
        predicted_name = name

    return render_template('predict.html', prediction=predicted_name, image=f'./static/images/iris.png')



if __name__ == '__main__':
  app.run()