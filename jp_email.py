# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-10-04 09:03:24.076000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.1
# Newpy ID: 159
# Description: Any easy way to send email in script.

import requests
import unittest

g_email_proxy="http://sendemail.duapp.com/"
#g_email_proxy="http://localhost:8000"

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
  def attach(self,a_filename,a_file):
    self.m_attach[a_filename]=a_file
    return self
  def send(self):
    if not (self.m_subject and self.m_body and self.m_to):
      return False
    l_data={'subject':self.m_subject,
        'message':self.m_body,
        'to':self.m_to}
    l_files={}
    for i in range(len(self.m_attach)):
      l_files['file'+str(i)]=(self.m_attach.keys()[i],self.m_attach.values()[i])
    try:
      l_res=requests.post(g_email_proxy,data=l_data,files=l_files)
      if l_res.text =='ok':
        return True
      else:
        return False
    except Exception,e:
      print e
      return False
    
class _UT(unittest.TestCase):
  def test_quickway(self):
    l_ret = Email('test','this is a test!','jackandking@gmail.com').send()
    self.failUnless(l_ret)
  def test_two_recver(self):
    l_ret = Email('test two receivers','this is a test!','jackandking@gmail.com,jackandking@sina.cn').send()
  def test_one_attach(self):
    l_ret = Email('test with attachment','this is a test with one attachment!','jackandking@gmail.com').attach('test.py',open('jp_email.py','rb')).send()
    self.failUnless(l_ret)
  def test_two_attach(self):
    l_ret = Email('test with two attachment','this is a test with one attachment!','jackandking@gmail.com').attach('test.py',open('jp_email.py','rb')).attach('APP_usecase.jpg',open('APP_usecase.jpg','rb')).send()
    self.failUnless(l_ret)

def main():
  unittest.main(verbosity=3)

if __name__ == '__main__':
  main()
