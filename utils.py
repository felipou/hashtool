# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from builtins import str

import json
import gzip
import re
import os.path

###############################################################################
def loadHashDBFile( filename ):
    if filename[-3:] == ".gz":
        f = gzip.open( filename, 'rb' )
    else:
        f = open( filename, 'rb' )

    return json.loads( str( f.read(), "utf-8" ) )
###############################################################################



###############################################################################
data_size_suffixes = [ "Bytes", "KB", "MB", "GB", "TB" ]

def formatDataSize( size_in_bytes ):
    size_in_bytes = float( size_in_bytes )
    count = 0

    while size_in_bytes > 1000 and count < len( data_size_suffixes ) - 1:
        size_in_bytes /= 1000
        count += 1

    return str( size_in_bytes ) + " " + data_size_suffixes[ count ]
###############################################################################



###############################################################################
ignored_files = [ ]
ignore_regexes = [ ]

def shouldIgnore( file_path, prefix ):
    if prefix is not None and not file_path.startswith( prefix ):
        return True

    for name in ignored_files:
        if os.path.basename( file_path ) == name:
            return True

    for name in ignore_regexes:
        if re.match( name, os.path.basename( file_path ) ):
            return True

    return False
###############################################################################
