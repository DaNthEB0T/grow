import magic 
import string

def get_mime_type(file):
    """
    Get MIME by reading the header of the file
    """
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(initial_pos)
    return mime_type

def queryset_diff(qs1, qs2):
    return qs1.exclude(id__in=qs2.values_list("id", flat=True))

def contains_whitespace(s):
    for c in s:
        if c in string.whitespace:
            return True
    return False