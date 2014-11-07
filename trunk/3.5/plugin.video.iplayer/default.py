#/bin/python

import sys, os, re, time
import urllib, cgi
from socket import setdefaulttimeout
import traceback
import operator

import xbmc, xbmcgui, xbmcplugin
import utils

__addoninfo__ = utils.get_addoninfo()
__addon__ = __addoninfo__["addon"]
__version__ = __addoninfo__["version"]

sys.path.insert(0, os.path.join(__addoninfo__['path'], 'lib'))

try:
    import iplayer2 as iplayer
    import iplayer_search
except ImportError, error:
    print error
    print sys.path
    d = xbmcgui.Dialog()
    d.ok(str(error), 'Please check you installed this plugin correctly.')
    raise

DIR_USERDATA   = xbmc.translatePath(__addoninfo__["profile"])
HTTP_CACHE_DIR = os.path.join(DIR_USERDATA, 'iplayer_http_cache')
SUBTITLES_DIR  = os.path.join(DIR_USERDATA, 'Subtitles')
SEARCH_FILE    = os.path.join(DIR_USERDATA, 'search.txt')
VERSION_FILE   = os.path.join(DIR_USERDATA, 'version.txt')
iplayer.IPlayer.RESUME_FILE    = os.path.join(DIR_USERDATA, 'iplayer_resume.txt')
iplayer.IPlayer.RESUME_LOCK_FILE = os.path.join(DIR_USERDATA, 'iplayer_resume_lock.txt')

if os.path.isfile(iplayer.IPlayer.RESUME_LOCK_FILE):
    if not xbmc.Player().isPlaying():
        utils.log("Detected stale resume lock file, deleting...",xbmc.LOGSEVERE)
        os.remove(iplayer.IPlayer.RESUME_LOCK_FILE)

__plugin_handle__ = utils.__plugin_handle__

def file_read(filename):
    text = ''
    fh = open(filename, "r")
    try:
        text = fh.read()
    finally:
        fh.close()
    return text

def file_write(filename, data):
    fh = open(filename, "wb")
    try:
        fh.write(data)
    finally:
        fh.close()

def sort_by_attr(seq, attr):
    intermed = map(None, map(getattr, seq, (attr,)*len(seq)), xrange(len(seq)), seq)
    intermed.sort()
    return map(operator.getitem, intermed, (-1,) * len(intermed))

def get_plugin_thumbnail(image):

    # support user supplied .png files
    userpng = os.path.join(iplayer.get_thumb_dir(), xbmc.getSkinDir(), image + '.png')
    if os.path.isfile(userpng):
        return userpng
    userpng = os.path.join(iplayer.get_thumb_dir(), image + '.png')
    if os.path.isfile(userpng):
        return userpng
    else:
        return os.path.join(iplayer.get_thumb_dir(), 'bbc.png')

def get_feed_thumbnail(feed):
    thumbfn = ''
    if not feed or not feed.channel: return ''

    # support user supplied .png files
    userpng = get_plugin_thumbnail(feed.channel)
    if userpng: return userpng

    # check for a preconfigured logo
    if iplayer.stations.channels_logos.has_key(feed.channel):
        url = iplayer.stations.channels_logos[feed.channel]
        if url == None:
            url = os.path.join(iplayer.get_thumb_dir(), 'bbc_local_radio.png')
        return url

    # national TV and Radio stations have easy to find online logos
    if feed.tvradio == 'radio':
        url = "http://www.bbc.co.uk/iplayer/img/radio/%s.gif" % feed.channel
    else:
        url = "http://www.bbc.co.uk/iplayer/img/tv/%s.jpg" % feed.channel

    return url

def make_url(feed=None, listing=None, pid=None, tvradio=None, category=None, series=None, url=None, label=None, radio=None):
    base = sys.argv[0]
    d = {}
    if series: d['series'] = series
    if feed:
        if feed.channel:
            d['feed_channel'] = feed.channel
        if feed.atoz:
            d['feed_atoz'] = feed.atoz
    if category: d['category'] = category
    if listing: d['listing'] = listing
    if pid: d['pid'] = pid
    if tvradio: d['tvradio'] = tvradio
    if url: d['url'] = url
    if label: d['label'] = label
    if radio: d['radio'] = radio
    params = urllib.urlencode(d, True)
    return base + '?' + params

