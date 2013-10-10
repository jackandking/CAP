# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-09-23 13:10:20.602000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.1
# Newpy ID: 146
# Description: I'm a lazy person, so you have to figure out the function of this script by yourself.

import storage
import urllib, urllib2, cookielib
import logging
logging.basicConfig(level=logging.DEBUG)
import socket
socket.setdefaulttimeout(30)

g_rt_username = 'yingjie.liu'
g_rt_password = 'password'

class RTFetcher():
  def login(self):
    l_cj = cookielib.CookieJar()
    l_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(l_cj))
    l_login_data = urllib.urlencode({'user' : g_rt_username, 'pass' : g_rt_password})
    l_opener.open('http://collectionscoresupport.ime.reuters.com/rt', l_login_data)
    self.m_opener=l_opener
    logging.debug("login done.")

  def fetch(self,a_from='2013-10-01',a_to='2013-11-01'):
    l_resp = self.m_opener.open("http://collectionscoresupport.ime.reuters.com/rt/Search/Results.tsv?Format=%27%20%20%20%3Cb%3E%3Ca%20href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__id__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3A%23%27%2C%0A%27%3Cb%3E%3Ca%20href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__Subject__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3ASubject%27%2C%0A%27__Status__%27%2C%0A%27__QueueName__%27%2C%0A%27__OwnerName__%27%2C%0A%27__Priority__%27%2C%0A%27__NEWLINE__%27%2C%0A%27%27%2C%0A%27%3Csmall%3E__Requestors__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__CreatedRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__ToldRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__LastUpdatedRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__TimeLeft__%3C%2Fsmall%3E%27&Order=ASC%7CASC%7CASC%7CASC&OrderBy=id%7C%7C%7C&Page=1&Query=Created%20%3C%20%27"+a_to+"%27%20AND%20Created%20%3E%20%27"+a_from+"%27&Rows=50")
    self.m_content=l_resp.read()
    logging.debug("fetch done.")

  def save(self, a_filename):
    l_store = storage.storage()
    l_store.write({'filename':a_filename,'content':self.m_content})
    logging.debug("save done.")

if __name__ == '__main__':
  l_f=RTFetcher()
  l_f.login()
