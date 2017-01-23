from flask import Flask, render_template, request
from database import Database

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('main.html')

@app.route('/add')
def got_to_add():
	return render_template('add_issue.html')

@app.route('login')
def login():
	return render_template('login.html')

	
if __name__ == '__main__':
	app.run()