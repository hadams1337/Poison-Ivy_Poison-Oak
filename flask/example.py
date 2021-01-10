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
  region_options = ['east', 'south', 'midwest', 'west', 'pacific', 'desert']
  season_options = ['spring', 'summer', 'fall', 'winter']
  return render_template('home.html', region_options=region_options, season_options=season_options)


@app.route('/pictures', methods=['POST','GET'])
def pictures():
    region_id = request.form['region']
    season_id = request.form['season']
    picture=os.listdir('./static/'+season_id+'/'+region_id)[1]
    return render_template('pictures.html', season_id=season_id, region_id=region_id, url=f'./static/{season_id}/{region_id}/{picture}')

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
        img = keras.preprocessing.image.load_img('static/uploads/'+filename , target_size=(300, 200))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        # Load model
        model = tf.keras.models.load_model('models/')
        # Predict on user input
        #return f"{model.predict(np.array(test_data).reshape(1,300,200,3)).flatten()}"
        prediction = model.predict(img_array)
        score = np.round(np.max(tf.nn.softmax(prediction[0]))*100)
        target_names=['Benign Plants', 'Poison Ivy', 'Poison Oak']

        # Index target names at prediction values
        predicted_name = target_names[np.argmax(prediction[0])]
        return results(predicted_name, filename, score)
        #return render_template('/results.html', prediction=predicted_name, score=score)
  else:
    return render_template('/uploader.html')

#@app.route('/results', methods=['POST'])
def results(predicted_name, filename, score):
    return render_template('results.html', prediction=predicted_name, image=f'./static/uploads/'+filename, score=score)

if __name__ == '__main__':
  app.run()