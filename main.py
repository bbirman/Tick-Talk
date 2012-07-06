#!/usr/bin/env python
# encoding: utf-8
"""
Created by Brianna Birman on 2012-06-19.
"""

import imaplib
import sys
import os
import email
import datetime
import pickle
from tkinter import *
from tkinter import ttk
from display import Display


data = {}
names = []
years = []
weekTotals = {}

def countLines(email):
	count = email.count("<cli:body>") + email.count("<=\r\ncli:body>") + email.count("<c=\r\nli:body>") + email.count("<cl=\r\ni:body>") + email.count("<cli=\r\n:body>") + email.count("<cli:=\r\nbody>") + email.count("<cli:b=\r\nody>") + email.count("<cli:bo=\r\ndy>") + email.count("<cli:bod=\r\ny>") + email.count("<cli:body=\r\n>")
	return count

def matchMonth(month):
	if month == "Jan":
		return 1
	elif month == "Feb":
		return 2
	elif month == "Mar":
		return 3
	elif month == "Apr":
		return 4
	elif month == "May":
		return 5
	elif month == "Jun":
		return 6
	elif month == "Jul":
		return 7
	elif month == "Aug":
		return 8
	elif month == "Sep":
		return 9
	elif month == "Oct":
		return 10
	elif month == "Nov":
		return 11
	elif month == "Dec":
		return 12

#Takes the date header and returns a tuple of (0) year, (1) week number, (2) day of the week
def parseDate(dateString):
	day = -1
	monthNum = -1
	year = -1
	
	#if date is one digit long
	if dateString[6] == ' ':
		day = dateString[5:6] 
		month = dateString[7:10]
		monthNum = matchMonth(month)
		year = dateString[11:15]
	#date is two digits long
	else:
		day = dateString[5:7]
		month = dateString[8:11]
		monthNum = matchMonth(month)	
		year = dateString[12:16]
	
	date = datetime.date(int(year), monthNum, int(day))
	dateTuple = date.isocalendar()	
	return dateTuple
	
def mergeNames(keepName, mergeNames):
	
	for mergeName in mergeNames:
		for year in years:
			for i in range(54):
				data[year][keepName][i] += data[year][mergeName][i]
			del data[year][mergeName]
		names.remove(mergeName)
		
	for mergeName in mergeNames:
		for j in range(54):
			data[0000][keepName][j] += data[0000][mergeName][j]
		del data[0000][mergeName]
		

def mergeTheseNames():
	#mergeName("Example name", ["Example name duplicate"])
	pass
	
def chooseYear(event):
	display.canvas.delete("all")
	item = display.yearList.get(ACTIVE)
	print("Item: " + str(item))
	if item == 2009:
		display.drawThis(display.drawList.get(ACTIVE), "By year", 2009)
	elif item == 2010:
		display.drawThis(display.drawList.get(ACTIVE), "By year", 2010)
	elif item == 2011:
		display.drawThis(display.drawList.get(ACTIVE), "By year", 2011)
	elif item == 2012:
		display.drawThis(display.drawList.get(ACTIVE), "By year", 2012)

def typeSelected(event):
	selection = display.timeList.get(ACTIVE)
	print("Selection: " + selection)
	if selection == "By year":	
		display.yearList.pack(side=LEFT, padx=30)
		display.yearList.bind("<ButtonRelease-1>", chooseYear)
	elif selection == "Total": 
		display.canvas.delete("all")
		display.yearList.pack_forget()
		display.drawThis(display.drawList.get(ACTIVE), "Total")
			
FILE = open("post3-2.txt", "rb") 
raw_emails = pickle.load(FILE)
FILE.close()	

for raw_email in raw_emails:
	email_message = email.message_from_bytes(raw_email)
	name = email.utils.parseaddr(email_message['From'])[0] #0 for name, 1 for email address
	year = parseDate(str(email_message['Date']))[0]
	if names.count(name) == 0:
		names.append(name)
	if years.count(year) == 0:
		years.append(year)
		print("year: #" + str(year) + "#")

for year in years:
	data[year] = {}
	for name in names: 
		data[year][name] = [0]*54
	data[year]["Total"] = [0]*54

#set up "year" 0000 for total instead of dividing by year
data[0000] = {}
for name in names: 
	data[0000][name] = [0]*54
data[0000]["Total"] = [0]*54


for raw_email in raw_emails:	
	email_message = email.message_from_bytes(raw_email)
	name = email.utils.parseaddr(email_message['From'])[0] #0 for name, 1 for email address
	dateTuple = parseDate(str(email_message['Date']))
	weekBucket = dateTuple[1]
	yearBucket = dateTuple[0]
	lines = 0
	for index in range(len(email_message.get_payload())):
		lines = countLines(str(email_message.get_payload()[index]))
		data[yearBucket][name][weekBucket] += lines
		data[yearBucket]["Total"][weekBucket] += lines
		data[0000][name][weekBucket] += lines
		data[0000]["Total"][weekBucket] += lines
		

mergeTheseNames()

display = Display(data, names, years)
display.yearList.pack(side=LEFT, padx=30)
display.timeList.bind("<Button-1>", typeSelected)
display.drawThis("Line count", "By year", 1970); 
	
mainloop()


