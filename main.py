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


	
def main():		
	FILE = open("post3-2.txt", "rb") 
	raw_emails = pickle.load(FILE)
	FILE.close()	
	
	names = []
	for raw_email in raw_emails:
		email_message = email.message_from_bytes(raw_email)
		name = email.utils.parseaddr(email_message['From'])[0] #0 for name, 1 for email address
		if names.count(name) == 0:
			names.append(name)
			#print(name)
		
	#set up dictionary with each name correlating to a list of the counts of each week (over a year)
	peopleCounts = {}
	for name in names:
		yearList = [0]*54
		peopleCounts[name] = yearList

	for raw_email in raw_emails:	
		email_message = email.message_from_bytes(raw_email)
		name = email.utils.parseaddr(email_message['From'])[0] #0 for name, 1 for email address
		dateTuple = parseDate(str(email_message['Date']))
		weekBucket = dateTuple[1]
		lines = 0
		for index in range(len(email_message.get_payload())):
			lines = countLines(str(email_message.get_payload()[index]))
			peopleCounts[name][weekBucket] += lines	



	#for name in names:
	#	print("--" + name + "--")
	#	for week in peopleCounts[name]:
	#		print(week)

	root = Tk()
	root.title("Tick-Talk")
	YOFFSET = 800

	canvas = Canvas(root, width=1200, height=1000)
	canvas.pack()
	
	xcoord = 1080
	bottomHeight = [YOFFSET]*108
	i = 0
	while i < 108:
		if i%2 == 0:
			bottomHeight[i] = xcoord
			xcoord = xcoord - 20
		i = i + 1

	num = 0 
	for name in names:
		topHeight = [0]*54;

		xcoord = 1080
		j = 53
		while j >= 0:
			topHeight[j] = xcoord
			topHeight.insert(j+1, .25*peopleCounts[name][j])
			xcoord = xcoord - 20
			j = j - 1

		for h in range(108):
			if h%2 == 1:
				topHeight[h] = bottomHeight[108 - h] - topHeight[h]  

		topHeight.append(topHeight[106])
		topHeight.append(bottomHeight[107])
		plotThis = topHeight + bottomHeight
	
		
		color = "lightblue"
		if num%10 == 8:
			color = "green"
		elif num%10 == 7: 
			color = "hot pink"
		elif num%10 == 6: 
			color = "yellow"
		elif num%10 == 5: 
			color = "gray"
		elif num%10 == 4:
			color = "pink"
		elif num%10 == 3:
			color = "purple"
		elif num%10 == 2:
			color = "orange"
		elif num%10 == 1:
			color = "blue"
		elif num%10 == 0:
			color = "red"
			
			
		
		canvas.create_polygon(plotThis,fill=color,outline="brown",width=2, smooth="true")
			

		num = num + 1

		k = 0
		while k < 108:
			if k%2 == 1:

				bottomHeight[k] = topHeight[108 - k]
			k = k+1
		
	
	mainloop()
	
if __name__ == '__main__':
	main()

