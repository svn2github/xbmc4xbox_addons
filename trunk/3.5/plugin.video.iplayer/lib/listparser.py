#
# Provides a simple and very quick way to parse list feeds
#

import re, utils, sys

from xml.etree import ElementTree as ET

if sys.version_info >= (2, 7):
    import json as _json
else:
    import simplejson as _json

datematch = re.compile(':\s+([0-9]+)/([0-9]+)/([0-9]{4})')

class listentry(object):
     def __init__(self, title=None, id=None, updated=None, summary=None, categories=None, series=None, episode=None, thumbnail=None):
         self.title      = title
         self.id         = id
         self.updated    = updated
         self.summary    = summary
         self.categories = categories
         self.series     = series
         self.episode    = episode
         self.thumbnail  = thumbnail

class listentries(object):
     def __init__(self):
         self.entries = []

def parse(data, format):
    ret = None
    if format == 'xml':
        ret = parse_xml(data)
    if format == 'json':
        ret = parse_json(data)
    return ret

def parse_json(json):
    try:
        json = _json.loads(json)
    except:
        return None
    
    elist = listentries()
    for entry in json['blocklist']:
        title = entry['complete_title']
        id = entry['id']
        updated = entry['updated']
        
        if 'synopsis' in entry:
            summary = entry['synopsis']
        else:
            summary = None

        thumbnail = entry['my_image_base_url'] + id + "_640_360.jpg"
        
        series = entry['toplevel_container_title']
        
        if 'position' in entry and len(entry['position']) > 0:
            episode = entry['position']
            episode = int(episode)
        else:
            episode = None

        match = datematch.search(title)
        if match:
            # if the title contains a data at the end use that as the updated date YYYY-MM-DD
            updated = "%s-%s-%s" % ( match.group(3), match.group(2), match.group(1) )

        e_categories = []
        for category in entry['categories']:
            e_categories.append(category['short_name'])

        elist.entries.append(listentry(title, id, updated, summary, e_categories, series, episode, thumbnail))

    return elist

def parse_xml(xml):

    xml = utils.xml_strip_namespace(xml)

    try:
        root = ET.fromstring(xml)
    except:
        return None

    elist = listentries()
    for entry in root.getiterator('episode'):
        title = entry.find('complete_title').text
        id = entry.find('id').text
        updated = entry.find('updated').text
        summary = entry.find('synopsis').text
        thumbnail = entry.find('my_image_base_url').text + id + "_640_360.jpg"

        series = entry.find('toplevel_container_title').text
        episode = entry.find('position').text
        if episode is not None:
            episode = int(episode)

        match = datematch.search(title)
        if match:
            # if the title contains a data at the end use that as the updated date YYYY-MM-DD
            updated = "%s-%s-%s" % ( match.group(3), match.group(2), match.group(1) )

        e_categories = []
        for category in entry.find('categories').findall('category'):
            e_categories.append(category.find('short_name').text)

        elist.entries.append(listentry(title, id, updated, summary, e_categories, series, episode, thumbnail))

    return elist
