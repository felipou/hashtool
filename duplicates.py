# -*- coding: utf-8 -*-
#
# hashtool - hashing of entire trees of files
# Copyright (C) 2015 - Felipe Machado
#
#

from __future__ import print_function

import os.path
import re

from utils import loadHashDBFile, formatDataSize, shouldIgnore

###############################################################################
FOLDER_HAS_DUPLICATES = 0
FOLDER_HAS_ORIGINALS = 1
FOLDER_HAS_DUPLICATES_AND_ORIGINALS = 2


def updateFoldersStates( folders_data, file_path, is_original ):
    current_path = file_path

    while os.path.split( current_path )[1]:
        current_path = os.path.split( current_path )[0]

        if current_path in folders_data:
            if ( ( folders_data[ current_path ] == FOLDER_HAS_ORIGINALS
                    and
                    not is_original )
                or
                ( folders_data[ current_path ] == FOLDER_HAS_DUPLICATES
                    and
                    is_original ) ):

                folders_data[ current_path ] == FOLDER_HAS_DUPLICATES_AND_ORIGINALS

        else:
            folders_data[ current_path ] = ( FOLDER_HAS_ORIGINALS if is_original
                else FOLDER_HAS_DUPLICATES )


def findDuplicates( config ):
    file_db = loadHashDBFile( config.hash_db )

    hashes_map = {}
    count = 0
    acc_size = 0

    duplicate_folders = {}

    for ( file_path, file_metadata ) in sorted( file_db.items(),
                                                key=lambda x: x[0] ):
        if shouldIgnore( file_path, config.prefix ):
            continue

        file_hash = file_metadata["hash"]
        file_folder = os.path.dirname( file_path )

        if file_hash in hashes_map:
            if config.print_single_files:
                print( "'%s' is a duplicate of '%s'"
                    % ( hashes_map[ file_hash ], file_path ) )

            updateFoldersStates( duplicate_folders, file_path, False )

            count += 1
            acc_size += file_metadata["size"]
        else:
            hashes_map[ file_hash ] = file_path

            updateFoldersStates( duplicate_folders, file_path, True )


    print( str( count ) + " duplicates found" )
    print( "Total duplicates size: " + formatDataSize( acc_size ) )


    folders_lists = [ [], [], [] ]

    sorted_duplicate_folders = \
        sorted( [ ( s, d ) for ( d, s ) in duplicate_folders.items() ] )

    for ( folder_state, folder_path ) in sorted_duplicate_folders:
        folders_lists[ folder_state ].append( folder_path )

    if not config.dont_print_folders_with_duplicates:
        folders_list = folders_lists[ FOLDER_HAS_DUPLICATES ]
        print( "Folders with only duplicate files (%d):" % len( folders_list ) )
        for path in folders_list:
            print( path )

    if config.print_folders_with_originals:
        folders_list = folders_lists[ FOLDER_HAS_ORIGINALS ]
        print( "Folders with only original files (%d):" % len( folders_list ) )
        for path in folders_list:
            print( path )

    if config.print_folders_with_both:
        folders_list = folders_lists[ FOLDER_HAS_DUPLICATES_AND_ORIGINALS ]
        print( "Folders with duplicates and originals files (%d):"
            % len( folders_list ) )
        for path in folders_list:
            print( path )
###############################################################################
