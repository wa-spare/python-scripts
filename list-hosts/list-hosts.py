#Creates a CSV dump file of hosts, management zones, and HUs consumed
import requests,json

tenant = 'https://{tenant}.live.dynatrace.com'
key = '{key}'

url = "/api/v1/entity/infrastructure/hosts?includeDetails=false"
outputFile = open('host_list.csv', 'w')
outputFile.write('hostname; managementzone; hostunits' + "\n")
page = 1
npk=''
npk_list =[]
print('Printing all Hosts to host_list.csv.  Please wait...')

req_url = f'{tenant}{url}?format=json&api-token={key}' 
print(req_url)
response = requests.get(req_url)
jresponse = response.json()

#print(jresponse1)
for record in jresponse:
    try: 
        host1 = record['displayName']
        host2 = record['discoveredName']
        hus = record['consumedHostUnits']
        mzs = record['managementZones'][0]['name']
    except:
        host1 = record['displayName']
        host2 = record['discoveredName']
        hus = record['consumedHostUnits']
        mzs = 'No MZ assigned'
    outputFile.write(f'{host2};{mzs};{hus}' + "\n")
