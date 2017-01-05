#!/usr/bin/env python
'''Utility to manipulate pdf metadata'''

import json
from subprocess import Popen, PIPE
import sys

class PdfMeta(object):
    '''Class for metadata object'''

    tags = ['Author', 'Title', 'Subject', 'Keywords']


def read_meta(filename):
    '''Read metadata from pdf'''

    proc = Popen(['exiftool', '-j', filename], stdout=PIPE, stderr=PIPE)
    outs, _ = proc.communicate()
    # take 1st element from list because we only parse one file one time
    allmeta = json.loads(bytes.decode(outs, encoding=sys.getdefaultencoding()))[0]
    meta = {}
    for key in allmeta:
        if key in PdfMeta.tags:
            meta[key] = allmeta[key]
    return meta

def write_meta(filename, meta):
    '''Write metadata into pdf'''

    # Add SourceFile tag, man exiftool for more informations
    meta['SourceFile'] = '*'
    proc = Popen(['exiftool', '-j=-', '-overwrite_original', filename], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.communicate(bytes(json.dumps([meta]), encoding=sys.getdefaultencoding()))
    return

def print_meta(meta):
    for tag in meta:
        print(tag + ': ' + str(meta[tag]))

def main():
    '''The main function'''

    print('Read metadata from README.pdf')
    meta = read_meta('README.pdf')
    print_meta(meta)
    meta['Title'] = 'PDFMeta: Simple Utility for Manipulating Metadata in PDF File'
    meta['Author'] = 'Weida Hong'
    meta['Subject'] = 'Utility'
    meta['Keywords'] = ['pdf', 'metadata']
    print('Write metadata from README.pdf')
    print_meta(meta)
    write_meta('README.pdf', meta)
    return

if __name__ == '__main__':
    main()
