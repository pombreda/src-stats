#!/usr/bin/env python

import sys
import math

from optparse import OptionParser
from cStringIO import StringIO

from languages import Language
from linecounter import count_file, Result
from table import Table, Column
from vcs import VcsWrapper

parser = OptionParser('usage: %prog [options] file [file ...]')
parser.add_option('-l', '--by-language',
                  help='Order result by language instead of by file',
                  default=False,
                  action="store_true")

def add_results(dest, src):
    dest.source += src.source
    dest.comment += src.comment
    dest.blank += src.blank

def sum_result(result):
    return result.source + result.comment + result.blank

def print_result_set(table, header, result):
    print table.row((header,
                     result.source,
                     result.comment,
                     result.blank,
                     sum_result(result)))

def print_totals(table, totals):
    print table.separator()
    print_result_set(table, 'Total', totals)

def print_language_stats(table, language_stats):
    items = language_stats.items()
    items.sort(cmp=lambda x, y: cmp(sum_result(x[1]),
                                    sum_result(y[1])),
               reverse=True)
    
    for lang, stats in items:
        print_result_set(table, lang.name, stats)

def process_file(table, options, language_stats, totals, filename, stream):
    lang = Language.from_filename(filename)

    if not lang:
        return False
    
    result = count_file(stream, lang)
    
    add_results(totals, result)
    
    if options.by_language:
        if lang not in language_stats:
            language_stats[lang] = Result()
            
        add_results(language_stats[lang], result)
    else:
        print_result_set(table, filename, result)

    return True

def main_func():
    (options, args) = parser.parse_args()

    if not args:
        parser.print_usage()
        return 1

    table = Table((Column('Filename', align='l'),
                   Column('Source', 9, align='r'),
                   Column('Comments', 11, align='r'),
                   Column('Blank', 8, align='r'),
                   Column('Total', 11, align='r')))
    
    print table.header()
    print table.separator()

    totals = Result()

    language_stats = {}
    files_processed = 0

    for filename in args:
        try:
            could_process = process_file(table, options, language_stats, totals, filename, open(filename))
        except IOError:
            could_process = False

        if not could_process:
            vcs = VcsWrapper.vcs_for_path(filename)

            if not vcs:
                continue

            for f in vcs.head.file_iter:
                if process_file(table, options, language_stats, totals, f.path, StringIO(f.stream.read())):
                    files_processed += 1
        else:
            files_processed += 1

    if options.by_language:
        print_language_stats(table, language_stats)

    if len(language_stats) > 1 or (not options.by_language and files_processed):
        print_totals(table, totals)
