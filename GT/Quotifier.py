'''
Created on May 30, 2014

@author: Pa

read contents of Search Terms control file and add quotes around each term
output to searchterms_quotes.txt

'''

import codecs
#This is the name of the "Search Terms" Control File 
Search_Terms_Control_File = 'T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\New_Search_Terms_trunc.txt'
New_Search_Terms_Control_File = 'T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\New_Search_Terms_Qtrunc.txt'

i=0
f=codecs.open(Search_Terms_Control_File,'r', encoding='utf-16')
o=codecs.open(New_Search_Terms_Control_File, 'w', encoding='utf-16')
#list_of_Search_Terms = f.readlines()
list_of_Search_Terms = list(f)
for Search_Term in list_of_Search_Terms:
    i+=1
    print "input search term = (" + str(i) + ") " + Search_Term 
    New_Search_Term = Search_Term.replace(' + ', '" + "')
    New_Search_Term = '"' + New_Search_Term.rstrip() + u'"'
    print "output search term = (" + str(i) + ") " + New_Search_Term
    o.write(New_Search_Term)
    o.write(u"\r\n")
o.close()
    