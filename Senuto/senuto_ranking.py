import requests
from senuto import token
import pandas as pd
import json
import datetime
from sheets import sheet_service

"""
Script get data about visibility, top10 keywords and ranking changes based on thematic category. Senuto file is required for authorization
"""
#Categories in dict consists of category name as key and category id as value
#Example {"Fashion":"290"}
categories = {}
sheet = sheet_service()
def ranking_data(category_name):
    r = requests.post("https://api.senuto.com/api/visibility_analysis/tools/domains_ranking/getRankingData",
                      data={"offset":0,"page":1,"limit":50,"match_mode":"main_domain", "categories_ranking": categories[category_name]}
                      , headers={"Authorization": "Bearer "+token}).content
    print(r)
    results = json.loads(r)['data']
    print(pd.DataFrame(results))
    last_monday = str(datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday()))
    results=[{'domena': results[row]['domain'],
      'kategoria': results[row]['category'],
      'udział': results[row]['share'],
      'miejsce w rankingu': results[row]['statistics']['rank']['recent_value'],
      'starsze miejsce w rankingu': results[row]['statistics']['rank']['recent_value'],
      'zmiana w rankingu': results[row]['statistics']['rank']['diff'],
      'widocznosc': results[row]['statistics']['visibility']['recent_value'],
      'starsza widocznosc': results[row]['statistics']['visibility']['older_value'],
      'zmiana % widocznosci': results[row]['statistics']['visibility']['percent'],
      'liczba fraz w top10': results[row]['statistics']['top10']['recent_value'],
      'starsza liczba fraz w top10': results[row]['statistics']['top10']['older_value'],
      'zmiana % liczby fraz w top10': results[row]['statistics']['top10']['percent'],
      'time' : last_monday}
             for row in range(len(results))]
    return results

if __name__ == '__main__':
    SPREADSHEET_ID = 'SPREADSHEET_ID'
    for category_name in categories:
        df_old = pd.read_excel('Link_to_spreadsheet_with_previous_data',
                               sheet_name=category_name, dtype={'time': str})
        results = ranking_data(category_name)

        df = pd.concat([df_old, pd.DataFrame(results)])
        body = {
            "range": category_name+'!A:M',
            "majorDimension": "ROWS",
            "values": [df.columns.tolist()]+df.fillna(0).to_numpy().tolist(),
        }
        result = sheet.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=category_name+'!A:M',
            valueInputOption='USER_ENTERED', body=body).execute()
else:
    print(__name__)