#  List Dynatrace Problems for a defined timeframe to csv file
#  Developed by Wallace Abbott Aug 9, 2022

import requests, json, time
tenant = 'https://{tenant}.live.dynatrace.com'
key = '{key}'

timenow = time.ctime()
outputFile = open('problem-list.csv', 'w')  #use 'a' for append

timefrom = input('Problem List Report Begin FROM [INPUT: -1M, -1w, -1d, -1h]: ')
timeto = input('Problem List Report End Thru/TO [INPUT: now, -1w, -1d, -1h]: ')
uri = '/api/v2/problems'
timeframe=f'from={timeto}{timefrom}'
print(f'Timeframe Selected= {timefrom} thru {timeto}.  Generating report to problem-list.csv')
#timeframe = 'from=now-5M'
base_rqst_url = f'{tenant}{uri}?{timeframe}&format=json&api-token={key}' 

def write_report(problem_data):
            for record in problem_data:      
                problem_displayid = record['displayId']           
                #problem_id = record['problemId']
                problem_title = record['title']
                problem_status = record['status']
                problem_start = record['startTime']
                problem_end = record['endTime']
                problem_rc = record['rootCauseEntity']
                outputFile.write(f'{problem_displayid},{problem_status},{problem_title},{problem_start},{problem_end},{problem_rc}' + "\n")

def api_rqst(req_url):
    #print(req_url)
    response = requests.get(req_url)
    jresponse = response.json()
    totalcount = jresponse['totalCount']
    pagesize = jresponse['pageSize']
    try:
        npk = jresponse['nextPageKey']
    except:
        npk = None   
    problem_data = jresponse['problems']
    return(totalcount, pagesize, npk, problem_data)

def main_loop():
    npk = None
    req_url = f'{base_rqst_url}' 
    row_count, pagesize, npk, problem_data = api_rqst(req_url)

    if row_count > 0:
      outputFile.write(f'{row_count} New Problem(s) Found. Report generated at {timenow}' + '\n')
      outputFile.write('problem_displayid,problem_status,problem_title,problem_start,problem_end,problem_rc' + '\n')
      print(f'{row_count} New Problem(s) Found. Writing report. Please wait...') 
      write_report(problem_data)

      if(npk is not None):
        #print(f'npk exists: {npk}' + '\n')
        write_count = pagesize
        while write_count < row_count:
            req_url = f'{tenant}{uri}?nextPageKey={npk}&api-token={key}' 
            #print(req_url)
            nn1, nn2, npk, problem_data = api_rqst(req_url)
            write_report(problem_data)
            write_count = write_count + pagesize
        else:
            outputFile.close()
            print('Done!')
    else:
        outputFile.write(f' No Problems Found. Report generated at {timenow}' + "\n")
        outputFile.close()
        print(f'No Problems Found.')
main_loop()
