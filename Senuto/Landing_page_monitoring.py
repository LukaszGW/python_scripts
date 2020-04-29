import requests
from senuto import token
import pandas as pd
import json
import time

"""
Script chceck position based on Senuto data and report
"""

#Load seo tags from csv file
frazy = pd.read_csv('allSeotags.txt', header=0)['Name']
print(frazy)

#Empty list for final results
results_all = []

#Function processing data from json
def data_senuto(r):
    print(r.content)
    results = json.loads(r.content)
    if bool(results['data']) == True:
        print('działa')
        results = [{'fraza': results['data'][keyword]['keyword'], 'searches': results['data'][keyword]['searches'],
                'pozycja': results['data'][keyword]['position'],
               "url": results['data'][keyword]['url'], "pozycja_ostatni_poniedziałek": results['data'][keyword]['position_last_monday'],
                "url_ostatni_poniedziałek": results['data'][keyword]["url_last_monday"],
                'pozycja poniedziałek tydzień temu': results['data'][keyword]['position_week_ago_monday'],
                'trend_1': results['data'][keyword]['trend_1'],
                'trend_2': results['data'][keyword]['trend_2'],
                'trend_3': results['data'][keyword]['trend_3'],
                'trend_4': results['data'][keyword]['trend_4'],
                'trend_5': results['data'][keyword]['trend_5'],
                'trend_6': results['data'][keyword]['trend_6'],
                'trend_7': results['data'][keyword]['trend_7'],
                'trend_8': results['data'][keyword]['trend_8'],
                'trend_9': results['data'][keyword]['trend_9'],
                'trend_10': results['data'][keyword]['trend_10'],
                'trend_11': results['data'][keyword]['trend_11'],
                'trend_12': results['data'][keyword]['trend_12']
                }
                for keyword in range(len(results['data'])) if results['data'][keyword]['keyword'] == query]

    elif bool(results['data']) == False and 'data' in results:
        print('brak frazy')
        results = [{'fraza': query, 'pozycja': 'brak'}]
    else:
        print('błąd')
        print(results)
    return results

#Iterate through every query
for query in frazy[4196:frazy.last_valid_index()]:
    print(query)
    time.sleep(2)
    try:
        #Request to Senuto API documentation may be wrong
        #https://docs.senuto.com/#api-VisibilityAnalysis2.0-Pobieras%C5%82owa,_na_kt%C3%B3re_widoczna_jest_dana_domena
        #It is worth to look to network app.senuto.com to look how api requests
        r = requests.post("https://api.senuto.com/api/visibility_analysis/reports/domain_keywords/getImportantKeywords",
                          data = json.dumps({
                                "domain": "Your_domain_name",
                                "fetch_mode": "topLevelDomain",
                                "filtering": [
                                    {
                                        "filters":[
                                            {
                                                "key": "keywords",
                                                "items": [
                                                    {
                                                        "value": query,
                                                        "match": "exact"
                                                    }
                                                ]

                                                }
                                             ]
                                            }
                                        ],
                                "limit": 10
                            })
        , headers={"Authorization": "Bearer "+token})
        print(r.status_code)
    except Exception as e:
        print(e)
    if r.status_code == 200:
        results = data_senuto(r)
    elif r.status_code == 502:
        #Emergency write data to file in case of connection trouble
        writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Desktop\\monitoring\\LP_monitoring-part1.xlsx')
        print(results_all)
        pd.DataFrame.from_dict(results_all).to_excel(writer)
        writer.save()
        #After 502 wait 10 minutes and request with the same query
        while r.status_code == 502:
            print(r.status_code)
            time.sleep(600)
            r = requests.post(
                "https://api.senuto.com/api/visibility_analysis/reports/domain_keywords/getImportantKeywords",
                data=json.dumps({
                    "domain": "domodi.pl",
                    "fetch_mode": "topLevelDomain",
                    "filtering": [
                        {
                            "filters": [
                                {
                                    "key": "keywords",
                                    "items": [
                                        {
                                            "value": query,
                                            "match": "exact"
                                        }
                                    ]

                                }
                            ]
                        }
                    ],
                    "limit": 10
                })
                , headers={"Authorization": "Bearer " + token})
            results = data_senuto(r)
    results_all = results_all+results
    print(results_all)

#Writing final data to file
print(results_all)
writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Desktop\\monitoring\\LP_monitoring1.xlsx')
pd.DataFrame.from_dict(results_all).to_excel(writer)
writer.save()