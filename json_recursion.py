"""
recursive travelling to json data
"""
import json


def handler(data, out, jd, keys):
    """
    iteration
    """

    # ---------- find depth of the json object
    if depth(data) > 1:
        for index, key in enumerate(data):
            # -----------remove one key if same level iteration
            if index > 0:
                keys.pop()
            # ----------append key
            keys.append(key)
            handler(data[key], out, jd, keys)

        # -----next level iteration
        if keys:
            keys.pop()

    # ----------- if data is list
    elif type(data) is list:
        line_keys = ','.join("'" + safe_get(keys, i) + "'" for i in range(jd))

        for value in data:
            write_to_file(line_keys, value, out)

    # ----------- if data is dict
    elif type(data) is dict:

        for key, value in data.items():
            keys.append(key)
            # ----------row of key values
            row = ','.join("'" + safe_get(keys, i) + "'" for i in range(jd))

            write_to_file(row, value, out)
            keys.pop()

    # ---------- id data is string
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


def main():
    """
    step for generating csv file
    """

    try:
        # --------conf file
        conf_file = open("conf.json", "r")
        conf_data = json.load(conf_file)

        # -------input and output file
        input_file = open(conf_data["input_file"], "r")
        out_file = open(conf_data["output_file"], "w")

        # --------csv headers
        out_file.write(" ".join(conf_data["csv_header"]))

        # --------iteration through json
        data = json.load(input_file)["data"]
        json_depth = depth(data)
        handler(data, out_file, json_depth, keys=[])

    except Exception as err:
        print("Error : ", err)


if __name__ == '__main__':
    main()
