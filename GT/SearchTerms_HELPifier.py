#coding=utf-8 
'''
Created on Jun 2, 2014

@author: Pa
'''
import codecs
#This is the name of the "Search Terms" Control File 
Search_Terms_Control_File = 'T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\New_Search_Terms_trunc.txt'
New_Search_Terms_Control_File = 'T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\New_Search_Terms+ITALY.txt'

i=0
f=codecs.open(Search_Terms_Control_File,'r', encoding='utf-16')
o=codecs.open(New_Search_Terms_Control_File, 'w', encoding='utf-16')
# HELP_Term will be added as base term each Search Term Row
#HELP_Term = u'助け'
HELP_Term = u'search'
list_of_Search_Terms = list(f)
for Search_Term in list_of_Search_Terms:
    i+=1
    print "input search term = (" + str(i) + ") " + Search_Term 
    New_Search_Term = HELP_Term + ", " + Search_Term
    #New_Search_Term = New_Search_Term.rstrip()
    print "output search term = (" + str(i) + ") " + New_Search_Term
    o.write(New_Search_Term)
    #o.write(u"\r\n")
o.close()