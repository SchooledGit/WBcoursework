from flask import Flask, render_template
from flask import request
import csv
import datetime
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/attractions')
def attractions():
	return render_template('attactions.html')
		
@app.route('/reviews')
def reviews():
	inList = readFile('static\\reviews.csv')
	return render_template('reviews.html',inList = inList)

def readFile(aFile):
	with open(aFile,'r') as inFile:
		reader = csv.reader(inFile)
		inList = [row for row in reader]
	return inList

def writeFile(aList,aFile):
	with open(aFile,'w',newline="") as outFile:
		writer = csv.writer(outFile)
		writer.writerows(aList)
	return

@app.route('/addReview', methods = ['POST'])
def addReview():
    reviewFile = 'static\\reviews.csv'
    inList = readFile(reviewFile)
	
    name = request.form['name']
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    rating = request.form['rating']
    comment = request.form['comment']
    newReview = [name,date,rating,comment]
    inList.append(newReview)
    
    writeFile(inList,reviewFile)
    return render_template('reviews.html',inList = inList)

@app.route('/addContact',methods = ['POST'])
def addContact():
	contactFile = 'static\\contacts.csv'
	skillList = readFile(contactFile)
	
	contact = request.form['contact']
	number = request.form['number']
	
	newContact = [contact, number]
	skillList.append(newContact)
	
	writeFile(skillList,contactFile)
	return render_template('contacts.html',skillList = skillList)



if __name__ == '__main__':
	app.run(debug=True)