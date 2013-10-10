# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-09-21 11:59:07.975000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.0
# Newpy ID: 145
# Description: This is the main entry to CCT Audit Platform
# Change History:
# 2013-10-07 1:01:16 PM Integrate ConvertRawData


import unittest
from RTFetcher import RTFetcher 
from ConvertRawData import *
from CCSReportGenerator import CCSReportGenerator
import logging

class CAP_UT(unittest.TestCase):

    def testOne(self):
      l_f=RTFetcher()
      l_f.login()
      l_f.fetch()
      l_fn="Results1.csv"
      l_f.save(l_fn)

      l_c=RawDateConverter()
      l_c.get_raw_data(l_fn)
      l_c.generate_local_file(get_date_with_offset(-7))

      l_g=CCSReportGenerator()
      l_g.callPerlScript()
      #l_g.save()
      l_g.publish()
    def test2(self):
      l_c=RawDateConverter()
      l_c.get_raw_data()
      l_c.generate_local_file(get_date_with_offset(-7))

      l_g=CCSReportGenerator()
      l_g.callPerlScript()
      l_g.save()

def main():
    unittest.main()

if __name__ == '__main__':
  logging.warning("please make sure http_proxy is not set")
  main()


