import pandas as pd
import requests
import json

"""
Script collect and process data from page speed insight and write it to file. Script checks mobile and desktop version of site.
"""

#List of competition
serwisy = [""]

#Dictionary of competition Main Page. Dict consist of url and competition name
#Example: {"https://allegro.pl":"allegro.pl"}
SG = {""}

#Dictionary of competition Article Page. Dict consist of url and competition name
Artykuły = {''}

#Dictionary of competition product listing Page of competition consist of url and competition name
Listingi_produktowe = {''}


widoki = {'SG':SG, 'Artykuły':Artykuły, 'Listingi_produktowe':Listingi_produktowe}

def getdatapagespeed(url, strategy, category):
    r = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+url+'&strategy='+strategy+'&category='+category+'&locale=pl').content
    dane = json.loads(r)
    return dane

strategies = ['Mobile', 'Desktop']

writer = pd.ExcelWriter('dfspeed.xlsx')

for material_type in widoki:
    df = pd.read_excel('File with domain data', header = [0], sheet_name = material_type)
    index = pd.MultiIndex.from_tuples(list(zip(*[df.Category.tolist(), df.Audit.tolist()])), names=['Category', 'Audit'])
    df = pd.DataFrame(df, index=index)
    for url in widoki[material_type]:
        print(url)
        for strategy in strategies:
            print(strategy)
            for category in list(set(df.index.get_level_values(0))):
                print(category)
                dane = getdatapagespeed(url, strategy, category)
                for audit in df.loc[category].index.get_level_values(0).tolist():
                    print(df.loc[category].index.get_level_values(0).tolist())
                    print(audit)
                    try:
                        df[widoki[material_type][url]+'-'+strategy].loc[category, audit] = dane['lighthouseResult']['audits'][audit]['score']
                        if widoki[material_type][url] == 'allani.pl':
                            df['Uwagi-'+strategy].loc[category, audit] = dane['lighthouseResult']['audits'][audit]['title']+'\\n'+dane['lighthouseResult']['audits'][audit]['description']
                        else:
                            print(widoki[material_type][url])
                    except KeyError as e:
                        print(e)
                        print(dane)
    print(df)
    df.to_excel(writer, sheet_name = material_type)
    writer.save()