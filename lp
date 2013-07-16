#!/usr/bin/env python

from zipimport import zipimporter, ZipImportError

try:
    distro = zipimporter('lp.zip')
except ZipImportError:
    print "The 'lp.zip' distribution wasn't found. Try this:"
    print " $ make"


lp = distro.load_module('lp_cli')
lp.main()