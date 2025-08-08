from time import gmtime, strftime

def log(message):
    print("%s %s" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()),message))