def read_url():
    args = cgi.parse_qs(sys.argv[2][1:])
    feed_channel = args.get('feed_channel', [None])[0]
    feed_atoz    = args.get('feed_atoz', [None])[0]
    listing      = args.get('listing', [None])[0]
    pid          = args.get('pid', [None])[0]
    tvradio      = args.get('tvradio', [None])[0]
    category     = args.get('category', [None])[0]
    series       = args.get('series', [None])[0]
    url          = args.get('url', [None])[0]
    label        = args.get('label', [None])[0]
    deletesearch = args.get('deletesearch', [None])[0]
    radio        = args.get('radio', [None])[0]
    deleteresume = args.get('deleteresume', [None])[0]
    force_resume_unlock = args.get('force_resume_unlock', [None])[0]
    playfromstart = args.get('playfromstart', [None])[0]
    playresume   = args.get('playresume', [None])[0]
    content_type = args.get('content_type', [None])[0]

    feed = None
    if feed_channel:
        feed = iplayer.feed('auto', channel=feed_channel, atoz=feed_atoz, radio=radio)
    elif feed_atoz:
        feed = iplayer.feed(tvradio or 'auto', atoz=feed_atoz, radio=radio)

    if content_type:
        if content_type == 'video':
            tvradio = 'tv'
        elif content_type == 'audio':
            tvradio = 'radio'

    if not (feed or listing):
        section = __addon__.getSetting('start_section')
        if   section == '1': tvradio = 'tv'
        elif section == '2': tvradio = 'radio'

    return (feed, listing, pid, tvradio, category, series, url, label, deletesearch, radio, deleteresume, force_resume_unlock, playfromstart, playresume)

def list_feeds(feeds, tvradio='tv', radio=None):
    xbmcplugin.addSortMethod(handle=__plugin_handle__, sortMethod=xbmcplugin.SORT_METHOD_TRACKNUM )

    folders = []
#    if tvradio == 'tv':
#    folders.append(('Watch Live', 'tv', make_url(listing='livefeeds', tvradio=tvradio)))
    if tvradio == 'tv':
        add_featured_feeds(folders, tvradio)
    if tvradio == 'radio':
        folders.append(('Listen Live', 'listenlive', make_url(listing='livefeeds', tvradio=tvradio, radio=radio)))

    total = len(folders) + len(feeds) + 1

    i = 1
    for j, (label, tn, url) in enumerate(folders):
        listitem = xbmcgui.ListItem(label=label)
        listitem.setIconImage('defaultFolder.png')
        thumb = get_plugin_thumbnail(tn)
        if thumb:
            listitem.setThumbnailImage(thumb)
        listitem.setProperty('tracknumber', str(i + j))
        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=url,
            listitem=listitem,
            isFolder=True,
        )

    i = len(folders) + 1
    for j, f in enumerate(feeds):
        listitem = xbmcgui.ListItem(label=f.name)
        listitem.setIconImage('defaultFolder.png')
        listitem.setThumbnailImage(get_feed_thumbnail(f))
        listitem.setProperty('tracknumber', str(i + j))
        url = make_url(feed=f, listing='list')
        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=url,
            listitem=listitem,
            isFolder=True,
        )
    xbmcplugin.endOfDirectory(handle=__plugin_handle__, succeeded=True)

def add_featured_feeds(folders, tvradio):
    folders.append(('Categories', 'categories', make_url(listing='categories', tvradio=tvradio)))
    folders.append(('Highlights', 'highlights', make_url(listing='highlights', tvradio=tvradio)))
    folders.append(('Popular', 'popular', make_url(listing='popular', tvradio=tvradio)))
    folders.append(('Latest', 'latest', make_url(listing='latest', tvradio=tvradio)))
    folders.append(('Search', 'search', make_url(listing='searchlist', tvradio=tvradio)))

def list_live_feeds(feeds, tvradio='tv'):
    #print 'list_live_feeds %s' % feeds
    if tvradio == 'radio':
        xbmcplugin.setContent(__plugin_handle__, 'songs')
    xbmcplugin.addSortMethod(handle=__plugin_handle__, sortMethod=xbmcplugin.SORT_METHOD_TRACKNUM)

    i = 0

    for j, f in enumerate(feeds):

        try: utils.log('Processing feed %s' % str(f.name),xbmc.LOGINFO)
        except: continue

        if f.channel == 'bbc_hd': continue

        # === Set up the XBMC ListItem
        listitem = xbmcgui.ListItem(label=f.name)

        listitem.setIconImage(get_feed_thumbnail(f))
        listitem.setThumbnailImage(get_feed_thumbnail(f))
        if tvradio == 'radio':
            listitem.setProperty('tracknumber', str(i + j))

        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=make_url(pid=f.channel, feed=f),
            listitem=listitem,
            isFolder=False,
        )

    xbmcplugin.endOfDirectory(handle=__plugin_handle__, succeeded=True)

re_stream_mms = re.compile('href\s*\=\s*"(mms.*?)"', re.IGNORECASE)

def parse_asx(radio_url):
    txt = iplayer.httpget(radio_url)
    match_mms  = re_stream_mms.search(txt)
    if  match_mms:
        stream_url = match_mms.group(1)
    else:
        stream_url = radio_url

    return stream_url

