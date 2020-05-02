import json


# Use the below methods to read and write data to files in your APIs.

def read_file(path):
    """
        This method will return the data saved in your file as a Python Object
        Args:
            path: path to the file from which you wish to read the data.
                Example - './data/users'
        Return:
            data - the json data saved in the file as a python object.
                Example - In our case, it will return a list of dictionary objects corresponding to either User or Move
    """
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def write_to_file(path, data):
    """
        This method will save the passed data in the specified file

        path: path to the file in which you wish to write the data.
                Example - './data/users'
        data: a python object you wish to write in the file.
                Example - In your case, it should be a list of dictionary objects corresponding to either User or Move.
    """
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
