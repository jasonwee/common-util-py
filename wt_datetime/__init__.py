import datetime

def convertUnixTimeToDateTimeUTC(unixTsSec):
    return datetime.datetime.fromtimestamp(unixTsSec, datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')