def list_tvradio():
    """
    Lists five folders - one for TV and one for Radio, plus A-Z, highlights and popular
    """
    xbmcplugin.addSortMethod(handle=__plugin_handle__, sortMethod=xbmcplugin.SORT_METHOD_TRACKNUM)

    folders = []
    folders.append(('TV', 'tv', make_url(tvradio='tv')))
    folders.append(('Radio', 'radio', make_url(tvradio='radio')))
    folders.append(('Settings', 'settings', make_url(tvradio='Settings')))

    for i, (label, tn, url) in enumerate(folders):
        listitem = xbmcgui.ListItem(label=label)
        listitem.setIconImage('defaultFolder.png')
        thumbnail = get_plugin_thumbnail(tn)
        if thumbnail:
            listitem.setThumbnailImage(get_plugin_thumbnail(tn))
        folder=True
        if label == 'Settings':
            # fix for reported bug where loading dialog would overlay settings dialog
            folder = False
        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=url,
            listitem=listitem,
            isFolder=folder,
        )

    xbmcplugin.endOfDirectory(handle=__plugin_handle__, succeeded=True)

def list_radio_types():
    """
    Lists folders - National, Regional & Local Radio + Search
    """
    xbmcplugin.addSortMethod(handle=__plugin_handle__, sortMethod=xbmcplugin.SORT_METHOD_TRACKNUM)

    folders = []
    add_featured_feeds(folders, 'radio')
    folders.append(('National Radio Stations', 'national', make_url(tvradio='radio',radio='national')))
    folders.append(('Regional Radio Stations', 'regional', make_url(tvradio='radio',radio='regional')))
    folders.append(('Local Radio Stations',    'local',    make_url(tvradio='radio',radio='local')))

    for i, (label, tn, url) in enumerate(folders):
        listitem = xbmcgui.ListItem(label=label)
        listitem.setIconImage('defaultFolder.png')
        if tn in [ 'national', 'regional', 'local' ]:
            listitem.setThumbnailImage(get_plugin_thumbnail('bbc_radio'))
        else:
            listitem.setThumbnailImage(get_plugin_thumbnail(tn))
        folder=True
        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=url,
            listitem=listitem,
            isFolder=folder,
        )

    xbmcplugin.endOfDirectory(handle=__plugin_handle__, succeeded=True)


def get_setting_thumbnail_size():
    size = __addon__.getSetting('thumbnail_size')
    #Biggest|Large|Small|Smallest|None
    if size:
        if size == '0':
            return 'biggest'
        elif size == '1':
            return 'large'
        elif size == '2':
            return 'small'
        elif size == '3':
            return 'smallest'
        elif size == '4':
            return 'none'
    # default
    return 'large'

def get_setting_subtitles():
    subtitles = __addon__.getSetting('subtitles_control')
    #values="None|Download and Play|Download to File" default="None"
    if subtitles:
        if subtitles == 'None' or subtitles == '0':
            return None
        elif subtitles == 'Download and Play' or subtitles == '1':
            return 'autoplay'
        elif subtitles == 'Download to File' or subtitles == '2':
            return 'download'
    # default
    return None

def add_programme(feed, programme, totalItems=None, tracknumber=None, thumbnail_size='large', tvradio='tv'):
    title     = programme.title
    thumbnail = programme.get_thumbnail(thumbnail_size, tvradio)
    summary   = programme.summary

    utils.log("Adding program: %s" % programme.__dict__,xbmc.LOGDEBUG)

    listitem = xbmcgui.ListItem(label=title,
                                label2=summary,
                                iconImage='defaultVideo.png',
                                thumbnailImage=thumbnail)

    datestr = programme.updated[:10]
    date=datestr[8:10] + '/' + datestr[5:7] + '/' +datestr[:4]#date ==dd/mm/yyyy

    if programme.categories and len(programme.categories) > 0:
        genre = ''
        for cat in programme.categories:
            genre += cat + ' / '
        genre=genre[:-2]
    else:
        genre = ''

    listitem.setInfo('video', {
        'Title': programme.title,
        'Plot': programme.summary,
        'PlotOutline': programme.summary,
        'Genre': genre,
        "Date": date,
    })
    listitem.setProperty('Title', str(title))
    if tracknumber: listitem.setProperty('tracknumber', str(tracknumber))

    #print "Getting URL for %s ..." % (programme.title)

    # tv catchup url
    url=make_url(feed=feed, pid=programme.pid)
    resume, dates_added = iplayer.IPlayer.load_resume_file()
    if programme.pid in resume.keys():
        listitem.setInfo('video', {'Title': "%s [I](resumeable %s)[/I] " % (programme.title, tohms(resume[programme.pid])), 'LastPlayed': dates_added[programme.pid]})
        cmd1 = "XBMC.RunPlugin(%s?deleteresume=%s)" % (sys.argv[0], urllib.quote_plus(programme.pid))
        cmd2 = "XBMC.RunPlugin(%s?playfromstart=%s)" % (sys.argv[0], urllib.quote_plus(programme.pid))
        cmd3 = "XBMC.RunPlugin(%s?playresume=%s)" % (sys.argv[0], urllib.quote_plus(programme.pid))
        listitem.addContextMenuItems([('Resume from %s' % tohms(resume[programme.pid]), cmd3), ('Play from start', cmd2), ('Remove resume point', cmd1)])

    xbmcplugin.addDirectoryItem(
        handle=__plugin_handle__,
        url=url,
        listitem=listitem,
        totalItems=totalItems
    )

    return True

