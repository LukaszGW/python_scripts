import pandas as pd
import operator
import ast

"""
Script choose best keyword based on search volume
"""

df = pd.read_excel('duplikaty_sv_dolphin.xlsx', index_col=0, dtype={'0': list})
df['najlepsza fraza'] = ''
print(df)
frazy = df.index.tolist()
for lista in df['listy']:
    print(lista)
    print(type(lista))
    true_lista = ast.literal_eval(lista)
    print(true_lista)
    słownik = {fraza.strip(): df.at[fraza.strip(), 'SV'] for fraza in true_lista}
    print(słownik)
    best_fraza = max(słownik.items(), key=operator.itemgetter(1))[0]
    print('najlepsza fraza ', best_fraza)
    print(df.loc[df['listy']==lista])
    print(df)
    df.loc[df['listy']==lista, 'najlepsza fraza'] = best_fraza
    print(df)

writer = pd.ExcelWriter('duplikaty_sv_dolphin_best.xlsx')
df.to_excel(writer)
writer.save()