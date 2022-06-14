import pandas as pd
import numpy as np
!pip install tabula-py
import tabula
from tabula import read_pdf
idx = pd.IndexSlice
    
###### ESPN PPR Top 300 Scraper
df = read_pdf('https://g.espncdn.com/s/ffldraftkit/22/NFLDK2022_CS_PPR300.pdf', pages = 1,silent = True)
df = np.array(df[0])
ESPNDF = pd.DataFrame(df)
ESPNDF = ESPNDF.dropna(axis = 'columns', how = 'all')
ESPNDF = ESPNDF.dropna(axis = 'rows', how = 'all')
ESPNDF.columns = ['Rankings 1-80','Players 1-80','Auction 1-80','Bye 1-80','Rankings 81-160','Players 81-160','Auction 81-160',
                  'Bye 81-160','Rankings 161-240', 'Players + Auction 161-240', 'Bye 161-240','Rankings 241-300','Players 241-300','Auction 241-300','Bye 241-300']
ESPNDF = ESPNDF.drop(columns = ['Auction 1-80','Bye 1-80','Auction 81-160','Bye 81-160','Bye 161-240','Auction 241-300','Bye 241-300'])
ESPNDF['OVR 1-80'] = ESPNDF['Rankings 1-80'].str.split('.').str[0]
ESPNDF['PosAndRank 1-80'] = ESPNDF['Rankings 1-80'].str.split('.').str[1]
ESPNDF['Players 1-80'] = ESPNDF['Players 1-80'].str.split(',').str[0]
ESPNDF['OVR 81-160'] = ESPNDF['Rankings 81-160'].str.split('.').str[0]
ESPNDF['PosAndRank 81-160'] = ESPNDF['Rankings 81-160'].str.split('.').str[1]
ESPNDF['Players 81-160'] = ESPNDF['Players 81-160'].str.split(',').str[0]
ESPNDF['OVR 161-240'] = ESPNDF['Rankings 161-240'].str.split('.').str[0]
ESPNDF['PosAndRank 161-240'] = ESPNDF['Rankings 161-240'].str.split('.').str[1]
ESPNDF['Players 161-240'] = ESPNDF['Players + Auction 161-240'].str.split('.').str[0]
ESPNDF['Players 161-240'] = ESPNDF['Players 161-240'].str.split(',').str[0]
ESPNDF['PosAndRank 241-300'] = ESPNDF['Rankings 241-300'].str.split('.').str[1]
ESPNDF['Players 241-300'] = ESPNDF['Players 241-300'].str.split(',').str[0]

ESPNDF['PosAndRank 241-300'] = ESPNDF['PosAndRank 241-300'].dropna(axis = 'rows', how = 'any')
    
NewESPN = ESPNDF[['OVR 1-80','Players 1-80','PosAndRank 1-80','OVR 81-160','Players 81-160','PosAndRank 81-160'
                  ,'OVR 161-240','PosAndRank 161-240','Players 161-240']]
NewESPN = NewESPN.dropna(axis = 'rows', how = 'any')

ESPNDF = NewESPN
Top80 = ESPNDF[['OVR 1-80','Players 1-80','PosAndRank 1-80']].copy()
Top160 = ESPNDF[['OVR 81-160','Players 81-160','PosAndRank 81-160']].copy()
Top240 = ESPNDF[['OVR 161-240','Players 161-240','PosAndRank 161-240']].copy()
    
all_dfs = [Top80, Top160, Top240]
for df in all_dfs:
    df.columns = ['ESPNOverall','ESPNPlayer','ESPNPosAndRank']
    ESPNRanks = pd.concat(all_dfs).reset_index(drop = True)
    ESPNRanks = ESPNRanks.dropna()
    ESPNRanks['ESPNPlayer'] = ESPNRanks['ESPNPlayer'].str.lstrip()
    ESPNRanks['ESPNPlayer'] = ESPNRanks['ESPNPlayer'].str.rstrip()
    ESPNRanks['ESPNPosAndRank'] = ESPNRanks['ESPNPosAndRank'].str.lstrip()
    ESPNRanks['ESPNPosAndRank'] = ESPNRanks['ESPNPosAndRank'].str.rstrip()
    ESPNRanks['ESPNPosAndRank'] = ESPNRanks['ESPNPosAndRank'].str.strip('(')
    ESPNRanks['ESPNPosAndRank'] = ESPNRanks['ESPNPosAndRank'].str.strip(')')
    ESPNRanks = ESPNRanks[ESPNRanks['ESPNPosAndRank'].str[:3] != 'DST']
    ESPNRanks = ESPNRanks[ESPNRanks['ESPNPosAndRank'].str[:1] != 'K']
    ESPNRanks['ESPNPosRank'] = ESPNRanks['ESPNPosAndRank'].str[2:]

QBRanks = ESPNRanks[ESPNRanks['ESPNPosAndRank'].str[:2] == 'QB']
RBRanks = ESPNRanks[ESPNRanks['ESPNPosAndRank'].str[:2] == 'RB']
WRRanks = ESPNRanks[ESPNRanks['ESPNPosAndRank'].str[:2] == 'WR']
TERanks = ESPNRanks[ESPNRanks['ESPNPosAndRank'].str[:2] == 'TE']
print(WRRanks)
