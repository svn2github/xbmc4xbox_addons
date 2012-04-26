#/bin/python
# -*- coding: utf-8 -*-

import os
import xbmcplugin
import xbmcgui
import re
import geturllib
import mycgi

gPluginName  = 'plugin.video.demand5'
gPluginHandle = int(sys.argv[1])
gBaseURL = sys.argv[0]


#==============================================================================
# ShowCategories
#
# List the programme categories in same order as http://www.channel5.com/shows
# NOTE: the category list is hard-coded
#==============================================================================

def ShowCategories():
	categories = [ 'Entertainment', 'Drama', 'Documentary', 'Soap', 'Milkshake!', 'Sport', 'Films' ]
	
	listItems = []
	# Start with a Search entry
	#newListItem = xbmcgui.ListItem( "Search" )
	#url = gBaseURL + '?search=1'
	#listItems.append( (url,newListItem,True) )
	for category in categories:
		newListItem = xbmcgui.ListItem( label = category )
		genre = category.lower()
		url = gBaseURL + '?category=' + mycgi.URLEscape(genre) + '&title=' + mycgi.URLEscape(category)
		listItems.append( (url,newListItem,True) )
	xbmcplugin.addDirectoryItems( handle=gPluginHandle, items=listItems )
	xbmcplugin.endOfDirectory( handle=gPluginHandle, succeeded=True )

#==============================================================================

def ShowCategory( category ):
	# Get the page with the category shows
	html = geturllib.GetURL( "http://www.channel5.com/shows?availability=on-demand&genre=%s" % category, 20000 ) # ~6 hrs
	
	# Extract the shows list section
	html = re.search( '<ul class="resource_list shows shows_index">(.*?)</ul>', html, re.DOTALL).groups()[0]
	
	# Remove the advert blocks which would otherwise complicate the show parsing
	p = re.compile( '<li class="mpu_wrapper">.*?</li>', re.DOTALL)
	html = re.sub( p, '', html )
	
	# Parse out the shows
	showsInfo = re.findall( '<li.*?<a href="(.*?)".*?<img.*?src="(.*?)".*?<em>(.*?)</em>.*?</li>', html, re.DOTALL )
	
	listItems = []
	for showInfo in showsInfo:
		showPath = showInfo[0]
		thumbnail = showInfo[1] 
		showTitle = showInfo[2]
		
		# Fix encoded characters
		showTitle = showTitle.replace( "&amp;", "&" )
		showTitle = showTitle.replace( "&quot;", '"' )
		showTitle = showTitle.replace( "&pound;", '£' )
		
		# Titles which really begin with "The " are shown on website with suffix ", The". Let's fix that:
		if ( showTitle.endswith(', The') ):
			showTitle = "The " + showTitle.replace( ', The', '' )
		
		newListItem = xbmcgui.ListItem( showTitle )
		newListItem.setThumbnailImage(thumbnail)
		url = gBaseURL + '?category=' + category + '&show=' + mycgi.URLEscape(showPath) + '&title=' + mycgi.URLEscape(showTitle)
		listItems.append( (url,newListItem,True) )
	
	xbmcplugin.addDirectoryItems( handle=gPluginHandle, items=listItems )
	xbmcplugin.endOfDirectory( handle=gPluginHandle, succeeded=True )

#==============================================================================

def ShowEpisodes( showId, showTitle ):
	# Get the page with episodes for this show
	print "Looking for episodes for: " + showTitle
	url = "http://www.channel5.com" + showId + "/episodes"

        html    = geturllib.GetURL( url, 20000 ) # ~6 hrs  
	epsInfo = re.findall( 'episodes\?season=(.*?)">(.*?)</a>', html, re.DOTALL )
 		
	for season, series in epsInfo:                      
            ParseEpisodes(url+"?season="+season, showTitle, series)

        if len(epsInfo) == 0:
            ParseEpisodes(url, showTitle)

        xbmcplugin.endOfDirectory( handle=gPluginHandle, succeeded=True )

