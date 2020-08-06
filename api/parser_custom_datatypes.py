# The term 'datatypes' is used loosely here. Simply implies that these functions may be passed
# into the 'type' parameter of reqparse.RequestParser.add_argument

# dealing with custom datatypes: https://github.com/noirbizarre/flask-restplus/issues/124


def splitter(name, allowed_set):

    def list_splitter(values):

        split_vals = values.split(',')

        # validate
        for val in split_vals:
            if val not in allowed_set:
                raise ValueError(f". Invalid option '{val}' given for '{name}' parameter. Valid options are {allowed_set} ")

        return split_vals

    # for the swagger page to get data_type
    list_splitter.__schema__ = {"type": "list_string"}

    return list_splitter


def dollar_value(value):
    try:
        value = float(value)
        assert value >= 0
    except (AssertionError, ValueError):
        raise ValueError(f"Dollar value must be a number > 0. Given value is '{value}'")

    return value


dollar_value.__schema__ = {"type": "dollar_value"}


def percentage_value(value):

    try:
        value = float(value)
        assert 0 <= value <= 1
    except (AssertionError, ValueError):
        raise ValueError(f"Dollar value must be a number > 0. Given value is '{value}'")

    return value


percentage_value.__schema__ = {"type": "percentage_value"}
