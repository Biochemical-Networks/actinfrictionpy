"""Functions for naming calculation outputs."""


def savename(prefix, params, digits=2, suffix=None, ignored_fields=[]):
    sorted_items = sorted(params._asdict().items())
    filename = [prefix]
    for key, value in sorted_items:
        if key in ignored_fields:
            pass
        elif value is None:
            pass
        elif isinstance(value, list):
            filename.append(f"{key}={value[0]}-{value[-1]}")
        elif int(value) == value:
            filename.append(f"{key}={int(value)}")
        elif isinstance(value, float):
            filename.append(f"{key}={value:.{digits}e}")
        else:
            filename.append(f"{key}={value}")

    filename = "_".join(filename)
    if suffix is not None:
        filename += f"{suffix}"

    return filename