def ParseEpisodes(url, showTitle, series = ""):      	

        print "URL: " + url
        html = geturllib.GetURL( url, 20000 ) # ~6 hrs  

	listItems = []
	# Does this show have multiple episodes?
	x = re.search( '<ul class="resource_list episodes">(.*?)<!-- /#contents -->', html, re.DOTALL)
	if ( x != None ):
		# Extract the section with the episode list
		html = x.groups()[0]
		
		# Parse out the episodes
		epsInfo = re.findall( '<li class="clearfix">.*?<a href="(.*?)".*?<img .*?src="(.*?)".*?<h3><a.*?>(.*?)</a>.*?<p class="description">(.*?)</p>(.*?)</div>', html, re.DOTALL )
		
		for epInfo in epsInfo:
			href = epInfo[0]
			thumbnail = epInfo[1] 
			title = epInfo[2]
			description = epInfo[3]
			x = epInfo[4]
			
			title = title.replace( '&amp;', '&' )
			title = title.replace( "&quot;", '"' )
			title = title.replace( "&pound;", '£' )
			
			fn = showTitle + " - " + title
			fn = re.sub('[:\\/*?\<>|"]+', '.', fn)
			
			if ( re.search( 'vod_availability', x, re.DOTALL) ): 
                                fullTitle = title
                                if series != "":
                                    fullTitle = series + ": " + fullTitle                                 
				newListItem = xbmcgui.ListItem(fullTitle)
				newListItem.setThumbnailImage(thumbnail)
				newListItem.setInfo('video', {'Title': title, 'Plot': description, 'PlotOutline': description})
				url = gBaseURL + '?ep=' + mycgi.URLEscape(href) + "&title=" + mycgi.URLEscape(title) + "&fn=" + mycgi.URLEscape(fn)
					
				listItems.append( (url,newListItem,False) )
	else:
		title = re.search( '<h3 class="episode_header"><span class="sifr_grey_light">(.*?)</span></h3>', html, re.DOTALL ).groups()[0]
		description = re.search( 'property="og:description" content="(.*?)"', html, re.DOTALL ).groups()[0]
		thumbnail = re.search( 'property="og:image" content="(.*?)"', html, re.DOTALL ).groups()[0]
		href = re.search( 'property="og:url" content="(.*?)"', html, re.DOTALL ).groups()[0]
		
		href = re.search( '(/shows.*)', href ).groups()[0]
		thumbnail = thumbnail.replace( 'facebook_with_play', 'large_size' )
		
		if ( title <> showTitle ):
			fn = showTitle + " - " + title
		else:
			fn = showTitle
		
		url = gBaseURL + '?ep=' + mycgi.URLEscape(href) + "&title=" + mycgi.URLEscape(title) + "&fn=" + mycgi.URLEscape(fn)
		
		newListItem = xbmcgui.ListItem(title)
		newListItem.setThumbnailImage(thumbnail)
		newListItem.setInfo('video', {'Title': title, 'Plot': description, 'PlotOutline': description})
		
		listItems.append( (url,newListItem,False) )
		
	xbmcplugin.addDirectoryItems( handle=gPluginHandle, items=listItems )
	#xbmcplugin.endOfDirectory( handle=gPluginHandle, succeeded=True )

#==============================================================================


