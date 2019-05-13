import csv


def getdict(struct):
    '''
    Translates a ctype.structure into a dictionary.
    To be ohnest, copied from stackoverflow, but it has some changes.
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
        elif type(value) in (list, tuple):
            # A list or a tuple of other structures
            value_ = []
            for elem in value:
                value_.extend(getdict(elem))
            value = value_
        result[field] = value
    return result


# Another version from stackoverflow
def getlist(struct):
    result = []
    #print struct
    def get_value(value):
         if (type(value) not in [int, long, float, bool]) and not bool(value):
             # it's a null pointer
             value = None
         elif hasattr(value, "_length_") and hasattr(value, "_type_"):
             # Probably an array
             #print value
             value = get_array(value)
         elif hasattr(value, "_fields_"):
             # Probably another struct
             value = getlist(value)
         return value
    def get_array(array):
        ar = []
        for value in array:
            value = get_value(value)
            ar.append(value)
        return ar
    for f  in struct._fields_:
         field = f[0]
         value = getattr(struct, field)
         # if the type is not a primitive and it evaluates to False ...
         value = get_value(value)
         result.append(value)
    return result


def csv_saver(csv_file, data):
    '''
    Takes a list of data and adds it to the csv_file
    '''
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(data)