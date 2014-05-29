'''
Created on Apr 11, 2014

@author: Pa

THIS VERSION IS TO BE RUN ON Pa's Arizona Desktop
===========================================

call google trends (Google.com/trends) with query built from two control files
1) Search_Terms_Control_File : list of country names in several languages
    each row is a single country with the country name specified in multiple languages, each separated by a comma.
2) Geos_Multi_Control_File : list of geography codes - 5 at a time (sample is 5_Geos.txt)
    each row is a list of 5 geo codes separated by commas and spaces
    
This program builds a query that combines each row of the search term file with each of the rows of the geo codes file.
The output of each query is a csv file = search term country name + geo control file row number + GTrends.csv
The location of the output files are determined by the data_location_library

These queries are run under a single login to google.com
the login credentials are specified by the google username and google password variables

This program is the general logic but calls to generic module pyGTrends for the login processing and query execution

The idea for this code originated from similar code published by Sal Uryasev under the MIT license :
https://github.com/suryasev/unofficial-google-trends-api/blob/master/pyGTrends.py
and is modified for the specific needs of Kelly Matush.
'''

from pyGTrends import pyGTrends
import csv, time, sys, codecs
import re

# this is the google sign on info used 
# google_username = "KSM.ABC111"
# google_password = "ksmabc111"
# google_username = "susie.matush"
# google_password = "redwood81"
google_username = "KSM.SDSUPS"
google_password = "testtest99"

#This is the location of the output files = Searchterm+GEOs.GTrends.csv
data_location_library = "c:\\Users\\Pa\\Documents\\GoogleTrendsReports\\"
#data_location_library = "T:\\Dropboxb\\Kelly\\GoogleTrendsData\\"

#This is the name of the "Search Terms" Control File 
Search_Terms_Control_File = 'T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\Search_Terms.txt'

#This is the name of the "Base Search Terms" control File (Unused in this program)
Geos_Control_File = 'T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\Base_Searchterm.txt'
#This is the name of the "Geos_Multi" control File - it is used to develop the geos term of the search using multiple country codes
Geos_Multi_Control_File = 'T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\5_GEOS.txt'

print "terms defined"

def read_csv_data( data ):
    """
        Reads CSV from given path and Return list of dict with Mapping
    """
    csv_reader = csv.reader( data )
    # Read the column names from the first line of the file
    fields = csv_reader.next()
    data_lines = []
    for row in csv_reader:
        items = dict(zip(fields, row))
        data_lines.append(items)
    return data_lines

def progressbar(it, prefix = "", size = 60):
    count = len(it)
    
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
    
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()

def getGTData(search_query="Afganistan", date="all", geo="all", scale="1", position = "end" ) :
    
    #search_query_term = 'q='+search_query.rstrip()
    #geo_term = 'geo='+geo.rstrip()
        
    search_query_term = search_query.rstrip()
    print "search_query_term = " + search_query_term
    URL_Search_Term = search_query.split('+')[0]   
    URL_Search_Term = str(URL_Search_Term.strip())
    geo = geo.rstrip()
    geo_term = geo

    #country_name = Geo_Dictionary(geo)
    
    #print "country_name = " + country_name
    print "URL_Search_Term = " + URL_Search_Term
    #print "geo = " + geo
    print "geo_term = " + geo_term
    #geo_name = Geo_Dictionary[geo]
#     print "geo name = " + geo_name
  
    #search_base_term = Geo_Baseterm_Dictionary[URL_Search_Term]
    #there is no base term in this version of code
    #print "search_base_term = " + search_base_term    
        
    #connector.get_csv((search_query_term,search_base_term),geo_term)
    connector.get_csv((search_query_term),geo_term)
    connector.raw_data.split('\n')
    
    data = connector.csv( section='Main' ).split('\n')
    
    #print "csv data :::"
    #print data
    # now read back in the output of connector.csv in data
    csv_reader = csv.reader( data ) 
   
    #with open( data_location_library + URL_Search_Term + '_' + geo_name + '_GTrends.csv', 'wb') as csv_out:
    with open( data_location_library + URL_Search_Term + str(gcount) + '_GTrends.csv', 'wb') as csv_out:
        positionInWeek = { "start" : 0, "end" : 1 }
        separator = " - "
        csv_writer = csv.writer( csv_out )
        #write query URL as first row of output CSV - convert string to single element list
        csv_writer.writerow([connector.Source_URL])
        
        #print "LOOPING ON ENTRIES"
        for count, row in enumerate( csv_reader ):
            if len(row)==0:
                #row = ' '
                #csv_writer.writerow( row )
                #print "row is empty = insert a blank"
                continue
            
            if separator not in row[0] : 
                csv_writer.writerow( row )
                #print "separator not in row"
                continue

            date = row[0].split( separator )[ positionInWeek[ position ] ] 
            if date == 'present':
                csv_writer.writerow( row )
                #print "separator is the word present"
                continue
                
        # we want to remove any whitespaces from the value entry since we are not interested in blank data points
            built_row = [date]
            for value_number in xrange(1,len(row)):
                val = re.sub(r'\s+', '', row[value_number] )
                if len(val) > 0 :
                    built_row.append(val)
                    continue
            #row = str(date)+','+str(val)
            
            if count == 0:
                csv_writer.writerow( row )
            else:
                csv_writer.writerow( built_row)
    #print "File saved: %s " % ( URL_Search_Term + '_' + geo_name + '_GTrends.csv' )
    print "File saved: %s " % ( URL_Search_Term + str(gcount) + '_GTrends.csv' )

