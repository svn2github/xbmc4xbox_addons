import os
import xbmc
import xbmcgui
import xbmcplugin
import pydoc


def _get_browse_dialog( default="", heading="", dlg_type=3, shares="files", mask="", use_thumbs=False, treat_as_folder=False ):
    """ shows a browse dialog and returns a value
        - 0 : ShowAndGetDirectory
        - 1 : ShowAndGetFile
        - 2 : ShowAndGetImage
        - 3 : ShowAndGetWriteableDirectory
    """
    dialog = xbmcgui.Dialog()
    value = dialog.browse( dlg_type, heading, shares, mask, use_thumbs, treat_as_folder, default )
    return value

def _create_base_paths():
  try:
    os.makedirs( xbmc.translatePath( doc_path ) )
  except:
    pass

doc_path = _get_browse_dialog( "", "Folder for pydocs"  )
if ( doc_path ):
    _create_base_paths()    

    pDialog = xbmcgui.DialogProgress()
    pDialog.create( "Python Docs Maker" )

    doc = pydoc.HTMLDoc()

    pDialog.update( 0, "Creating pydoc:", xbmc.translatePath( os.path.join( doc_path, "xbmc.html" ) ) )
    f = open( xbmc.translatePath( os.path.join( doc_path, "xbmc.html" ) ), "w" )
    f.write( doc.document( xbmc ) )
    f.close()

    pDialog.update( 33, "Creating pydoc:", xbmc.translatePath( os.path.join( doc_path, "xbmcplugin.html" ) ) )
    f = open( xbmc.translatePath( os.path.join( doc_path, "xbmcplugin.html" ) ), "w" )
    f.write( doc.document( xbmcplugin ) )
    f.close()

    pDialog.update( 67, "Creating pydoc:", xbmc.translatePath( os.path.join( doc_path, "xbmcgui.html" ) ) )
    f = open( xbmc.translatePath( os.path.join( doc_path, "xbmcgui.html" ) ), "w" )
    f.write( doc.document( xbmcgui ) )
    f.close()

    pDialog.update( 100 )
    pDialog.close()
