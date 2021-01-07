from flask import Flask, render_template, url_for, request
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from flask import request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
  return 'Hello, World!'

@app.route('/')
def home():
  region_options = ['East', 'South', 'Midwest', 'West', 'Pacific Coast', 'Desert']
  season_options = ['Spring', 'Summer', 'Fall', 'Winter']
  return render_template('home.html', region_options=region_options, season_options=season_options)



@app.route('/', methods=['POST', "GET"])
def graphs():
    region = int(request.form['region']) - 1
    season = int(request.form['season']) - 1

      return render_template('home.html', col1=col1+1, col2=col2+1, url=f'./static/images/col{col1}col{col2}.png', image=image)

@app.route('/predict', methods=['POST', 'GET'])

def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            print(image)

            return redirect(request.url)


    return render_template("public/upload_image.html")


def results():
    test_data = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1, -1)

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