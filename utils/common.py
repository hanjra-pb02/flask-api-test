def validate_response(expected, actual, ignore_keys=None):
    if ignore_keys is None:
        ignore_keys = []

    def _strip_keys(d):
        if isinstance(d, dict):
            return {k: _strip_keys(v) for k, v in d.items() if k not in ignore_keys}
        elif isinstance(d, list):
            return [_strip_keys(i) for i in d]
        else:
            return d

    return _strip_keys(expected) == _strip_keys(actual)