def tohms(time):
    hours = int(time / 3600)
    mins = int(time / 60) % 60
    secs = int(time) % 60
    return str.format("{0:02}:{1:02}:{2:02}", hours, mins, secs)

def list_categories(tvradio='tv', feed=None, channels=None, progcount=True):

    # list of categories within a channel
    xbmcplugin.addSortMethod(handle=__plugin_handle__, sortMethod=xbmcplugin.SORT_METHOD_NONE)
    for label, category in feed.categories():
        url = make_url(feed=feed, listing='list', category=category, tvradio=tvradio)
        listitem = xbmcgui.ListItem(label=label)
        if tvradio == 'tv':
            listitem.setThumbnailImage(get_plugin_thumbnail('tv'))
        else:
            listitem.setThumbnailImage(get_plugin_thumbnail('radio'))
        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=url,
            listitem=listitem,
            isFolder=True,
        )

    xbmcplugin.endOfDirectory(handle=__plugin_handle__, succeeded=True)


re_series_match = [re.compile('^(Late\s+Kick\s+Off\s+)'), \
                   re.compile('^(Inside\s+Out\s+)'), \
                   re.compile('^(.*?):')]

def series_match(name):
    # match the series name part of a programme name
    match = None

    for s in re_series_match:
        match = s.match(name)
        if match:
            break

    return match

def list_series(feed, listing, category=None, progcount=True):

    c = 0
    name = feed.name

    d = {}
    d['list'] = feed.list
    d['popular'] = feed.popular
    d['highlights'] = feed.highlights
    programmes = d[listing]()

    ## filter by category
    if category:
        temp_prog = []
        # if a category filter has been specified then only parse programmes
        # in that category
        for p in programmes:
            for cat in p.categories:
                if cat == category:
                    temp_prog.append(p)
                    continue
        programmes = temp_prog

    ## extract the list of series names
    series = {}
    episodes = {}
    categories = {}
    dates = {}

    thumbnail_size = get_setting_thumbnail_size()
    for p in programmes:

        match = series_match(p.title)
        thumb = p.get_thumbnail(thumbnail_size, feed.tvradio)

        if match:
            seriesname = match.group(1)
        else:
            # the programme title doesn't have a series delimiter
            seriesname = p.title

        series[seriesname] = thumb
        datestr = p.updated[:10]
        if not episodes.has_key(seriesname):
            episodes[seriesname] = 0
            dates[seriesname] = datestr

        episodes[seriesname] += 1
        categories[seriesname] = p.categories

    serieslist = series.keys()
    serieslist.sort()

    for s in serieslist:
        url = make_url(feed=feed, listing='list', category=category, series=s )
        if progcount:
            label = "%s (%s)" % (s, episodes[s])
        else:
            label = s
        listitem = xbmcgui.ListItem(label=label, label2=label)
        listitem.setThumbnailImage(series[s])
        date=dates[s][8:10] + '/' + dates[s][5:7] + '/' +dates[s][:4] #date ==dd/mm/yyyy
        listitem.setInfo('video', {'Title': s, 'Date': date, 'Size': episodes[s], 'Genre': "/".join(categories[s])})
        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=url,
            listitem=listitem,
            isFolder=True,
        )
        c += 1

    if c == 0:
        # and yes it does happen once in a while
        label = "(no programmes available - try again later)"
        listitem = xbmcgui.ListItem(label=label)
        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url="",
            listitem=listitem,
        )

    xbmcplugin.endOfDirectory(handle=__plugin_handle__, succeeded=True)


def search(tvradio, searchterm):

    if not searchterm:
        searchterm = iplayer_search.prompt_for_search()
        if searchterm != None and len(searchterm) >= 3:
            iplayer_search.save_search(SEARCH_FILE, tvradio, searchterm)
        else:
            return

    utils.log("searchterm=%s" % searchterm,xbmc.LOGINFO)
    feed = iplayer.feed(tvradio, searchterm=searchterm)

    list_feed_listings(feed, 'list')

