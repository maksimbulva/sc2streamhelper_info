def to_int(value):
    try:
        return int(value)
    except TypeError:
        pass
    except ValueError:
        pass
    return None
