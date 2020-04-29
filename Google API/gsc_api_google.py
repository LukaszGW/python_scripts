from gsca_api_analyze import build_request, webmasters_service
import pandas as pd
from datetime import timedelta, datetime, date
import time

"""
Script request for data from Google Search Console based on url list and write it to Excel file.
Script requires credentials file load b gsca_api_anlyze.
"""

urle = pd.read_excel('C:\\Users\\lukasz.girzycki\\Desktop\\seo_tagi-slp2.xlsx', sheet_name="200")['url']
print(urle)

end_date = '2020-02-17'
start_date = '2019-02-18'
print(start_date)
print(end_date)
property_uri = 'Website_Property'
dimensions = ['page']
resultsall = []

for url in urle:
    print(url)
    filters = [
        {
          "dimension": 'page',
          "operator": 'equals',
          "expression": url
        }
      ]
    request_api = build_request(filters, str(start_date), str(end_date), dimensions, row=0, row_limit=25000, aggregationType="byPage")
    print(request_api)
    try:
        response = webmasters_service.searchanalytics().query(siteUrl=property_uri, body=request_api).execute()
        print(response)
    except Exception as e:
        print(e)
        writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Desktop\\baza slp\\seotagi_allyear-part.xlsx')
        pd.DataFrame(resultsall).to_excel(writer)
        writer.save()
        time.sleep(300)
        response = webmasters_service.searchanalytics().query(siteUrl=property_uri, body=request_api).execute()

    if 'rows' in response:
        results = [{'url': key['keys'][0], 'clicks': key['clicks'], 'impressions': key['impressions'],
          'ctr': key['ctr'], 'position': key['position']} for key in response['rows']]
        resultsall = resultsall+results
    print(resultsall)

dfeffect = pd.DataFrame(resultsall)
writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Desktop\\baza slp\\seotagi_allyear.xlsx')
dfeffect.to_excel(writer)
writer.save()