def search_delete(tvradio, searchterm):
    iplayer_search.delete_search(SEARCH_FILE, tvradio, searchterm)
    xbmc.executebuiltin("Container.Refresh")

def search_list(tvradio):
    # provide a list of saved search terms
    xbmcplugin.addSortMethod(handle=__plugin_handle__, sortMethod=xbmcplugin.SORT_METHOD_NONE)
    searchimg = get_plugin_thumbnail('search')

    # First item allows a new search to be created
    listitem = xbmcgui.ListItem(label='New Search...')
    listitem.setThumbnailImage(searchimg)
    url = make_url(listing='search', tvradio=tvradio)
    ok = xbmcplugin.addDirectoryItem(
          handle=__plugin_handle__,
          url=url,
          listitem=listitem,
          isFolder=True)

    # Now list all the saved searches
    for searchterm in iplayer_search.load_search(SEARCH_FILE, tvradio):
        listitem = xbmcgui.ListItem(label=searchterm)
        listitem.setThumbnailImage(searchimg)
        url = make_url(listing='search', tvradio=tvradio, label=searchterm)

        # change the context menu to an entry for deleting the search
        cmd = "XBMC.RunPlugin(%s?deletesearch=%s&tvradio=%s)" % (sys.argv[0], urllib.quote_plus(searchterm), urllib.quote_plus(tvradio))
        listitem.addContextMenuItems( [ ('Delete saved search', cmd) ] )

        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=url,
            listitem=listitem,
            isFolder=True,
        )

    xbmcplugin.endOfDirectory(handle=__plugin_handle__, succeeded=True)

def list_feed_listings(feed, listing, category=None, series=None, channels=None):
    xbmcplugin.addSortMethod(handle=__plugin_handle__, sortMethod=xbmcplugin.SORT_METHOD_NONE)

    d = {}
    d['list'] = feed.list
    d['popular'] = feed.popular
    d['highlights'] = feed.highlights
    d['latest'] = feed.latest
    programmes = d[listing]()

    ## filter by series
    if series:
        temp_prog = []
        # if a series filter has been specified then only parse programmes
        # in that series
        i = len(series)

        for p in programmes:
            matchagainst = p.title
            match = series_match(p.title)
            if match: matchagainst = match.group(1)
            #print "matching %s,%s" % (p.title, matchagainst)
            if series == matchagainst:
                temp_prog.append(p)
        programmes = temp_prog

    programmes = sort_by_attr(programmes, 'episode')


    # add each programme
    total = len(programmes)
    if channels: total = total + len(channels)
    count =  0
    thumbnail_size = get_setting_thumbnail_size()
    for p in programmes:
        try:
            if not add_programme(feed, p, total, count, thumbnail_size, feed.tvradio):
                total = total - 1
        except:
            traceback.print_exc()
            total = total - 1
        count = count + 1

    # normally from an empty search
    if not programmes:
        label = "(no programmes available - try again later)"
        listitem = xbmcgui.ListItem(label=label)
        ok = xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url="",
            listitem=listitem
        )
        count= count + 1


    # add list of channels names - for top level Highlights and Popular
    if channels:
        for j, f in enumerate(channels):
            listitem = xbmcgui.ListItem(label=f.name)
            listitem.setIconImage('defaultFolder.png')
            listitem.setThumbnailImage(get_feed_thumbnail(f))
            listitem.setProperty('tracknumber', str(count))
            count = count + 1
            url = make_url(feed=f, listing=listing, tvradio=feed.tvradio, category=category)
            ok = xbmcplugin.addDirectoryItem(
                handle=__plugin_handle__,
                url=url,
                listitem=listitem,
                isFolder=True,
            )

    xbmcplugin.setContent(handle=__plugin_handle__, content='episodes')
    xbmcplugin.endOfDirectory(handle=__plugin_handle__, succeeded=True)


def get_item(pid):
    #print "Getting %s" % (pid)
    p = iplayer.programme(pid)
    #print "%s is %s" % (pid, p.title)

    #for i in p.items:
    #    if i.kind in ['programme', 'radioProgrammme']:
    #        return i
    return p.programme

re_subtitles = re.compile('^\s*<p.*?begin=\"(.*?)\.([0-9]+)\"\s+.*?end=\"(.*?)\.([0-9]+)\"\s*>(.*?)</p>')