def getGoogleTrendData( search_query ="Italy", date="all", geo = ["all"], scale="1" ) :
    global gcount #gcount is the number of rows in the geoterms list
    gcount = 0
    for geo_term in progressbar( geo, "Downloading: ", 40 ):
        gcount = gcount + 1
        getGTData(search_query, geo = geo_term)
    time.sleep(1)  # Delay for x seconds    
    return True

class Recoder(object):
    def __init__(self, stream, decoder, encoder, eol='\r\n'):
        self._stream = stream
        self._decoder = decoder if isinstance(decoder, codecs.IncrementalDecoder) else codecs.getincrementaldecoder(decoder)()
        self._encoder = encoder if isinstance(encoder, codecs.IncrementalEncoder) else codecs.getincrementalencoder(encoder)()
        self._buf = ''
        self._eol = eol
        self._reachedEof = False

    def read(self, size=None):
        r = self._stream.read(size)
        raw = self._decoder.decode(r, size is None)
        return self._encoder.encode(raw)

    def __iter__(self):
        return self

    def __next__(self):
        if self._reachedEof:
            raise StopIteration()
        while True:
            line,eol,rest = self._buf.partition(self._eol)
            if eol == self._eol:
                self._buf = rest
                return self._encoder.encode(line + eol)
            raw = self._stream.read(1024)
            if raw == '':
                self._decoder.decode(b'', True)
                self._reachedEof = True
                return self._encoder.encode(self._buf)
            self._buf += self._decoder.decode(raw)
    next = __next__

    def close(self):
        return self._stream.close()


if __name__=="__main__":
    
    # read control file to get list of search terms
    
    i=0
    f=codecs.open(Search_Terms_Control_File,'r', encoding='utf-16')
    #list_of_Search_Terms = f.readlines()
    list_of_Search_Terms = list(f)
    for Search_Term in list_of_Search_Terms:
        i+=1
        print "(" + str(i) + ") " + Search_Term  
     
    # read control file to get list of geos version 1
#     i=0
#     f=open('T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\GEOS.txt','r')
#     list_of_geos = list(f)
#     for geo in list_of_geos:
#         i+=1
#         print "(" + str(i) + ") " + geo
        
    # read control file to get list of geos version2
    # field_names = ['Geo_Code', 'Country', "BLS"]
    #delimiter = '\t'
    #quote_character = '"'
    #Geo_List = []
    
    #csv_fp = open(Geos_Control_File, 'rb')
    #sr = Recoder(csv_fp, 'utf-16', 'utf-8')

    #csv_reader = csv.DictReader(sr, fieldnames=[], restkey='undefined-fieldnames', delimiter=delimiter, quotechar=quote_character)

    #current_row = 0
    #for row in csv_reader:
    #

    #     print"the Country for GEO CODE DJ = " + Geo_Dictionary['DJ'] 
    
    # Remove duplicate entries in the list if there are any...
    #list_of_Search_Terms = list( set( list_of_Search_Terms ) )   
    #list_of_geos = list( set( list_of_geos ) )
    
    # read control file to get list of geos version 3 (multiple geos per query)
    i=0
    f=open(Geos_Multi_Control_File,'r')
    list_of_geos = list(f)
    for geo in list_of_geos:
        i+=1
        print "(" + str(i) + ") " + geo      
    
    # sign on to google
    connector = pyGTrends( google_username, google_password )
    
    #Get Trend data for each line in Search Terms control File - iterating over the GEOs control file lines
    for Search_Term in list_of_Search_Terms :
        #if getGoogleTrendData( search_query = Search_Term, geo = Geo_Dictionary.keys()) :
        if getGoogleTrendData( search_query = Search_Term, geo = list_of_geos) :
            print "Google Trend Data aquired."
        

