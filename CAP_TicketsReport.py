import unittest
from RTFetcher import RTFetcher 
from ConvertRawData import *
from CCSReportGenerator import SupportTicketsReportGenerator
import logging
from time import time

class CAP_TicketsReport():
    """docstring for CAP_TicketsReport"""
    def run(self):
        l_f=RTFetcher()
        l_f.login()
        l_f.fetch(a_from='2013-10-20')
        l_f.savetofile()

        l_c=RawDateConverter()
        l_c.generate_local_file(get_date_with_offset(-7))
        logging.debug("file process done")

        l_g = SupportTicketsReportGenerator()
        l_g.run()

class UT(unittest.TestCase):
    """unit test of CAP_TicketsReport"""
    def testOne(self):
        l_fn="Results_"+ str(time()) +".csv"
        l_f=RTFetcher()
        l_f.login()
        l_f.fetch(a_from='2013-10-20')
        # l_f.save(l_fn)
        l_f.savetofile()

        l_c=RawDateConverter()
        # l_c.get_raw_data(l_fn)
        l_c.generate_local_file(get_date_with_offset(-7))
        logging.debug("file process done")

        l_g = SupportTicketsReportGenerator()
        l_g.run()

def main():
    report = CAP_TicketsReport()
    report.run()

if __name__ == '__main__':
    main()