def PlayOrDownloadEpisode( episodeId, title, defFilename='' ):
	import xbmcaddon
	
	addon = xbmcaddon.Addon(id=gPluginName)
	action = addon.getSetting( 'select_action' )
	if ( action == 'Ask' ):
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(title, 'Do you want to play or download?', '', '', 'Download',  'Play') # 1=Play; 0=Download
	elif ( action == 'Download' ):
		ret = 0
	else:
		ret = 1
	
	if ( ret == 1 ):
		# Play
		url = "http://www.channel5.com" + episodeId
		html = geturllib.GetURL( url, 3600 )
		refId = re.search( 'videoPlayer=ref:(.*?)&', html, re.DOTALL).groups()[0]
		Play( refId, title )
	else:
		# Download
		# Ensure rtmpdump has been located
		rtmpdump_path = addon.getSetting('rtmpdump_path')
		if ( rtmpdump_path is '' ):
			d = xbmcgui.Dialog()
			d.ok('Download Error','You have not located your rtmpdump executable.\n Please update the addon settings and try again.','','')
			addon.openSettings(sys.argv[ 0 ])
			return
			
		# Ensure default download folder is defined
		downloadFolder = addon.getSetting('download_folder')
		if downloadFolder is '':
			d = xbmcgui.Dialog()
			d.ok('Download Error','You have not set the default download folder.\n Please update the addon settings and try again.','','')
			addon.openSettings(sys.argv[ 0 ])
			return
			
		if ( addon.getSetting('ask_filename') == 'true' ):
			kb = xbmc.Keyboard( defFilename, 'Save programme as...' )
			kb.doModal()
			if (kb.isConfirmed()):
				filename = kb.getText()
			else:
				return
		else:
			filename = defFilename
		
		if ( filename.endswith('.flv') == False ): 
			filename = filename + '.flv'
		
		if ( addon.getSetting('ask_folder') == 'true' ):
			dialog = xbmcgui.Dialog()
			downloadFolder = dialog.browse(  3, 'Save to folder...', 'files', '', False, False, downloadFolder )
			if ( downloadFolder == '' ):
				return
				
		filename = re.sub('[:\\/*?\<>|"]+', '', filename)
		savePath = os.path.join( "T:"+os.sep, downloadFolder, filename )
		from subprocess import Popen, PIPE, STDOUT
		
		url = "http://www.channel5.com" + episodeId
		html = geturllib.GetURL( url, 3600 )
		refId = re.search( 'videoPlayer=ref:(.*?)&', html, re.DOTALL).groups()[0]
		cmdline = CreateRTMPDUMPCmd( refId, rtmpdump_path, savePath )
		print "COMMAND LINE: " + cmdline
		xbmc.executebuiltin('XBMC.Notification(4oD,Starting download: %s)' % filename)
		p = Popen( cmdline, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT )
		x = p.stdout.read()
		import time 
		while p.poll() == None:
			time.sleep(2)
			x = p.stdout.read()
			
		xbmc.executebuiltin("XBMC.Notification(Download Finished!,"+filename+",2000)")
	return

#==============================================================================

def Play( refId, title ):
	playerKey = '8e8e110bb9d7d95eb3c3e500a86a21024eccd983'
	url = 'http://www.channel5.com/shows'
	#playerID = '105253688001'
	playerID = '1384899516001'
	x = get_episode_info( playerKey, refId, url, playerID )
	z = x['programmedContent']
	y = z['videoPlayer']
	x = y['mediaDTO']
	w = x['renditions']
	y = w[0]
	u = y['defaultURL']
	u = u.replace( '.com/', '.com:1935/' )
	u = u.replace( '.net/', '.net:1935/' )
	playpath = re.search( '(mp4:.*)', u, re.DOTALL ).groups()[0]
	u = u + " pswfvfy=true swfurl=" + "http://admin.brightcove.com/viewer/us20111026.1813/connection/ExternalConnection_2.swf"
	url = re.findall( '(.*?)mp4:', u, re.DOTALL )[0]
	swfplayer = "http://admin.brightcove.com/viewer/us20111026.1813/connection/ExternalConnection_2.swf"
	playURL = "%s playpath=%s swfurl=%s swfvfy=true" % (url,playpath,swfplayer)
	print "PLAY URL: " + playURL
	
	li = xbmcgui.ListItem(title)
	li.setInfo('video', {'Title': title})
	xbmc.Player().play( playURL, li )

#==============================================================================

