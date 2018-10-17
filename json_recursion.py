"""
This is the program to demonstrate how to generate csv
from json data using recursion.
"""

import json
import os
from argparse import ArgumentParser


def handler(data, out, jd, keys):
    """
    iteration
    """

    # find depth of the json object
    if depth(data) > 1:
        for index, key in enumerate(data):
            # remove one key if same level iteration
            if index > 0:
                keys.pop()

            # append key
            keys.append(key)
            handler(data[key], out, jd, keys)

        # next level iteration
        if keys:
            keys.pop()

    # if data is list
    elif type(data) is list:
        line_keys = ','.join("'" + safe_get(keys, i) + "'" for i in range(jd))

        for value in data:
            write_to_file(line_keys, value, out)

    # if data is dict
    elif type(data) is dict:

        for key, value in data.items():
            keys.append(key)
            # row of key values
            row = ','.join("'" + safe_get(keys, i) + "'" for i in range(jd))

            write_to_file(row, value, out)
            keys.pop()

    # id data is string
    elif type(data) is str:
        line_keys = ','.join("'" + safe_get(keys, i) + "'" for i in range(jd))

        write_to_file(line_keys, data, out)


def write_to_file(prefix, value, out):
    """
    Write each line to csv file
    """
    out.write("\n" + prefix + " ,'" + str(value) + "'")


def safe_get(l, idx):
    """
    Getting item from list safely
    """

    try:
        return l[idx]
    except IndexError:
        return ""


def depth(x):
    """
    Find depth of the json
    """

    if type(x) is dict and x:
        return 1 + max(depth(x[a]) for a in x)
    if type(x) is list and x:
        return 1 + max(depth(a) for a in x)
    return 0


def read_conf(file):
    """
    :param file defines conf file path.
    :return conf file object.
    """

    try:
        conf_file = open(file, "r")
        params = json.load(conf_file)
        return params

    except Exception as err:
        print("Error: ", err)


def get_arguments():
    """
    read command line arguments
    :return conf file path
    """

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", help="Provide conf file path")
    conf_file = parser.parse_args().filename

    while conf_file is None:
        file = input("Please provide config file path:")
        if os.path.exists(file) and os.access(file, os.R_OK):
            conf_file = file

    return conf_file


if __name__ == '__main__':

    # Read conf file.
    config_file = get_arguments()
    conf_data = read_conf(config_file)

    # Open input and output files.
    in_file = open(conf_data["file_in"], "r")
    out_file = open(conf_data["file_out"], "w")

    # Write csv headers to output file if have anything in conf file.
    out_file.write(" ".join(conf_data["csv_header"]))

    # Iteration through json data and construct csv.
    input_data = json.load(in_file)["data"]
    print(input_data)

    # json_depth = depth(data)
    # handler(data, out_file, json_depth, keys=[])
