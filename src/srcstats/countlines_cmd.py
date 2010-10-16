#!/usr/bin/env python

import sys
import math

from languages import Language
from linecounter import count_file
from table import Table, Column

def main_func():
    if len(sys.argv) == 1:
        print >>sys.stderr, 'Usage: %s filename [filename ...]'
        return 1

    table = Table((Column('Filename', align='l'),
                   Column('Source', 9, align='r'),
                   Column('Blank', 9, align='r'),
                   Column('Total', 9, align='r')))

    print table.header()
    print table.separator()

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

        print table.row((filename,
                         result.source,
                         result.comment,
                         result.blank,
                         result.source + result.comment + result.blank))

    if len(sys.argv) > 2:
        print table.separator()
        print table.row(('Total',
                         source_total,
                         comment_total,
                         blank_total,
                         source_total + comment_total + blank_total))
