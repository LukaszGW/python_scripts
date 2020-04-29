import pandas as pd

'''
Script compare desktop and mobile version of website based on Screaming Frog results and write differences to Excel file.
'''

df = pd.read_excel('Path_To_ScreamingFrog_Results', index_col=0)
attr = ['H2-2 length', 'Inlinks', 'Status Code', 'External Outlinks', 'Crawl Depth', 'Outlinks', 'Unique Inlinks',
        'Canonical Link Element 1', 'Title 1 Length', 'Content', 'H2-1 length', 'Indexability', 'Hash',
        'HTTP rel="prev" 1', 'Meta Description 1', 'H2-1', 'H2-2', 'URL Encoded Address', 'Last Modified', '% of Total',
        'Meta Keyword 1', 'H1-1', 'X-Robots-Tag 1', 'Unique External Outlinks', 'Title 1 Pixel Width', 'Meta Robots 1',
        'Meta Description 1 Pixel Width', 'Size (bytes)', 'Text Ratio', 'Unique Outlinks', 'Meta Description 1 Length',
        'Word Count', 'H1-1 length', 'Meta Refresh 1', 'Link Score', 'HTTP rel="next" 1', 'Response Time',
        'rel="prev" 1', 'Status', 'Redirect URL', 'Title 1', 'Indexability Status', 'Redirect Type', 'rel="next" 1'
        , 'Meta Keywords 1 Length']
print(df)
df = df.fillna(0)
for attribute in attr:
    print(attribute)
    dfcomp = df.loc[df[attribute+'_mobile'].eq(df[attribute+'_desktop']) == False]
    #print(dfcomp)
    if bool(dfcomp.values.tolist()):
        dfcomp = dfcomp[[attribute+'_mobile', attribute+'_desktop']]
        print(dfcomp)
        writer = pd.ExcelWriter('C:\\Users\\lukasz.girzycki\\Desktop\\mobile_desktop_inspiracje\\różnice\\comparison_mobile_desktop'+attribute+'.xlsx')
        dfcomp.to_excel(writer)
        writer.save()
    else:
        print('brak różnic')