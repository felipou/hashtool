# -*- coding: utf-8 -*-

from __future__ import print_function

from utils import loadHashDBFile, shouldIgnore

import gzip
import os.path
import re

###############################################################################
def get_hash_db( files_db ):
    hashes_db = {}
    for f in files_db:
        if shouldIgnore( f, None ):
            continue

        #files_db[ f ][ "hashes" ]
        if "hashes" in files_db[ f ]:
            for hash_function in files_db[ f ][ "hashes" ]:
                hash_value = files_db[ f ][ "hashes" ][ hash_function ]

                hashes_db[ hash_function + "_" + hash_value ] = {
                    "size": files_db[ f ][ "size" ],
                    "path": f
                }
        else:
            hashes_db[ "sha1_" + files_db[ f ][ "hash" ] ] = {
                "size": files_db[ f ][ "size" ],
                "path": f
            }

    return hashes_db


def compare_hash_dbs( d1, d2 ):
    not_in = []
    for h in d2:
        if h not in d1:
            not_in.append( d2[ h ][ "path" ] )

    return not_in


def get_folders( file_list ):
    folders = {}
    for f in file_list:
        fdir = os.path.dirname(f)
        folders[ fdir ] = folders.get( fdir, 0 ) + 1

    return folders


def compare( config ):

    d1 = loadHashDBFile( config.hash_db1 )
    d2 = loadHashDBFile( config.hash_db2 )

    hashes1 = {}

    hashes1 = get_hash_db( d1 )
    hashes2 = get_hash_db( d2 )

    not_in1 = compare_hash_dbs( hashes1, hashes2 )

    if config.print_single_files:
        print( "\nFiles not included in first hash database:" )
        for f in sorted( not_in1 ):
            print( f )
    else:
        print( "\nFolders with files not included in first hash database:" )
        for ( f, count ) in sorted( get_folders( not_in1 ).items() ):
            print( f, " - ", count, " files" )

    if config.two_way:
        not_in2 = compare_hash_dbs( hashes2, hashes1 )

        if config.print_single_files:
            print( "\nFiles not included in second hash database:" )
            for f in sorted( not_in2 ):
                print( f )
        else:
            print( "\nFolders with files not included in second hash database:" )
            for f in sorted( get_folders( not_in2 ) ):
                print( f )
