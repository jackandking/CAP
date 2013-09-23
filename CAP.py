# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-09-21 11:59:07.975000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.0
# Newpy ID: 145
# Description: This is the main entry to CCT Audit Platform


import unittest
from RTFetcher import RTFetcher 
import logging

class CAP_UT(unittest.TestCase):

    def testOne(self):
      l_f=RTFetcher()
      l_f.login()
      l_f.fetch()
      l_f.save()


def main():
    unittest.main()

if __name__ == '__main__':
  logging.warning("please make sure http_proxy is not set")
  main()


