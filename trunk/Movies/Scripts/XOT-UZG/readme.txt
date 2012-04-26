--------------------------------------------------------------------------------------------
 XOT-Uzg.v3.x.x                                                                   
--------------------------------------------------------------------------------------------
 Contents
 0. License
 1. Introduction
 2. Changelog
 3. Skinning
 4. Known Issues
 4a.Some channels are not working? How come?
 5. Acknowledgements
 6. Donations
--------------------------------------------------------------------------------------------
 
--------------------------------------------------------------------------------------------
 0. License
--------------------------------------------------------------------------------------------
The XOT-Framework is licensed under the Creative Commons Attribution-Non-Commercial-No 
Derivative Works 3.0 Unported License. To view a copy of this licence, visit 
http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to Creative Commons, 
171 Second Street, Suite 300, San Francisco, California 94105, USA. Files that belong to 
the XOT-Framework have a disclaimer stating that they are licensed under the Creative 
Commons Attribution-Non-Commercial-No Derivative Works 3.0 Unported License.

All channels, skins and config.py (further called XOT Additions) are free software: 
you can redistribute it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation, either version 3 of the License, or (at your 
option) any later version. XOT Additions are distributed in the hope that it will be 
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
details. You should have received a copy of the GNU General Public License along with 
XOT Additions. If not, see <http://www.gnu.org/licenses/>.
 
--------------------------------------------------------------------------------------------
 1. Introduction
--------------------------------------------------------------------------------------------
An XBox Media Center script which allows playback of streams from www.uitzendinggemist.nl. 
This version has options for streaming multiple past episodes from different TV Shows.
 
Discussion of the script can be done at this thread at the XBMC Forums. Please post any 
problems/suggestions in either of these threads:
 - http://www.xboxmediacenter.com/forum/showthread.php?p=130060) 
 - Most recent XBMC thread at http://gathering.tweakers.net (Dutch only)

Download the latest version at: 
 - http://www.rieter.net/pages/XOT:Uzg or use the official XOT-Uzg.v3 repository (http://www.rieter.net/pages/XOT:Download#XBMC_Repository)

Direct contact can be done using the following e-mailadres: 
 - uitzendinggemist.vx[@t]gmail[d0t]com

--------------------------------------------------------------------------------------------
 2. Changelog
--------------------------------------------------------------------------------------------
Changelog v3.2.13 - 2012-02-15

 Framework related
* Added: Proxy password options (Issue 310)
* Fixed: CacheResponse was empty if a exception occured (stream was at the end).
* Fixed: Cached Responses could cause exceptions
* Fixed: SAMI -> SRT lost special characters
* Added: Subtitle support to SMIL helper
* Fixed: SubtitleHelper now handles SAMI better
* Fixed: If description of a MediaItem was None, it would fail to generate a XBMC item.
* Fixed: None stringvalue is decoded to None
* Fixed: No video item resulted in no update in the GUI (part of Issue 299)
* Updated: stopwatch Stop() method.
* Updated: Stopwatch to show delta time.
* Changed: CreatePageItem can now return None and will be ignored.
* Fixed: Compile error in PyAMF
* Changed: Adding a favorite in the Video Add-On now redirects to favorites. This way XBMC waits for the adding to be finished
* Changed: logger is now passed into the LockWithDialog decorator
* Fixed: TypeError in PyAmf
* Added: some DB connection cleanup
* Added: Busy Dialog in Plugin (locker.py)
* Added: UrlDecode to the HTML Entity Helper
* Changed: shortened "Remove from favorites" -> "Remove favorite"
* Added: A small fix to PyAMF (commented now)
* Added: Restart message to settings
* Added: Option to change backgrounds
* Fixed: Some UTF-8 issues with XBMC paths
* Added: show error when XOT-Uzg.v3 is not installed using repository on non Xbox systems


 Skin related
* None

 Channel related
* Fixed: iRTL channel was broken due to XML changes
* Added: Freecaster.tv became Extreme.com (Issue 309)
* Added: Subtitle support to TV4.se (Thanks to Göran). It does need a XOT framework update.
* Fixed: Date extraction of iRTL channel
* Fixed: after an update the TV4.se is not marked as completed (part of Issue 299)
* Fixed: Slow Regexes in a number of channels
* Fixed: Search did not work in NOS channel
* Fixed: Southpark.nl did not play more than one act (Issue 309).
* Fixed: Southpark.nl SWF path updated.
* Changed: BETA Uitzending Gemist channel is now the main one, as the old one is offline.
* Fixed: "Een.be" channel had wrong videos (Issue 305)
* Added: Search to NOS Uitzendinn Gemist BETA (Issue 304)
* Added: TOP50 for Uitzendinggemist BETA (Issue 304)
* Fixed: NOS Beta does not display shows that start with a number (Issue 303)
* Added: Hardware.info TV
* Fixed: NOS Uitzendinggemist BETA (Issue 301). Rearranged the channel.
* Changed: iRTL now works on XBCM4Xbox again (Issue 300)
* Fixed: iRTL did not playback (Issue 302)


Changelog v3.2.12 - 2011-12-15

 Framework related
* Fixed: reverted part of Environment check fix. The Unknown = 1 basically fixed it already.
* Fixed: No ChannelUpdate for Xbox Plugin
* Fixed: Do not cache downloads
* Changed: ContextMenu missing method is now a warning
* Updated: Added a real HEAD request method to UriOpener
* Fixed: XBMC code has more Envirmonts and broke ATV2 support (Issue 293)
* Added: SearchSite is now implemented in chn_class. Makes using it easier.
* Added: Version class and comparisons
* Removed: self.maxXotVersion from all channels
* Fixed: logging of initialization error
* Changed: Version is now check based on Addon.xml version
* Changed: OutOfDate is no longer used

 Skin related
* None

 Channel related
* Added: NOS.nl channel (Issue 192)
* Added: Download items from NOS Beta
* Fixed: SVT SWF Url
* Fixed: Exclude video's in SBS.nl streams (only show episodes)
* Fixed: TV4 Did not show all episodes (Issue 290)
* Fixed: No episodes for "Bonde söker fru" (Issue 294)
* Fixed: ViaSat Sport and TV6.lt did not play due to SWF Verification (Issue 290)
* Fixed: BBC Iplayer Regex issues
* Added: Search to NOS.nl channel
* Fixed: TV4.se would not play (Issue 257)
* Added: Premium label added TV4.se (part of Issue 257)
* Fixed: Prefix clips with "Klipp" in Kanal5.se and Kanal9.se (Issue 291)


