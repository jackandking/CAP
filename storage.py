# -*- coding: utf-8 -*-
# Author: liang.zhang1@thomsonreuters.com
# DateTime: 2013-09-15 15:48:54.512000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 0.8
# Newpy ID: 0
# Description: I'm a lazy person, so you have to figure out the function of this script by yourself.


# MongoDB - NoSQL

from pymongo import MongoClient
import datetime

class storage:
	def __init__(self):
		self.client = MongoClient('localhost', 27017)
		self.db = self.client.mydb
		self.coll = self.db.mycollection

	#write to db, the format shold be {key:file name, value:file content, date:current date}
	def write(self, content):
		self.coll.insert(content)
	
	#if no filter needed, call this method by read({})	
	def read(self,filter):
		self.content = []
		for item in self.coll.find(filter):
			self.content.append(item)
		return self.content


if __name__ == '__main__':
	store = storage()
	store.write({"key":"test","value":"testvalue", "date":datetime.datetime.now()})
	for i in store.read({}):
		print i
