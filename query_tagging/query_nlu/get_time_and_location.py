import requests, sys

def get_nlu_tags(sysargs):
    url = "http://generic-resolver-prod-flight.trafficmanager.net/api/resolver/genericlu"
    query = sysargs[0]
    timexdomain= "timex"
    locationdomain = "location"
    nlu_tags = {}

    data = {'query': query, 'domains': timexdomain}
    nlu_tags['timex'] = requests.get(url, data).text

    data['domains'] = locationdomain
    nlu_tags['location'] = requests.get(url, data).text

    return nlu_tags


# Main method.
if __name__ == '__main__':
    get_nlu_tags(sys.argv[1:])

