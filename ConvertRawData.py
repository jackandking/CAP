# -*- coding: utf-8 -*-
# Author: Hongfeng.Yao@thomsonreuters.com
# DateTime: 2013-09-26 16:06:10.517000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 0.8
# Newpy ID: 0
# Description:
# This is used to convert search result downloaded from RT server
# Input:   Results.xls
# Output:  responds.csv and all_hist.csv 


import csv 
import datetime
import time
import storage

#get date n_days before or after oneday
def get_date_with_offset(n_days,in_date=str(datetime.date.today())[:10]):
    begin_date = in_date.split("-")
    begin_date = [int(num) for num in begin_date]
    return str(datetime.datetime(begin_date[0],begin_date[1],begin_date[2]) + datetime.timedelta(days=n_days))[:10]
    
class RawDateConverter():
    def get_raw_data(self,a_filename):
        l_store = storage.storage()
        self.m_content = l_store.read({'filename':a_filename})
        ofile=open("results.xls","wb")
        ofile.write(self.m_content[0]['content'].encode('cp1252'))
        ofile.close()
        
    def save(self):
        l_store = storage.storage()
        l_store.write({'filename':'all_hist.csv ','content':self.m_content})
        #TODO

        
    def generate_local_file(self, from_date_str=""):
        # write first line of each output file
        # responds.csv
        response_csv_head = ["id", "Subject", "CF-System Type", "CF-Region", "Status", "Priority", "Owner", "Created", "Resolved",  "Queue", "CF-Root Cause", "Responded"]
        ofile_response=open("responds.csv","wb")
        response_csv_writer = csv.writer(ofile_response, delimiter='\t')
        ofile_response.write('#start_date: '+from_date_str+'\n')
        response_csv_writer.writerow(response_csv_head)


        # all_hist.csv
        hist_csv_head = ["id", "Created", "Resolved", "Status", "Queue", "CF-System Type", "CF-Region"]

        ofile_hist=open("all_hist.csv","wb")
        hist_csv_writer = csv.writer(ofile_hist, delimiter=',')
        ofile_hist.write("#")
        hist_csv_writer.writerow(hist_csv_head)


        #colomn of result.xls: id	Queue	Subject	Status	TimeEstimated	TimeWorked	TimeLeft	Priority	FinalPriority
        #Owner	Requestors	Cc	AdminCc	Due	Told	Created	Resolved	LastUpdated	CF-TeamTrack Id	CF-System Type
        #CF-Technical Centre	CF-Domain	CF-Region	CF-Node	CF-Feed	CF-External ID	CF-Root Cause


        mapQueue = {"General":1,"Service Affecting" :3,"Defect Report" :4,"Request For Help" :5}


        ifile  = open('Results.xls', "rb")
        reader = csv.reader(ifile,dialect='excel-tab')
         
        rownum = 0
        for row in reader:
            # Save header row.
            if rownum == 0:
                header = row
            else:
                temp_dict={}
                colnum = 0
                for col in row:
                    temp_dict[header[colnum]] = col
                    #print '%-8s: %s' % (header[colnum], col)
                    colnum += 1 
                #print temp_dict
                #'stalled' ticket is treated as 'resolved', and 'ResolveDate' should be 'LastUpdated'
                if temp_dict["Status"] == "stalled":
                    temp_dict["Status"] = "Resolved"
                    temp_dict["Resolved"] = temp_dict["LastUpdated"] 

                date_creat = datetime.datetime.strptime(temp_dict["Created"], "%Y-%m-%d %H:%M:%S")
                from_date = datetime.datetime.strptime(from_date_str, "%Y-%m-%d")
                #print date_creat, from_date
                if  date_creat > from_date:
                    #compose and write response line if Created time is later than parameter-from_date
                    response_line = []
                    for item in response_csv_head:
                        if temp_dict.has_key(item):
                            response_line.append(temp_dict[item])
                    response_csv_writer.writerow(response_line)

                #history has the Queue mapped to queue id
                if mapQueue.has_key(temp_dict["Queue"]):
                    temp_dict["Queue"] = mapQueue[temp_dict["Queue"]]
                else:
                    temp_dict["Queue"] = ""
                #compose and write history line
                hist_line = []
                for item in hist_csv_head:
                    if temp_dict.has_key(item):
                        hist_line.append(temp_dict[item])
                hist_csv_writer.writerow(hist_line)
            rownum += 1
         
        #end and close all files
        ifile.close()
        ofile_response.close()
        ofile_hist.close()

if __name__ == '__main__':
    l_f = RawDateConverter()
#    l_f.get_raw_data()
    l_f.generate_local_file(get_date_with_offset(-7))
    
