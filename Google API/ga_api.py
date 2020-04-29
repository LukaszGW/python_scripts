from google_analytics import ga_request, analytics_service
from datetime import date, timedelta
import pandas as pd
import re
import time

'''
Script request Google Analytics API based on url list and credentials from google_analytics file.

Below example for metric filter
{
  "metricName": "ga:pageviews",
  "operator": "GREATER_THAN",
  "comparisonValue": "2"
}

Below example for dimension filter
{
"dimensionName": "ga:browser",
              "operator": "EXACT",
              "expressions": ["Chrome"]
}

Filter documentation
https://developers.google.com/analytics/devguides/reporting/core/v3/reference#filters
'''


url_list = pd.read_excel('C:\\Users\\lukasz.girzycki\\Desktop\\niejednolita nawigacja\\response_codes_all.xlsx', sheet_name='200')['Address'].tolist()
filter_metric = [{}]

analytics = analytics_service()

serwis = 'View_Name' #Usually our site name
end_date = date.today()
start_date = end_date - timedelta(days=30)
metrics = ['Users', 'entrances', 'pageValue']
dimension = ['pagePath', 'source']

body = ga_request(metrics, dimension, serwis, start_date=str(start_date), end_date=str(end_date))
print(body)
results_all = []
for url in url_list:
    print()
    url = re.search('URL_Pattern_in_regex', url).group(1)
    print(url)
    filter_dimension = [{ "filters":
            [{
            "dimensionName": "ga:pagePath",
            "operator": "EXACT",
            "not": False,
            "expressions": [url]
    }]}]
    if filter_metric[0]:
      body['reportRequests'][0]['metricFilterClauses'] = filter_metric
    elif filter_dimension[0]:
      body['reportRequests'][0]['dimensionFilterClauses'] = filter_dimension
    print(body)
    try:
        response = analytics.reports().batchGet(body=body).execute()
        print(response)
        if 'rows' in response['reports'][0]['data']:
            results_all = results_all+response['reports'][0]['data']['rows']
            print(results_all)
        else:
            print('nie znaleziono ruchu')
    except Exception as e:
        print(e)
        writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Desktop\\baza slp\\seotagi_allyear-part.xlsx')
        pd.DataFrame(results_all).to_excel(writer)
        writer.save()
        time.sleep(300)
        response = analytics.reports().batchGet(body=body).execute()

df = pd.DataFrame(index=[str(response['reports'][0]['data']['rows'][row]['dimensions'][0]) for row in range(len(response['reports'][0]['data']['rows']))],
                  columns=metrics+['źródło'],
                  data=[response['reports'][0]['data']['rows'][row]['metrics'][0]['values']+[response['reports'][0]['data']['rows'][row]['dimensions'][1]] for row in range(len(response['reports'][0]['data']['rows']))])

writer = pd.ExcelWriter('test_ga.xlsx')
df.to_excel(writer)
writer.save()