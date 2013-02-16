# -*- coding: UTF-8 -*-

import os, sys, re, xbmc, xbmcgui, string, urllib, ElementTree as XMLTree
from utilities import log

_                = sys.modules[ "__main__" ].__language__
__settings__     = sys.modules[ "__main__" ].__settings__
__profile__      = sys.modules[ "__main__" ].__profile__

apiurl           = "http://api.bierdopje.com/"
apikey           = "369C2ED4261DE9C3"
showids_filename = os.path.join( __profile__ ,"bierdopje_show_ids.txt" )

#====================================================================================================================
# Functions
#====================================================================================================================

def apicall(command, paramslist):
    url = apiurl + apikey + "/" + command
    for param in paramslist:
        url = url + "/" + urllib.quote_plus(param)
    log( __name__ ," getting url '%s'" % url )
    try:
        response = urllib.urlopen(url)
    except:
        okdialog = xbmcgui.Dialog()
        ok = okdialog.ok("Error", "Failed to contact Bierdopje site.")
        log( __name__ ," failed to get url '%s'" % url )
    else:
        try:
            xml = XMLTree.parse(response)
            status = gettextelements(xml, "response/status")
        except:
            okdialog = xbmcgui.Dialog()
            ok = okdialog.ok("Error", "Failed to contact Bierdopje site.")
            log( __name__ ," failed to get proper response for url '%s'" % url )
            return None
        if status == "false":
            okdialog = xbmcgui.Dialog()
            ok = okdialog.ok("Error", "Failed to contact Bierdopje site.")
            log( __name__ ," failed to get proper response (status = false) for url '%s'" % url )
            return None
        else:
            return xml

def gettextelements(xml, path):
    textelements = []
    try:
        elements = xml.findall(path)
    except:
        return
    for element in elements:
        textelements.append(element.text)
    return textelements

def getshowid(showname):
    showids = {}
    if os.path.isfile(showids_filename):
        showids_filedata = file(showids_filename,'r').read()
        showids = eval(showids_filedata)
        if showname in showids:
            log( __name__ ," show id for '%s' is '%s' (from cachefile '%s')" % (showname, showids[showname], showids_filename))
            return showids[showname]
    response = apicall("GetShowByName",[showname])
    if response is not None:
        showid = gettextelements(response,"response/showid")
        if len(showid) == 1:
            log( __name__ ," show id for '%s' is '%s'" % (showname, str(showid[0])) )
            showids[showname] = str(showid[0])
            file(showids_filename,'w').write(repr(showids))
            return str(showid[0])
        elif ("'" in showname):
            response = apicall("GetShowByName",[string.replace(showname,"'","''")])
            if response is not None:
                showid = gettextelements(response,"response/showid")
                if len(showid) == 1:
                    log( __name__ ," show id for '%s' is '%s' (replaced ' with '')" % (string.replace(showname,"'","''"), str(showid[0])) )
                    showids[showname] = str(showid[0])
                    file(showids_filename,'w').write(repr(showids))
                    return str(showid[0])
        okdialog = xbmcgui.Dialog()
        ok = okdialog.ok("Error", "Failed to get a show id from Bierdopje for " + showname)
        log( __name__ ," failed to get a show id for '%s'" % showname )


def isexactmatch(subsfile, moviefile):
    match = re.match("(.*)\.", moviefile)
    if match:
        moviefile = string.lower(match.group(1))
        subsfile = string.lower(subsfile)
        log( __name__ ," comparing subtitle file with moviefile to see if it is a match (sync):\nsubtitlesfile  = '%s'\nmoviefile      = '%s'" % (string.lower(subsfile), string.lower(moviefile)) )
        if string.find(string.lower(subsfile),string.lower(moviefile)) > -1:
            log( __name__ ," found matching subtitle file, marking it as 'sync': '%s'" % (string.lower(subsfile)) )
            return True
        else:
            return False
    else:
        return False

