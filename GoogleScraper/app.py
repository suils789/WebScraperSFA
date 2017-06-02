from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)


data = '1'


@app.route('/')
def index():
	return render_template('index.html', data = data)

@app.route('/hello/')
def hello():
	return 'hello'