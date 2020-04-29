import pandas as pd
import re

"""
Script remove duplicate and theirs lexical change identified by regex
"""

frazy = pd.read_excel('C:\\Users\\lukasz.girzycki\\Desktop\\frazy.xlsx').Frazy.tolist()
writerunique = pd.ExcelWriter('frazy_unikalne_dolphin.xlsx')
df = pd.DataFrame()
df.to_excel(writerunique)
writerunique.save()

def find_canibalization(fraza):
    print(fraza)
    try:
        regex = ' '.join([re.search("(\w{"+str(len(słowo)-2)+"})\w+", słowo).group(1)+'\w+' for słowo in fraza.split(' ')])
        print(regex)
        duplikaty = re.findall('[\s*\w*\s*]*' + regex + '[\s*\w*\s*]*', ';'.join(frazy))
        print(duplikaty)
    except AttributeError:
        duplikaty = ''
    return duplikaty

dane = {fraza: find_canibalization(fraza) for fraza in frazy}
df = pd.DataFrame([dane]).T
writer = pd.ExcelWriter('duplikaty_dolphin.xlsx')
df.to_excel(writer)
writer.save()

