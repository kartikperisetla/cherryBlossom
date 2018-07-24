import requests

url = "http://generic-resolver-prod-flight.trafficmanager.net/api/resolver/genericlu"
query = "setup a meeting tomorrow 3 pm at bellevue"
timexdomain= "timex"
locationdomain = "location"

data = {'query': query, 'domains': [timexdomain, locationdomain]}
print(requests.get(url, data).text)

#data['domains'] = locationdomain
#print(requests.get(url, data).text)

