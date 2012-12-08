
import urllib,re,xbmc,os
import xbmcaddon


addon = xbmcaddon.Addon(id='script.module.recaptcha')
profile_path = xbmc.translatePath(addon.getAddonInfo('profile'))

if not (os.path.exists(profile_path)):
    try:
        os.makedirs(profile_path)
    except:
        print "folder creation failed"

challengefile = profile_path +'challengeToken'

def _open(filename):
     fh = open(filename, 'r')
     contents=fh.read()
     fh.close()
     return contents

def _save(filename,contents):  
     fh = open(filename, 'w')
     fh.write(contents)  
     fh.close()

def checkForReCaptcha(html):
     #check for recaptcha in the page source, and return true or false.
     if 'recaptcha_challenge_field' in html:
          return True
     else:
          return False


def checkIfSuceeded(html):
     #reverse the boolean to check for success.
     if 'recaptcha_challenge_field' in html:
          return False
     else:
          return True

def getCaptcha(html):
     #get the captcha image url and save the challenge token
     print 'initiating recaptcha passthrough'

     try:
         token = (re.compile('http://www.google.com/recaptcha/api/noscript\?k\=(.+?)"').findall(html))[0]
     except:
         print "couldn't find the challenge token"

     try:
         challengehtml = urllib.urlopen('http://www.google.com/recaptcha/api/challenge?k=' + token)
     except:
         print "couldn't load the challenge url"
         

     try:
         challengeToken = (re.compile("challenge : '(.+?)'").findall(challengehtml.read()))[0]
     except:
         print "couldn't get challenge code"
        
     imageurl = 'http://www.google.com/recaptcha/api/image?c=' + challengeToken

     #hacky method --- save challenge to file, to reopen in next step
     _save(challengefile, challengeToken)

     return imageurl


def buildResponse(solved):
     #build the response
     try:       
         challengeToken = _open(challengefile)
     except:
         print 'failed to open the challengeToken file'
     else:
         print 'challenge token: '+challengeToken
         
     parameters = urllib.urlencode({'recaptcha_challenge_field': challengeToken, 'recaptcha_response_field': solved})

     return parameters
