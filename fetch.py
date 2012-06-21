#!/usr/bin/env python
# encoding: utf-8
"""
Created by Brianna Birman on 2012-06-19.
"""

import imaplib
import sys
import os
import cPickle

def main():		
	gmail = imaplib.IMAP4_SSL('imap.gmail.com')
	gmail.login('test@gmail.com', 'testpassword')
	gmail.debug=4
	gmail.select('[Gmail]/Chats', readonly=True) # connect to chat section, must be readonly 
	
	result, uids = gmail.uid('search', None, "ALL") #all messages within chats
													#result is ok, no, bad, etc. 
	id_list = uids[0].split() # ids is a space separated string
	raw_emails = []
	FILE = open('batch1.txt', 'w') 
	
	for id in id_list: #goes from oldest to newest
		result, data = gmail.uid('fetch', id, '(RFC822)') # fetch the email body (RFC822) for the given ID
		raw_email = data[0][1] 	#raw text of the whole email
		raw_emails.append(raw_email)	
	
	cPickle.dump(raw_emails, FILE)
	FILE.close()
	gmail.logout()

if __name__ == '__main__':
	main()