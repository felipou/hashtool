#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# hashtool - hashing of entire trees of files
# Copyright (C) 2015 - Felipe Machado
#
#

import os.path
import argparse
import hashlib

from build import buildTreeHash
from duplicates import findDuplicates
from compare import compare


###############################################################################
def inexistentFile(x):
    if os.path.exists(x):
        raise argparse.ArgumentTypeError( "{0} already exists".format(x) )
    return os.path.abspath(x)

def isFolder(x):
    if os.path.exists(x) and os.path.isdir(x):
        return os.path.abspath(x)

    raise argparse.ArgumentTypeError(
        "{0} is not an existing folder".format(x) )

def isFile(x):
    if os.path.exists(x) and os.path.isfile(x):
        return os.path.abspath(x)

    raise argparse.ArgumentTypeError(
        "{0} is not an existing file".format(x) )

def commaSplitString( x ):
    hash_functions = x.split(',')

    for hash_function in hash_functions:
        if hash_function not in hashlib.algorithms_available:
            raise argparse.ArgumentTypeError(
                "Invalid hash function {0}".format( hash_function ) )

    return hash_functions

def parseArgs():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers( dest='command' )

    parser_build = subparsers.add_parser( 'build' )
    parser_build.add_argument( 'path', type=isFolder )
    parser_build.add_argument( '-o', '--out', metavar='OUTPUT_FILE',
                               type=inexistentFile )
    parser_build.add_argument( '-H', '--hashes', metavar='HASHES',
                               type=commaSplitString, default=["sha1"] )
    parser_build.set_defaults( func=buildTreeHash )

    parser_duplicates = subparsers.add_parser( 'find_duplicates' )
    parser_duplicates.add_argument( 'hash_db', type=isFile )
    parser_duplicates.add_argument( '-p', '--print-single-files',
                                    action="store_true",
                                    default=False )
    parser_duplicates.add_argument( '--print-folders-with-both',
                                    action="store_true",
                                    default=False )
    parser_duplicates.add_argument( '--print-folders-with-originals',
                                    action="store_true",
                                    default=False )
    parser_duplicates.add_argument( '--dont-print-folders-with-duplicates',
                                    action="store_true",
                                    default=False )
    parser_duplicates.add_argument( '-x', '--prefix', metavar='PREFIX',
                                    type=str, default=None )
    parser_duplicates.set_defaults( func=findDuplicates )

    parser_compare = subparsers.add_parser( 'compare' )
    parser_compare.add_argument( 'hash_db1', type=isFile )
    parser_compare.add_argument( 'hash_db2', type=isFile )
    parser_compare.add_argument( '--print-single-files',
                                 action="store_true",
                                 default=False )
    parser_compare.add_argument( '--two-way',
                                 action="store_true",
                                 default=False )
    parser_compare.set_defaults( func=compare )

    args = parser.parse_args()

    if not args.command:
        parser.print_usage()
        exit(1)

    return args

def main():
    args = parseArgs()
    args.func(args)
###############################################################################



###############################################################################
if __name__ == '__main__':
    main()
###############################################################################
