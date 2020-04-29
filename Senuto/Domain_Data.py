import pandas as pd
import requests
from senuto import token
import json
import re

"""
Script loads basic data about domain from Senuto API. Authorization required senuto file.
"""

file = 'C:\\Users\\lukasz.girzycki\\Desktop\\Linkbuilding\\Baza stron linkujących do stron konkurencji.xlsx'
zakładki = pd.ExcelFile(file).sheet_names
writerdomen = pd.ExcelWriter('linkbuilding_domeny.xlsx')

def dane_domen(link):
    print(link)
    dfdomena = pd.read_excel('C:\\Users\\lukasz.girzycki\\Desktop\\Linkbuilding\\dane_domeny.xlsx')
    if bool(re.search("//www\.", link)):
        print(link, 'z www')
        domena = re.search('www\.(.*\.\w+)', link).group(1)
        print(domena)
    elif bool(re.search("//", link)):
        print(link, 'bez wwww z http')
        print(re.search('//(.*\.\w+)', link).group(0))
        domena = re.search('//(.*\.\w+)', link).group(1)
        print(domena)
    else:
        print(link, ' bez www bez http')
        print(re.search('.*\.\w+', link).group(0))
        domena = re.search('.*\.\w+', link).group(0)
        print(domena)
    r = json.loads(requests.get('https://api.senuto.com/api/visibility_analysis/reports/dashboard/getDomainData',
                     {"domain": domena, "fetch_mode": "subdomain"}, headers={"Authorization": "Bearer "+token}).content)
    print(r)

    r_widoczności = requests.get('https://api.senuto.com/api/visibility_analysis/reports/dashboard/getDomainStatistics', {"domain":domena, "fetch_mode":"topLevelDomain"}, headers={"Authorization": "Bearer "+token}).content
    print(r_widoczności)
    if json.loads(r_widoczności)['data']['statistics']:
        widoczność = json.loads(r_widoczności)['data']['statistics']['visibility']['recent_value']
    else:
        print('brak statystyk')
        widoczność = 'brak statystyk'
    print(widoczność)
    dane = {kategoria: r['data']['categories'][kategoria]['statistics']['visibility']['recent_value'] for kategoria in range(len(r['data']['categories']))}
    df = pd.DataFrame.from_dict(dane, columns=['obecna wartość visibility'], orient='index')
    df['domena'] = domena
    df['widoczność'] = widoczność
    print(df)
    dfall = pd.concat([dfdomena, df.reset_index()])
    print(dfall)
    writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Desktop\\Linkbuilding\\dane_domeny.xlsx')
    dfall.to_excel(writer, index=False)
    writer.save()

for zakładka in zakładki:
    try:
        print(zakładka)
        writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Desktop\\Linkbuilding\\dane_domeny.xlsx')
        pd.DataFrame().to_excel(writer)
        writer.save()
        dfdomena = pd.read_excel(file, sheet_name=zakładka)
        links = dfdomena['Link'].dropna().tolist()
        list(map(lambda link: dane_domen(link), links))
        df = pd.read_excel('C:\\Users\\lukasz.girzycki\\Desktop\\Linkbuilding\\dane_domeny.xlsx')
        df.to_excel(writerdomen, sheet_name=zakładka, index=False)
    except Exception as e:
        print(e, ' błąd!!!')
        writerdomen.save()

writerdomen.save()