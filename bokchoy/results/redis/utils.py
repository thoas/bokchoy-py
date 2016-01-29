from bokchoy.compat import as_text


def decode_hash(h):
    return dict((as_text(k), h[k]) for k in h)
