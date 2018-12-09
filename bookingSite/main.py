from flask import Flask, render_template
from flask import request
import csv
import os
import datetime
from slide import Slide
import encryption

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))


@app.route('/')
def home():
    slides = loadSlides('home')
    return render_template('home.html', slides=slides)


@app.route('/attractions')
def attractions():
    slides = loadSlides('attractions')
    return render_template('attractions.html', slides=slides)


@app.route('/reviews')
def reviews():
    inList = readFile('static//reviews.csv')
    return render_template('reviews.html', inList=inList)


@app.route('/rentals')
def rentals():
    inList = readFileColumns('static//rentals.csv', [0, 1, 4])
    return render_template('rentals.html', inList=inList)


@app.route('/bookings')
def bookings():
    return render_template('bookings.html')


@app.route('/admin')
def admin():
    inList = readFile('static//rentals.csv')
    return render_template('admin.html', inList=inList)


def readFile(filePath):
    with open(filePath, 'r') as inFile:
        reader = csv.reader(inFile)
        inList = [row for row in reader]
    return inList


def readFileColumns(filePath, inclColumns):
    with open(filePath, 'r') as inFile:
        reader = csv.reader(inFile)
        inList = []
        for row in reader:
            inList.append(list(row[i] for i in inclColumns))
    return inList


def appendFile(aList, filePath):
    # https://www.guru99.com/reading-and-writing-files-in-python.html
    with open(filePath, 'a') as outFile:
        writer = csv.writer(outFile)
        writer.writerows(aList)
    return


def writeFile(aList, filePath):
    with open(filePath, 'w', newline="") as outFile:
        writer = csv.writer(outFile)
        writer.writerows(aList)
    return


@app.route('/addAdmin', methods=['POST'])
def addAdmin(verification):
    inList = readFile('static\\accounts.csv')
    # if verification == "admin1": #in later iterations, use a fully padded verification system (for example hashing and with a ver code)
    #    inList = readFile('static\\accounts.csv')
    return render_template('admin.html', inList=inList)


@app.route('/addReview', methods=['POST'])
def addReview():
    reviewFile = 'static\\reviews.csv'

    name = request.form['name']
    date = datetime.datetime.today().strftime('%d-%m-%Y')
    rating = request.form['rating']
    comment = request.form['comment']

    appendFile([[name, date, rating, comment]], reviewFile)
    inList = readFile(reviewFile)

    return render_template('reviews.html', inList=inList)


@app.route('/addContact', methods=['POST'])
def addContact():
    contactFile = 'static\\contacts.csv'

    contact = request.form['contact']
    number = request.form['number']
    appendFile([[contact, number]], contactFile)

    inList = readFile(contactFile)

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

    appendFile([[sdate, edate, name, email, confirmed]], bookingFile)
    
    inList = readFileColumns('static\\rentals.csv', [0, 1, 4])
    return render_template('rentals.html', inList=inList)


@app.route('/confirmBooking', methods=['POST'])
def confirmBooking():
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
    writeFile(inList, bookingFile)
    return render_template('admin.html', inList=inList)


def loadSlides(pageName):
    sList = []
    tempList = readFile('static\\' + pageName + '.csv')
    for i in tempList:
        sList.append(Slide('../static/images/' + pageName +
                           '/' + i[0], i[1], i[2], i[3]))
    return sList


if __name__ == '__main__':
    app.run(debug=True)
