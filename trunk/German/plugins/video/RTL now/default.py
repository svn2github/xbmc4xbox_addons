import xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp

thisPlugin = int(sys.argv[1])

urlHost = "http://rtl-now.rtl.de"
ajaxUrl = "/xajaxuri.php"
# -----regexContent-------
# [0] is url (/foo.php)
# [1] is name (foo is bar)
# ------------------------
# -----regexSeries--------
# [0] is class even or odd 
# [1] is url to videourl
# [2] is title
# [3] is time
# All content is in!
# the free-content will be filtered in code (paytype)

regexContent = '<div class="seriennavi_free" style=""><a href="(.*?)".*?>FREE.*?</div>.*?<div style="" class="seriennavi_link">.*?">(.*?)</a>.*?</div>'
regexSeries = '<div class="line (even|odd)"><div onclick="link\(\'(.*?)\'\); return false;".*?<a href=".*?" title=".*?">(.*?)</a>.*?class="time">(.*?</div>.*?)</div>.*?class="minibutton">(.*?)</a></div></div>'
regexVideoData = "data:'(.*?)'"
regexXML = '<filename.*?><!\[CDATA\[(.*?)\]\]></filename>'
regexTextOnly = '<\s*\/?\s*\s*.*?>'
regexTabVars = '<select\s*?onchange.*?xajax_show_top_and_movies.*?\'(.*?)\'.*?\'(.*?)\'.*?\'(.*?)\'.*?\'(.*?)\'.*?\'(.*?)\'.*?>(.*?)</select>'
regexTabEntry = '<option.*?value=\'(\d)\'.*?>'
# ------------------------

def showContent():
	global thisPlugin

	content = getUrl(urlHost)
	match = re.compile(regexContent,re.DOTALL).findall(content)
	for m in match:
		addDirectoryItem(m[1].strip(), {"urlS": m[0]})  
		#print m[0]
	print "--- showContent ok"	
	xbmcplugin.endOfDirectory(thisPlugin)

def showSeries(urlS):
	global thisPlugin

	content = getUrl(urlS)

	vars = re.compile(regexTabVars,re.DOTALL).search(content)
	
	if vars:
		tabVars = "&xajaxargs[]="+vars.group(1)+"&xajaxargs[]="+vars.group(2)+"&xajaxargs[]="+vars.group(3)+"&xajaxargs[]="+vars.group(4)+"&xajaxargs[]="+vars.group(5)+"&xajax=show_top_and_movies&xajaxr="+str(time.time()).replace('.','')
		tabentries = re.compile(regexTabEntry,re.DOTALL).findall(vars.group(6))
		content = ""
		
		for te in tabentries:
			ajcon = postUrl(urlHost+ajaxUrl,"xajaxargs[]="+te+tabVars);
			content += ajcon;

	match = re.compile(regexSeries,re.DOTALL).findall(content)
	print match
	for m in match:
		print m
		if "kostenlos" in m[4]:
		##xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=m[3]+" "+decode_htmlentities(m[2]), isFolder=False)
			addPlayableItem(decode_htmlentities(m[2])+" - "+remHTML(m[3]), {"urlV": m[1], "vidN": m[2]})
		##print m[2]  
	print "--- showSeries ok"	
	xbmcplugin.endOfDirectory(thisPlugin)

def showVideo(urlV, vidN):
	print "--- showVideo"
	global thisPlugin
	print "--- "+urlV
	content = getUrl(urlV)
	match=re.compile(regexVideoData).findall(content)
	xmlUrl = urlHost+urllib.unquote(match[0])
	print "--- "+xmlUrl
	contentB = getUrl(xmlUrl)
	print contentB
	matchfilename = re.compile(regexXML).findall(contentB)
	splitted = matchfilename[0].split('/')
	print "------DebugOutput showVideo--"	
	print splitted
	# -----
	videoUrl=splitted[0]+"//"+splitted[2]+"/"+splitted[3]+"/"
	videoUrlB=splitted[2]+"/"+splitted[3]+"/"
	addpre=""	
	if splitted[5][-4:-1] == ".f4":
		addpre="mp4:"
	if splitted[5][-4:-1] == ".fl":
		splitted[5]=splitted[5][0:-4]

	playpath = addpre+splitted[4]+"/"+splitted[5]
	
	print "playPath -- "+playpath


	swfUrl = "http://rtl-now.rtl.de/includes/vodplayer.swf"
	pageUrl = "http://rtl-now.rtl.de/p"
	item = xbmcgui.ListItem(vidN)

	fullData=videoUrl+' swfVfy=1 playpath='+playpath+' app=rtlnow/_definst_ pageUrl='+pageUrl+'/ tcUrl='+videoUrl+' swfUrl='+swfUrl 
	print fullData
	print "------------"
	listitem = xbmcgui.ListItem(path=fullData)
	return xbmcplugin.setResolvedUrl(thisPlugin, True, listitem)
	

# ------ helper ------

def remHTML(text):
	result = re.compile(regexTextOnly,re.DOTALL).sub('',text)
	return result

def postUrl(url, values):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req, values)
    link=response.read()
    response.close()
    return link

def getUrl(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

def addPlayableItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    li.setInfo( type="Video", infoLabels={ "Title": name } )
    li.setProperty('IsPlayable', 'true')
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=False)
	
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def substitute_entity(match):
    ent = match.group(3)
    
    if match.group(1) == "#":
        if match.group(2) == '':
            return unichr(int(ent))
        elif match.group(2) == 'x':
            return unichr(int('0x'+ent, 16))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode_htmlentities(string):
    entity_re = re.compile(r'&(#?)(x?)(\w+);')
    return entity_re.subn(substitute_entity, string)[0]

# ----- main -----

params = parameters_string_to_dict(sys.argv[2])
urlSeries = str(params.get("urlS", ""))
urlVideo = str(params.get("urlV", ""))
vidName = str(params.get("vidN", ""))

if not sys.argv[2]:
	# new start
	ok = showContent()
else:
	if urlSeries:
		newUrl = urlHost + urllib.unquote(urlSeries)
		print newUrl
		ok = showSeries(newUrl)
	if urlVideo:
		newUrl = urlHost + decode_htmlentities(urllib.unquote(urlVideo))
		print newUrl
		ok = showVideo(newUrl, decode_htmlentities(urllib.unquote_plus(vidName)))