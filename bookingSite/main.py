from flask import Flask, render_template
from flask import request
import csv
import os
import datetime
from slide import Slide

from encryption import *

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
    with open(filePath, 'a+', newline="") as outFile:
        writer = csv.writer(outFile)
        writer.writerows(aList)
    return


def writeFile(aList, filePath):
    with open(filePath, 'w', newline="") as outFile:
        writer = csv.writer(outFile)
        writer.writerows(aList)
    return

#https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string
def listToPlain(aList):
    output = ""
    for line in aList:
        output += ''.join(line)
        output += "\n"
    return output
    
    
@app.route('/addAdmin', methods=['POST'])
def addAdmin():
    accountFile = 'static\\accounts.csv'
    name = request.form['user']
    password = request.form['pass']
    verification = request.form['verification']
    isAdmin = False
    
    if checkVerification(verification): #in future, one may send one-time passes to email which are stored in a temporary csv
        salt=''
        hash=''
        salt = generateSalt(20) #even numbers
        hash = hashInput(password, salt)
        newAccount = [name, salt, hash]
        appendFile([newAccount], accountFile)
        inList = readFile('static\\rentals.csv')
        isAdmin = True
    slides = loadSlides('home')
    if isAdmin:
        return render_template('admin.html',inList = inList)
    else:
        return render_template('home.html',slides=slides)


def checkVerification(verification):
    return verification == 'admin1' #in future, one may send one-time passes to email which are stored in a temporary csv

@app.route('/verifyAdmin',methods=['POST'])
def verifyAdmin():
    accountFile = 'static\\accounts.csv'
    inList = readFile(accountFile)
    name = request.form['user']
    password = request.form['pass']
    isAdmin = False

    for i in range(len(inList)):
        if inList[i][0] == name and not isAdmin:
            if validate(password, inList[i][1], inList[i][2]): #compares hashes
                isAdmin = True
                inList = readFile('static//rentals.csv')
    slides = loadSlides('home')

    if isAdmin:
        return render_template('admin.html',inList = inList)
    else:
        return render_template('home.html',slides=slides)


@app.route('/addReview', methods=['POST'])
def addReview():
    reviewFile = 'static\\reviews.csv'

    name = request.form['name']
    date = datetime.datetime.today().strftime('%d-%m-%Y')
    rating = request.form['rating']
    comment = request.form['comment']
    newReview = [name, date, rating, comment]

    appendFile([newReview], reviewFile)
    inList = readFile(reviewFile)

    return render_template('reviews.html', inList=inList)
    
#https://stackoverflow.com/questions/29706239/python-check-if-two-tripsdates-overlap
def dateCheck(start1,end1,start2,end2):
    return (start1 <= start2 <= end1 or start1 <= end2 <= end1 or start2 <= start1 and end2 >= end1)
    
@app.route('/addBooking', methods=['POST'])
def addBooking():
    currentDate = datetime.datetime.today().strftime('%d-%m-%Y')

    bookingFile = 'static\\rentals.csv'
    inList = readFile(bookingFile)
    sdate = request.form['sdate']
    edate = request.form['edate']
    name = request.form['name']
    email = request.form['email']
    confirmed = "false"
    isOkay = False

    if dateCheck(currentDate,currentDate,sdate,edate):
        for line in inlist:
            if not isOkay and dateCheck(line[0],line[1],sdate,edate):
                newBooking = [sdate, edate, name, email, confirmed]
                appendFile([newBooking], bookingFile)
                isOkay = True

    inList = readFileColumns(bookingFile, [0, 1, 4])
    if isOkay:
        return render_template('rentals.html', inList=inList)
    else:
        return render_template('bookings.html')


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


# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
def loadSlides(pageName):
    # https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
    sList = []
    tempList = readFile('static\\' + pageName + '.csv')
    for i in tempList:
        imgPath = '../static/images/' + pageName + '/' + i[0]
        textPath = 'static\\text\\' + i[2]
        txt = ''
        if i[2] != "":
            txt = listToPlain(readFile(textPath))
        sList.append(Slide(imgPath, i[1], txt, i[3]))
    return sList


if __name__ == '__main__':
    app.run(debug=True)