def download_subtitles(url):
    # Download and Convert the TTAF format to srt
    # SRT:
    #1
    #00:01:22,490 --> 00:01:26,494
    #Next round!
    #
    #2
    #00:01:33,710 --> 00:01:37,714
    #Now that we've moved to paradise, there's nothing to eat.
    #

    # TT:
    #<p begin="0:01:12.400" end="0:01:13.880">Thinking.</p>

    utils.log('subtitles at = %s' % url,xbmc.LOGINFO)
    outfile = os.path.join(SUBTITLES_DIR, 'iplayer.srt')
    fw = open(outfile, 'w')

    if not url:
        fw.write("1\n0:00:00,001 --> 0:01:00,001\nNo subtitles available\n\n")
        fw.close()
        return

    txt = iplayer.httpget(url)

    i=0
    prev = None

    # some of the subtitles are a bit rubbish in particular for live tv
    # with lots of needless repeats. The follow code will collapse sequences
    # of repeated subtitles into a single subtitles that covers the total time
    # period. The downside of this is that it would mess up in the rare case
    # where a subtitle actually needs to be repeated
    for line in txt.split('\n'):
        entry = None
        m = re_subtitles.match(line)
        if m:
            start_mil = "%s000" % m.group(2) # pad out to ensure 3 digits
            end_mil   = "%s000" % m.group(4)

            ma = {'start'     : m.group(1),
                  'start_mil' : start_mil[:3],
                  'end'       : m.group(3),
                  'end_mil'   : end_mil[:3],
                  'text'      : m.group(5)}

            ma['text'] = ma['text'].replace('&amp;', '&')
            ma['text'] = ma['text'].replace('&gt;', '>')
            ma['text'] = ma['text'].replace('&lt;', '<')
            ma['text'] = ma['text'].replace('<br />', '\n')
            ma['text'] = ma['text'].replace('<br/>', '\n')
            ma['text'] = re.sub('<.*?>', '', ma['text'])
            ma['text'] = re.sub('&#[0-9]+;', '', ma['text'])
            #ma['text'] = ma['text'].replace('<.*?>', '')

            if not prev:
                # first match - do nothing wait till next line
                prev = ma
                continue

            if prev['text'] == ma['text']:
                # current line = previous line then start a sequence to be collapsed
                prev['end'] = ma['end']
                prev['end_mil'] = ma['end_mil']
            else:
                i += 1
                entry = "%d\n%s,%s --> %s,%s\n%s\n\n" % (i, prev['start'], prev['start_mil'], prev['end'], prev['end_mil'], prev['text'])
                prev = ma
        elif prev:
            i += 1
            entry = "%d\n%s,%s --> %s,%s\n%s\n\n" % (i, prev['start'], prev['start_mil'], prev['end'], prev['end_mil'], prev['text'])

        if entry: fw.write(entry)

    fw.close()
    return outfile

# To be removed
def get_matching_stream(item, pref, streams):
    """
    tries to return a media object for requested stream,
    falling back on a lower stream if requested one is not available. if there are no lower ones, it will
    return the first stream it finds.
    """
    media = item.get_media_for(pref)

    for i, stream in enumerate(streams):
        if pref == stream:
            break

    while not media and i < len(streams)-1:
        i += 1
        utils.log('Stream %s not available, falling back to %s stream' % (pref, streams[i]),xbmc.LOGINFO)
        pref = streams[i]
        media = item.get_media_for(pref)

    # problem - no media found for default or lower
    if not media:
        # find the first available stream in reverse order
        for apref in reversed(streams):
            media = item.get_media_for(apref)
            if media:
                pref=apref
                break

    return (media, pref)

