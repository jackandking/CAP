# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-10-04 09:03:24.076000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.1
# Newpy ID: 159
# Description: Any easy way to send email in script.

import urllib, urllib2
import unittest

#g_email_proxy="http://sendemail.duapp.com/"
g_email_proxy="http://localhost:8000"

class Email:
  def __init__(self,a_sub=None,a_body=None,a_to=None):
    self.m_subject=a_sub
    self.m_body=a_body
    self.m_to=a_to
    self.m_attach={}
  def subject(self,a_sub):
    self.m_subject=a_sub
    return self
  def body(self,a_body):
    self.m_body=a_body
    return self
  def to(self, a_to):
    if self.m_to:
      self.m_to=self.m_to+","+a_to
    else:
      self.m_to=a_to
    return self
  def attach(self,a_filename,a_content):
    self.m_attach[a_filename]=a_content
    return self
  def send(self):
    if not (self.m_subject and self.m_body and self.m_to):
      return False
    l_dict={'subject':self.m_subject,
        'message':self.m_body,
        'to':self.m_to}
    if len(self.m_attach) == 1:
      l_dict['filename']=self.m_attach.keys()[0]
      l_dict['content']=self.m_attach.values()[0]
    elif len(self.m_attach) == 2:
      l_dict['filename']=self.m_attach.keys()[0]
      l_dict['content']=self.m_attach.values()[0]
      l_dict['filename2']=self.m_attach.keys()[1]
      l_dict['content2']=self.m_attach.values()[1]
    try:
      l_params=urllib.urlencode(l_dict)
      l_res=urllib2.urlopen(g_email_proxy,l_params).read()
      if l_res=='ok':
        return True
      else:
        return False
    except:
      return False
    
class _UT(unittest.TestCase):
  def test_quickway(self):
    l_ret = Email('test','this is a test!','jackandking@gmail.com').send()
    self.failUnless(l_ret)
  def test_two_recver(self):
    l_ret = Email('test two receivers','this is a test!','jackandking@gmail.com,jackandking@sina.cn').send()
  def test_one_attach(self):
    l_ret = Email('test with attachment','this is a test with one attachment!','jackandking@gmail.com').attach('test.py',open('jp_email.py','rb').read()).send()
    self.failUnless(l_ret)
  def test_two_attach(self):
    l_ret = Email('test with two attachment','this is a test with one attachment!','jackandking@gmail.com').attach('test.py',open('jp_email.py','rb').read()).attach('APP_usecase.jpg',open('APP_usecase.jpg','rb').read()).send()
    self.failUnless(l_ret)

def main():
  unittest.main(verbosity=3)

if __name__ == '__main__':
  main()
