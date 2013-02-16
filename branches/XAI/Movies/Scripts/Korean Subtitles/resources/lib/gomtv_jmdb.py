# -*- coding: utf-8 -*-
"""
  Subtitle from GomTV site
"""
import sys,urllib2,md5
import string,re

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__

reqhdr = {'User-Agent': 'GomPlayer 2, 1, 23, 5007 (KOR)'}
gomtv_home  = "http://gom.gomtv.com"

def gomtv_jamak_from_file(f):
  f.seek(0)
  buff = f.read(1024*1024)    # size=1M
  # calculate MD5 key from file
  m = md5.new(); m.update(buff); key = m.hexdigest()

  ###--- Search subtitle in GomTV site
  queryAddr = gomtv_home+"/jmdb/search.html?key=%s"%key
  print "search subtitle at %s"%queryAddr
  req = urllib2.Request(queryAddr, None, reqhdr)
  try: resp = urllib2.urlopen(req)
  except urllib2.URLError, e:
    print e.reason
    return None
  link = resp.read(); resp.close()

  match = re.match('''<script>location.href = '([^']*)';</script>''',link)
  if match:
    url = match.group(1)
    if 'noResult' in url:            # no result (old style)
      print "Unusual result page, "+queryAddr
      return []
    url = gomtv_home+'/jmdb/'+url
    title = gomtv_check_result(url)
    if title:
      return [ ('gomtv', title, url) ]
    else:
      return []            # no result

  link = link.decode('euc-kr').encode('utf-8')
  # regular search result page
  url_match  = re.compile('''<div><a href="([^"]*)">\[([^\]]*)\]([^<]*)</a>''',re.U).findall(link)
  date_match = re.compile('''<td>(\d{4}.\d{2}.\d{2})</td>''').findall(link)
  if len(url_match) == 0 or len(url_match) != len(date_match): 
    print "Unusual result page, "+queryAddr
    return []

  ###----- Select a subtitle to download
  title_list = []
  for i in range(0,len(date_match)):
    title = "[%s] %s (%s)"%(url_match[i][1], string.strip(url_match[i][2]), date_match[i])
    title_list.append( ('gomtv', title, gomtv_home+url_match[i][0]) )
  return title_list

def gomtv_check_result(url):
  req = urllib2.Request(url, None, reqhdr)
  try: resp = urllib2.urlopen(req)
  except urllib2.URLError, e:
    print e.reason
    return None
  link = resp.read(); resp.close()
  if "<div id='search_failed_smi'>" in link:
    print "no result found, "+url
    return ""

  link = link.decode('euc-kr').encode('utf-8')
  # regular search result page
  query = re.compile('''<th>제목</th>\s*<td[^>]*>\s*<strong>\[[^\]]*\]\s*([^<]*)</strong>''',re.U|re.S).search(link)
  return query and query.group(1)

def gomtv_jamak_url(url):
  print "parse subtitle page at %s"%url
  req = urllib2.Request(url, None, reqhdr)
  try: resp = urllib2.urlopen(req)
  except urllib2.URLError, e:
    print e.reason
    return ''
  link = resp.read(); resp.close()
  downid = re.search('''javascript:save[^\(]*\('(\d+)','(\d+)','[^']*'\);''',link).group(1,2)
  return gomtv_home+"/jmdb/save.html?intSeq=%s&capSeq=%s"%downid

if __name__ == "__main__":
  import os
  f = open(os.path.join('d:'+os.sep,'work','test','test.avi'), 'rb')
  for supl,title,url in gomtv_jamak_from_file(f):
    print "[%s] %s = %s" % (supl,title,url)
  f.close
  print "smi: %s" % gomtv_jamak_url(url[0])
  print "no smi: %s" % gomtv_check_result("http://gom.gomtv.com/jmdb/searchCaptionInference.html?fn2=&key=09d595ebdf13a7bc7373cee539b86a0f&skey=")
# vim: softtabstop=2 shiftwidth=2 expandtab
