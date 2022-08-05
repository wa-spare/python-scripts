import requests,json

outputFile = open('metric_list.txt', 'w')
tenant = 'https://{tenant}.live.dynatrace.com'
key = '{key}'
url = "/api/v2/metrics"
page = 1
npk=''
npk_list =[]
print('Printing all DT Metrics to metrics_list.txt.  Please wait...')

def fetch_npks(npk):
   if npk in npk_list or npk==None: # or equal to "none"
       print('Done!')
       outputFile.close()      
       quit()
   else:    
      npk_list.append(npk)
      if npk:
        req_url = f'{tenant}{url}?format=json&api-token={key}&nextPageKey={npk}'
      else:
        req_url = f'{tenant}{url}?format=json&api-token={key}' 
      response = requests.get(req_url)
      jresponse = response.json()
      metrics = jresponse['metrics']
      for record in metrics:
         metricid = record['metricId']
         outputFile.write(metricid + "\n")
      npk = jresponse['nextPageKey']
   fetch_npks(npk)  
fetch_npks(npk)
