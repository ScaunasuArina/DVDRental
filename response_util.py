def format_response(columns, values):
    '''
    This function takes the columns list and the response from the database and return them as a dict
    :param columns: List of columns retrieved from database
    :param values: Tuple of values for retrieved columns
    :return: Dict of pairs column:value
    '''

    response_dict = dict()
    values = list(values)
    for i in range(len(columns)):
        if isinstance(values[i], str):
            values[i] = values[i].strip()
        response_dict[columns[i]] = values[i]

    return response_dict