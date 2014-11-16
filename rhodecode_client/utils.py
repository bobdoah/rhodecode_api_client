import urlparse
import urllib2

def normalised_url(url):
    parsed_url = urlparse.urlparse(url)
    normalised_path = urllib2.quote("{}{}".format(parsed_url.hostname, parsed_url.path)).replace('//', '/')
    return "{}://{}".format(parsed_url.scheme, normalised_path)