def CreateRTMPDUMPCmd( refId, rtmpdump_path, savePath ):
	playerKey = '8e8e110bb9d7d95eb3c3e500a86a21024eccd983'
	url = 'http://www.channel5.com/shows'
	#playerID = '105253688001'
	playerID = '1384899516001'
	x = get_episode_info( playerKey, refId, url, playerID )
	z = x['programmedContent']
	y = z['videoPlayer']
	x = y['mediaDTO']
	w = x['renditions']
	y = w[0]
	u = y['defaultURL']
	u = u.replace( '.com/', '.com:1935/' )
	u = u.replace( '.net/', '.net:1935/' )
	rtmpUrl = re.findall( '(.*?)mp4:', u, re.DOTALL )[0]
	app = re.search( '1935/(.*?)mp4:', u, re.DOTALL ).groups()[0]
	swfplayer = "http://admin.brightcove.com/viewer/us20111026.1813/connection/ExternalConnection_2.swf"
	playpath = re.search( '(mp4:.*)', u, re.DOTALL ).groups()[0]
	
	args = [
				rtmpdump_path,
				"--rtmp", '"%s"' % rtmpUrl,
				#"--app", '"%s"' % app,
				"--flashVer", '"WIN 11,0,1,152"',
				"--swfVfy", '"%s"' % swfplayer,
				"--conn", "Z:",
				"--playpath", '"%s"'%playpath,
				"-o", '"%s"' % savePath,
				"--verbose"
				]
	cmdline = ' '.join(args)
		
	return cmdline
	
#==============================================================================

class ViewerExperienceRequest(object):
	def __init__(self, URL, contentOverrides, experienceId, playerKey, TTLToken=''):
		self.TTLToken = TTLToken
		self.URL = URL
		self.deliveryType = float(0)
		self.contentOverrides = contentOverrides
		self.experienceId = experienceId
		self.playerKey = playerKey

class ContentOverride(object):
	def __init__(self, contentId, contentType=0, target='videoPlayer'):
		self.contentType = contentType
		self.contentId = contentId
		self.target = target
		self.contentIds = None
		self.contentRefId = None
		self.contentRefIds = None
		self.contentType = 0
		self.featureId = float(0)
		self.featuredRefId = None

def build_amf_request(key, content_refid, url, exp_id):
	from pyamf import register_class
	from pyamf import remoting
	
	const = '686a10e2a34ec3ea6af8f2f1c41788804e0480cb'
	register_class(ViewerExperienceRequest, 'com.brightcove.experience.ViewerExperienceRequest')
	register_class(ContentOverride, 'com.brightcove.experience.ContentOverride')
	content_override = ContentOverride(0)
	content_override.contentRefId = content_refid
	viewer_exp_req = ViewerExperienceRequest(url, [content_override], int(exp_id), key)
	
	env = remoting.Envelope(amfVersion=3)
	env.bodies.append(
	(
		"/1",
		remoting.Request(
			target="com.brightcove.experience.ExperienceRuntimeFacade.getDataForExperience",
			body=[const, viewer_exp_req],
			envelope=env
			)
		)
	)
	return env
		

def get_episode_info(key, content_refid, url, exp_id):
	import httplib
	from pyamf import remoting
	
	conn = httplib.HTTPConnection("c.brightcove.com")
	envelope = build_amf_request(key, content_refid, url, exp_id)
	conn.request("POST", "/services/messagebroker/amf?playerKey="+key, str(remoting.encode(envelope).read()),{'content-type': 'application/x-amf'})
	response = conn.getresponse().read()
	response = remoting.decode(response).bodies[0][1].body
	return response

#==============================================================================
   
if __name__ == "__main__":
	try:
		geturllib.SetCacheDir( xbmc.translatePath(os.path.join( "T:"+os.sep,"addon_data", gPluginName,'cache' )) )
		
		if ( mycgi.EmptyQS() ):
			ShowCategories()
		else:
			(category, showId, episodeId, title, search) = mycgi.Params( 'category', 'show', 'ep', 'title', 'search' )
			print "search: " + search
			if ( search <> '' ):
				DoSearch()
			elif ( showId <> '' ):
				ShowEpisodes( showId, title )
			elif ( category <> '' ):
				ShowCategory( category )
			elif ( episodeId <> '' ):
				PlayOrDownloadEpisode( episodeId, title, mycgi.Param('fn') )
	except:
		# Make sure the text from any script errors are logged
		import traceback
		traceback.print_exc(file=sys.stdout)
		raise