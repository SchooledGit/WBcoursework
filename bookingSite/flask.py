from flask import Flask, render_template
from flask import request
import csv
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/attractions')
def attractions():
	return render_template('attactions.html')
		
@app.route('/rental')
def rental():
	return render_template('rental.html')

@app.route('/reviews')
def reviews():
	return render_template('reviews.html')


if __name__ == '__main__':
	app.run(debug=True)
