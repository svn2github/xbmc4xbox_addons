'''
    ustvnow XBMC Plugin
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import re
import sys
import xbmc
import xbmcgui

# from functools import wraps

from t0mm0.common.addon import Addon

addon = Addon('plugin.video.ustvnow', sys.argv)

class TextBox:
    # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % ( self.WINDOW, ))
        # get window
        self.win = xbmcgui.Window(self.WINDOW)
        # give window time to initialize
        xbmc.sleep(1000)
        self.setControls()

    def setControls(self):
        # set heading
        heading = "ustvnow v%s" % (addon.get_version())
        self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
        # set text
        root = addon.get_path()
        faq_path = os.path.join(root, 'xbmc4xbox.news')
        f = open(faq_path)
        text = f.read()
        self.win.getControl(self.CONTROL_TEXTBOX).setText(text)
from resources.lib import Addon, ustvnow

import sys
Addon.plugin_url = sys.argv[0]
Addon.plugin_handle = int(sys.argv[1])
Addon.plugin_queries = Addon.parse_query(sys.argv[2][1:])

email = Addon.get_setting('email')
password = Addon.get_setting('password')
ustv = ustvnow.Ustvnow(email, password)

Addon.log('plugin url: ' + Addon.plugin_url)
Addon.log('plugin queries: ' + str(Addon.plugin_queries))
Addon.log('plugin handle: ' + str(Addon.plugin_handle))

mode = Addon.plugin_queries['mode']

if mode == 'main':
    Addon.log(mode)
    if email == "":
        TextBox()
    elif email == "hubwizard@hushmail.com":
	    TextBox()
    Addon.add_directory({'mode': 'live'}, Addon.get_string(30001))
    Addon.add_directory({'mode': 'recordings'}, Addon.get_string(30002))

elif mode == 'live':
    Addon.log(mode)
    stream_type = ['rtmp', 'rtsp'][int(Addon.get_setting('stream_type'))]
    channels = ustv.get_channels(int(Addon.get_setting('quality')), 
                                     stream_type)
    for c in channels:
        Addon.add_video_item(c['url'],
                             {'title': '%s - %s' % (c['name'], 
                                                    c['now']['title']),
                              'plot': c['now']['plot']},
                             img=c['icon'])

elif mode == 'recordings':
    Addon.log(mode)
    stream_type = ['rtmp', 'rtsp'][int(Addon.get_setting('stream_type'))]
    recordings = ustv.get_recordings(int(Addon.get_setting('quality')), 
                                     stream_type)
    for r in recordings:
        cm_del = (Addon.get_string(30003), 
                  'XBMC.RunPlugin(%s/?mode=delete&del=%s)' % 
                       (Addon.plugin_url, urllib.quote(r['del_url'])))
        title = '%s (%s on %s)' % (r['title'], r['rec_date'], r['channel'])
        Addon.add_video_item(r['stream_url'], {'title': title, 
                                               'plot': r['plot']},
                             img=r['icon'], cm=[cm_del], cm_replace=True)

elif mode == 'delete':
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno(Addon.get_string(30000), Addon.get_string(30004), 
                       Addon.get_string(30005))
    if ret == 1:
        ustv.delete_recording(Addon.plugin_queries['del'])
elif mode == 'Help':
    
    TextBox() 
Addon.end_of_directory()
        

