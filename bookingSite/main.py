from flask import Flask, render_template
from flask import request
import csv
import os
from slide import Slide

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))

#https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
def loadSlides(pageName):
	#https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
	filepath = dir_path + '\\static\\' + pageName + '.csv'
	sList = []
	with open(filepath, 'r') as inFile:
		reader = csv.reader(inFile)
		aList = list(reader)
		for i in aList:
			sList.append(Slide('../static/images/' + pageName + '/' + i[0], i[1], i[2], i[3]))
	return sList

@app.route('/')
def home():
	slides = loadSlides('home')
	return render_template('home.html', slides = slides)

@app.route('/attractions')
def attractions():
	slides = loadSlides('attractions')
	return render_template('attractions.html', slides = slides)

@app.route('/rental')
def rental():
	return render_template('rental.html')

@app.route('/reviews')
def reviews():
	return render_template('reviews.html')

if __name__ == '__main__':
	app.run(debug = True)
