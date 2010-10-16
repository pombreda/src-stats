import itertools

class Column(object):
    justifiers = {'l': str.ljust,
                  'r': str.rjust,
                  'c': str.center}
    
    def __init__(self, header, width=None, align='l'):
        """Constructs a column header for use with the Table class.

        Arguments:
        header -- A string that will be the column header,
        width -- The width of the header. If set to None, it will fill available space.
        align -- The textual aligment of both the header and contents. 'l', 'r' or 'c'.
        """
        self.header = header
        self.width = width
        self.align = align

    def justified_header(self, append_pipe=True):
        return self.justified_data(self.header, append_pipe)
    
    def justified_data(self, data, append_pipe=True):
        width = self.width - 2 if append_pipe else self.width

        data = '%s%s%s' % (' ' if self.align == 'l' else '',
                           data,
                           ' ' if self.align == 'r' and not append_pipe else '')
        
        return (self.justifiers[self.align](data, width)[-width:] +
                (' |' if append_pipe else ''))
    

class Table(object):
    def __init__(self, columns, width=80):
        assert len(columns) >= 0
        
        self.columns = columns
        self.width = width

        self._update_column_widths()

    def _update_column_widths(self):
        total_fixed_width = sum(c.width for c in self.columns if c.width)
        auto_columns = [c for c in self.columns if c.width is None]

        assert self.width >= total_fixed_width

        if auto_columns:
            total_space_left = self.width - total_fixed_width

            assert total_space_left > 0
            
            space_per_column = total_space_left / len(auto_columns)
            wider_columns = total_space_left % len(auto_columns)
            
            for index, col in zip(itertools.count(), auto_columns):
                col.width = space_per_column + (1 if index < wider_columns else 0)

    def header(self):
        s = ''
        for index, col in zip(itertools.count(), self.columns):
            s += col.justified_header(index < len(self.columns)-1)
        return s

    def separator(self, char='='):
        return char*self.width

    def row(self, row):
        s = ''
        for index, col, row in zip(itertools.count(), self.columns, row):
            s += col.justified_data(str(row), index < len(self.columns)-1)
        return s
