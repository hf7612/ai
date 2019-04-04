#!/usr/bin/env python
#coding:UTF-8
import string
import time
import datetime
def trav_file():
	filename = 'n' #raw_input('Enter your file name')
	file = open(filename,'r')	
	l=file.readline()
	s=l.split();
	# print 'ee',l
	while l:
		if l != '': # print aLine print l
			s = l.split(); #print s[0]; #("%s"%("ee"))
			# print "jfjfj", l
			for i in s:
				# print "lkjj",i
				if i.find("open(")>=0:
					print i[6:len(i)-2]
				elif i.find("openat(")>=0:
					s2=s[2]
					s3=s2.rstrip(',')
					print s3 # print i[12:len(i)-2]
		l = file.readline()
	file.close()
trav_file()
