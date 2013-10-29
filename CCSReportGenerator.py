# -*- coding: utf-8 -*-
# Author: jiu.chen@thomsonreuters.com
# DateTime: 2013-09-26 13:10:20.602000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 1.1
# Newpy ID: 146
# Description: I'm a lazy person, so you have to figure out the function of this script by yourself.

import os
import unittest
import subprocess
import logging
logging.basicConfig(level=logging.DEBUG)
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

from datetime import date,timedelta

import storage
from mail import *

class STRGTest(unittest.TestCase):
    """Test class of SupportTicketsReportGenerator (STRG)"""

    def testOne(self):
        gen = SupportTicketsReportGenerator()
        gen.genSystemGraph()
        gen.genRegionGraph()

    def testTwo(self):
        gen = SupportTicketsReportGenerator()
        gen.run()

    def testThree(self):
        gen = SupportTicketsReportGenerator()
        gen.genTicketsOverviewReport()

    def testMail(self):
        to=['jiu.chen@thomsonreuters.com']
        send_mail('yingjie.liu@thomsonreusters.com',to,'test', "This is a test")

if __name__ == '__main__':
    unittest.main()

class SupportTicketsReportGenerator():
    """Class of Support Tickets Report generator"""

    def callPerlScript(self):
        subprocess.call(["perl", "_2_gen_report_GQS.pl"])
        subprocess.call(["perl", "_3_gen_report_ALL.pl"])
        subprocess.call(["perl", "_4_gen_graph_month.pl"])
        subprocess.call(["perl", "_4_gen_graph_week.pl"])

    def autolabel(self, rects):
        for rect in rects:
            height = rect.get_height()
            if (height < 3):
                y = rect.get_y()-2
            elif (height <= 9):
                y = rect.get_y()
            else:
                y = 0.35*height + rect.get_y()
            plt.text(rect.get_x()+rect.get_width()/2., y, '%d'%int(height), ha='center', va='bottom')

    def drawBarPlot(self, x_ray, y_1, y_2, y_3, y_max, title, legend1, legend2, legend3, outputfile):
        plt.cla()
        ind = np.arange(len(x_ray))
        width = 0.35

        y_3_bottom = []
        for i in range(len(y_1)):
            y_3_bottom.append(y_1[i] + y_2[i])

        p1 = plt.bar(ind, y_1, width, color='r')
        p2 = plt.bar(ind, y_2, width, color='y', bottom=y_1)
        p3 = plt.bar(ind, y_3, width, color='g', bottom=y_3_bottom)

        self.autolabel(p1)
        self.autolabel(p2)
        self.autolabel(p3)

        plt.title(title + '\n')
        plt.xticks(ind+width/2., x_ray )
        plt.yticks(np.arange(0,y_max,20))
        plt.legend( (p1[0], p2[0], p3[0]), (legend1, legend2, legend3) )

        plt.grid(True)
        plt.savefig(outputfile)

    def genSystemPlot(self):
        """Tickets Per System"""
        r = mlab.csv2rec('all_hist_graph_month.csv')
        x_ray = []
        y_GQS = []
        y_RAQ = []
        y_SDD = []
        y_SDD_bottom = []

        ind = np.arange(len(r))
        for i in range(len(r)):
            if i%2==0:
                x_ray.append(r[i][0])
            else:
                x_ray.append("")
            y_GQS.append(r[i][3])
            y_RAQ.append(r[i][5])
            y_SDD_bottom.append(r[i][3]+r[i][5])
            y_SDD.append(r[i][7])

        self.drawBarPlot(x_ray, y_GQS, y_RAQ, y_SDD, 121, "Tickets Per System", 
            'GQS', 'RAQ/DCMLS/TQS', 'SDD', "tickets-per-system.png")

    def genRegionPlot(self):
        """Tickets Per Region"""
        r = mlab.csv2rec('all_hist_graph_month.csv')
        x_ray = []
        y_EMEA = []
        y_AMERS = []
        y_APAC = []

        ind = np.arange(len(r))
        for i in range(len(r)):
            if i%2==0:
                # x_ray.append(r[i][0].strftime("%Y-%m"))
                x_ray.append(r[i][0])
            else:
                x_ray.append("")
            y_EMEA.append(r[i][11])
            y_AMERS.append(r[i][13])
            y_APAC.append(r[i][15])

        self.drawBarPlot(x_ray, y_EMEA, y_AMERS, y_APAC, 121, "Tickets Per Region", 
            'EMEA', 'AMERS', 'APAC', "tickets-per-region.png")

    def genTicketsOverviewPlot(self):
        """"Total Tickets Overview"""
        r = mlab.csv2rec('all_hist_graph.csv')
        x_ray = []
        y_create_total = []
        y_close_total = []
        ind = range(len(r))
        for i in ind:
            if i % 8 == 0:
                x_ray.append(r[i][1].strftime('%m/%d/%y'))
            else:
                x_ray.append("")
            y_create_total.append(r[i][10])
            y_close_total.append(r[i][11])

        p1 = plt.plot(ind, y_create_total, 'bo-')
        p2 = plt.plot(ind, y_close_total, 'ro-')
        plt.axis([ind[0], ind[-1], 0, 3500])
        plt.xticks(ind, x_ray)

        plt.title('Total Tickets Overview\n')
        plt.legend( (p1[0], p2[0]), ('Create Total', 'Close Total'), loc=4 )
        plt.grid(True, axis='y')
        fig = plt.gcf()
        fig.set_figwidth(13)
        plt.savefig("total-tickets.png")

    def run(self):
        # run perl script to generate report file
        # save those report file to DB
        # process all_hist_graph.csv, all_hist_graph_month.csv to get graph
        # send email with html content and png file
        # clear all temporary file: *.htm, *.csv, *.png

        self.callPerlScript()
        self.genTicketsOverviewPlot()
        self.genSystemPlot()
        self.genRegionPlot()

        strDate = (date.today()-timedelta(days=7)).strftime("%Y-%m-%d")
        reportAllFilename = "WeeklySummary_" + strDate + "_ALL.htm"
        # reportAllFilename = "WeeklySummary_2013-10-17_ALL.htm"
        # reportGqsFilename = "WeeklySummary_" + strDate + "_GQS.htm"

        srcFile = open(reportAllFilename)
        reportAllContent = srcFile.read()
        srcFile.close()

        # srcFile = open(reportGqsFilename)
        # reportGqsContent = srcFile.read()
        # srcFile.close()

        attachmentList = ['tickets-per-system.png', 'tickets-per-region.png', 'total-tickets.png']
        to=['COLL-GLOBAL-TECH-CORE-EVA@thomsonreuters.com']
        send_mail('jiu.chen@thomsonreusters.com',to,'CCS Weekly Report',reportAllContent, attachmentList)
        # to=['jiu.chen@thomsonreuters.com', 'hongfeng.yao@thomsonreuters.com']
        # send_mail('yingjie.liu@thomsonreusters.com',to,'Support Tickets Report', reportAllContent, attachmentList)

class CCSReportGenerator():
  """docstring for CCSReportGenerator"""

  def publish(self):
    strDate = (date.today()-timedelta(days=7)).strftime("%Y-%m-%d")
    reportAllFilename = "WeeklySummary_" + strDate + "_ALL.htm"
    reportGqsFilename = "WeeklySummary_" + strDate + "_GQS.htm"
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


    #to=['chao.xie@thomsonreuters.com','yingjie.liu@thomsonreuters.com','liang.zhang1@thomsonreuters.com']
    to=['COLL-GLOBAL-TECH-CORE-EVA@thomsonreuters.com']
    #to=['sheng.chen@thomsonreuters.com','yingjie.liu@thomsonreuters.com','stephen.wang@thomsonreuters.com','abhilash.abraham@thomsonreuters.com','zhe.wang@thomsonreuters.com','francis.wang@thomsonreuters.com','jianping.zuo@thomsonreuters.com','cynthia.wang@thomsonreuters.com','stephen.li@thomsonreuters.com']
    send_mail('jiu.chen@thomsonreusters.com',to,'CCS Weekly Report',reportAllContent)

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

