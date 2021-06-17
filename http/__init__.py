import urllib.parse as urlparse
from urllib.parse import parse_qs


def get_param_from_url(url, param):
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed.query)[param]

def get_param_from_query_string(query_string, param):
    return parse_qs(query_string)[param]
