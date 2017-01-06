#!/usr/bin/env python
'''Utility to manipulate pdf metadata'''

import json
from subprocess import Popen, PIPE

META_TAGS = ['Author', 'Title', 'Subject', 'Keywords']


def read_meta(filename):
    '''Read metadata from pdf'''

    proc = Popen(['exiftool', '-j', filename], stdout=PIPE, stderr=PIPE)
    outs, _ = proc.communicate()
    # take 1st element from list because we only parse one file one time
    allmeta = json.loads(bytes.decode(outs))[0]
    meta = {}
    for key in allmeta:
        if key in META_TAGS:
            meta[key] = allmeta[key]
    return meta


def write_meta(filename, meta):
    '''Write metadata into pdf'''

    # Add SourceFile tag, man exiftool for more informations
    meta['SourceFile'] = '*'
    proc = Popen(['exiftool', '-j=-', '-overwrite_original', filename],
                 stdin=PIPE, stdout=PIPE, stderr=PIPE)
    _, errs = proc.communicate(str.encode(json.dumps([meta])))
    return bytes.decode(errs)


def print_meta(meta):
    '''Print all metadata'''

    for tag in META_TAGS:
        if tag in meta.keys():
            print(tag + ': ' + repr(meta[tag]))
    return


def edit_meta(meta):
    '''Edit metadata'''

    for tag in META_TAGS:
        if tag in meta.keys():
            print(tag + ': ' + repr(meta[tag]))
            try:
                meta[tag] = eval(input(tag + ': '))
            except EOFError:
                print('Tag value unchange')
    return


def main():
    '''The main function'''

    print('Read metadata from README.pdf')
    meta = read_meta('README.pdf')
    print_meta(meta)
    meta['Title'] = 'PDFMeta: Utility for Manipulating Metadata in PDF File'
    meta['Author'] = 'Weida Hong'
    meta['Subject'] = 'Utility'
    meta['Keywords'] = ['pdf', 'metadata']
    print_meta(meta)
    edit_meta(meta)
    print('Write metadata from README.pdf')
    write_meta('README.pdf', meta)
    return

if __name__ == '__main__':
    main()
