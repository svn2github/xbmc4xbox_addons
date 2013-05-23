import re
import urllib2

from time import mktime,strptime

import xbmc
from xbmc import log

import unicodedata

# Only used if we fail to parse the URL from the website
__SwfPlayerDefault__ = 'http://www.channel4.com/static/programmes/asset/flash/swf/4odplayer-11.34.1.swf'
__Aug12__ = mktime(strptime("12 Aug 2012", "%d %b %Y"))

# Return true if date is later than 12 Aug 2012
def isRecentDate(dateString):
	try:
		dateCompare = mktime(strptime(dateString, "%d %b %Y"))

		if dateCompare > __Aug12__:
			return True

	except ( Exception ),e:
		if dateString is None:
			dateString = 'None'

		xbmc.log ( 'Exception: ' + str(e) + ', dateString: ' + str(dateString), xbmc.LOGERROR )

	return False

def log(msg, level = xbmc.LOGNOTICE, method = None):
    try:
        if method is None:
            method = inspect.stack()[1][3]
            
        if isinstance(msg, unicode):
            xbmc.log((u"%s : '%s'" % (method, msg)).encode('utf8'), level)
        else:
            xbmc.log(to_unicode((u"%s : '%s'" % (method, msg))).encode('utf8'), level)
    except ( Exception ),e:
        xbmc.log(u"FALLBACK %s : '%s'" % (method, repr(msg)), level)


def findString(method, pattern, string, flags = (re.DOTALL | re.IGNORECASE)):
	match = ( pattern, string, flags )
	#match = None ###
	if match is not None:
		return (match.group(1))

	return None
	# Limit logging of string to 1000 chars
	limit = 1000
	# Can't find pattern in string
	messageLog = "\nPattern - \n%s\n\nString - \n%s\n\n" % (pattern, string[0:limit])

	return (None, ErrorHandler(method, ErrorCodes.CANT_FIND_PATTERN_IN_STRING, messageLog))




def GetSwfPlayer( html ):
	log (u"html size:" + str(len(html)), xbmc.LOGDEBUG)

	try:
		swfRoot = re.search(u'var swfRoot = \'(.*?)\'', html, re.DOTALL | re.IGNORECASE).group(1)
		fourodPlayerFile = re.search(u'var fourodPlayerFile = \'(.*?)\'', html, re.DOTALL | re.IGNORECASE).group(1)
		#TODO Find out how to get the "asset/flash/swf/" part dynamically
		swfPlayer = u"http://www.channel4.com" + swfRoot + u"asset/flash/swf/" + fourodPlayerFile

		# Resolve redirect, if any
		req = urllib2.Request(swfPlayer)
		res = urllib2.urlopen(req)
		swfPlayer = res.geturl()
	except (Exception),e:
		log (u"Exception resolving swfPlayer URL: " + str(e), xbmc.LOGWARNING)
		log (u"Unable to determine swfPlayer URL. Using default: " + __SwfPlayerDefault__, xbmc.LOGWARNING)  

		swfPlayer = __SwfPlayerDefault__
	
	return swfPlayer


def remove_leading_slash(data):
    p = re.compile(r'/')
    return p.sub('', data)

def remove_square_brackets(data):
    p = re.compile(r' \[.*?\]')
    return p.sub('', data)

def remove_brackets(data):
    p = re.compile(r' \(.*?\)')
    return p.sub('', data)

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)

def replace_non_alphanum(data):
    p = re.compile(r'[^0-9A-Za-z]+')
    return p.sub('', data)

def valueIfDefined(value, name = None):
    try:
        if name is None:
            return value
        else:
            return name + ": " + value
    except NameError:
        if name is None:
            return ""
        else:
            return name + ": Not defined"

def isVariableDefined(variable):
    try:
        variable
        return True
    except NameError:
        return False
    
def extractJSON(text):
    start = text.index('(') + 1
    end = text.rindex(')')
    
    return text[start:end]


def drepr(x, sort = True, indent = 0):
    if isinstance(x, dict):
        r = '{\n'
        if sort:
            items = sorted(x.items())
        else:
            items = x.iteritems()
        for (key, value) in (items):
            r += (' ' * (indent + 4)) + repr(key) + ': '
            r += drepr(value, sort, indent + 4) + ',\n'
        r = r.rstrip(',\n') + '\n'
        r += (' ' * indent) + '}'
    elif hasattr(x, '__iter__'):
        r = '[\n'
        if sort:
            items = sorted(x)
        else:
            items = x
        for value in (items):
            r += (' ' * (indent + 4)) + drepr(value, sort, indent + 4) + ',\n'
        r = r.rstrip(',\n') + '\n'
        r += (' ' * indent) + ']'
    else:
        r = repr(x)
    return r

def normalize(text):
    if isinstance(text, str):
        try:
            text = text.decode('utf8')
        except:
            try:
                text = text.decode('latin1')
            except:
                text = text.decode('utf8', 'ignore')

    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')

