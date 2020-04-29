from pytrends.request import TrendReq
import pandas as pd
import requests
import time
from datetime import date

"""
Script request for google trends interest over time based on enter keyword.
"""

dfrazy = pd.read_excel('Link_To_Google_Sheet_With_Keywords', index_col=0)
print(dfrazy)
keywords = dfrazy.index.tolist()
print(keywords)
writer = pd.ExcelWriter('trendy.xlsx')
df = pd.DataFrame()
print(df)
df.to_excel(writer)
writer.save()


proxy = requests.get('Link_To_Proxy_List').text.split('\n')
print(proxy)
ipiki = {'https':'https://'+ip for ip in proxy}
print(ipiki)
a = 0
def get_data(keyword, writer, a):
    dfall = pd.read_excel('trendy.xlsx', index_col=0)
    print(keyword)
    print('dfall początek\n', dfall)
    kw_list = [keyword]
    results = None
    while results is None:
        print(results)
        try:
            pytrends = TrendReq(hl='pl', tz=-60, timeout=(10, 25))
            pytrends.build_payload(kw_list, timeframe='2019-01-01 '+str(date.today()), geo='PL', gprop='')
            results = pytrends.interest_over_time()
        except Exception as e:
            print(e)
            a += 1
            print(ipiki[a])
            time.sleep(300)
            try:
                pytrends = TrendReq(hl='pl', tz=-60, timeout=(10, 25))
                pytrends.build_payload(kw_list, timeframe='2019-01-01 '+str(date.today()), geo='PL', gprop='')
                results = pytrends.interest_over_time()
            except Exception as e:
                writer = pd.ExcelWriter('trendy-part.xlsx')
                dfall.to_excel(writer)
                print(e)
                pass
    try:
        results = results.drop(columns='isPartial')
        print(results.T)
        print(results.T.columns)
        df = results.T
        print(df.index)
        print('dfall przed połączeniem', dfall)
        dfall = pd.concat([dfall, df])
        print(dfall.columns)
        print('dfall przed zapisaniem ', dfall)
        dfall.to_excel(writer)
        writer.save()
    except Exception as e:
        print(e)
        print('błąd dla słowa', keyword)
        pass

list(map(lambda keyword: get_data(keyword, writer, a), keywords))