Changelog v3.2.11 - 2011-10-18

 Framework related
* Updated: Moved channel importing to a point after logfile cleaning in plug-in mode
* Added: Option to disable channels on different platforms
* Fixed: Finally the dreaded Linux-logfile-append-issue is fixed 
* Changed: Do not cache thumbs in plugin mode that's XBMC's work
* Fixed: ContextMenu items that do not need Complete items, no do not force an update
* Fixed: Python 2.4 issue with proxies (should have http:// in front of it)
* Added: iPlayer related settings (proxy and port)
* Added: British channel settings
* Fixed: Ignore empty MediaParts when creating a PlayList
* Updated: Subtitle Regex for TTML
* Added: SubtitleHelper now supports DCSubtitle format
* Fixed: Error when no SRT could be determined
* Changed: Cannot add favorites without URL
* Added: HTTP reponse caching (experimental and enabled by default)
* Added: First time channel run messages (informational messages for different channels)
* Changed: plugin sorting now checks if there are any dates available when sorting by dates. If not: sorting defaults to label.
* Changed: HQ icons in Plugin mode
* Added: Ability to also use Named Group in regular expression. 

 Skin related
* Fixed: Error icon would not disappear even after a second attempt was OK

 Channel related
* Fixed: Eén channel was broken due to the changing of the media URL's
* Fixed: Eén Different date formats caused some episodes to not show
* Fixed: NOS Beta channel returned .sort() and broke (Thanks to Mart.@forum.xbmc.org)
* Added: Different RTL icons for different channels. 
* Fixed: RTL channel broke due to XML changes
* Fixed: iRTL broke due to XML changes
* Added: iRTL should not load on Xbox (it's not compatible)
* Fixed: SBS6 label is now SBS 6
* Fixed: SBS6, NET5 and Veronica changed to Brightcove player
* Updated: Nick Jr. url
* Fixed: Nick.nl regex (Regression)
* Fixed: Eredivisie live missed items due to a "gistere/yesterday" label (Issue 288)
* Added: BBC channels (iPlayer)
* Fixed: TV.se (TV3.se, TV6.se, TV8.se, TV3.lv, TV3.no, Viasat4.no) and MTG.se channel regex (Regression)
* Added: TV5.se and TV9.se channels (Issue 148)
* Added: TV6.se, TV3.se, TV8.se, TV3.lv, TV3.no and TV4.no now support subtitles
* Added: TV4.se now supports multiple bitrates
* Fixed: Channel9 channel had some regex issues. Now using XmlHelper
* Fixed: MyVideo regex broke the videos


Changelog v3.2.10 - 2011-09-04

 Framework related
* Added: New setting to enable advanced plugin mode (default enabled). Enables these features:
* Added: Plugin Contextmenu generated from channel contexmenuitems
* Added: Plugin show favorites from mainlist and channel overview
* Fixed: Refresh issue fixed for plugin for Xbox
* Added: Favorites handling for plugin
* Added: Playlist support in Plugin
* Added: Subtitle support for Plugin

* Changed: Thumbs are now cached using their MD5 hashed URL as filename
* Added: HTML helper should also trigger on 'attribute' instead of just "attribute"
* Added: Do not show already installed channel updates in XBox Channel update window.
* Changed: sortorder of some channels
* Fixed: channel importer was too limited in importing and breaking inheritance of classes (Issue 281)
* Fixed: if no subtitle was found, don't try downloading it again.
* Updated: set Year Infolabel if available
* Updated: encode the description just like the title
* Added: Set ContentType in Plugin to "Movie"
* Updated: Replaced Dutch error message

 Skin related
* Fixed: Some skin issues related to contextmenu and update window.

 Channel related
* Fixed: AMT had some issues with thumbs and some URL formats
* Updated: AMT now get's high definition posters
* Updated: RTL iPad channel to have dates and multi bitrates. This channel is no longer supported on XBMC4Xbox.
* Updated: RTL XL 
* Added: Eredivisie Live
* Updated: TV4 to have a nice thumb 
* Fixed: tv3.no not working due to SWF verification (Issue 286)


Changelog v3.2.9 - 2011-08-12

 Framework related
* Updated: Load ProgramList with AddItems instead of AddItem
* Updated: Fill Plot and PlotOutline with Description information.
* Changed: no part number in plug-in if only one part
* Added: Refresh option in main window
* Added: Timed Text Markup Language -> SRT converter
* Added: Sort method "None" -> makes the order identical to the order on the websites
* Fixed: sort by in the plugin now takes Addon settings into account.
* Fixed: set no-image to incomplete video item.
* Fixed: HTML helper attribute order was incorrect.
* Fixed: pass user-agent to on when using the plug-in. Fixes AMT as plugin.
* Added: Belgium language code to settings
* Fixed: Unicode errors in XOT DB
* Fixed: Don't add duplicates to favorites
* Fixed: cache path could not be created if profile path did not exist (Issue 276, thanks to Sven)

 Skin related
* Updated: XOT Logo
* Updated: Logo's and Icons renewed

 Channel related
* Fixed: AMT channel
* Updated: AMT add description to items
* Fixed: 123Video channel did not play recent video's
* Added: Nick Junior
* Fixed: Nickelodeon channel
* Added: UR Play (Swedish)
* Added: AT5
* Added: VRT channels (Sporza, Ketnet, De Redactie, Cobra)
* Fixed: Lama's channel was broken due to website changes
* Added: Canvas.be
* Added: Een.be to channels
* Updated: Southpark channel now has high quality movies

Changelog v3.2.8 - 2011-07-13

 Framework related
* Fixed: Sorting issue. list.sort() always returns None and caused errors updating already loaded channels.
* Fixed: DimValue returned an error as it was not implemented yet.
* Fixed: Plugin did not create Cache folder (Thanks to Göran)
* Added: Error icon if item update failed
* Fixed: force close the logfile for script

 Skin related
* None

 Channel related
* None


Changelog v3.2.7 - 2011-07-12

 Framework related
* Added: ACTION_NAV_BACK in order to be compatible with commit 9ceddb029b0b01e67973.
* Fixed: Default value for bitrate is 800 which is not in the list!
* Fixed: context menu in some cases passed the index of the wrong list (favorites broke)
* Fixed: Apparently showing your own progressbar breaks the normal plugin progressbar. Disabling it again. Thanks to Göran for pointing it out.
* Changed: in plugin mode, we just pass the thumbUrl to XBMC instead of loading it.
* Fixed: Download from Plugin
* Updated: User-Agent handling changed so it can be passed on to XBMC
* Moved: Cache folder to profile
* Added: Setting for subtitle mode: show or not
* Fixed: Change active channel index only on select.

 Skin related
* None

 Channel related
* Fixed: The regex in SVT searches for "ram" which matches "Program"! So a lot of false matches (Thanks again Göran)
* Added: Refresh option for completed items. I some cases (NOS) the video URL expires and you will have to get a new one.
* Changed: Apple Movie Trailers now starts playback immediately instead of downloading. Download is now a context menu option
* Added: subtitles to SVT.se (Thanks to Göran for pointing it out)

Changelog v3.2.6 - 2011-07-04

 Framework related
* Fixed: in some cases Unicode was hidden in normal string and thus not correctly decoded. Hopefully the Unicode issues are now all solved (Thanks to Göran for pointing out the issue)
* Added: Encoding info to startup
* Added: json now replaces \uxxxx values with Unicode characters.
* Fixed: Linux x64 caused an error due to the -1 value of 4294967295. This is now temporarily fixed with a workaround (Thanks to Maurizo and Cartaphilus @forum.xbmc.org)
* Added: Settings logging
* Fixed: HasMediaItemParts fixed (it now also checks for streams)
* Fixed: resort mainlist after settings changed.
* Fixed: Progressbar animation
* Added: Download parts from plugin
* Added: UriHandler now accepts an user-agent overwrite to it's download method.
* Added: Date helper 
* Changed: Use bitrate instead of stream quality. This makes it more usefull (Thanks to Göran for the idea).
* Changed: XBMC4Xbox should not deploy channels outside it's folder (thanks vriesm@XBMC4Xbox for the idea)
* Changed: month lookup in DateHelper

 Skin related
* Fixed: Folder icon does not show under Linux due to CAPS issue in xot_DefaultFolder.png. 
* Fixed: Memory issues due to background

 Channel related
* Fixed: file:// issue under Linux preventing iRTL to work.
* Fixed: SVT SWF verification (Thanks to Göran)
* Added: Apple Movie Trailers 
* Fixed: NOS channels now show better bitrates
* Fixed: Added Includes.xml to prevent error messages
* Changed: XBMC4Xbox now loads its channels from the \channels\ path
* Reverted: use none MMS stream for NOS2010
* Fixed: TV4.se did not load images

Changelog v3.2.5 - 2011-06-15

 Framework related
* Fixed: bug in settings module if called from a non-Eden XBMC. (Issue 268)

Changelog v3.2.4 - 2011-05-03
 Skin related
* Added: skin.xot is not the default skin and reworked the complete skinning engine of XOT
* Removed: all other skins

 Channel related
* Added: Channel 9 @ MSDN
* Added: Toppers to dumpert (Issue 263)
* Fixed: UZG for IOS (Issue 261)
* Added: NOS Beta now has subtitle support
* Updated: NOS Beta Channel fixes (regex + date lookup)
* Fixed: Workaround for bug in geo-checking in NOS site (thanks to Reinoud).
* Added: Norwegian channels thanks to Rbiez (Jan Christian Liby)
* Fixed: RTL-Ipad channel
* Added: TV Stations (Issue 255)
* Fixed: Radiostations would not list (Issue 254)
* Fixed: Freecaster channel (Issue 241,149)
* Fixed: Freecaster changed their site again, so I had to update the channel
* Removed: SBS and RTL backgrounds
* Fixed: Southpark channel (still Type mismatch: client sent 6, server answered 9)

 Framework related
* Changed: MediaItems now have MediaItemParts which again have MediaStreams
* Added: caching of retrieved items and pre-adding option
* Added: Log the language of channels.
* Changed: Sorting of channels moved to Channel class
* Fixed: Unicode logging issues
* Fixed: Chuncked data no longer causes empty data to return. It now returns up to where the opener got.
* Added: RawEncode and IngoreEncode methods
* Added: date sorting option for items with dates (selectable via via the Addon settings, requires XOT restart)
* Fixed: Menu now returns to channel window instead of going up (Issue 142) 
* Fixed: Deprecated warnings for Eden Repository API
* Changed: os.getcwd() to addon.getAddonInfo('path') (Compatibility for the new Eden Repository API)
* Added: Subtitle support to channels, including caching
* Added: Channel deployer can now deleted old channels
* Added: Norwegian language
* Added: French and English Canadian language options
* Removed: XOT User Agent (too tricky for tracing)
* Fixed: Hopefully fixed UTF-8 text displaying corrupt
* Fixed: deployment on other than net.rieter.xot folder locations

Changelog v3.2.3 - 2011-01-26
* Added: Updating channels via XBMC Repository functionality (XBMC4Xbox still uses old method).
* Fixed: Updater now uses deploy mechanism to deploy channels after XOT upgrade (=workaround
  for XBMC addon implementation)
* Added: Addon Settings.xml for XOT-Uzg.v3. Settings can be accessed from Context Menu of XBMC 
  or Context menu of XOT-Uzg.v3.
* Added: High, Medium and Low bitrate playback support, configurable via Addon Settings. Plugin 
  shows bitrates in the title of the item.
* Removed: Context Menu items High and Low Bitrate. Info is now retrieved from Add-on settings.
* Added: Setting to allow disabling of channels of a certain language
* Changed: XOT database file is now stored in the script profile location, so it won't get 
  deleted on XOT update.
* Updated: TV3,6&8 with new SWF and new site layout (Issue 245)
* Fixed: TV4.se channel due to site changes (Issue 243, Issue 231) 
* Added: NOS Beta.uitzendinggemist.nl channel (with multi-bitrate support).
* Added: bitrate selection to SVT (Issue 233)
* Fixed: RTL channel now uses RTL-XL. 
* Fixed: Freecaster.tv channel (Issue 241)
* Fixed: folders in plugin are not accessible (thanks to PsychoCheF@forums.xbmc.org
* Fixed: not all labels in the Default skin had a <textcolor> tag, so in some skin's the text would not appear (thanks to xbmcvis@forum.xbmc.org and jolid@forum.xbmc.org)
* Fixed: Repository did not have a correct MD5 file.
* Removed: unneeded imports

Changelog v3.2.2 - 2010-11-05 **** Needs at least XBMC revision r31434 ****
* Updated: Plugin is now independent of WindowXML.GUI
* Changed: Split channel class in two parts: GUI and Channel. Improves speed and memory usage
* Removed: Not used imports to improve speed
* Added: ChannelImporter and redesigned channel initialization
* Fixed: All names are now De-Prefixed (The, A, An, Een, De, Het)
* Fixed: Logging error in chn_class.py
* Added: De-prefixing titles (the, a, an, de, het, een)
* Fixed: Episodelist could cause XBMC to crash due to wrong order in IF statement
* Added: option to UriOpener to only download the first xxxx bytes to speedup downloading
* Fixed: Channel updater could not handle new channels (thank to Fabian)
* Added: better detection of 64-bit environments
* Changed: external Python detection (Python > 2.4)
* Changed: using external libs if external Python is detected
* Changed: using SQLite3 if available instead of PySQL2
* Added: Support for XBMC on OpenElec.tv (Thanks to Martijn Elzenaar)
* Fixed: MTV channel
* Fixed: TV4.se channel
* Fixed: RTL 4,5,7&8 channel
* Fixed: RTL iPad channel
* Fixed: GeoLock support for TV3,6&8.se (Issue 199)
* Added: SWF Verification for TV3,4,6,8 and SportSE
* Added: SWF verification to Nick.NL (Issue 215)
* Added: 720p Default Skin files (Issue 226)
* Added: 4:3 Default Skin files (Issue 226)

Changelog v3.2.1 - 2010-08-08 **** Needs at least XBMC revision r31434 ****
* Added: TV4.se (Issue 149)
* Fixed: Plugin now uses base64 encoding to prevent messing up of pickle item (Fixes Issue 197)
* Added: Southpark channel for The Netherlands only (Issue 140)(if more countries want it, then they should send me a fiddler trace of browsing their southpark site)
* Changed: plugin now displays date in title if present (thanks to Julian Kooij) (Issue 195)
* Fixed: NOS channel still used progressbars in plugin mode
* Fixed: SVT channel, added new RTMP regex

Changelog v3.2.0 - 2010-07-10 **** Needs at least XBMC revision r31434 ****
* Fixed: XOT-Uzg.v3 is now Addon compatible
* Added: Repository definition (1.0.0)
* Renamed: Confluence Skin to skin.confluence
* Added: XBMC Addon Support
* Added: iRTL (iPhone RTL channel without DRM)
* Fixed: SBS Broadcasting Channel
* Added: option to create a UriOpener that does never use a progressbar (needed for plugin)
* Fixed: Plugin would crash due to progressbar appearing (a bug in XBMC)
* Fixed: Issue with logfile flushing before closing.
* Fixed: Freecaster.tv
* Fixed: NOS Channel: Top50, New items and Tips in NOS channels
* Fixed: Skins for 1080i
* Fixed: Veronica channel paging 
* Fixed: RTL channel
* Added: Radio channels (thanks to BigFoot87)

Changelog v3.2.0b7 - 2010-01-26 **** Needs at least XBMC revision R17016 ****
* Removed: Kanalenkiezer for the time being, because they start to link to HTML more and more
* Fixed: Turbo Nick RTMP urls
* Fixed: Freecaster.tv
* Updated: SVT to handel AJAX calls beter (Issue 151)
* Added: Confluence Skin
* Fixed: added some code to make sure XOT updater does not suffer from a googelcode-page bug
* Fixed: Bug with closing of progressbar
* Added: Contextmenu Close support

Changelog v3.2.0b6 - 2009-11-26 **** Needs at least XBMC revision R17016 ****
* Fixed: Fine tuned SVT regex's 
* Fixed: SVT.se channel could not handle rtmpe (thanks to Stefan Nilsson)
* Added: Viasat Sport (thanks to fldc @ XBMC.org)
* Added: TV3, TV6 and TV8.se
* Fixed: RTL channel more compatible with XBMC Win32/Linux (Thanks to Menno). Still long loading times
* Fixed: Freecaster.tv channel
* Fixed: Plugin broke with new XBMC version
* Fixed: Loging broke with new XBMC version
* Fixed: bug with logging of mediaitem 
* Added: MiniMeedia skin
* Changed: Xbox Media Center into XBMC Media Center
* Updated: Logo's
* Updated: Build Scripts

Changelog v3.2.0b5 - 2009-05-07 **** Needs at least XBMC revision R17016 ****
* Fixed: Freecaster.tv
* Added: proxy support
* Fixed: __eq__ could not handle None objects
* Fixed: plugin did not work because of __eq__ bug.

Changelog v3.2.0b4 - 2009-04-28 **** Needs at least XBMC revision R17016 ****
* Added: TV3.se and TV6.se
* Fixed: RTL 4,5,7&8 channel
* Removed: PCZapper SBS6
* Added: Freecaster.tv
* Fixed: SVT.se channel. 
* Fixed: 123Video now detects correct mediaserver
* Fixed: De Lama's channel
* Added: TurboNick
* Fixed: MTV.nl Channel
* Fixed: Southpark channel (partly)
* Fixed: NOS channels
* Added: Unicode support (fixed scrambling of special characters)
* Added: Minor improvements to UI and added Events
* Added: detection of duplicate GUIDs of channels. The duplicate is removed and error is logged
* Added: Helpers library
* Added: HtmlEntityHelper class. 
* Fixed: Default Skin scroll
* Renamed: clistItem to MediaItem

Changelog v3.2.0b3 - 2009-01-23 **** Needs at least XBMC revision R17016 ****
* Added: MediaStream skin (thanks to Poeier from tweakers.net)
* Fixed: RTL channel
* Added: better sorting of items (date still needs some tweaking)
* Added: Mouseclick support (Requires Rev 17016)
* Added: Z@PP Channel
* Fixed: SVT Channel

Changelog v3.2.0b2 - 2008-11-24 **** Needs at least XBMC revision R14899 ****
* Updated: SVT.se
* Fixed: mediaUrl error in Plugin
* Fixed: Environment always showed Win32 even on xbox. Now it imports win32 but displays XBOX
* Fixed: Icon had bad pixels
* Changed: entity-converter did not work if entities had capitals
* Fixed: Regex for NET5/SBS6 and Veronica (Again)
* Added: NOS Top 50
* Fixed: RTL now loads the additional programms better
* Fixed: Regex for NET5/SBS6 and Veronica
* Added: Paging to NET5/SBS6 and Veronica

Changelog v3.2.0b1 - 2008-09-29 ****Needs at least XBMC revision R14899 ****
* Added: Official southpark channel
* Fixed: RTL Channel adjusted to new RTL Player
* Added: new environment detecting
* Added: 64bit support
* Fixed: NOS Channel adjustments for new url layout (and future use of WMC)
* Fixed: Plugin for multiple mediaurls

Changelog v3.2.0a3 - 2008-09-04 ****Needs at least XBMC revision R14899 ****
* Fixed: Linux Logging
* Fixed: Linux pal -> PAL in skin folder names

Changelog v3.2.0a2 - 2008-09-02 ****Needs at least XBMC revision R14899 ****
* Fixed: path issues with Linux. os.path.join is used now everywhere.
* Fixed: SBS6nl channel
* Fixed: RTL457&8 channel
* Added: Environment detection and OS dependend packages (idea taken from AMT)

Changelog v3.2.0a1 - 2008-08-19 ****Needs at least XBMC revision R14899 ****
* Fixed: NOS channel needed fixing because of new check on the website.
* Fixed: quickfix for unexplainable clearing of channellist
* Changed: layout of script folder to support WindowXML rev14899
* Fixed: MyVideo regex
* Fixed: some more syntax issues
* Changed: User Agent for URLLib is now XOT/3.0 (compatible; XBMC; U)
* Removed: Unneeded imports
* Fixed: RTL changed their layout
* Fixed: Regex changed for Kanalenkiezer
* Changed: Veronica channel needed multiple fixes (FLV detection)
* Changed: Favorites now use ChannelGUID for identification
* Added: GUID for each channel used for identification.
* Added: bitrate selection of RTL streams
* Updated: SVT.se image
* Updated: Donations updated in readme.txt

Changelog v3.1.0 - 2008-05-07 ****Needs at least XBMC revision R10008 ****
* Added: Auto Channel Updater
* Changed: update now has a verbose option to also show a message if no update was available
* Fixed: www.uitzendinggemist.nl introduced a SecurityCode to obtain the mediaurl. For now it is fixed by loading an extra page that holds that code.
* Fixed: Regex for results in NOS Zoeken fine-tuned
* Fixed: Dumpert.nl MediaUrlRegex
* Fixed: Pagecontrols where showing for channel description labels
* Added: Official SBS6.nl channel. The previous one now has PCZapper in it's name and description
* Added: NET5 from www.net5.nl
* Added: Veronicatv.nl
* Fixed: Cosmetic changes to contextmenu
* Added: self.defaultPlayer option to channels
* Changed: Prevent addition of duplicate items in Mainlist
* Added: more debugging info if an AttributeError occurs after importing libraries. This should give more information on what went wrong.
* Fixed: on some XBox systems the timeout of on Open action would occur immediately due to a problem with the threading.join() method. (Thanks to Arnova [tweakers.net])
* Fixed: Caching of thumb would not return the default self.NoImage if an exception occured.
* Changed: GuiController now ignores exceptions that occur when non essential controls are missing from the skin file (like the channelinfo controls and rating controls).
* Fixed: Contextmenu had disappeared in some channels
* Fixed: RTL XML Layout changed

Changelog v3.0.1 - 2008-03-10 ****Needs at least XBMC revision R10008 ****
* Added: more download algorithms
* Added: more support for quicksilverscreen.com
* Added: people who donated
* Fixed: Searchregex www.uitzendinggemist.nl was not correct
* Added: Swedish television SVT.se
* Added: BeautifulSoup support via common.DoSoupFindAll
* Added: chn_class.py now accepts lists/tuples for playback. They will be converted to playlists
* Changed: maxVersion to 3.0.1
* Added: MyVideos.nl
* Added: new pagenavigation images
* Added: favorites now go into Database file
* Added: sqlite2 library
* Changed: context menu now uses onClick and works with mouse
* Fixed: Crash on detection of script/plugin from within XBMC for Linux
* Fixed: Crash on mouse movement when mouse is not over a control in ProgWindow. 
* Fixed: UrlJoin used for url creation in CreatePageItem
* Fixed: GuiController check self.PluginMode
* Added: Page support in XOT Plugin (they show as folders)
* Added: XBMC version and compile date in Directory Printer
* Changed: scrolling through pagelist now also allows from top -> bottom jump
* Fixed: UZG changed their layout. ParseMainList now parses multiple pages

Changelog v3.0.0 - 2008-01-28 ****Needs at least XBMC revision R10008 ****
* Changed: Item is now first pushed onto the history stack before fetching of new items, so the 
  parent item can be called via the history stack (for descriptions for instance)
* Changed: sort-order of Lama's channel
* Added: Quicksilverscreen.com channel
* Added: Ratings
* Changed: Modified the www.uitzendinggemist.nl search channel to a 'specials' channel 
  including search, popular items, newly added items, etc..etc.. 

Changelog v3.0.0b2 - 2008-01-07 ****Needs at least XBMC revision R10008 ****
* Fixed: issue with getFocus() for GUI types that are XBMCGUI specific.
* Fixed: Minor issue on NOS Page handling
* Fixed: Progressbar dissappeared in NOS channel
* Added: Favorites can now be every folder in each channel. 
* Changed: ContextMenu is moved from Channel to ChannelClass. In the Channel now has a 
  self.contextMenuItems which is a list of ContextMenu.ContextMenuItems. Each item has 
  a label, a callback function and an indication wether it should show on video/folder/completed items.
* Added: Favorites
* Added: Settings.xml
* Added: contextmenu to 123video
* Added: 123Videos.nl
* Changed: chn_nos - NOS now only retrieves recent items and displays an archive folder with older items

Changelog v3.0.0b1 - 2007-12-23 ****Needs at least XBMC revision R10008 ****
* Fixed: Kanalenkiezer.nl is now working again
* Changed: Dumpert.nl icons renamed
* Changed: 'De Lama's' Channel changed to not retrieve 1000 items, but only 500. This should solve timeouts opening the channel.
* Fixed: Text not appearing in textboxes
* Added: Better handling of xbmcplugin interface.
* Changed: Fixed some overlaps in skins.

Changelog v3.0.0a1 - 2007-11-25 ****Needs at least XBMC revision R10008 ****
* Added: Caching of items. On 'back' items are retrieved from the cache! This reduces the URL lookups 
  dramatically
* Added: self.pluginMode, if in plugin-mode, this variable is True
* Added: initPlugin method to Channel. This one can be used to do the initialisation of a channel. Remember
  to add the self.pluginMode = True to this part.
* Added: item.Downloadable indicates whether an item is downloadable. Should be used in the future to
  determine if it can be downloaded or not.
* Added: Plugin support (dates still missing in listing)
* Added: Dumpert.nl channel
* Changed: had to remove some UI related stuff from the channels, to make sure they would work as a plugin.
* Changed: channels may NOT contain any reference to objects of the XOT-Script UI. If they do, make
  sure to not adres them when in script mode.
* Fixed: Joox.net channel
* Added: if mediaurl is not filled in updatevideo, the item is always marked als not complete
* Fixed: date is now grey when item is not selected in progwindow
* Changed: mplayer and dvdplayer can now be selected explicitly. Defaults to the default XBMC player.

Changelog v2.7.x - 2007-10-12 ****Needs at least XBMC revision R8683****
* Added: Cachefolder cleanup
* Added: New GTST episodes to RTL channel
* Added: Channelnames in Programwindow
* Added: Channeldescriptions in Programwindow
* Added: Channeldescriptions to all channels
* Added: item=complete checkmark
* Fixed: RTL Error in Regex due to changes in XML layout
* Changed: renamed self.onUpDownEnabled to self.onUpDownUpdateEnabled for better displaying its function
* Added: Lama's channel
* Added: self.CacheThumb to chn_class.py to automate the caching of thumbs
* Fixed: RTL script updated for GTST (ParseMainList adds an extra item: GTST)
* Fixed: RTL script updated. The XML layout changed a bit. 
* Added: an user agent to the uriopener (thanks to VincePirez @ xbmc forums)
* Fixed: SBS Regex
* Added: Date for programs in progwindow
* Added: Option to disable sorting alphabetically and sort by date
* Fixed: layout of Kanalenkiezer.nl changed. Had to adjust the regular 
  expressions and urls.
* Changed: no URL fetching on item selection. Only on click! 
  (Done using the self.onUpDownEnabled = False).
* Added: when self.onUpDownEnabled = False and ignore = False then 
  only the data is shown and no update is done of the videoitem.
* Changed: no onupdown for TVLink until the issues are fixed. Now update via contextmenu
* Added: onUpDownEnabled to Channel settings and onUpDown(ignoreDisabled=True/False)
* Added: Controlgroup for onUpDown to controls.py
* Changed: self.initialUri to self.mainListUri. self.intialUri still exists, but is 
  set when the Episode window opens (ShowEpisodeWindow)
* Added: Progressbar for filling lists larger than 50 items
* Added: Canceling of URL opening even if no data is comming in
* Removed: Talpa as it now is RTL8
* Added: Locking mechanisme to prevent multiple background updates (very Experimental)
* Fixed: <string> error in XBMC log due to XOT logger
* Added: Print directory of script on startup for debugging options
* Fixed: KK channels where out of sync due to webpage layout!
* Added: Locking for video update
* Added: Don't break on not resolving www.rieter.net
* Fixed: No more frenzy internet lookups: onUpDown now only starts after last 
  onUp in 500ms
* Changed: uriOpener now has private variables for methodes to prevent multithread 
  problems
* Added: New backgrounds for RTL, SBS and Talpa
* Added: ConvertURLEntity and ConvertHTMLEntity in common.py (replacing StripHTML)
* Added: maxXotVerison to channels. If XOT updates older channels may lead to 
  conflicts, so they won't be loaded then.
* Added: TV-Link.co.uk support (needs more file type detection)
* Fixed: Changing list position while loading first item would lead to wrongly 
  display item info on the newly selected one.
* Added: Default compare value in progwindow channel comparison
* Added: UriOpener.Header now also returns the real url after redirection
* Added: Code.google.com page: http://code.google.com/p/xot-uzg/
* Changed: Uitzendinggemist.v2 will be called XOT:Uzg (XBMC Online TV: Uitzendinggemst)
* Changed: UZG is now based on seperate framework called: XOT (XBMC Online TV)
* Added: Custom sorting of channels using SortOrder property
* Changed: Chn_class.py is now completely UZG free
* Changed: Media files that do not explicitly belong to UZG are 
  renamed from uzg_ to xot_
* Changed: Progwindow Skin
* Fixed: Visibility on Panel now works
* Added: Checking if image is present in SkinFolder. If it is present, 
  that one is used, else the file in the channel folder is used
* Changed: Media of channels now in channelfolder OR in skinfolder. The latter 
  overwrites the former (skinfolder is the most important location).  
* Changed: Each channel has its own folder now: chn_name.py has to be 
  located \name\chn_name.py
* Changed: Moved chn_class to libs. 
* Added: New skin for progwindow
* Added: Control groups for up/down and exit/back
* Changed: Graphics for channels
* Added: Possibility to have both a list of channels and buttons. Nr of buttons 
  must be equal to number of channels
* Changed: Register items to 'channelSelect -> channelRegister'
* Changed: buttons are now registered from within the channelClass
* Added: Dynamically load channels
* Changed: Contextmenu and progwindow skin-name in config.sys
* Changed: More UZG-name related stuff into the config.py
* Added: appName to config.py
* Changed: UpdateUrl now in config.py
* Changed: UzgLog to logFile (for general purpose)
* Removed: Some unneccessary imports
* Added: UZG Logger class, not based on Python logging
* Added: option to log exceptions in both UZG and XBMC log
* Added: GUID for identification of cListItems
* Added: Uriopener checks if filenames are in correct xfat format now
* Fixed: Some bugs in Uriopener
* Changed: Joox regex
* Added: .flv detection to SBS6/PCZapper script
* Added: registration of all channels in their own chn_name.py
* Removed: PMIII skin. Now defaults to Default
* Added: SBS6 support (from pczapper.tv)
* Added: Progressbar information while opening
* Added: complete contextmenu support (used AMT for inspiration but changed a lot). Menu
  is triggered by the Info Key/Button
* Changed: renamed skin xml files to uzg-windowname.xml ("uzg-" added)
* Added: ClearityMod skin
* Fixed: MC360 skin
* Changed: only importing common.py and controls.py for others a link to the object in __main__ is used.
* Added: config.py with all config stuff
* Added: controls.py with all control and window ID's
* Changed: Joox download enabled. Defaults to Cache Dir and uses item name as filename.
* Changed: moved first load of www.uitzendinggemist.nl from default.py to chn_nos.py and 
  added cookie check to chn_nos.py.
* Fixed: integer instead of float value to progressbar dialog (float is decrepated)
* Fixed: Minor bug playing KK streams 
* Changed: logging now happens in the 'uzg.log' file in the script folder of UZG. The 
  logfile from the previous session is named 'uzg.old.log'.
* Added: MultiLine Logger Class with Exception Handling
* Changed: NOS Search now accepts multiple characters.

Changelog v2.6.x - 2007-06-20 ****Needs at least XBMC revision R8683****
* Added: Joox Support
* Added: Version Checking
* Changed: UriOpener now has False as default. Only True on data retrieval
* Fixed: Skin list scrolling
* Fixed: uriopener did not open file if filesize was smaller than chucksize
* Changed: cleanup of uriopen method. Also adding more debuginfo
* Changed: ListItem methodes to comply with XBMC R9198
* Fixed: wrong tag in skin XML-Files
* Fixed: re-initialisation of episode window after video playback
* Fixed: MC360 skin
* Changed: New Skinlayout, first draft
* Fixed: Initialisation of Talpa-window continued even when login failed.
* Added: The "Concept" skin.
* Fixed: Errors due to very large amounts of URL's queueing up when scrolling an episode list
  fast.
* Added: Talpa.tv Uitzendinggemist Support(READ 4.a below)

Changelog v2.5.x - 2007-05-17 ****Needs Recent Version of XBMC with WindowXML support****
* Fixed: Problem with image-links in Default skin. Prevented correct display of images
  when the default skin was selected.
* Added: PMIII skin.
* Fixed: RTL 4,5&7 streams were not working due to server changes at RTL.
* Fixed: Pixel column at left side of button removed.
* Added: initial MC360 skin support (Still needs testing)
* Changed: More NOS Uitzendinggemist history. All episodes present on the site should now 
  be visible. 
* Fixed: cleaning of URL with &amp; insided the url
* Added: common.py has ID's for the used controls defined in channelwindow.xml
* Added: windowxml skinning support (See further down for more notes)
* Changed: icons for channels/episodes
* Changed: more robust checking for streams in Kanalenkiezer. Html is now filtered out 
  before playback (had to check HTTP first) to prevent problems with mplayer.
* Changed: location of constants changed to the channel-libary files
* Changed: all constants in CAPITALS, variable in camelCase and methodes in PascalCase

Changelog v2.4.x - 2007-04-24
* Changed: to make things a bit more easy to maintain I changed from a single default.py 
  to multiple files.
* Added: seperate python scripts for libraries (libs), channels and a default.py.
* Changed: each channel has it's own python file with instructions.
* Fixed: on some systems the Cache dir was not present which prevented the script from 
  running! Checking this now on startup.
* Added: BETA support for www.kanalenkiezer.nl
* Changed: search algorithm for www.uitzendinggemist.nl

Changelog v2.3.x - 2007-04-04
* Fixed: lookup string was wrong due to missing Q, X and Y.
* Fixed: no episodes were displayed if no date was found for episodes. 
* Added: searching NED1,2&3 Using the first letter of a program!

Changelog v2.2.x - 2007-04-04
* Added: progressbar to indicate the opening of URLs

Changelog v2.1.x - 2007-04-04
* Fixed: scaling when using HD resolutions
* Added: parsing of ASX/ASF for compatibility with older XBMC versions
* Added: first support for RTL 4,5 & 7 (please use the XBMC forum link to let me know if
  there are bugs)
* Added: icons for folders/video-files

Changelog v2.0.x - 2007-03-30
* Added: animations
* Changed: tabs instead of spaces for indentation
* Added: readme.txt
* Fixed: now again working with www.uitzendinggemist.nl
* Fixed: working ASF streams
* Added: support for multiple episodes of a programm
* Changed: split window-class into to parts: program-window and episode-window
* Added: new background
* Changed: layout
* Fixed: display most recent programms, instead of the first in alphabetical ranking

--------------------------------------------------------------------------------------------
 3. Skinning
--------------------------------------------------------------------------------------------
For future version of Uitzendinggemist.v2 a build that supports WindowXML is required. Such
a version can be found at the *ussual places*. 

For Developers: New skins need to follow these guidelines to function correctly:

* A skinfolder must be placed inside the folder 'skins'
* Uitzendinggemist uses the same folder-name to lookup the skin as the foldername XBMC is 
  using. So the skinfolder for Uitzendinggemist.v2 should have the same name as the folder 
  in which the XBMC-skin is present. E.g. for MC360: the XBMC skin-folder for MC360 is 
  called 'MC360'. So the folder that holds the skin for Uitzendinggemist.v2 should also be 
  called 'MC360' and should be located in the '<scriptfolder of uitzendinggemist>\skins\' 
  folder (which is usually scripts\uitzendinggemist\skins\'.
  If no identically named folder is found. The skin located in the 'Skins\Default' folder 
  is used.
* Inside the skin-folder should at least be a 'Media' and 'PAL' folder. The Media folder 
  holds all the images and the PAL folder the XML for the PAL oriented skins (See XBMC 
  Wiki for more info on skinning-folders).
* The XML files that need to be present are called 'progwindow.xml' and 'channelwindow.xml'. 
* IMPORTANT: Never remove the items which have ID's. These are mandatory for the script. 
  Their appearance can be changed. But they may NEVER be removed. They should keep their ID's. 
* The 'progwindow.xml' holds all the layout for the main window from where the channels
  can be chosen.
* The 'channelwindow.xml' holds all the layout for the episode windows. This is the windows
  from where you can select the episodes.

If you have made a skin, please mail it to me at uitzendinggemist.vx[@t]gmail[d0t]com so 
it can be included in future releases.

--------------------------------------------------------------------------------------------
 4. Known Limitations
--------------------------------------------------------------------------------------------
* Older XBMC builds do not completely support playing of ASF playlist files and streaming 
will fail. Updating to a more recent build of XBMC will solve the problem.
* Not all Kanalenkiezer channels are working. This is a limitation of the www.kanalenkiezer.nl
website. It cannot be fixed. I can override stream-urls. But therefore I need the correct 
URL's for the stream. You can mail them to: uitzendinggemist.vx[@t]gmail[d0t]com with a clear
description of the channel and stream URL.

--------------------------------------------------------------------------------------------
 4.a Some channels are not working? How come?
--------------------------------------------------------------------------------------------
Very often the problem is not the script but the site that is having the problems! So before
you start posting/writing-e-mails/sending-me-logfiles CHECK THE WEBSITES of the channels 
first. Go to www.uitzendinggemist.nl, www.tien.tv, www.rtl.nl, joox.net and/or 
www.pczapper.tv to see if the websites are up and running. If they are not working, neither
will Uitzendinggemist.v2!
If you have verified that the websites are up and running and the script is still not 
working then start posting/writing-e-mails/sending-me-logfiles, but please, always include
the COMPLETE uzg.log logfile so I can see what the problem is.

--------------------------------------------------------------------------------------------
 5. Acknowledgement
--------------------------------------------------------------------------------------------
The first idea for XOT-Uzg came from a script by by BaKMaN (http://xbox.readrss.com).

I would like to thank Ian Parker from Evanescent Light Photography 
(http://parkerlab.bio.uci.edu/evlight.htm) for allowing me to use one of his pictures as 
the channel background in the Confluece skin.  

--------------------------------------------------------------------------------------------
 6. Donations
--------------------------------------------------------------------------------------------
The following persons have supported XOT by donating (the list is sorted chronologically): 
- David Testas 
- Stef Olde Scholtenhuis 
- Gerhard ten Hove 
- J.C. Frerichs 
- Kenny Horbach 
- Laurens De Graaff 
- Stehpan van Rooij
- Niels Walta
- Rene Wieldraaijer
- Bastiaan van Perlo
- Anton Vanhoucke
- Niels van den Boogaard
- Ferry Plekkenpol
- Michel Bos 
- M. Spaans 
- Rogier Duurkoop 
- Jonthe Grotenhuis 
- Maurice van Trijffel 
- Bjorn Stam 
- Prism Open Source 
- Serge Kapitein 
- Robbert Hilgeman 
- Jorn Luttikhold 
- Tom de Goeij
- Gecko (Martijn Pet)
- Henri Lier 
- Edwin Endstra 
- Fabian Labohm 
- Jeroen van den Burg 
- Ronald Geerlings 
- Simon Algera 
- Floris Dirkzwager 
- Jurjen van Dijk 
- J. Tebbes 
- Dennis808 
- Joost Wouterse 
- Slashbot28 
- Jasper Westerhof 
- Jacques Overdijk 
- Ramon Broekhuijzen
- Eymert Versteegt
- Rick van Venrooij 
- Frans Hondeman 
- RSJ Kok 
- Jamie Janssen 
- Thomas Novin 
- Emiel Havinga 
- De php programmeur 
- Tijs Gerritsen  
- Bonny Gijzen
- Dennis van Kapel
- Cameq
- Bart Macco
- Markus Sjöström
- Mathijs Groothuis
- Rene Popken
- KEJ Kamperman
- Angelo Potter
- Athlete Hundrafemtionio
- Dennis Brekelmans
- Ted Backman
- Michiel Klooster
- Webframe.NL
- Jan Willemsen
- Marcin Holmstrom
- Örjan Magnusson
- M H Jongen
- Ola Lindberg
- Elcyion
- Dennis van Kapel
- Pieter Geljon
- Andreas Ljunggren
- Miroslav Puskas
- Floris van de Kamer
- Walter Bressers
- Sjoerd Molenaar
- Patrik Johansson
- Willy van Knippenberg
- Stephan van Rooij
- D J vd Wielen 
- Erik Bots
- Alexander Jongeling
- Robert Thörnberg
- Tom Urlings
- Dirk Jeroen Breebaart
- Hans Nijhuis
- Michel ten Hove
- Rick van Venrooij
- Mattias Lindblad
- Anton Opgenoort
- Jasper van den Broek
- Dick Branderhorst
- Mans Jonasson
- Frans Dijkstra
- Michael Forss
- Dick Verwoerd
- Dimitri Olof Areskogh
- Andreas Hägg
- Oscar Gala y Hondema
- Tjerk Pruyssers
- Ramon de Klein
- Wouter Maan
- Thomas Novin
- Arnd Brugman
- David Kvarnberg
- Jasper van den Broek
- Jeroen Koning 
- Saskia Dijk
- Erik Hond
- Frank Hart
- Rogier Werschkull
- Chris Evertz
- Reinoud Vaandrager
- Lucas van der Haven
- Robert Persson
- Harm Verbeek
- Lars lessel
- Just van den Broecke
- Arvid van Kasteel
- G.F.P. van Dijck
- Thijs van Nuland
- Mathijs van der Kooi
- Michael Rydén
- Jelmer Hartman
- Tirza Bosma
- Tijmen Klein
- Chris de Jager
- Albert Kaufman
- Erik Abbevik
- Scott Beijn
- Peter van der Velden
- Jens Lindberg
- Derek Smit