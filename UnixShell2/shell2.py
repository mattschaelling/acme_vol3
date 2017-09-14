# shell2.py
"""Volume 3: Unix Shell 2.
Matthew Schaelling
Math 402
September 7, 2017
"""

import os
from os.path import join, getsize
import fnmatch
from glob import glob


# Problem 5
def grep(target_string, file_pattern):
    """Find all files in the current directory or its subdirectories that
    match the file pattern, then determine which ones contain the target
    string.

    Parameters:
        target_string (str): A string to search for in the files whose names
            match the file_pattern.
        file_pattern (str): Specifies which files to search.
    """
    matching_files = []
    # '''
    for f in glob("**/" + file_pattern, recursive = True):
        with open(f, 'r') as handle:
            if target_string in handle.read():
                matching_files.append(f)
    return matching_files
    '''
    for root, dirs, files in os.walk("."):
        for f in files:
            if fnmatch.fnmatch(f, file_pattern):
                with open(join(root,f), 'r') as handle:
                   if target_string in handle.read():
                       matching_files.append(join(root, f))
    return matching_files
    '''


# Problem 6
def largest_files(n):
    """Return a list of the n largest files in the current directory or its
    subdirectories (from largest to smallest).
    """
    file_sizes = []
    for root, dirs, files in os.walk("."):
        for name in files:
            file_sizes.append([getsize(join(root, name)), join(root, name)])
    file_sizes = sorted(file_sizes, key = lambda tup: tup[0], reverse = True)
    big_files = []
    for i in range(n):
        big_files.append(file_sizes[i][1])
    return big_files
