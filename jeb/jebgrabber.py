#!/bin/python

# jeb grabber
# it grabs jebs emails
# whats it to ya
# 
# beepz paulz 


from html2text import html2text
import httplib, urllib, json




def getEmails():
    jebme = httplib.HTTPConnection("www.jebbushemails.com")
    params = urllib.urlencode({'year':'2001','month':'01','day':'02','locale':'en-us'})
    headers = {"Content-Type": "application/x-www-form-urlencoded", 
               "Accept": "application/json"}
    jebme.request("POST", "/api/email.py/", params, headers )
    response = jebme.getresponse()
    data = json.loads(response.read())
    json.dumps(data, sort_keys=True, indent=4)
    return data