def getallsubs(showid, file_original_path, tvshow, season, episode, languageshort, languagelong, subtitles_list):
    not_sync_list = []
    response = apicall("GetAllSubsFor",[showid, str(season), str(episode), languageshort])
    if response is not None:
        filenames = gettextelements(response,"response/results/result/filename")
        downloadlinks = gettextelements(response,"response/results/result/downloadlink")
        if len(filenames) > 0:
            log( __name__ ," found %s %s subtitles" % (len(filenames), languagelong))
            for i in range(len(filenames)):
                if string.lower(filenames[i][-4:]) == ".srt":
                    filenames[i] = filenames[i][:-4]
                sync = False
                if isexactmatch(filenames[i], os.path.basename(file_original_path)):
                    sync = True
                    subtitles_list.append({'rating': '0', 'no_files': 1, 'format': 'srt', 'movie':  tvshow, 'language_id': '', 'filename': filenames[i], 'sync': sync, 'link': downloadlinks[i], 'language_flag': 'flags/' + languageshort + '.gif', 'language_name': languagelong, 'ID': '0'})
                else:
                    not_sync_list.append({'rating': '0', 'no_files': 1, 'format': 'srt', 'movie':  tvshow, 'language_id': '', 'filename': filenames[i], 'sync': sync, 'link': downloadlinks[i], 'language_flag': 'flags/' + languageshort + '.gif', 'language_name': languagelong, 'ID': '0'})
            for i in range(len(not_sync_list)):
                subtitles_list.append(not_sync_list[i])
        else:
            log( __name__ ," found no %s subtitles" % (languagelong))


def search_subtitles( file_original_path, title, tvshow, year, season, episode, set_temp, rar, lang1, lang2, lang3, stack ): #standard input
    subtitles_list = []
    msg = ""
    if len(tvshow) > 0:
        tvshow_id= getshowid(tvshow)
        dutch = 0
        if string.lower(lang1) == "dutch": dutch = 1
        elif string.lower(lang2) == "dutch": dutch = 2
        elif string.lower(lang3) == "dutch": dutch = 3

        english = 0
        if string.lower(lang1) == "english": english = 1
        elif string.lower(lang2) == "english": english = 2
        elif string.lower(lang3) == "english": english = 3

        if ((dutch > 0) and (english == 0)):
            getallsubs(tvshow_id, file_original_path, tvshow, season, episode, "nl", "Dutch", subtitles_list)

        if ((english > 0) and (dutch == 0)):
            getallsubs(tvshow_id, file_original_path, tvshow, season, episode, "en", "English", subtitles_list)

        if ((dutch > 0) and (english > 0) and (dutch < english)):
            getallsubs(tvshow_id, file_original_path, tvshow, season, episode, "nl", "Dutch", subtitles_list)
            getallsubs(tvshow_id, file_original_path, tvshow, season, episode, "en", "English", subtitles_list)

        if ((dutch > 0) and (english > 0) and (dutch > english)):
            getallsubs(tvshow_id, file_original_path, tvshow, season, episode, "en", "English", subtitles_list)
            getallsubs(tvshow_id, file_original_path, tvshow, season, episode, "nl", "Dutch", subtitles_list)

        if ((dutch == 0) and (english == 0)):
            msg = "Won't work, Bierdopje is only for Dutch and English subtitles."
    else:
        msg = "Won't work, Bierdopje is only for tv shows."
    return subtitles_list, "", msg #standard output


def download_subtitles (subtitles_list, pos, zip_subs, tmp_sub_dir, sub_folder, session_id): #standard input
    local_tmp_file = os.path.join(tmp_sub_dir, "bierdopje_subs.srt")

    log( __name__ ," downloading subtitles from url '%s'" % subtitles_list[pos][ "link" ] )
    try:
        response = urllib.urlopen(subtitles_list[pos][ "link" ])
    except:
        okdialog = xbmcgui.Dialog()
        ok = okdialog.ok("Error", "Failed to contact Bierdopje site.")
        log( __name__ ," failed to get url '%s'" % subtitles_list[pos][ "link" ] )
    else:
        log( __name__ ," saving subtitles to '%s'" % local_tmp_file )
        try:
            local_file_handle = open(local_tmp_file, "w" + "b")
            local_file_handle.write(response.read())
            local_file_handle.close()
        except:
            okdialog = xbmcgui.Dialog()
            ok = okdialog.ok("Error", "Failed to save subtitles.")
            log( __name__ ," failed to save subtitles to '%s'" % local_tmp_file )
        else:
            language = subtitles_list[pos][ "language_name" ]
            return False, language, local_tmp_file #standard output
