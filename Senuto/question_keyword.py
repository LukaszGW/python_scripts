import requests
from senuto import token
import pandas as pd
import json

"""
Scirpt get question queries based on keyword. Senuto file is required for authorization
"""

dffrazy = pd.read_excel('sheet_with_keywords')['Keyword']
print(dffrazy)
frazy = dffrazy.tolist()
print(frazy)
def get_data(query, token):
    r = requests.post("https://api.senuto.com/api/keywords_analysis/reports/keywords/getQuestions",
                     json.dumps({"offset":0,"page":1,"limit":50,"parameters":[{"data_fetch_mode":"keyword",
                        "value":[query]}],"country_id":"1","match_mode":"narrow","filtering":[{"filters":[]}]})
                      , headers={"Authorization": "Bearer "+token}).content
    return r


results_all = []
for query in frazy:
    print(query)
    dfall = pd.DataFrame()
    try:
        r = get_data(query, token)
        print(r)
        r = json.loads(r)
    except Exception as e:
        print(e)
        writer = pd.ExcelWriter('results_questions-part.xlsx')
        pd.DataFrame.from_dict(results_all).to_excel(writer)
        writer.save()
    if r['success'] == True:
        try:
            results = [{'parent_keyword': query, 'fraza': r['data'][row]['keyword'], 'SV': r['data'][row]['searches']} for row in range(len(r['data']))]
            results_all = results_all + results
        except IndexError:
            print("błąd w indeksie  ", r)

writer = pd.ExcelWriter('results_questsions.xlsx')
pd.DataFrame.from_dict(results_all).to_excel(writer)
writer.save()