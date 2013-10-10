# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-10-04 09:03:24.076000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.1
# Newpy ID: 159
# Description: Any easy way to send email in script.

import requests
import unittest

#g_email_proxy="http://sendemail.duapp.com/"
#g_email_proxy="http://localhost:8000"
#g_email_proxy="http://localhost:8080/sendemail"
g_email_proxy="http://jpauto.sinaapp.com/sendemail"

class Email:
  '''Email proxy
  '''
  _ext_to_disposition = {
        'bmp':  'I', 'css':  'A',
        'csv':  'A', 'gif':  'I',
        'htm':  'I', 'html': 'I',
        'jpeg': 'I', 'jpg':  'I',
        'jpe':  'I', 'pdf':  'A',
        'png':  'I', 'rss':  'I',
        'text': 'A', 'txt':  'A',
        'asc':  'A', 'diff': 'A',
        'pot':  'A', 'tiff': 'A',
        'tif':  'A', 'wbmp': 'I',
        'ics':  'I', 'vcf':  'I'
    } 
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
    ext = a_filename.split('.')[-1]

    disposition = self._ext_to_disposition.get(ext)
    if not disposition:
      raise Exception("InvalidAttachmentTypeError: "+str(ext))
    self.m_attach[a_filename]=a_file
    return self
  def send(self,a_server=None,a_port=None,a_from=None,a_pswd=None):
    if not (self.m_subject and self.m_body and self.m_to):
      return False
    l_data={'subject':self.m_subject,
        'message':self.m_body,
        'to':self.m_to}
    if a_server:
      l_data['server']=a_server
    if a_port:
      l_data['port']=a_port
    if a_from:
      l_data['from']=a_from
    if a_pswd:
      l_data['pswd']=a_pswd
    l_files={}
    for i in range(len(self.m_attach)):
      l_files['file'+str(i)]=(self.m_attach.keys()[i],self.m_attach.values()[i])
    try:
      l_res=requests.post(g_email_proxy,data=l_data,files=l_files,proxies={"http":"http://10.40.14.34:80"})
      if l_res.text =='ok':
        return True
      else:
        return False
    except Exception,e:
      print e
      return False
    
class _UT(unittest.TestCase):
  def test_1632TR(self):
    l_ret = Email('test 163 to TR','this is a test!','yingjie.liu@thomsonreuters.com').send()
    self.failUnless(l_ret)

  def test_mandrill(self):
    l_ret = Email('test mandrill to TR','this is a test!','yingjie.liu@thomsonreuters.com').send(a_server='smtp.mandrillapp.com',a_from='jackandking@gmail.com',a_pswd='ansxkLz0lOWK6eGcu0bRmA')
    self.failUnless(l_ret)

  def test_quickway(self):
    l_ret = Email('test','this is a test!','cctauditplatform@sina.com').send()
    self.failUnless(l_ret)

  def test_sina2sina(self):
    l_ret = Email('test','this is a test sina to sina!','cctauditplatform@sina.com').send(a_server='smtp.sina.com',a_from='cctauditplatform@sina.com')
    self.failUnless(l_ret)

  def test_sina2TR(self):
    l_ret = Email('test','this is a test sina.cn to sina.com!','cctauditplatform@sina.com').send(a_server='smtp.sina.com',a_from='cctauditplatform@sina.com')
    self.failUnless(l_ret)

  def test_sina2163(self):
    l_ret = Email('test','this is a test sina to 163!','cctauditplatform@163.com').send(a_server='smtp.sina.com',a_from='cctauditplatform@sina.com')
    self.failUnless(l_ret)

  def test_1632sina(self):
    l_ret = Email('test','this is a test 163 to sina!','cctauditplatform@sina.com').send(a_server='smtp.163.com',a_from='cctauditplatform@163.com',a_pswd='6sigma')
    self.failUnless(l_ret)

  def test_two_recver(self):
    l_ret = Email('test two receivers','this is a test!','jackandking@gmail.com,jackandking@sina.cn').send()
    self.failUnless(l_ret)

  def test_one_attach(self):
    l_ret = Email('test with one attachment','this is a test with one attachment!','cctauditplatform@sina.com').attach('test.txt',open('jp_email.py','rb')).send()
    self.failUnless(l_ret)

  def test_two_attach(self):
    l_ret = Email('test with two attachment','this is a test with two attachments!','cctauditplatform@sina.com').attach('test.txt',open('jp_email.py','rb')).attach('APP_usecase.jpg',open('APP_usecase.jpg','rb')).send()
    self.failUnless(l_ret)

def main():
  unittest.main(verbosity=3)

if __name__ == '__main__':
  main()
