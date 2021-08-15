import json

def update(json_file, key, value):
    """
    update the json file based on the key and value specified

    :param json_file: the json file where the key and value should be written to
    :param key: the key to write into the json_file
    :param value: the value that belong to the key to write into the json_file
    :returns: None

    """
    with open(json_file, 'r') as f:
        data = json.load(f)

    with open(json_file, 'w') as f:
        data[key] = value
        json.dump(data, f, indent=3, sort_keys=True)
        f.write("\n")

def get_all(json_file):
    with open(json_file, 'r') as f:
        data = json.dumps(json.load(f), indent=4)
    return data

def get_value(json_file, key):
    """
    return the value associated with the key in the specified json file

    :param json_file: the json file where the key and value present
    :param key: the key where the value is associated with
    :returns: 0 if there is not key found in the json_file. else return the 
              value associated with the key

    """
    count = 0
    with open(json_file, 'r') as f:
        data = json.load(f)

        if key not in data:
            return count
        count = data[key]
    return count

def create_json_file(json_file, template):
    """
    create json file based on the template

    :param json_file: the json file about to be create
    :param template: the template use to create json_file. 
    :returns: None

    """
    with open(template, 'r') as f:
        data = json.load(f)

        with open(json_file, 'w') as sf:
            json.dump(data, sf, indent=3, sort_keys=True)
            sf.write("\n")

