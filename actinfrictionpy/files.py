"""Functions for naming calculation outputs."""

def savename(prefix, params, digits=2, suffix=None, ignored_fields=[]):
    sorted_items = sorted(params._asdict().items())
    filename = [prefix]
    for key, value in sorted_items:
        if isinstance(value, float):
            filename.append(f'{key}={value:.{digits}e}')
        elif isinstance(value, list):
            filename.append(f'{key}={value[0]}-{value[-1]}')
        elif value in None or key in ignored_fields:
            pass
        else:
            filename.append(f'{key}={value}')

    filename = '_'.join(filename)
    if suffix is not None:
        filename += f'{suffix}'

    return filename