def watch(feed, pid, resume=False):

    times = []
    times.append(['start',time.clock()])

    subtitles_file = None
    item      = get_item(pid)
    times.append(['get_item',time.clock()])
    thumbnail = item.programme.thumbnail
    title     = item.programme.title
    summary   = item.programme.summary
    updated   = item.programme.updated
    channel   = None
    thumbfile = None
    if feed and feed.name:
        channel = feed.name
    times.append(['setup variables',time.clock()])
    utils.log('watching channel=%s pid=%s' % (channel, pid),xbmc.LOGINFO)
    times.append(['logging',time.clock()])
    utils.log('thumb =%s   summary=%s' % (thumbnail, summary),xbmc.LOGINFO)
    times.append(['logging',time.clock()])
    subtitles = get_setting_subtitles()
    times.append(['get_setting_subtitles',time.clock()])

    if thumbnail:
        if feed is not None and pid == feed.channel:
            # Listening to a live radio station, use the pre-downloaded file
            thumbfile = get_feed_thumbnail(feed)
        else:
            # attempt to use the existing thumbnail file
            thumbcache = xbmc.getCacheThumbName( sys.argv[ 0 ] + sys.argv[ 2 ] )
            if utils.get_os() == "xbox":
                thumbfile = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video", thumbcache[ 0 ], thumbcache )
            else:
                thumbfile = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", thumbcache[ 0 ], thumbcache )
            utils.log('Reusing existing thumbfile=%s for url %s%s' % (thumbfile, sys.argv[ 0 ], sys.argv[ 2 ]),xbmc.LOGINFO)

    if thumbnail and not os.path.isfile(thumbfile):
        # thumbnail wasn't available locally so download
        try:
            # The thumbnail needs to accessed via the local filesystem
            # for "Media Info" to display it when playing a video
            iplayer.httpretrieve(thumbnail, thumbfile)
            times.append(['retrieve thumbnail',time.clock()])
        except:
            pass

    (media_list, above_limit) = item.get_available_streams()

    if len(media_list) == 0:
        # Nothing usable was found
        d = xbmcgui.Dialog()
        d.ok('Stream Error', 'Can\'t locate any usable streams.')
        return False

    for media in media_list:
        player = None
        if item.is_tv:
            # TV Stream
            iconimage = 'DefaultVideo.png'

            if above_limit:
                d = xbmcgui.Dialog()
                if d.yesno('Default Stream Not Available', 'Play higher bitrate stream?') == False:
                    return False

            times.append(['media 2',time.clock()])
            url = media.url
            times.append(['media.url',time.clock()])
            utils.log('watching url=%s' % url,xbmc.LOGINFO)
            times.append(['logging',time.clock()])

            if subtitles:
                subtitles_media = item.get_media_list_for('captions', None)
                times.append(['subtitles_media',time.clock()])
                if subtitles_media and len(subtitles_media) > 0:
                    subtitles_file = download_subtitles(subtitles_media[0].url)
                    times.append(['subtitles download',time.clock()])

            listitem = xbmcgui.ListItem(title)
            times.append(['create listitem',time.clock()])
            if not item.live:
                listitem.setInfo('video', {
                                           "TVShowTitle": title,
                                           'Plot': summary + ' ' + updated,
                                           'PlotOutline': summary,})
            times.append(['listitem setinfo',time.clock()])
            play=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            times.append(['xbmc.PlayList',time.clock()])

        else:

            if not media:
                d = xbmcgui.Dialog()
                d.ok('Stream Error', 'Error: can\'t locate radio stream')
                return False

            if media.application in ['wma9', 'wma+asx']:
                url = parse_asx(media.url)
            else:
                url = media.url

            utils.log('Listening to url=%s' % url,xbmc.LOGINFO)

            listitem = xbmcgui.ListItem(label=title)
            times.append(['listitem create',time.clock()])
            listitem.setIconImage('defaultAudio.png')
            times.append(['listitem.setIconImage',time.clock()])
            play=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
            times.append(['xbmc.PlayList',time.clock()])

        utils.log('Playing preference %s %s' % (media.connection_kind, media.application),xbmc.LOGINFO)
        times.append(['logging.info',time.clock()])
        listitem.setInfo(type='Music', infoLabels = {'title': title})
        times.append(['listitem.setproperty x 3',time.clock()])

        if thumbfile:
            listitem.setIconImage(thumbfile)
            times.append(['listitem.setIconImage(thumbfile)',time.clock()])
            listitem.setThumbnailImage(thumbfile)
            times.append(['listitem.setThumbnailImage(thumbfile)',time.clock()])

        if url.startswith( 'rtmp://' ):
            core_player = xbmc.PLAYER_CORE_DVDPLAYER
        else:
            core_player = xbmc.PLAYER_CORE_AUTO

        try:
            player = iplayer.IPlayer(core_player, pid=pid, live=item.is_live)
        except iplayer.IPlayerLockException:
            exception_dialog = xbmcgui.Dialog()
            exception_dialog.ok("Stream Already Playing", "Unable to open stream", " - To continue, stop all other streams (try pressing 'x')[CR] - If you are sure there are no other streams [CR]playing, remove the resume lock (check addon settings -> advanced)")
            return

        times.append(['xbmc.Player()',time.clock()])
        player.resume_and_play(url, listitem, item.is_tv, resume)

        # Successfully started playing something?
        if player.isPlaying():
            break;

        times.append(['player.play',time.clock()])

    # Auto play subtitles if they have downloaded
    utils.log("subtitles: %s   - subtitles_file %s " % (subtitles,subtitles_file),xbmc.LOGINFO)
    times.append(['logging.info',time.clock()])
    if subtitles == 'autoplay' and subtitles_file:
        player.setSubtitles(subtitles_file)
        times.append(['player.setSubtitles',time.clock()])

    if not item.is_tv:
        # Switch to a nice visualisation if playing a radio stream
        xbmc.executebuiltin('ActivateWindow(Visualisation)')

    del item

    if __addon__.getSetting('enhanceddebug') == 'true':
        pt = times[0][1]
        for t in times:
            utils.log('Took %2.2f sec for %s' % (t[1] - pt, t[0]),xbmc.LOGINFO)
            pt = t[1]

    if os.environ.get( "OS" ) != "xbox":
        while player.isPlaying() and not xbmc.abortRequested:
            xbmc.sleep(500)

        utils.log("Exiting playback loop... (isPlaying %s, abortRequested %s)" % (player.isPlaying(), xbmc.abortRequested),xbmc.LOGDEBUG)
        player.cancelled.set()

