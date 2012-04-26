# coding: utf-8
'''
Created on 9 jan 2011

@author: Emuller
'''
import os,sys
import urllib,urllib2,re
import string
from xml.dom import minidom
import xbmc,xbmcplugin,xbmcgui,xbmcaddon


class ShoutcastCore(object):
    __addonname__ = "plugin.audio.shoutcastradio"
    __settings__ = sys.modules[ "__main__" ].__settings__    
    __DEVID__ = "th1Cr5jwu-qu_vWJ"
    
    def getHttpResponse(self, url):      
        
        data = urllib.urlencode({})
        headers = { 'Accept-Charset' : 'utf-8' }
        
        request = urllib2.Request(url, data, headers)
        
          
        response = urllib2.urlopen(request)
        encoding = re.findall("charset=([a-zA-Z0-9\-]+)", response.headers['Content-Type'])            
        
        if len(encoding) > 0:            
            responsetext = unicode( response.read(), encoding[0] );
        else:
            responsetext = unicode( response.read(), "utf-8");
            
        response.close()
        return responsetext.encode("utf-8")
    
    def getHttpPostResponse(self, url, parameters):        
         
        data = urllib.urlencode(parameters)    # Use urllib to encode the parameters
        headers = { 'Accept-Charset' : 'utf-8' }
        
        request = urllib2.Request(url, data, headers)
        
        response = urllib2.urlopen(request)    # This request is sent in HTTP POST
        
        #response = urllib2.urlopen(url)
        encoding = re.findall("charset=([a-zA-Z0-9\-]+)", response.headers['Content-Type'])
        
        if len(encoding) > 0:            
            responsetext = unicode( response.read(), encoding[0] );
        else:
            responsetext = unicode( response.read(), "utf-8");
            
        response.close()
        return responsetext.encode("utf-8")
    
    def getXmlResponse(self, url):
        self.log_notice("getXmlResponse from " + url)
        response = urllib2.urlopen(url)
        encoding = re.findall("charset=([a-zA-Z0-9\-]+)", response.headers['content-type'])
        if len(encoding) > 0:            
            responsetext = unicode( response.read(), encoding[0] );
        else:
            responsetext = unicode( response.read(), "utf-8");
        xmldoc = minidom.parseString(responsetext.encode("utf-8"))
        response.close()
        return xmldoc
    
    def getShoutcastGenres(self):
        xmldoc = self.getXmlResponse("http://api.shoutcast.com/genre/primary?k=%s&f=xml" % (self.__DEVID__))
        entries = xmldoc.getElementsByTagName("genre")
        
        genres = []
        for entry in entries:
            genres.append({'title' : entry.getAttribute('name') , 'id' : entry.getAttribute('id') } )

        return genres
    
    def getShoutcastSubGenres(self, id, genre):         
        xmldoc = self.getXmlResponse("http://api.shoutcast.com/genre/secondary?parentid=%s&k=%s&f=xml" % (id, self.__DEVID__))
        
        entries = xmldoc.getElementsByTagName("genre")
        
        subgenres = []
        for entry in entries:
            subgenres.append({'title' : entry.getAttribute('name') , 'id' : entry.getAttribute('id') } )
            
        return subgenres
    
    def getShoutcastStations(self, genre, type, index):      
        xmldoc = self.getXmlResponse("http://api.shoutcast.com/legacy/genresearch?genre=%s&k=%s&f=xml&limit=%s,%s" % (genre, self.__DEVID__, index, (20,40,60,80,100)[int(self.__settings__.getSetting('numresults'))]))
        
        entries = xmldoc.getElementsByTagName("station")
        
        stations = []
        for entry in entries:
            stations.append({ 'id' : entry.getAttribute('id') , 'title' : entry.getAttribute('name'), 'href' : "http://yp.shoutcast.com/sbin/tunein-station.pls?id=%s&k=%s" % (entry.getAttribute('id'), self.__DEVID__), 'playing' : entry.getAttribute('ct'), 'listeners' : entry.getAttribute('lc'), 'bitrate' : entry.getAttribute('br'), 'type' : entry.getAttribute('mt')})
        
                
        hasMore = (len(entries) >= (20,40,60,80,100)[int(self.__settings__.getSetting('numresults'))])
        
        return (stations,hasMore)
    
    def getShoutcastStreams(self, url):
        responsetext = self.getHttpResponse(url)
        matches = re.finditer('File(?P<id>[0-90-9?])=(?P<url>.*).*\n.*Title[0-90-9?]=(?P<title>.*).*\n', responsetext)
        streams = []
        for match in matches:
            streams.append(match.groupdict())
        return streams

    
    def log_notice(self, msg):
        xbmc.output("### [%s] - %s" % (self.__addonname__,msg,),level=xbmc.LOGNOTICE )
        