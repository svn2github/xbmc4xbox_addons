#!/usr/bin/python
# icescraper.py
# example scraping service

import urllib2, urllib, sys, os, re
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

DB_TYPE = 	''		# mysql | sqlite
DB_ADDRESS = 	''		# mysql server address
DB_NAME = 	''		# mysql database name
DB_USER = 	''		# mysql username
DB_PASS = 	''		# mysql password
DB_FILE = 	''		# XBMC sqlite database file ie. /path/to/MyVideosXX.db
TV_SHOWS_PATH = ''		# Set path to tv shows


if DB_TYPE == 'mysql':
	try:	
		import mysql.connector as database
		DBH = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
	except:
		import MySQLdb as database
		DBH=database.connect(host=DB_ADDRESS,user=DB_USER,passwd=DB_PASS,db=DB_NAME)
	DBC = DBH.cursor()
else:
	try:
    		from sqlite3 import dbapi2 as sqlite
    		print "Loading sqlite3 as DB engine"
	except:
    		from pysqlite2 import dbapi2 as sqlite
    		print "Loading pysqlite2 as DB engine"
	DBH = sqlite.connect(DB_FILE)
	DBC = DBH.cursor()

ICEFILMS_URL = "http://www.icefilms.info"
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'




def getFavorites():
	SQL = "SELECT url, name FROM ice_favorites ORDER BY name ASC"
	DBC.execute(SQL)
	rows = DBC.fetchall()
	for row in rows:
		print row[1]        		
		getEpisodes(row[0], row[1])


