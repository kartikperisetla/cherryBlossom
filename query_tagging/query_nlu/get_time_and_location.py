import requests, sys, json
from collections import defaultdict

def get_nlu_tags(sysargs):
    url = "http://generic-resolver-prod-flight.trafficmanager.net/api/resolver/genericlu"
    query = sysargs[0]
    timexdomain= "timex"
    locationdomain = "location"
    nlu_tags = defaultdict(list)

    data = {'query': query, 'domains': timexdomain}
    timex = json.loads(requests.get(url, data).text)
    
    if timex is not None:
        timex = timex.get('Domains',[{}])[0].get('Item',{}).get('Slots',{})
        if timex is not None:
            timex = timex.get('Item',[])

            for tag in timex:
                
                resolved_values =  [ [ entity['Value'] for entity in propertygroup['Properties'] 
                                                                if entity['Name'] == 'value'][0] for propertygroup 
                                                                in tag['ResolutionInfo']['PropertyGroups'] ]
                nlu_tags[tag['Name']].append({'OriginalText': tag['Text'], 'CanonicalValue': tag['ResolutionInfo']['CanonicalValue'],
                                            'ResolvedValues': resolved_values})

    data['domains'] = locationdomain
    location = json.loads(requests.get(url, data).text)
    
    if location is not None:
        location = location.get('Domains',[{}])[0].get('Item',{}).get('Slots',{})
        if location is not None:
            location = location.get('Item',[])

            for tag in location:
                nlu_tags[tag['Name']].append({'Place': tag['Text'], 'ResolutionInfo': tag['ResolutionInfo']})
        

    return nlu_tags


# Main method.
if __name__ == '__main__':
    print(get_nlu_tags(sys.argv[1:]))

