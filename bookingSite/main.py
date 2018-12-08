from flask import Flask, render_template
from flask import request
import csv
import os
import datetime
from slide import Slide

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def home():
    slides = loadSlides('home')
    return render_template('home.html',slides=slides)
@app.route('/attractions')
def attractions():
    slides = loadSlides('attractions')
    return render_template('attractions.html',slides=slides)
@app.route('/reviews')
def reviews():
    inList = readFile('static//reviews.csv')
    return render_template('reviews.html',inList=inList)
@app.route('/rentals')
def rentals():
    inList = readWithoutColumnsFile('static//rentals.csv',[0, 1, 4])
    return render_template('rentals.html',inList=inList)
@app.route('/bookings')
def bookings():
    return render_template('bookings.html')

def readFile(aFile):
    with open(aFile, 'r') as inFile:
        reader = csv.reader(inFile)
        inList = [row for row in reader]
    return inList
    
def readWithoutColumnsFile(aFile, inclColumns):
    with open(aFile, 'r') as inFile:
        reader = csv.reader(inFile)
        inList = []
        for row in reader:
            inList.append(list(row[i] for i in inclColumns))
    return inList
    
def writeFile(aList, aFile):
    with open(aFile, 'w', newline="") as outFile:
        writer = csv.writer(outFile)
        writer.writerows(aList)
    return
@app.route('/addReview', methods=['POST'])
def addReview():
    reviewFile = 'static\\reviews.csv'
    inList = readFile(reviewFile)

    name = request.form['name']
    date = datetime.datetime.today().strftime('%d-%m-%Y')
    rating = request.form['rating']
    comment = request.form['comment']
    newReview = [name, date, rating, comment]
    inList.append(newReview)

    writeFile(inList, reviewFile)
    return render_template('reviews.html', inList=inList)
@app.route('/addContact', methods=['POST'])
def addContact():
    contactFile = 'static\\contacts.csv'
    inList = readFile(contactFile)

    contact = request.form['contact']
    number = request.form['number']

    newContact = [contact, number]
    inList.append(newContact)

    writeFile(inList, contactFile)
    return render_template('contacts.html', inList=inList)

@app.route('/addBooking', methods=['POST'])
def addBooking():
    bookingFile = 'static\\rentals.csv'
    inList = readFile(bookingFile)

    sdate = request.form['sdate']
    edate = request.form['edate']
    name = request.form['name']
    email = request.form['email']
    confirmed = "false"

    newBooking = [sdate, edate, name, email, confirmed]
    inList.append(newBooking)

    writeFile(inList, bookingFile)
    inList = readWithoutColumnsFile('static\\rentals.csv', [0, 1, 4])
    return render_template('rentals.html', inList=inList)
    
@app.route('/checkLogin',methods=['POST'])
def checkLogin():
    accountFile = 'static\\accounts.csv'
    inList = readFile(accountFile)
    enterName = request.form['user']
    enterPass = request.form['pass']
    for i in range(len(inList)):
        if inList[i][0] == enterName and inList[i][1] == enterPass:
            inList = readFile('static//rentals.csv')
            return render_template('admin.html',inList = inList)
    slides = loadSlides('home')
    return render_template('home.html',slides=slides)

@app.route('/editAdmin',methods=['POST'])
def editAdmin():
    bookingFile = 'static\\rentals.csv'
    inList = readFile(bookingFile)
    index = request.form['choice']
    index = int(index) - 1
    confirmed = inList[index][4]
    if confirmed == "false":
        confirmed = "true"
    else:
        confirmed = "false"
    inList[index][4] = confirmed
    writeFile(inList,bookingFile)
    return render_template('admin.html', inList = inList)

# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
def loadSlides(pageName):
    # https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
    sList = []
    tempList = readFile('static\\' + pageName + '.csv')
    for i in tempList:
        sList.append(Slide('../static/images/' + pageName + '/' + i[0], i[1], i[2], i[3]))
    return sList

if __name__ == '__main__':
    app.run(debug=True)