def getEpisodes(url, show_name):
	print "Getting episodes for: " + show_name
	page = ICEFILMS_URL + url
	pagedata = GetURL(page)
	if pagedata=='':
		return False
	month = [' ','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	month_nr = [' ','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	soup = BeautifulSoup(pagedata)
	list = soup.find("span", { "class" : "list" })
	stars = list.findAll("img", { "class" : "star" })
	year_loc = soup.findAll( "a", {"name" : re.compile(r"[0-9]{4}")})
	print year_loc
	for y in year_loc:
		season = y['name']
		b = y.parent.nextSibling
		while getattr(b, 'name', None) != 'h3':
			try:
				if getattr(b, 'name', None) == 'img':
					a = b.findNextSibling('a')
					name_split = re.split(r'[^a-zA-Z0-9_]',str(a.string))
					try:
						name = season+'.'+month_nr[month.index(name_split[0])]+'.'+name_split[1]
					except ValueError:
						name = name_split[1]
					href = a['href']
					if re.search('\\(\\d\\d\\d\\d\\)$', show_name):
						has_year = True
					else:
						has_year = False
					show_path = os.path.join(TV_SHOWS_PATH, CleanFileName(show_name, has_year, use_encoding = True))
					#CreateDirectory(show_path)		
					season_path = os.path.join(show_path, 'Season ' + season)
					#CreateDirectory(season_path)
					sname = CleanFileName(show_name, has_year, False, False)
					#CreateStreamFile(name, href, season_path, False, showid, show_name=sname)	
				b = b.nextSibling
			except AttributeError:
				break
	for star in stars: 
		a = star.findNextSibling('a')
		name = str(a.string)
		href = a['href']
		save_episode = True
		
		#Get the season number
		season = name.split("x")[0]
		try:
			int(season)
		except:
			if EXCLUDE_PROBLEM_EPISODES:
				#print show_name, season
				save_episode = False
			else:
				season = "0"
		if save_episode:
			if re.search('\\(\\d\\d\\d\\d\\)$', show_name):
				has_year = True
			else:
				has_year = False
			show_path = os.path.join(TV_SHOWS_PATH, CleanFileName(show_name, has_year, use_encoding = True))
			CreateDirectory(show_path)
			season_path = os.path.join(show_path, 'Season ' + season)
			CreateDirectory(season_path)
			sname = CleanFileName(show_name, has_year, False, False)		
			CreateStreamFile(name, href, season_path, False, show_name=sname)


def GetURL(url, params = None, referrer = ICEFILMS_URL, cookie = None, save_cookie = False):
	if params:
		req = urllib2.Request(url, params)
	else:
		req = urllib2.Request(url)

	req.add_header('User-Agent', USER_AGENT)
	if referrer:
		req.add_header('Referer', referrer)
	if cookie:
		req.add_header('Cookie', cookie)

	print url
	
	try:
		response = urllib2.urlopen(req)
		body = response.read()
	except:
		print "Failed to connect to Icefilms.info"
		return ''

	if save_cookie:
		setcookie = response.info().get('Set-Cookie', None)
		#print "Set-Cookie: %s" % repr(setcookie)
		if setcookie:
			setcookie = re.search('([^=]+=[^=;]+)', setcookie).group(1)
			body = body + '<cookie>' + setcookie + '</cookie>'

	response.close()
	return body

def CreateStreamFile(name, href, dir, remove_year, show_name=''):
	cur = db.cursor()	
	try:
		
		if len(show_name) > 0:
			show_name = show_name + ' '
		filename = CleanFileName(name, remove_year) + ".strm"
		path = os.path.join(dir, filename)
		strm_string = "plugin://video/icelibrary24xbox/?href=" + urllib.quote(href) + "&mode=10&name=" + urllib.quote(show_name + name) + "&path=" + urllib.quote(path)

		if os.path.exists(path):
			#print "Exists: " + path
			return False
		file = open(path,'w')
		file.write(strm_string)
		file.close()
	except:
		print "Error while creating strm file for : " + name

def CleanFileName(s, remove_year, use_encoding = False, use_blanks = True):
	if remove_year:
		s = s[0:len(s)-7]
	s = s.replace(' (Eng subs)', '')
	s = s.replace(' (eng subs)', '')
	s = s.replace(' (English subs)', '')
	s = s.replace(' (english subs)', '')
	s = s.replace(' (Eng Subs)', '')
	s = s.replace(' (English Subs)', '')
	s = s.replace('&#x26;', '&')
	s = s.replace('&#x27;', '\'')
	s = s.replace('&#xC6;', 'AE')
	s = s.replace('&#xC7;', 'C')
	s = s.replace('&#xF4;', 'o')
	s = s.replace('&#xE9;', 'e')
	s = s.replace('&#xEB;', 'e')
	s = s.replace('&#xED;', 'i')
	s = s.replace('&#xEE;', 'i')
	s = s.replace('&#xA2;', 'c')
	s = s.replace('&#xE2;', 'a')
	s = s.replace('&#xEF;', 'i')
	s = s.replace('&#xE1;', 'a')
	s = s.replace('&#xE8;', 'e')
	s = s.replace('%2E', '.')
	if use_encoding:
		s = s.replace('"', '%22')
		s = s.replace('*', '%2A')
		s = s.replace('/', '%2F')
		s = s.replace(':', ',')
		s = s.replace('<', '%3C')
		s = s.replace('>', '%3E')
		s = s.replace('?', '%3F')
		s = s.replace('\\', '%5C')
		s = s.replace('|', '%7C')
		s = s.replace('&frac12;', '%BD')
		s = s.replace('&#xBD;', '%BD') #half character
		s = s.replace('&#xB3;', '%B3')
		s = s.replace('&#xB0;', '%B0') #degree character		
	if use_blanks:
		s = s.replace('"', ' ')
		s = s.replace('*', ' ')
		s = s.replace('/', ' ')
		s = s.replace(':', ' ')
		s = s.replace('<', ' ')
		s = s.replace('>', ' ')
		s = s.replace('?', ' ')
		s = s.replace('\\', ' ')
		s = s.replace('|', ' ')
		s = s.replace('&frac12;', ' ')
		s = s.replace('&#xBD;', ' ') #half character
		s = s.replace('&#xB3;', ' ')
		s = s.replace('&#xB0;', ' ') #degree character
	s = s.strip()
	return s

def CreateDirectory(dir_path):
	dir_path = dir_path.strip()
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

def FileAlreadyExist(filename, files):
	for file in files:
		if filename == file:
			return True			
	return False


getFavorites()

