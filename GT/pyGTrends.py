"""
Created on Apr 11, 2014

@author: Pa

The idea for this code originated from similar code published by Sal Uryasev under the MIT license :
https://github.com/suryasev/unofficial-google-trends-api/blob/master/pyGTrends.py
and is modified for the specific needs of Kelly Matush.

"""

#import httplib
import urllib
import urllib2 
import re
#import csv
#import logging
import sys
import StringIO
import gzip
import random
import time


from cookielib import CookieJar

class pyGTrends( object ):
    """
    Google Trends API
    
    Recommended usage:
    
    from csv import DictReader
    r = pyGTrends(username, password)
    r.download_report(('pants', 'skirt'))
    d = DictReader(r.csv().split('\n'))
    """
    
    def __init__( self, username, password ):
        """
        provide login and password to be used to connect to Google Analytics
        all immutable system variables are also defined here
        website_id is the ID of the specific site on google analytics
        """        
        self.login_params = {
            "continue": 'http://www.google.com/trends',
            "PersistentCookie": "yes",
            "Email": username,
            "Passwd": password,
        }
        self.headers = [ ( "Referrer", "https://www.google.com/accounts/ServiceLoginBoxAuth" ),
                         ( "Content-type", "application/x-www-form-urlencoded" ),
                         ( 'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21' ),
                         ( "Accept", "text/plain" ) ]
        self.url_ServiceLoginBoxAuth = 'https://accounts.google.com/ServiceLoginBoxAuth'
        self.url_Export = 'http://www.google.com/trends/viz'
        self.url_CookieCheck = 'https://www.google.com/accounts/CheckCookie?chtml=LoginDoneHtml'
        self.url_PrefCookie = 'http://www.google.com'
        self.header_dictionary = {}
        self._connect()
        self.download_delay = 1.2
        self.url_service = "http://www.google.com/trends/"
        self.url_download = self.url_service + "trendsReport?"
        
    def _connect( self ):
        """
        connect to Google Trends
        """
        
        self.cj = CookieJar()                            
        self.opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cj ) )
        self.opener.addheaders = self.headers
        
        galx = re.compile( '<input name="GALX"[\s]+type="hidden"[\s]+value="(?P<galx>[a-zA-Z0-9_-]+)">' )
        
        resp = self.opener.open( self.url_ServiceLoginBoxAuth ).read()
        resp = re.sub( r'\s\s+', ' ', resp )
        #print resp

        m = galx.search( resp )
        if not m:
            raise Exception( "Cannot parse GALX out of login page" )
        self.login_params['GALX'] = m.group( 'galx' )
        params = urllib.urlencode( self.login_params )
        self.opener.open( self.url_ServiceLoginBoxAuth, params )
        self.opener.open( self.url_CookieCheck )
        self.opener.open( self.url_PrefCookie )
        
    def get_csv(self, keywords, geo_term="FR"):
        '''
        Download CSV reports
        '''
        throttle=True
        # Randomized download delay
        if throttle:
            r = random.uniform(0.5 * self.download_delay, 1.5 * self.download_delay)
            print "delay for " + str(r)
            time.sleep(r)
        print "keywords = " + keywords
        print "geoterm = " + geo_term
        if type( keywords ) not in ( type( [] ), type( ( 'tuple', ) ) ):
            keywords = [ keywords ]
        
        
        #params = search_term+'&'+geo_term+'&export=1'
        parm_list = {
            'q': ",".join( keywords ),                      
            'geo': geo_term,
            'export' : 1,
            'cmpt' : 'geo'
        }
        #convert parm_list to str for urlencode processing (which requires str instead of unicode)
        str_parm_list = {}
        for k, v in parm_list.iteritems():
            str_parm_list[k] = unicode(v).encode('utf-8')

        #print parm_list
        params = urllib.urlencode(str_parm_list)
         
        #print "get csv params = " +  params
        
        S_URL = self.url_download + params
        #print S_URL
        self.Source_URL = S_URL       
        
        r = self.opener.open(S_URL)
        try:
            r = self.opener.open(S_URL)
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            print e.args
        #print r.info()
        
        # Make sure everything is working ;)
        if not r.info().has_key('Content-Disposition'):
            print "You've exceeded your quota. Continue tomorrow..."
            sys.exit(0)
             
        if r.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( r.read())
            f = gzip.GzipFile(fileobj=buf)
            self.raw_data = f.read()
        else:
            self.raw_data = r.read()
            
        #print self.raw_data
              
        
    def csv(self, section="Main", as_list=False):
        """
        Returns a CSV of a specific segment of the data.
        Available segments include Main, City and Subregion.
        """
        if section == "Main":
            section = ("Week","Year","Day","Month")
        else:
            section = (section,)
            
        segments = self.raw_data.split('\n\n\n')
        #print "csv segments :"
        #print segments
        #print "Length of segments = " + str(len(segments))
        # problem in that we didnt skip the first 4 lines which usually contain information
        # such as Web Search interest: debt, United States; 2004 - present, Interest over time ...
        start = []
        found = False
        for i in range( len( segments ) ):
            lines = segments[i].split('\n')
            n = len(lines)
            #print "segment number i = " + str(i)
            #print "length of lines = " + str(n)
           
            for counter, line in enumerate( lines ):
                #print "counter = " + str(counter)
                if line.partition(',')[0] in section or found:
                    if counter + 1  != n: # stops us appending a stupid blank newspace at the end of the file
                        start.append( line + '\n' )
                        #print "line type 1 = " + line
                else :
                    start.append( line )
                    found = True
                    #print "line type 2"
                        
            segments[i] = ''.join(start)
        #print "segment 0 = " + segments[0]   	
        return segments[0]
        
#         for s in segments:
#             print "s = " + s
#             if s.partition(',')[0] in section:
#                 if as_list:
#                     return [line for line in csv.reader(s.split('\n'))]
#                 else:
#                     return s
#                 
        #logging.error("Could not find requested section")            
        #raise Exception("Could not find requested section")

    #def csv(self, section="main", as_list=False):
    #    """
    #    Returns a CSV of a specific segment of the data.
    #    Available segments include Main, Language, City and Region.
    #    """
    #    if section == "main":
    #        section = ("Week","Year","Day","Month")
    #    else:
    #        section = (section,)
    #        
    #    segments = self.raw_data.split('\n\n\n')
    #    for s in segments:
    #        if s.partition(',')[0] in section:
    #            if as_list:
    #                return [line for line in csv.reader(s.split('\n'))]
    #            else:
    #                return s
    #                
    #    raise Exception("Could not find requested section")

    def getData( self):

        return self.raw_data

    def writer( self, outputname = "report.csv" ) :
        o = open( outputname, "wb" )
        o.write( self.raw_data )
    
