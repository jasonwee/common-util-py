import threading
import json

global_lock = threading.Lock()

# https://gist.github.com/rahulrajaram/5934d2b786ed2c29dc418fafaa2830ad
def write_to_file(filename, content):
    while global_lock.locked():
        continue

    global_lock.acquire()

    with open(filename, "a+") as file:
        file.write(content)

    global_lock.release()

def writeListDictToFile(filename, rows):
    with open(filename, 'w') as fout:
        json.dump(rows, fout, indent=4, default=str, sort_keys=False)
