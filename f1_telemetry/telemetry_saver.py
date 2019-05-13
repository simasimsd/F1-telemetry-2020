import csv


def getdict(struct):
    '''
    Translates a ctype.structure into a dictionary.
    To be ohnest, copied from stackoverflow.
    '''
    result = {}
    for field, _ in struct._fields_:
        value = getattr(struct, field)
        # if the type is not a primitive and it evaluates to False ...
        if (type(value) not in [int, float, bool]) and not bool(value):
            # it's a null pointer
            value = None
        elif hasattr(value, "_length_") and hasattr(value, "_type_"):
            # Probably an array
            value = list(value)
        elif hasattr(value, "_fields_"):
            # Probably another struct
            value = getdict(value)
        result[field] = value
    return result


def getlist(struct):
    '''
    Translates a ctype.structure into a list.
    '''
    result = []
    for field, _ in struct._fields_:
        value = getattr(struct, field)
        # if the type is not a primitive and it evaluates to False ...
        if (type(value) not in [int, float, bool]) and not bool(value):
            # it's a null pointer
            value = None
        elif hasattr(value, "_length_") and hasattr(value, "_type_"):
            # Probably an array
            value = list(value)
        elif hasattr(value, "_fields_"):
            # Probably another struct
            value = getdict(value)
        result.append(value)
    return result


def csv_saver(csv_file, data):
    '''
    Takes a list of data and adds it to the csv_file
    '''
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(data)