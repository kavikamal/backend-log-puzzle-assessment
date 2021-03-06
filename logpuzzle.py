#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U;
Windows NT 5.1; en-US; rv:1.8.1.6)
Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # Method - 1
    # hostname = filename.rsplit('_', 1)
    # with open(filename, 'rt') as in_file:  # Open file for reading the text
    #     contents = in_file.read()
    #     result = re.findall(r'GET (\S*) HTTP', contents)
    #     result = [url for url in result if "puzzle" in url]
    #     new_list = []
    #     [new_list.append('http://'+hostname[-1]+url) for url in result]
    # return sorted(set(new_list))

    hostname = filename.rsplit('_', 1)
    # Open file for reading of text data.
    with open(filename, 'rt') as in_file:
        # Read the entire file into a variable named contents.
        contents = in_file.read()
        result = re.findall(r'GET (\S*) HTTP', contents)
        result = [url.rpartition('-') for url in result if "puzzle" in url]
        result = set(result)  # Removes the duplicate urls
        result = sorted(result, key=lambda tup: (tup[-1]))  # Sort the urls
        new_list = []
        [new_list.append('http://'
                         + hostname[-1]
                         + (''.join(url))) for url in result]
    return new_list


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)  # Create dest_dir if not exist already
    os.chdir(dest_dir)  # Change the current working dir to dest_dir
    with open('index.html', 'w+') as f:
        f.write('<html>\n<body>\n')
        for i in range(len(img_urls)):
            print "Retrieving..."+img_urls[i]
            urllib.urlretrieve(img_urls[i], 'img'+str(i))
            f.write('<img src="%s">' % ('img'+str(i)))
        f.write('\n</body>\n</html>')
    pass


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)
    if parsed_args.todir:
        print "download"
        download_images(img_urls, parsed_args.todir)
    else:
        print '\n'.join(img_urls)


if __name__ == '__main__':
    main(sys.argv[1:])
