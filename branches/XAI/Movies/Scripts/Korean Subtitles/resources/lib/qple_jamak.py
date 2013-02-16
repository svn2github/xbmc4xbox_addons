# -*- coding: utf-8 -*-
"""
  Subtitle from Tokplayer(former Qple)
"""
import sys,urllib2,md5
import string,re

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__

def qple_jamak_from_file(f):
  qple_home = 'http://www.tokplayer.com'

  f.seek(100*1024)
  buff1 = f.read(100*1024)    # 100KB starting at 100KB
  f.seek(0)
  buff2 = f.read(50*1024)     # 50KB starting at 0
  f.seek(100*1024)
  buff2 += f.read(50*1024)    # 50KB starting at 100KB

  # calculate MD5 key from file
  m = md5.new(); m.update(buff1); key1 = m.hexdigest()
  m = md5.new(); m.update(buff2); key2 = m.hexdigest()

  queryAddr1 = qple_home+"/app/subtitle/view_subtitle.html?q_hash=%s&q_newhash=%s"%(key1,key2)
  print "search subtitle at %s"%queryAddr1
  try: resp = urllib2.urlopen(queryAddr1)
  except urllib2.URLError, e:
    print e.reason
    return None
  link = resp.read(); resp.close()

  # empty list if found nothing
  match = re.search('''location.replace\('([^']*)'\)''',link)
  if match is None or "/notice/" in match.group(1):
    return []

  # parse result page
  queryAddr2 = qple_home+match.group(1)
  print "parse search result at %s"%queryAddr2
  req = urllib2.Request(queryAddr2)
  req.add_header('Referer', queryAddr1)
  try: resp = urllib2.urlopen(req)
  except urllib2.URLError, e:
    print e.reason
    return None
  link = resp.read(); resp.close()
  link = link.decode('euc-kr').encode('utf-8')

  # regular search result page
  url_match  = re.compile('''<a href="([^"]*)"[^>]*>\[다운로드 링크\]</a>''',re.U).findall(link)
  tit_match = re.compile('''<td class="txt_[^>]*>([^<]*)</td>''').findall(link)
  if len(url_match) == 0 or len(url_match) != len(tit_match): 
    print "Unusual result page, "+queryAddr2
    return []

  ###----- Select a subtitle to download
  title_list = []
  for i in range(0,len(url_match)):
    title_list.append( ('qple', string.strip(tit_match[i]), qple_home+url_match[i]) )
  return title_list

if __name__ == "__main__":
  import os
  f = open(os.path.join('d:'+os.sep,'work','test','test.avi'), 'rb')
  for supl,title,url in qple_jamak_from_file(f):
    print "[%s] %s = %s" % (supl,title,url)
  f.close
# vim: softtabstop=2 shiftwidth=2 expandtab
