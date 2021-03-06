#!/bin/python

# jeb grabber
# it grabs jebs emails
# whats it to ya
# 
# beepz paulz 


import httplib, urllib, json, re
from datetime import date, timedelta
from pymongo import MongoClient

"""
 workflow here:
 getEmails(date) - give me a date, I return data to you
 some sort of data function
 some sort of file structure
 some sort of put me in the mongodb thing

 i created a mongodb instance with a database jebgrabber
 and collection emails..

"""
client = MongoClient()
db = client.jebgrabber
regex = re.compile("\\n-----Original Message-----\\n")

def insertEmail(data):
    db.emails.insert(data)

def parseEmail(text):
    result = regex.split(text)
    return result[0]
    
"""
Need to catch when there is no data in this function, and alert the range
"""    
def getEmails(_date):
    jebme = httplib.HTTPConnection("www.jebbushemails.com")
    params = urllib.urlencode({'year':_date.strftime('%Y'),
                               'month':_date.strftime('%m'),
                               'day':_date.strftime('%d'),
                               'locale':'en-us'})
    headers = {"Content-Type": "application/x-www-form-urlencoded", 
               "Accept": "application/json"}
    jebme.request("POST", "/api/email.py/", params, headers )
    response = jebme.getresponse()
    data = json.loads(response.read())
    json.dumps(data, sort_keys=True, indent=4)
    return data

"""
ex. x = date(2001, 01, 01)
    y = date(2001, 01, 07)
    d = jebgrabber.getEmailsRange(x, y)

    d = { 'year-month-day' : [ email, email, email ], ... }
"""
def getEmailsRange(start_date, end_date):
    data = {}
    for _date in daterange(start_date, end_date):
        data[_date.strftime("%Y-%m-%d")] = getEmails(_date)['emails']
    return data

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def postEmails(days):
    for day in days:
        for email in day:
            insertEmail(email)
    return True

def grabAndPost(start_date, end_date):
    for _date in daterange(start_date, end_date):
        print _date.strftime("%Y-%m-%d")
        emails = getEmails(_date)['emails']
        for email in emails:
            email['message'] = parseEmail(email['message'])
            insertEmail(email)
