__author__ = 'Konrad Kopciuch'

def parse_from_string(fv):
    x = list(fv.split(';'))
    return map(lambda y: float(y), x)

def convert_to_string(list):
    length = len(list)
    s = ''
    for i in range(length):
        s += str(list[i])
        if i < length-1:
            s += ';'
    return s

