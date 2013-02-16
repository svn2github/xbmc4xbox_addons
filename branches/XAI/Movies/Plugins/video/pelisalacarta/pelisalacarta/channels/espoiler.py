# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para espoilertv by Soukron
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

import xbmc
import xbmcgui
import xbmcplugin

from core import config
from core import logger
from core import scrapertools
from core import xbmctools
from core import library
from servers import servertools
from pelisalacarta import buscador

CHANNELNAME = "espoilertv"

# Esto permite su ejecucion en modo emulado
try:
   pluginhandle = int( sys.argv[ 1 ] )
except:
   pluginhandle = ""

logger.info("[espoilertv.py] init")
DEBUG = True

def mainlist(params,url,category):
    logger.info("[espoilertv.py] mainlist")

    xbmctools.addnewfolder( CHANNELNAME , "getSearchResults", category , "Hoy"                , "http://espoilertv.com/calendario/?orden=serie","","")
    xbmctools.addnewfolder( CHANNELNAME , "getAlfabetical"  , category , "Listado alfabetico" , "","","")
    xbmctools.addnewfolder( CHANNELNAME , "doSearch"        , category , "Buscar"             , "","","")

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod(     handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory(    handle=int( sys.argv[ 1 ] ), succeeded=True )

def getAlfabetical(params, url, category):
    logger.info("[espoilertv.py] getAlfabetical")

    itemlist = getAlfabeticalList()

    for item in itemlist:
        xbmctools.addnewfolder(item.channel , item.action , category , item.title , item.url ,"","")

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod(     handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory(    handle=int( sys.argv[ 1 ] ), succeeded=True )

def getAlfabeticalList():
    logger.info("espoilertv.py] getAlfabeticalList")

    from core.item import Item
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="A", url="http://espoilertv.com/filtro/?b=A") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="B", url="http://espoilertv.com/filtro/?b=B") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="C", url="http://espoilertv.com/filtro/?b=C") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="D", url="http://espoilertv.com/filtro/?b=D") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="E", url="http://espoilertv.com/filtro/?b=E") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="F", url="http://espoilertv.com/filtro/?b=F") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="G", url="http://espoilertv.com/filtro/?b=G") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="H", url="http://espoilertv.com/filtro/?b=H") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="I", url="http://espoilertv.com/filtro/?b=I") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="J", url="http://espoilertv.com/filtro/?b=J") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="K", url="http://espoilertv.com/filtro/?b=K") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="L", url="http://espoilertv.com/filtro/?b=L") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="M", url="http://espoilertv.com/filtro/?b=M") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="N", url="http://espoilertv.com/filtro/?b=N") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="O", url="http://espoilertv.com/filtro/?b=O") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="P", url="http://espoilertv.com/filtro/?b=P") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="Q", url="http://espoilertv.com/filtro/?b=Q") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="R", url="http://espoilertv.com/filtro/?b=R") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="S", url="http://espoilertv.com/filtro/?b=S") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="T", url="http://espoilertv.com/filtro/?b=T") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="U", url="http://espoilertv.com/filtro/?b=U") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="V", url="http://espoilertv.com/filtro/?b=V") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="W", url="http://espoilertv.com/filtro/?b=W") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="X", url="http://espoilertv.com/filtro/?b=X") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="Y", url="http://espoilertv.com/filtro/?b=Y") )
    itemlist.append( Item(channel=CHANNELNAME, action="getSearchResults", title="Z", url="http://espoilertv.com/filtro/?b=Z") )

    return itemlist

def doSearch(params, url, category):
    logger.info("[espoilertv.py] doSearch")

    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            #convert to HTML
            tecleado = tecleado.replace(" ", "+")
            searchUrl = "http://espoilertv.com/filtro/?b="+tecleado
            params["title"]="Z"
            getSearchResults(params, searchUrl, category)
            
def getSearchResults(params, url, category):
    logger.info("[espoilertv.py] getSearchResults")

    title = urllib.unquote_plus( params.get("title") )

    data = scrapertools.cachePage(url)
    patronvideos = '<div class="ajax" id="ajaxSerie(.*?)">.*?<img class="tapa".*?src="(.*?)" alt="(.*?)" />'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:      
        scrapedtitle = match[2]
        scrapedthumbnail = match[1]
        scrapedplot= ""
        scrapedid=match[0]
        scrapedurl = "http://espoilertv.com/ajax/temporadas.php?idserie="+match[0]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            
        xbmctools.addnewfolder(CHANNELNAME, "getShowInfo" , category , scrapedtitle , scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot )

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod(     handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory(    handle=int( sys.argv[ 1 ] ), succeeded=True )

def getShowInfo(params, url, category):
    logger.info("[espoilertv.py] getShowInfo")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = params.get("thumbnail")
    plot = params.get("plot")
    id = params.get("id")
    
    data = scrapertools.cachePage(url)
    patronvideos = '<li style="cursor:pointer" name="botonesTemps.*?" onclick="muestroTempNro\(.*?, (.*?)\)" class=".*?">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        data2 = scrapertools.cachePage(url+"&temporada="+match[0])
        patronvideos2 = '<p onclick="abroCierroDescargas\(.*?,'+match[0]+',(.*?),'+match[0]+'\)" style="cursor:pointer" title="(.*?) (.*?)">'
        matches2 = re.compile(patronvideos2,re.DOTALL).findall(data2)
        scrapertools.printMatches(matches2)

        for match2 in matches2:
            if (int(match2[0]) > 0): xbmctools.addnewfolder(CHANNELNAME, "getEpisodeInfo", category, "Episodio "+match[0]+"x"+match2[0]+" - "+match2[2], url, thumbnail, plot )

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod(     handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory(    handle=int( sys.argv[ 1 ] ), succeeded=True )

def getEpisodeInfo(params, url, category):
    logger.info("[espoilertv.py] getEpisodeInfo")