import re

class Result(object):
    source = 0
    blank = 0
    comment = 0

def line_is_single_line_comment(line, lang):
    for pattern in lang.comment_filters['to_eol']:
        split = re.split(pattern, line)

        if len(split) > 1 and not split[0].strip():
            return True

    return False

# Returns (int, bool) for (pattern start or None, have source before start)
def line_is_multi_line_comment_start(line, lang):
    for i in range(len(lang.comment_filters['between'])):
        start_pattern, end_pattern = lang.comment_filters['between'][i]

        split = re.split(start_pattern, line)

        if len(split) > 1:
            return (i, bool(split[0].strip()))

    return (None, False)

def line_is_multi_line_comment_end(line, lang):
    for i in range(len(lang.comment_filters['between'])):
        start_pattern, end_pattern = lang.comment_filters['between'][i]

        split = re.split(end_pattern, line)

        if len(split) > 1:
            return (i, bool(split[1].strip()))

    return (None, False)

def count_file(f, lang):
    r = Result()

    # The index of the currently active "between"-style comment.
    in_comment = None
    
    # The previously read line
    last_line = None
    
    for l in f.readlines():
        last_line = l

        if in_comment is None: # We're not in a "between"-style comment.
            in_comment, have_source = line_is_multi_line_comment_start(l, lang)
            end_comment, have_end_source = line_is_multi_line_comment_end(l, lang)

            if in_comment is not None: # There is a comment that
                                       # starts here
                if have_source or have_end_source:
                    # If there is code on this line, count it as code.
                    r.source += 1
                else:
                    r.comment += 1

                # If there is an end comment marker on this line as
                # well, we're not in a comment anymore.
                if end_comment is not None:
                    in_comment = None
                
                continue
        else: # We're currently in a "between"-style comment
            end_comment, have_source = line_is_multi_line_comment_end(l, lang)

            if end_comment == in_comment: # The end comment marker on
                                          # this line is the same as
                                          # the comment we're in.
                in_comment = None
                if have_source:
                    r.source += 1
                else:
                    r.comment += 1

                continue

        if in_comment is not None or line_is_single_line_comment(l, lang):
            r.comment += 1
        elif not l or l.strip():
            r.source += 1
        else:
            r.blank += 1

    # If the last line in the file ends with a newline, count that as a blank line.
    if last_line and last_line[-1] == '\n':
        r.blank += 1

    return r
