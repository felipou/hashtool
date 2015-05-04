# -*- coding: utf-8 -*-
#
# hashtool - hashing of entire trees of files
# Copyright (C) 2015 - Felipe Machado
#
#

# Python future imports
from __future__ import print_function

# Python stanrad library
import sys
import os
import os.path
import hashlib
import json
import math
import argparse
import datetime



###############################################################################
def calculateFileHash( path, block_size=50*(2**20), hash_functions = ["sha1"] ):
    # Compact form:
    # return hashlib.sha1(open(path).read()).hexdigest()
    #
    # But reading and updating in blocks is much more efficient
    # for large files, and doesn't require much RAM

    f = open(path, 'rb')
    hash_objs = {}
    for hash_function in hash_functions:
        hash_objs[ hash_function ] = hashlib.new( hash_function )

    while True:
        data = f.read( block_size )
        if not data:
            break

        for hash_function in hash_functions:
            hash_objs[ hash_function ].update(data)

    for hash_function in hash_functions:
        hash_objs[ hash_function ] = hash_objs[ hash_function ].hexdigest()

    f.close()
    return hash_objs


def calculateHashes( files_info, total_size, hash_functions = ["sha1"] ):
    count = 0
    percentage = 0

    for file_path in files_info:
        file_hashes = calculateFileHash( file_path,
            hash_functions=hash_functions )
        files_info[file_path]["hashes"] = file_hashes

        # Progress counting and printing
        count += files_info[file_path]["size"]
        if math.floor( ( 10000 * count ) / total_size ) > percentage:
            percentage = math.floor( ( 10000 * count ) / total_size )
            print( datetime.datetime.now(), percentage / 100, "%", file=sys.stderr )


def createFilesInfoTable( path, files_info={} ):
    total_size = 0

    for f in os.listdir(path):
        filepath = os.path.join( path, f )

        if os.path.isdir(filepath):
            ( subfolder_info, subfolder_size ) = createFilesInfoTable(
                filepath, files_info )

            total_size += subfolder_size
        else:
            file_size = os.path.getsize(filepath)

            files_info[filepath] = {
                "size": file_size
            }

            total_size += file_size

    return ( files_info, total_size )
###############################################################################



###############################################################################
# Public function #
###################
def buildTreeHash( args ):
    root_folder = args.path
    output_file = args.out

    print("Folder: %s" % root_folder, file=sys.stderr)

    ( files_info, total_size ) = createFilesInfoTable(root_folder)

    calculateHashes( files_info, total_size, args.hashes )

    # JSON Pretty print
    json_string = json.dumps( files_info, sort_keys=True, indent=4,
                              separators=(',', ': ') )

    if output_file:
        open( output_file, 'w' ).write(json_string)
    else:
        print( json_string )
###############################################################################
