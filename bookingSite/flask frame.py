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
		
@app.route('/contacts')
def contacts():
	skillList = readFile('static\\contacts.csv')
	return render_template('contacts.html',skillList = skillList)

def readFile(aFile):
	with open(aFile,'r') as inFile:
		reader = csv.reader(inFile)
		skillList = [row for row in reader]
	return skillList

def writeFile(aList,aFile):
	with open(aFile,'w',newline="") as outFile:
		writer = csv.writer(outFile)
		writer.writerows(aList)
	return

@app.route('/addSkill', methods = ['POST'])
def addSkill():
	skillFile = 'static\\skills.csv'
	skillList = readFile(skillFile)
	
	skill = request.form['skill']
	rating = request.form['rating']
	
	newSkill = [skill,rating]
	skillList.append(newSkill)
	
	writeFile(skillList,skillFile)
	return render_template('skills.html',skillList = skillList)

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