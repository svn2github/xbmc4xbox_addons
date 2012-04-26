""" PlayCZ API for accessing www.play.cz streams """

import playcz_root
import playcz_czradio
import urllib

def parse_query(query):
    """ Parse argumets from query like '?param=value&param2=value2'
        and return it as dictionary
    """
    params = {}
    if query:
        query = query.split('?')[-1]
        for part in query.split('&'):
            (key, value) = part.split('=')
            params[key] = urllib.unquote_plus(value)
    return params
    


def main(argv):
    """ Plugin main function. It expects sys.argv as parameter """
    # plugin input args:
    baseurl = argv[0]
    handle  = int(argv[1])
    params  = parse_query(argv[2])

    if not params:
        playcz_root.Root(baseurl, handle)
    elif params.get('folder') == 'czradio':
        playcz_czradio.List(baseurl, handle)
    elif params.get('czradio'):
        playcz_czradio.Play(baseurl, handle, params.get('czradio'))

