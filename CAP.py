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
import logging
from apscheduler.scheduler import Scheduler
from time import time
import CAP_TicketsReport


sched = Scheduler()
@sched.cron_schedule(day_of_week=4,hour=6,minute=0)
def run_TicketsReport():
	report=CAP_TicketsReport.CAP_TicketsReport()
	report.run()


class CAP_UT(unittest.TestCase):

    def testOne(self):

      sched = Scheduler()

      #@sched.interval_schedule(seconds=10)
      @sched.cron_schedule(day_of_week=0,hour=5,minute=30)
      def testSched():
	      print "job invoked!"
        

      config = {'apscheduler.standalone': True}
      sched.configure(config)
      sched.start()
def main():
	config = {'apscheduler.standalone': True}
	sched.configure(config)
	sched.start()
    #unittest.main()

if __name__ == '__main__':
  logging.warning("please make sure http_proxy is not set")
  main()


