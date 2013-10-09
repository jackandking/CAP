# -*- coding: utf-8 -*-
# Author: jiu.chen@thomsonreuters.com
# DateTime: 2013-09-26 13:10:20.602000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.1
# Newpy ID: 146
# Description: I'm a lazy person, so you have to figure out the function of this script by yourself.

import unittest
import subprocess
import os
import storage
from datetime import date
import logging
logging.basicConfig(level=logging.DEBUG)

class FooTest(unittest.TestCase):
	"""docstring for FooTest"""
	# def __init__(self, arg):
	# 	super(FooTest, self).__init__()
	# 	self.arg = arg

	def testFoo(self):
		gen = CCSReportGenerator()
		result = gen.callPerlScript()
		print result

def main():
	unittest.main()

if __name__ == '__main__':
	main()

class CCSReportGenerator():
	"""docstring for CCSReportGenerator"""

	def callPerlScript(self):
		subprocess.call(["perl", "_2_gen_report_GQS.pl"])
		subprocess.call(["perl", "_3_gen_report_ALL.pl"])
		subprocess.call(["perl", "_4_gen_graph_month.pl"])
		subprocess.call(["perl", "_4_gen_graph_week.pl"])
	
	def save(self):
		strDate = date.today().strftime("%Y-%m-%d")
		reportAllFilename = "WeeklySummary_" + strDate + "_ALL.htm"
		reportGqsFilename = "WeeklySummary_" + strDate + "_ALL.htm"
		grapthMonthCsvFilename = "all_hist_graph_month.csv"
		graphWeekCsvFilename = "all_hist_graph.csv"
		savedGraphMonthFilename = "Grath_Month_" + strDate + ".csv"
		savedGraphWeekFilename = "Grath_Week_" + strDate + ".csv"

		srcFile = open(reportAllFilename)
		reportAllContent = srcFile.read()
		srcFile.close()

		srcFile = open(reportGqsFilename)
		reportGqsContent = srcFile.read()
		srcFile.close()

		srcFile = open(grapthMonthCsvFilename)
		graphMonthCsvContent = srcFile.read()
		srcFile.close()

		srcFile = open(graphWeekCsvFilename)
		graphWeekCsvContent = srcFile.read()
		srcFile.close()

		l_store = storage.storage()
		l_store.write({'filename':reportAllFilename,'content':reportAllContent})
		l_store.write({'filename':reportGqsFilename,'content':reportGqsContent})
		l_store.write({'filename':savedGraphMonthFilename,'content':graphMonthCsvContent})
		l_store.write({'filename':savedGraphWeekFilename,'content':graphWeekCsvContent})
		logging.debug("report save done.")
