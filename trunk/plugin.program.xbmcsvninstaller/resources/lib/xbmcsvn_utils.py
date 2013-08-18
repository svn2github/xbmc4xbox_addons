import os
import xbmc
import zlib
import httplib
import urllib
import urllib2
import gzip
import StringIO
import HTMLParser

#
# XBMC constants
#
result       = xbmc.executehttpapi('GetSystemInfoByName(system.buildversion;system.builddate)')
system_info  = result.split('<li>')
XBMC_BUILD_VERSION = system_info[1]
XBMC_BUILD_DATE    = system_info[2]

#
# HTTP responses
# See RFC 2616
#
HTTP_REPONSES = {
    400: 'Bad request syntax or unsupported method',
    401: 'No permission -- see authorization schemes',
    402: 'No payment -- see charging schemes',
    403: 'Request forbidden -- authorization will not help',
    404: 'Nothing matches the given URI',
    405: 'Specified method is invalid for this server.',
    406: 'URI not available in preferred format.',
    407: 'You must authenticate with this proxy before proceeding.',
    408: 'Request timed out; try again later.',
    409: 'Request conflict.',
    410: 'URI no longer exists and has been permanently removed.',
    411: 'Client must specify Content-Length.',
    412: 'Precondition in headers is false.',
    413: 'Entity is too large.',
    414: 'URI is too long.',
    415: 'Entity body in unsupported format.',
    416: 'Cannot satisfy request range.',
    417: 'Expect condition could not be satisfied.',

    500: 'Internal Server Error',
    501: 'Server does not support this operation',
    502: 'Invalid responses from another server/proxy.',
    503: 'The server cannot process the request due to a high load',
    504: 'The gateway server did not receive a timely response',
    505: 'HTTP Version Not Supported'
}

#
# HTTPCommunicator
#
class HTTPCommunicator :
    #
    # POST
    #
    def post( self, host, url, params ):
        parameters  = urllib.urlencode( params )
        headers     = { "Content-type"    : "application/x-www-form-urlencoded",
                        "Accept"          : "text/plain",
                        "Accept-Encoding" : "gzip" }
        connection  = httplib.HTTPConnection("%s:80" % host)
        
        connection.request( "POST", url, parameters, headers )
        response = connection.getresponse()
        
        # Compressed (gzip) response...
        if response.getheader( "content-encoding" ) == "gzip" :
            htmlGzippedData = response.read()
            stringIO       = StringIO.StringIO( htmlGzippedData )
            gzipper        = gzip.GzipFile( fileobj = stringIO )
            htmlData       = gzipper.read()
        # Plain text response...
        else :
            htmlData = response.read()

        # Cleanup
        connection.close()

        # Return value
        return htmlData

    #
    # GET
    #
    def get( self, url ):
        h = urllib2.HTTPHandler(debuglevel=0)
        
        try :
            request = urllib2.Request( url )
            request.add_header( "Accept"         , "*/*" )
            request.add_header( "Accept-Encoding", "gzip" )
            request.add_header( "User-Agent"     , "Python-urllib/%s (%s; XBMC/%s, %s)" % ( urllib2.__version__, os.name.upper(), XBMC_BUILD_VERSION, XBMC_BUILD_DATE ) )
            opener = urllib2.build_opener(h)
            f = opener.open(request)
        # Exception
        except urllib2.HTTPError, e :
            raise Exception( "HTTP Error %u: %s" % ( e.code, HTTP_REPONSES[ e.code ] ) )

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

#
# Convert HTML to readable strings...
#
class HTML2Text :
    #
    #
    #
    def convert( self, html ):
        text = html.replace( "&nbsp;", " " )
        return text.strip()

#
# HTMLStripper class - strip HTML tags from text
#
class HTMLStripper (HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.texts = []

    def handle_data(self, text):
        text = text.replace(u"\xa0", " ")
        text = text.replace(u"hr /", "")
        self.texts.append(text)
        
    def get_fed_data(self):
        return "".join(self.texts)
    