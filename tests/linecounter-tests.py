import srcstats.linecounter as lc
import srcstats.languages as langs

import unittest

from cStringIO import StringIO

class LineCounterTest(unittest.TestCase):
    testlang = langs.Language('Test Language',
                              tuple(),
                              {'to_eol': ('//', '#'),
                               'between': ((r'/\*', r'\*/'), (r'\(-', r'-\)'))})
    
    def test_blank_lines(self):
        src = '''

'''

        f = StringIO(src)

        result = lc.count_file(f, self.testlang)

        self.assertEqual(result.source, 0)
        self.assertEqual(result.comment, 0)
        self.assertEqual(result.blank, 3)

    def test_source_lines(self):
        src = '''test
        test
        test'''

        result = lc.count_file(StringIO(src), self.testlang)

        self.assertEqual(result.source, 3)
        self.assertEqual(result.comment, 0)
        self.assertEqual(result.blank, 0)

    def test_source_blank_mixed(self):
        src = '''test

        test
        '''

        result = lc.count_file(StringIO(src), self.testlang)

        self.assertEqual(result.source, 2)
        self.assertEqual(result.comment, 0)
        self.assertEqual(result.blank, 2)

    def test_one_line_comments_first(self):
        src1 = '// a comment'
        src2 = '# a comment'

        for src in (src1, src2):
            result = lc.count_file(StringIO(src), self.testlang)

            self.assertEqual(result.source, 0)
            self.assertEqual(result.comment, 1)
            self.assertEqual(result.blank, 0)

    def test_one_line_comments_source_mixed(self):
        src = 'test test // a comment'
        result = lc.count_file(StringIO(src), self.testlang)

        self.assertEqual(result.source, 1)
        self.assertEqual(result.comment, 0)
        self.assertEqual(result.blank, 0)

    def test_multi_line_comment_start(self):
        self.assertEqual(lc.line_is_multi_line_comment_start('/* a comment\n', self.testlang),
                         (0, False))
        self.assertEqual(lc.line_is_multi_line_comment_start('not a comment\n', self.testlang)[0],
                         None)
        self.assertEqual(lc.line_is_multi_line_comment_start('code /* a comment\n', self.testlang),
                         (0, True))
        self.assertEqual(lc.line_is_multi_line_comment_start('code (- a comment\n', self.testlang),
                         (1, True))

    def test_multi_line_comment_end(self):
        self.assertEqual(lc.line_is_multi_line_comment_end('a comment*/\n', self.testlang),
                         (0, False))
        self.assertEqual(lc.line_is_multi_line_comment_end('not a comment\n', self.testlang)[0],
                         None)
        self.assertEqual(lc.line_is_multi_line_comment_end('a comment */code\n', self.testlang),
                         (0, True))
        self.assertEqual(lc.line_is_multi_line_comment_end('a comment -)code\n', self.testlang),
                         (1, True))
        
    def test_multi_line_comments(self):
        src1 = '''/* a comment

        */'''
        src2 = '''(- a comment
        
        -)'''
        src3 = '''/* a comment
        -)
        */'''

        src4 = '''code/* a comment

        */code
        '''

        for src in (src1, src2, src3):
            result = lc.count_file(StringIO(src), self.testlang)

            self.assertEqual(result.source, 0)
            self.assertEqual(result.comment, 3)
            self.assertEqual(result.blank, 0)

        result = lc.count_file(StringIO(src4), self.testlang)
        self.assertEqual(result.source, 2)
        self.assertEqual(result.comment, 1)
        self.assertEqual(result.blank, 1)

    def test_single_multi_line_comments(self):
        src1 = '''/* a comment */

        code'''
        src2 = '''(- a comment -)

        code'''

        for src in (src1, src2):
            result = lc.count_file(StringIO(src), self.testlang)

            self.assertEqual(result.source, 1)
            self.assertEqual(result.comment, 1)
            self.assertEqual(result.blank, 1)

    def test_c_cpp(self):
        src = '''#include <stdio.h>

/* A simple program that will echo "Hello World" */
int main(int argc, char **argv) {
    printf("Hello World\\n");
    return 0;
}
'''
        result = lc.count_file(StringIO(src), langs.Language.by_name('C/C++'))

        assert result.source == 5
        assert result.comment == 1
        assert result.blank == 2

    def test_c_cpp_header(self):
        src = '''#ifndef __HEADER__
#define __HEADER__

int foo_function(); // Does some magic

// This function does som magic too
int bar_function();
#endif
'''
        result = lc.count_file(StringIO(src), langs.Language.by_name('C/C++ Header'))

        assert result.source == 5
        assert result.comment == 1
        assert result.blank == 3

    def test_c_sharp(self):
        src = '''import System;

// My namespace
namespace Foo
{
  class MainClass
  {
    public static void Main(string[] args)
    {
      Console.WriteLine("Hello there");
    }
  }
}
'''

        result = lc.count_file(StringIO(src), langs.Language.by_name('C#'))

        assert result.source == 11
        assert result.comment == 1
        assert result.blank == 2

    def test_python(self):
        src = '''#!/usr/bin/python

if __name__ == \'__main__\': # Standard preamble
    print "Hi there"
'''

        result = lc.count_file(StringIO(src), langs.Language.by_name('Python'))

        assert result.source == 2
        assert result.comment == 1
        assert result.blank == 2

    def test_makefile(self):
        src = '''CC=gcc-4.2 # Old version

# A simple target spec
target: dependent
    $(CC) dependent
'''

        result = lc.count_file(StringIO(src), langs.Language.by_name('Makefile'))

        assert result.source == 3
        assert result.comment == 1
        assert result.blank == 2
