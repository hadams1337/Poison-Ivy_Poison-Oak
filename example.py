from flask import Flask


app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
  return 'Hello, World!'

@app.route('/')
def home():
  return render_template('home.html')





if __name__ == '__main__':
  app.run()