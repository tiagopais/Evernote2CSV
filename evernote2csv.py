# coding=utf-8
import codecs
import os
import xml.dom.minidom
import datetime

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getDateFromTextDate(nodelist):
    dateAsText = getText(nodelist)

    return datetime.datetime.strptime(dateAsText, "%Y%m%dT%H%M%SZ")

def getValueFromTitle(title) :

    if '-' in title :
        return title.split('-')[0].strip()

    return '0'

def getDescriptionFromTitle(title) :
    if '-' in title :
        return title.split('-')[1].strip()

    return title

def getPaymentViaFromTags(tags):

    isCreditCard = False
    isCash = False
    for tag in tags :
        isCreditCard = isCreditCard or (getText(tag.childNodes) == 'creditcard')
        isCash = isCash or (getText(tag.childNodes) == 'cash')

    if isCreditCard and isCash :
        return 'WTF! Multiple Payments...'

    if isCreditCard :
        return 'Credit Card'

    if isCash :
        return 'Cash'
    
    return 'unknown'

def printExpenseLine(evernoteCSVFile, created, description, value, via):
    evernoteCSVFile.write(created.date().isoformat() + ', ' + value + ', ' + via + ', ' + description + '\n')

def getExpenseFromNote(expenseAsNote, evernoteCSVFile):
    created = getDateFromTextDate(expenseAsNote.getElementsByTagName("created")[0].childNodes)
    title = getText(expenseAsNote.getElementsByTagName("title")[0].childNodes)
    value = getValueFromTitle(title)
    description = getDescriptionFromTitle(title)
    tags = expenseAsNote.getElementsByTagName("tag")
    via = getPaymentViaFromTags(tags)

    printExpenseLine(evernoteCSVFile, created, description, value, via)

def printHeaders(evernoteCSVFile):
    evernoteCSVFile.write('When, How Much, Via, Why\n')

def handlesNotes(evernotedom, evernoteCSVFile):
    expensesAsNotes = evernotedom.getElementsByTagName("note")

    printHeaders(evernoteCSVFile)
    for expenseAsNote in expensesAsNotes :
        getExpenseFromNote(expenseAsNote, evernoteCSVFile)

evernoteXMLFilePath = '/users/tiagopais/Desktop/spreaddusexpenses.enex'
evernoteDOM = xml.dom.minidom.parse(evernoteXMLFilePath)

basename = os.path.splitext(evernoteXMLFilePath)[0]
evernoteCSVFile = codecs.open(os.path.splitext(basename)[0]+ '.csv', 'w', "utf-8" )
handlesNotes(evernoteDOM, evernoteCSVFile)

evernoteCSVFile.close()