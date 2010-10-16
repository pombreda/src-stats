from srcstats.languages import Language

def testExtensions():
    assert Language.from_filename('foo.c').name == 'C/C++'
    assert Language.from_filename('dir/foo.cpp').name == 'C/C++'

def testUnknown():
    assert Language.from_filename('unknown') is None
    assert Language.from_filename('foo.unknown') is None

def testPatterns():
    assert Language.from_filename('Makefile').name == 'Makefile'
