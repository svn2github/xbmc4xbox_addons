import os
import xbmc
import urllib2
import gzip
import StringIO

#
# XBMC constants
#
result       = xbmc.executehttpapi('GetSystemInfoByName(system.buildversion;system.builddate)')
system_info  = result.split('<li>')
XBMC_BUILD_VERSION = system_info[1]
XBMC_BUILD_DATE    = system_info[2]

#
# HTTPCommunicator
#
class HTTPCommunicator :
    #
    # GET
    #
    def get( self, url ):
        h = urllib2.HTTPHandler(debuglevel=0)
        
        request = urllib2.Request( url )
        request.add_header( "Accept"         , "*/*)" )
        request.add_header( "Accept-Encoding", "gzip" )
        request.add_header( "User-Agent"     , "Python-urllib/%s (%s; XBMC/%s, %s)" % ( urllib2.__version__, os.name.upper(), XBMC_BUILD_VERSION, XBMC_BUILD_DATE ) )
        opener = urllib2.build_opener(h)
        f = opener.open(request)

        # Compressed (gzip) response...
        if f.headers.get( "content-encoding" ) == "gzip" :
            htmlGzippedData = f.read()
            stringIO        = StringIO.StringIO( htmlGzippedData )
            gzipper         = gzip.GzipFile( fileobj = stringIO )
            htmlData        = gzipper.read()
            
            # Debug
            # print "[HTTP Communicator] GET %s" % url
            # print "[HTTP Communicator] Result size : compressed [%u], decompressed [%u]" % ( len( htmlGzippedData ), len ( htmlData ) )
            
        # Plain text response...
        else :
            htmlData = f.read()
        
        # Cleanup
        f.close()

        # Return value
        return htmlData
