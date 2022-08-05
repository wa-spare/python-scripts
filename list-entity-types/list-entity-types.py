import requests,json

debug_flg = 'N'

tenant = 'https://{tenant}.live.dynatrace.com'
key = '{key}'

url = '/api/v2/entityTypes'
dict_key = 'types'
sub_dict_key = 'type'

outputFile = open('entity_type_list.txt', 'w')
npk=''
npk_list =[]
print(f'Printing all {url} vals to entity_type_list.txt.  Please wait...')

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
      if debug_flg =='Y':
        print(npk_list)        
        print(req_url)
      response = requests.get(req_url)
      jresponse = response.json()
      if not npk:
          row_count = jresponse['totalCount']
          outputFile.write('Total Expected Rows:' + str(row_count) + "\n")
      json_data = jresponse[dict_key]
      for record in json_data:
         row_value = record[sub_dict_key]
         #print(row_value)
         outputFile.write(row_value + "\n")
       
      try:
         npk = jresponse['nextPageKey']
         #page += 1 
      except:
         print('Done!') 
         quit()
   fetch_npks(npk)  
fetch_npks(npk)
