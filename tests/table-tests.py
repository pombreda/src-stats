from srcstats.table import Column, Table

def test_column_constructor():
    col = Column('Header', 10, 'r')
    assert col.header == 'Header'
    assert col.width == 10
    assert col.align == 'r'

def test_column_header_justification():
    assert Column('Header', 10, 'r').justified_header() == '  Header |'
    assert Column('Header', 10, 'l').justified_header() == 'Header   |'
    assert Column('Header', 10, 'c').justified_header() == ' Header  |'

    assert Column('Header', 10, 'r').justified_header(False) == '    Header'
    assert Column('Header', 10, 'l').justified_header(False) == 'Header    '
    assert Column('Header', 10, 'c').justified_header(False) == '  Header  '

def test_column_data_justification():
    assert Column('Header', 10, 'r').justified_data('Test') == '      Test'
    assert Column('Header', 10, 'l').justified_data('Test') == 'Test      '
    assert Column('Header', 10, 'c').justified_data('Test') == '   Test   '

def test_too_wide_column_data_justification():
    assert Column('Header', 3, 'r').justified_data('Test') == 'est'
    assert Column('Header', 3, 'l').justified_data('Test') == 'est'
    assert Column('Header', 3, 'c').justified_data('Test') == 'est'

def test_table_constructor():
    t = Table((Column('A', 60),
               Column('B', 20)),
              width=80)

    assert t.width == 80
    assert t.columns[0].header == 'A'
    assert t.columns[0].width == 60
    assert t.columns[1].header == 'B'
    assert t.columns[1].width == 20

def test_auto_width_columns():
    t = Table((Column('A'),
               Column('B')),
              width=10)

    assert t.columns[0].width == 5
    assert t.columns[1].width == 5

def test_uneven_auto_width_columns():
    t = Table((Column('A'),
               Column('B'),
               Column('C')),
              width=10)

    assert t.columns[0].width == 4
    assert t.columns[1].width == 3
    assert t.columns[2].width == 3

def test_mixed_fixed_auto_columns():
    t = Table((Column('A', 5),
               Column('B'),
               Column('C')),
              width=10)

    assert t.columns[0].width == 5
    assert t.columns[1].width == 3
    assert t.columns[2].width == 2

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
    t = Table((Column('A', align='l'),
               Column('B', align='l')),
              width = 10)

    assert t.header() == 'A   |B    '
