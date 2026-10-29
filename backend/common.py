def check_missing_fields_from_json_data(data, fields):
    """Used for POST requests, so missing data doesn't become repetitive"""
    for field in fields:
        if (
            not isinstance(data.get(field.value), str)
            or not str(data[field.value]).strip()
        ):
            return field

    return None
