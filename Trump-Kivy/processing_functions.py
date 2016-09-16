# FUNCTIONS THAT PROCESS CSV AND LISTS

import random
import csv

def is_int_str(v):
    """
    sort of complex expression to check for numeric values that come from csv as strings
    see http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
    """
    v = str(v).strip()
    return v == '0' or (v if v.find('..') > -1 else v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()


def get_row(csvfile, record_id):
    """Retrieves a row with a specific ID
    input: csv file, record_id of a line;
    output: dictionary with headers as keys and row values as values
    id must be unique and labeled as 'id' - or else!"""
    with open(csvfile, 'rb') as csvfile:
        newfile = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        newrow = {}  # empty dictionary
        for row in newfile:
            if row['id'] == str(record_id):
                # id is numeric but at this point as it comes out of CSV, it is still a string!
                # row['id'] -> 'id' must be present in CSV or else!
                # no error prevention is in place now !!
                # mb add later addl id_format='id' later
                for lbl in row:
                    a = row[lbl]
                    if is_int_str(a):  # convert numeric STR to INT
                        a = int(a)
                        newrow.update({lbl: a})
                    else:  # do not convert STR to STR
                        newrow.update({lbl: a})
            else:
                pass
        return newrow


def csv_lookup(csvfile, row_id, column_id):
    """Function's intent: get a single cell defined by value in first column of the row and column header
    row id may be INT, column_id must be STR
    NOTE: row_id is 1,2...n - if value must be identified by id, used id instead"""
    with open(csvfile, 'rb') as csvfile:
        newfile = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        # iterate through newfile until Nth line is found
        # see ex. http://stackoverflow.com/questions/4876264/getting-specific-line-and-value-with-python-dictreader
        if any(line_num == row_id - 1 for line_num, line in enumerate(newfile)):
            # True == row_id valid
            for line_num, line in enumerate(newfile):
                if line_num == row_id - 1: # header row becomes a key, so CSV row 1 == DictReader row 0
                    if str(column_id) in line.keys():
                        # True == column_id valid
                        if is_int_str(line[column_id]):
                            # convert numbers from STR to INT
                            return int(line[column_id])
                        else:
                            # keep alphanum as STR
                            return line[column_id]
                    else:
                        # False == column_id invalid
                        print 'PF.csv_lookup says: No such column {}'.format(column_id)
        else:
            # False == row_id invalid
            print 'PF.csv_lookup says: row_id {} NOT found'.format(row_id)


def sort_flatten_list(list1, list2):
    """Flattens and sorts list of cards before generation
    https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions"""
    return sorted([num for elem in [list1, list2] for num in elem])
