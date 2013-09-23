# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-09-21 20:45:24.719000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.0
# Newpy ID: 0
# Description: I'm a lazy person, so you have to figure out the function of this script by yourself.

import storage

## URLFetch and Exception Handling
import urllib, urllib2, cookielib

username = 'yingjie.liu'
password = 'password'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'user' : username, 'pass' : password})
opener.open('http://collectionscoresupport.ime.reuters.com/rt', login_data)
print "login done."

resp = opener.open("http://collectionscoresupport.ime.reuters.com/rt/Search/Results.tsv?Format=%27%20%20%20%3Cb%3E%3Ca%20href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__id__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3A%23%27%2C%0A%27%3Cb%3E%3Ca%20href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__Subject__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3ASubject%27%2C%0A%27__Status__%27%2C%0A%27__QueueName__%27%2C%0A%27__OwnerName__%27%2C%0A%27__Priority__%27%2C%0A%27__NEWLINE__%27%2C%0A%27%27%2C%0A%27%3Csmall%3E__Requestors__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__CreatedRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__ToldRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__LastUpdatedRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__TimeLeft__%3C%2Fsmall%3E%27&Order=ASC%7CASC%7CASC%7CASC&OrderBy=id%7C%7C%7C&Page=1&Query=Created%20%3C%20%272013-09-01%27%20AND%20Created%20%3E%20%272013-08-01%27&Rows=50")
#resp = opener.open("http://collectionscoresupport.ime.reuters.com/rt/Search/Results.tsv?Format=%27%20%20%20%3Cb%3E%3Ca%20href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__id__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3A%23%27%2C%0A%27%3Cb%3E%3Ca%20href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__Subject__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3ASubject%27%2C%0A%27__Status__%27%2C%0A%27__QueueName__%27%2C%0A%27__OwnerName__%27%2C%0A%27__NEWLINE__%27%2C%0A%27%27%2C%0A%27%3Csmall%3E__Requestors__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__CreatedRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__ToldRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__LastUpdatedRelative__%3C%2Fsmall%3E%27&Order=ASC%7CASC%7CASC%7CASC&OrderBy=id%7C%7C%7C&Page=1&Query=id%20%3E%200&Rows=50")
content=resp.read()
print content

l_store = storage.storage()
l_store.write({'filename':'Results.csv','content':content})

exit()

import urllib,urllib2,sys
from urllib2 import URLError, HTTPError
try:
    params = urllib.urlencode({'Order': 'ASC|ASC|ASC|ASC', 'OrderBy': 'id', 'Page': '1','Query':'Created < 2013-09-01 AND Created > 2013-08-01','Rows':'50'})
    response=urllib2.urlopen("http://collectionscoresupport.ime.reuters.com/rt/Search/Results.tsv")
    print response.read(); 
except HTTPError, e:
    print 'The server could not fulfill the request.'
    print 'Error code: ', e.code
except URLError, e:
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
except:
    print "Unexpected error:", sys.exc_info()[0]


