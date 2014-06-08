#coding=utf-8
'''
Created on June 8, 2014

@author: Pa

THIS VERSION IS TO BE RUN ON multiple pcs - driven by master control file

Adds baseline term from control file to search terms
===========================================

call google trends (Google.com/trends) with query built from two control files
1) Search_Terms_Control_File : list of country names in several languages
    each row is a single country with the country name specified in multiple languages, each separated by a comma.
2) Master_Control_File : contains local and dropbox directory locations, baseline_term, and geo_term
    
This program builds a query that concatenates the baseline term with each row of the search term file.  
eg. "help, 'Afganistan......", where 'help' is the baseline_term. 
The Geo_term is used as the location for google trends query.
The output of each query is a csv file = search term country name + 0 + GTrends.csv
The location of the output files are determined by the data_location_library

These queries are run under a single login to google.com
the login credentials are specified by the google username and google password variables, which are specified in the
GIDPWFile.txt control file

This program is the general logic but calls to generic module pyGTrends for the login processing and query execution

The idea for this code originated from similar code published by Sal Uryasev under the MIT license :
https://github.com/suryasev/unofficial-google-trends-api/blob/master/pyGTrends.py
and is modified for the specific needs of Kelly Matush.
'''

from pyGTrends import pyGTrends
import csv, time, sys, codecs, re
from xlrd import open_workbook


MasterConfigFile = "T:\\Dropbox\\Kelly\\GoogleTrendsData\\SearchControls\\MasterConfigFile_GREECE.xls"
# read the Master Config File data into a dictionary of control terms
wb = open_workbook(MasterConfigFile)

Config_Dict = {}
for s in wb.sheets():
    print 'Master Config File Worksheet = ',s.name
    for row in range(s.nrows):
        Key = s.cell(row,0).value
        Value = s.cell(row,1).value
        Config_Dict[Key] = Value
        
GIDPWFile = Config_Dict['C_Root'] + Config_Dict['GIDPWFile']
data_location_library = Config_Dict['L_Root'] + Config_Dict['D_Root']
Search_Terms_Control_File = Config_Dict['L_Root'] + Config_Dict['C_Root'] + 'New_Search_Terms_trunc.txt'
Base_Term = Config_Dict['BASE_TERM'].rstrip()
GEO_Term = Config_Dict['GEO'].rstrip()

print "Google ID/PW File = " + GIDPWFile
print "data location library = " + data_location_library
print "Search_Terms_Control_File = " + Search_Terms_Control_File
print "Baseline Term = ", Base_Term
print "Location = ", Config_Dict['LOCATION']
print "Geo Term = ", GEO_Term

print "terms defined"
sys.exit()
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
    
    search_query_term = search_query.rstrip()
    print "search_query_term (unaltered) = " + search_query_term
    #concatenate the base_term to the front of the search query term
    search_query_term = Base_Term + ", " + search_query_term
    print "search_query_term (altered) = " + search_query_term
    
    URL_Search_Term = search_query.split('+')[0]   
    URL_Search_Term = URL_Search_Term.strip()
    URL_Search_Term = URL_Search_Term[1:-1] #remove quotes from beginning and end - and the base term eg "help"
    #URL_Search_Term = "JAPAN"
    #geo = geo.rstrip()
    #geo_term = geo
   
    print "URL_Search_Term = " + URL_Search_Term
    print "geo_term = " + GEO_Term    
       
    #connector.get_csv((search_query_term,search_base_term),geo_term)
    connector.get_csv((search_query_term), GEO_Term)
    connector.raw_data.split('\n')
    
    data = connector.csv( section='Main' ).split('\n')
    
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
    getGTData(search_query, geo = "JP")
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
    
    # read GOOGLE ID/PW from local control file
    f=open(GIDPWFile, 'r')
    f.readline() #skip the file instruction line 
    google_username = f.readline()
    google_password = f.readline()
    print "user name = " + google_username
    print "user pw = " + google_password
     
    # read Search_Terms_Control file to get list of search terms
    i=0
    f=codecs.open(Search_Terms_Control_File,'r', encoding='utf-16')
    #list_of_Search_Terms = f.readlines()
    list_of_Search_Terms = list(f)
    for Search_Term in list_of_Search_Terms:
        i+=1
        print "(" + str(i) + ") " + Search_Term          
    
    # sign on to google
    connector = pyGTrends( google_username, google_password )
    
    #Get Trend data for each line in Search Terms control File - iterating over the GEOs control file lines
    for Search_Term in list_of_Search_Terms :
        #if getGoogleTrendData( search_query = Search_Term, geo = Geo_Dictionary.keys()) :
        if getGoogleTrendData( search_query = Search_Term, geo = ['xx']) :
            print "Google Trend Data processing complete"       
