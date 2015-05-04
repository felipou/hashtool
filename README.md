
# Hashtool

Hashtool is an utility for dealing with file content hashes.

Currently it has 3 functions:
- build: builds a "hash database" - walks down a file system path recursively
    calculating the hashes of all the files found, and outputs this info
    in a formatted (json) output
- compare: compares hash databases - checks if all files in one hash database
    are included in the other, using the hashes of the files as key
- duplicates: checks for duplicates in a hash database by simply searching
    for multiple occurrences of the hash of each file

Hashtool is licensed under the GPLv2. For more information, check the LICENSE
file.

## Requirements

Hashtool is built for both Python 2 and Python 3 (using the future library to
help maintain the compatibility), but we suggest using Python 3.

