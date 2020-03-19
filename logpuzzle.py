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
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700]
"GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-"
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6)
Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def sort_puzzle(url):
    """
    Looks through a list of urls grabbing an individual url and seeing if it
    matches the regex and if it does it will return only the 2nd group
    in the regex
    """
    match = re.search(r'-(\w+)-(\w+)\.\w+', url)
    if match:
        return match.group(2)
    else:
        return url


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    # print(hostname)
    """
    Opens the file that the user specified.
    Searches to see if the host name is found.

    """
    with open(filename, "r") as document:
        puzzle_urls = []
        hostname = re.search(r"\_(code\.google\.com)", filename)
        if not hostname:
            print("Hostname not found")
            sys.exit(1)
        hostname = hostname.group(1)
        hostname_url = "http://" + hostname
        # print(hostname)
        document_text = document.read()
        # print(document_text)
        """
        Finds all the strings that match the regex.
        Then loops through the matched strings to see if they already exist
        in the puzzle_urls list.
        Finally it sorts the list with the key sort_puzzle function.
        """
        puzzle_list = re.findall(
            r"\"[GET]+\s([\/\w\-]+/puzzle/[\w\-.]+)",
            document_text)
        for url in puzzle_list:
            hostname_url += url
            if hostname_url not in puzzle_urls:
                # print(hostname_url)
                puzzle_urls.append(hostname_url)
            hostname_url = "http://" + hostname
        return sorted(puzzle_urls, key=sort_puzzle)


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    with open(os.path.join(dest_dir, 'index.html'), 'w') as index:
        """
        After the index.html is joined with the desired directory
        it wites the opening tags then loops through the list of
        urls and renames them to img1. img2, ect...
        Finally it will download the images and join them with desired
        directory.
        After the loop is finished it adds the closing tags.
        """
        index.write('<html><body>\n')
        img_count = 0
        for img_url in img_urls:
            local_name = 'img%d' % img_count
            print('Retrieving...', img_url)
            urllib.urlretrieve(img_url, os.path.join(dest_dir, local_name))
            index.write('<img src="%s">' % local_name)
            img_count += 1
        index.write('\n</body></html>\n')
        # print(url_dict.keys())


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
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
        """
        Checks if the directory the user inputs exists
        if the directory does not exist it will create it.
        """
        if os.path.exists(parsed_args.todir):
            download_images(img_urls, parsed_args.todir)
        else:
            os.makedirs(parsed_args.todir)
            download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
