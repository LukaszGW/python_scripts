import requests
import json
import pandas as pd
import time

'''
Script check if domain have quer in top50 search results and get information about this query
'''

df = pd.read_excel('C:\\Users\\lukasz.girzycki\\Desktop\\frazy.xlsx')
results_final = []
for query in df['Frazy']:
    print(query)
    url = 'http://api.semstorm.com/api-v3/explorer/explorer-keywords/get-data'
    data = '''{
    "domains": ["Your_Domain"],
    "filters": [{"field": "keyword", "operand": "contains", "value" :"'''+str(query)+'''"}],
    "services_token": "Your_Token"
    }'''
    header = {"Content-type": "application/json"}
    try:
        results = requests.post(url, data=data.encode('utf-8'), headers=header).content
        results = json.loads(results)
    except Exception as e:
        print(e)
        print('za często')
        df_semstorm = pd.DataFrame(results_final)
        writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Dropbox\\Narzędzia seo\\dane_semstorm-mask-part.xlsx')
        df_semstorm.to_excel(writer)
        writer.save()
        time.sleep(300)
        results = requests.post(url, data=data.encode('utf-8'), headers=header).content
        results = json.loads(results)
    print(results)
    try:
        if results['results']:
            print('jest fraza')
            results = results['results']
            results_all = [{'url_z_semstorm': key['url']['domain'],
                            'query': key['keyword'],
                            'pos': key['position']['domain'],
                            'pos_c': key['position_c']['domain'],
                            'traffic': key['traffic']['domain'],
                            'traffic_c': key['traffic_c']['domain'],
                            'Search Volume': key['volume'],
                            'competition_phrase': key['competitors'],
                            'styczeń SV': key['trends'].split(',')[0],
                            'luty SV': key['trends'].split(',')[1],
                            'marzec SV': key['trends'].split(',')[2],
                            'kwiecień SV': key['trends'].split(',')[3],
                            'maj SV': key['trends'].split(',')[4],
                            'czerwiec SV': key['trends'].split(',')[5],
                            'lipiec SV': key['trends'].split(',')[6],
                            'sierpień SV': key['trends'].split(',')[7],
                            'wrzesień SV': key['trends'].split(',')[8],
                            'październik SV': key['trends'].split(',')[9],
                            'listopad SV': key['trends'].split(',')[10],
                            'grudzień SV': key['trends'].split(',')[11],
                            } for key in results]
            print(results_all)
        else:
            print('Nie udało się znaleźć frazy ', query)
            continue
        results_final = results_final + results_all
    except Exception as e:
        print(query)
        print('Nieokreślony błąd ', e)
        df_semstorm = pd.DataFrame(results_final)
        writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Dropbox\\Narzędzia seo\\dane_semstorm-mask-hmbk-part.xlsx')
        df_semstorm.to_excel(writer)
        writer.save()

df_semstorm = pd.DataFrame(results_final)
writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Dropbox\\Narzędzia seo\\dane_semstorm-hmbk.xlsx')
df_semstorm.to_excel(writer)
writer.save()