from flask import Flask
from database import Database

app = Flask(__name__)


@app.route('/')
def hello_func():
    
    data = Database.select_all('users')
    return data[2]['username']


if __name__ == '__main__':
	app.run()