utils.log("Version: %s" % __version__,xbmc.LOGINFO)
utils.log("Subtitles dir: %s" % SUBTITLES_DIR,xbmc.LOGINFO)

old_version = ''

DIR_USERDATA

for d in [DIR_USERDATA, HTTP_CACHE_DIR, SUBTITLES_DIR]:
    if not os.path.isdir(d):
        try:
            utils.log("%s doesn't exist, creating" % d,xbmc.LOGINFO)
            os.makedirs(d)
        except IOError, e:
            utils.log("Couldn't create %s, %s" % (d, str(e)),xbmc.LOGINFO)
            raise

if not os.path.isfile(SEARCH_FILE):
    try:
        open(SEARCH_FILE, 'wb').close()
    except IOError, e:
        utils.log("Couldn't create %s, %s" % (d, str(e)),xbmc.LOGERROR)
        raise

if os.path.isfile(VERSION_FILE):
    old_version = file_read(VERSION_FILE)

if old_version != __version__:
    file_write(VERSION_FILE, __version__)
    d = xbmcgui.Dialog()
    d.ok('Welcome to the BBC IPlayer addon', 'Please be aware this addon only works in the UK.', 'The IPlayer service checks to ensure UK IP addresses.')

if __name__ == "__main__":
    try:

        # setup and check script environment
        if __addon__.getSetting('http_cache_disable') == 'false': iplayer.set_http_cache(HTTP_CACHE_DIR)

        environment = os.environ.get( "OS", "xbox" )
        try:
            timeout = int(__addon__.getSetting('socket_timeout'))
        except:
            timeout = 5
        if environment in ['Linux', 'xbox'] and timeout > 0:
            setdefaulttimeout(timeout)

        progcount = True
        if __addon__.getSetting('progcount') == 'false':  progcount = False

        # get current state parameters
        (feed, listing, pid, tvradio, category, series, url, label, deletesearch, radio, deleteresume, force_resume_unlock, playfromstart, playresume) = read_url()
        utils.log( str((feed, listing, pid, tvradio, category, series, url, label, deletesearch, radio, deleteresume, force_resume_unlock, playfromstart, playresume)),xbmc.LOGINFO )

        # update feed category
        if feed and category:
            feed.category = category

        # state engine
        if pid:
            watch(feed, pid, __addon__.getSetting('playaction') == "0")
        elif deletesearch:
            search_delete(tvradio or 'tv', deletesearch)
        elif deleteresume:
            iplayer.IPlayer.delete_resume_point(deleteresume)
            xbmc.executebuiltin('Container.Refresh')
        elif playfromstart:
            watch(feed, playfromstart)
        elif playresume:
            watch(feed, playresume, True)
        elif force_resume_unlock:
            iplayer.IPlayer.force_release_lock()
        elif not (feed or listing):
            if not tvradio:
                list_tvradio()
            elif tvradio == 'Settings':
                __addon__.openSettings()
            elif (tvradio == 'radio' and radio == None):
                list_radio_types()
            elif tvradio:
                feed = iplayer.feed(tvradio, radio=radio).channels_feed()
                list_feeds(feed, tvradio, radio)
        elif listing == 'categories':
            channels = None
            feed = feed or iplayer.feed(tvradio or 'tv',  searchcategory=True, category=category, radio=radio)
            list_categories(tvradio, feed)
        elif listing == 'searchlist':
            search_list(tvradio or 'tv')
        elif listing == 'search':
            search(tvradio or 'tv', label)
        elif listing == 'livefeeds':
            tvradio = tvradio or 'tv'
            channels = iplayer.feed(tvradio or 'tv', radio=radio).channels_feed()
            list_live_feeds(channels, tvradio)
        elif listing == 'list' and not series and not category:
            feed = feed or iplayer.feed(tvradio or 'tv', category=category, radio=radio)
            list_series(feed, listing, category=category, progcount=progcount)
        elif listing:
            channels=None
            if not feed:
                feed = feed or iplayer.feed(tvradio or 'tv', category=category, radio=radio)
                channels=feed.channels_feed()
            list_feed_listings(feed, listing, category=category, series=series, channels=channels)

    except:
        # Make sure the text from any script errors are logged
        traceback.print_exc(file=sys.stdout)
        raise
