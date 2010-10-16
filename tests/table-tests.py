from nose.tools import *

from srcstats.table import Column, Table

def test_column_constructor():
    col = Column('Header', 10, 'r')
    eq_(col.header, 'Header')
    eq_(col.width, 10)
    eq_(col.align, 'r')

def test_column_header_justification():
    eq_(Column('Header', 10, 'r').justified_header(), '  Header |')
    eq_(Column('Header', 10, 'l').justified_header(), ' Header  |')
    eq_(Column('Header', 10, 'c').justified_header(), ' Header  |')

    eq_(Column('Header', 10, 'r').justified_header(False), '   Header ')
    eq_(Column('Header', 10, 'l').justified_header(False), ' Header   ')
    eq_(Column('Header', 10, 'c').justified_header(False), '  Header  ')

def test_column_data_justification():
    eq_(Column('Header', 10, 'r').justified_data('Test'), '    Test |')
    eq_(Column('Header', 10, 'l').justified_data('Test'), ' Test    |')
    eq_(Column('Header', 10, 'c').justified_data('Test'), '  Test   |')

def test_too_wide_column_data_justification():
    eq_(Column('Header', 5, 'r').justified_data('Test'), 'est |')
    eq_(Column('Header', 5, 'l').justified_data('Test'), 'est |')
    eq_(Column('Header', 5, 'c').justified_data('Test'), 'est |')

def test_table_constructor():
    t = Table((Column('A', 60),
               Column('B', 20)),
              width=80)

    eq_(t.width, 80)
    eq_(t.columns[0].header, 'A')
    eq_(t.columns[0].width, 60)
    eq_(t.columns[1].header, 'B')
    eq_(t.columns[1].width, 20)

def test_auto_width_columns():
    t = Table((Column('A'),
               Column('B')),
              width=10)

    eq_(t.columns[0].width, 5)
    eq_(t.columns[1].width, 5)

def test_uneven_auto_width_columns():
    t = Table((Column('A'),
               Column('B'),
               Column('C')),
              width=10)

    eq_(t.columns[0].width, 4)
    eq_(t.columns[1].width, 3)
    eq_(t.columns[2].width, 3)

def test_mixed_fixed_auto_columns():
    t = Table((Column('A', 5),
               Column('B'),
               Column('C')),
              width=10)

    eq_(t.columns[0].width, 5)
    eq_(t.columns[1].width, 3)
    eq_(t.columns[2].width, 2)

def test_too_wide_should_raise():
    try:
        t = Table((Column('A', 10),
                   Column('B', 10)),
                  width=10)
    except AssertionError:
        return

    assert False

def test_no_space_left_should_raise():
    try:
        t = Table((Column('A', 5),
                   Column('B', 5),
                   Column('C')),
                  width=10)
    except AssertionError:
        return

    assert False

def test_table_header():
    eq_(Table((Column('A', align='l'),
               Column('B', align='l')),
              width=10).header(),
        ' A  | B   ')
    eq_(Table((Column('A', align='r'),
               Column('B', align='r')),
              width=10).header(),
        '  A |   B ')

def test_table_separator():
    eq_(Table((Column('A', align='r'),
               Column('B', align='r')),
              width=10).separator('='),
        '==========')

def test_table_row():
    eq_(Table((Column('A', align='l'),
               Column('B', align='l')),
              width=18).row(('data1', 'data2')),
        ' data1  | data2   ')

    eq_(Table((Column('A', align='r'),
               Column('B', align='r')),
              width=18).row(('data1', 'data2')),
        '  data1 |   data2 ')
