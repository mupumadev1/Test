import json

def format_request_data(request_data):
    """ Format request data to a list """

    # Convert the string to a list using json.loads()
    result_list = json.loads(request_data)

    # Use list comprehension to remove commas and quotes
    new_list = [item.strip('",') for item in result_list]

    return new_list