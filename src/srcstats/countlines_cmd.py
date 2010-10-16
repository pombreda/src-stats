#!/usr/bin/env python

import sys
import math

from languages import Language
from linecounter import count_file

def main_func():
    if len(sys.argv) == 1:
        print >>sys.stderr, 'Usage: %s filename [filename ...]'
        return 1

    print ' Filename%sSource | Comment | Blank  |  Total' % (' '*37, )
    print '='*80

    source_total = 0
    comment_total = 0
    blank_total = 0

    for filename in sys.argv[1:]:
        lang = Language.from_filename(filename)

        if not lang:
            continue
        
        result = count_file(open(filename), lang)

        source_total += result.source
        comment_total += result.comment
        blank_total += result.blank

        print '%s%s%s | %s | %s  |  %s' % (filename[-46:],
                                           ' '*(max(0, 46-len(filename))),
                                           str(result.source).rjust(6),
                                           str(result.comment).rjust(7),
                                           str(result.blank).rjust(5),
                                           str(result.source +
                                               result.comment +
                                               result.blank).rjust(5))

    if len(sys.argv) > 2:
        print '='*80
        print ' Total%s%s | %s | %s  |  %s' % (' '*40,
                                               str(source_total).rjust(6),
                                               str(comment_total).rjust(7),
                                               str(blank_total).rjust(5),
                                               str(source_total +
                                                   comment_total +
                                                   blank_total).rjust(5))
