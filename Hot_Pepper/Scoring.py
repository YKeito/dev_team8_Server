# ライブラリのインポート
import json
import requests
import pickle
import numpy as np
with open('allPref_Rating.binaryfile', 'rb') as web:
    Rating = pickle.load(web)

"""
q25, q75 = np.percentile(list(Rating['東京都'].values()), q=[25, 75])
iqr = q75 - q25
# 下限
lower_bound = q25 - (iqr * 1.5)
# 上限
upper_bound = q75 + (iqr * 1.5)
print("25パーセント点", q25)
print("75パーセント点", q75)
print("四分位範囲", iqr)
print('下限は', lower_bound)
print('上限は', upper_bound)
print(np.percentile(list(Rating['東京都'].values()), q=[0, 25, 50, 75, 100]))
#ミスである根拠
sibuni = np.percentile(list(Rating['愛知県'].values()), q=[0, 25, 50, 75, 100])
print(sibuni[0])
print(sibuni[1])
print(sibuni[2])
print(sibuni[3])
print(sibuni[4])
"""

CodeLIST_Endpoint = 'http://api.ekispert.jp//v1/json/railmap/list?key=test_yfwaB2jzcvw&stationName='
API_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=test_yfwaB2jzcvw&code='
Station = ['篠崎', '錦糸町', '東京']
StaName = []
PrefName = []
for Station_temp in Station:
    CodeLIST_Endpoint_temp = CodeLIST_Endpoint+Station_temp
    #Name → Code API接続の実行
    Code_result = requests.get(CodeLIST_Endpoint_temp)
    Code_jsonData = Code_result.json()
    Code_Station = Code_jsonData['ResultSet']['RailMap']['Point']['Station']
    Code = Code_Station['code']
    #Name → 色々 API接続の実行
    API_Endpoint_temp = API_Endpoint+Code
    result = requests.get(API_Endpoint_temp)
    jsonData = result.json()
    jsonData = jsonData['ResultSet']['Point']
    StaName.append(jsonData['Station']['Name'])
    PrefName.append(jsonData['Prefecture']['Name'])

Pref_dict = dict(zip(StaName, PrefName))
Score_key_BS = []
Score_key_WS = []
Score_value = []
for p in range(len(PrefName)):
    Rating_Base = Rating[PrefName[p]]
    Rate = np.percentile(list(Rating_Base.values()), q=[0, 25, 50, 75, 100])
    Pref_value = Rating_Base.get(StaName[p], "NotFound")
    Score_key_BS.append('Star_BS' + str(p+1))
    Score_key_WS.append('Star_WS' + str(p+1))
    if Pref_value >= Rate[0] and Pref_value < Rate[1]:
        Score_value.append(1)
    elif Pref_value >= Rate[1] and Pref_value < Rate[2]:
        Score_value.append(2)
    elif Pref_value >= Rate[2] and Pref_value < Rate[3]:
        Score_value.append(3)
    elif Pref_value >= Rate[3] and Pref_value < Rate[4]:
        Score_value.append(4)
    elif Pref_value >= Rate[4] and Pref_value <= Rate[5]:
        Score_value.append(5)
BS=[]
WS=[]
for scindex in range(len(Station)):
    if Score_value[scindex]==1:
        BS.append('★')
        WS.append('☆☆☆☆')
    elif Score_value[scindex]==2:
        BS.append('★★')
        WS.append('☆☆☆')
    elif Score_value[scindex]==3:
        BS.append('★★★')
        WS.append('☆☆')
    elif Score_value[scindex]==4:
        BS.append('★★★★')
        WS.append('☆')
    elif Score_value[scindex]==5:
        BS.append('★★★★★')
        WS.append('')


Score_dict_BS = dict(zip(Score_key_BS, BS))
Score_dict_WS = dict(zip(Score_key_WS, WS))
print(Score_dict)
#四分位を算出するときに、外れ値の処理をする必要がありそう。
#東京[   0.   18.   54.  166. 2224.]
#千葉[  0.   0.   4.  21. 372.]
#福岡[   0.    0.    2.  13. 1174.]

