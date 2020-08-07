# ライブラリのインポート
import json
import requests
import pickle
import time
start = time.time()
########################################################################
#都道府県ごとのレーティングを作成
#なぜかtest_yfwaB2jzcvwのAPI keyだと他がヒットしてしまう。
#フリー版のLE_umHHVYL54rWF8のAPI keyを使うことに使用
Prefectures={'北海道':1, '青森県':2, '岩手県':3, '宮城県':4, '秋田県':5, '山形県':6, '福島県':7, 
'茨城県':8, '栃木県':9, '群馬県':10, '埼玉県':11, '千葉県':12, '東京都':13, '神奈川県':14, 
'新潟県':15, '富山県':16, '石川県':17, '福井県':18, '山梨県':19, '長野県':20, '岐阜県':21, 
'静岡県':22, '愛知県':23, '三重県':24, '滋賀県':25, '京都府':26, '大阪府':27, '兵庫県':28, 
'奈良県':29, '和歌山県':30, '鳥取県':31, '島根県':32, '岡山県':33, '広島県':34, '山口県':35, 
'徳島県':36, '香川県':37, '愛媛県':38, '高知県':39, '福岡県':40, '佐賀県':41, '長崎県':42, 
'熊本県':43, '大分県':44, '宮崎県':45, '鹿児島県':46, '沖縄県':47}
#Rating_list = []
Rating_Code_list = []
Pref_Code_list = []
for Pref in list(Prefectures.values()):
    Ekispert_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=LE_umHHVYL54rWF8&type=train&prefectureCode='+str(Pref)
    API_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=test_yfwaB2jzcvw&code='
    result = requests.get(Ekispert_Endpoint).json()
    NumHits = result['ResultSet']['max']
    total = range(1, int(NumHits), 100)
    Results_Available = []
#    StaName_list = []
    StaCode_list = []
    for num in total:
        Ekispert_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=LE_umHHVYL54rWF8&type=train&prefectureCode='+str(Pref)+'&offset='+str(num)
        result = requests.get(Ekispert_Endpoint).json()
        jsonData = result['ResultSet']['Point']
        if isinstance(jsonData, list):
            for index in range(len(jsonData)):
#                StaName = jsonData[index]['Station']['Name']
#                StaName_list.append(StaName)
                StaCode = jsonData[index]['Station']['code']
                StaCode_list.append(StaCode)
                API_Endpoint_temp = API_Endpoint+str(StaCode)
                Code_result = requests.get(API_Endpoint_temp)
                Code_result = Code_result.json()
                Code_jsonData = Code_result['ResultSet']['Point']
                longi_d = Code_jsonData['GeoPoint']["longi_d"]
                lati_d = Code_jsonData['GeoPoint']["lati_d"]
                Hot_Pepper_Endpoint = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=088ae32e84ca8e20&format=json&lat=' + lati_d + '&lng=' + longi_d + '&range=3'
                HP_result = requests.get(Hot_Pepper_Endpoint).json()
                Results_Available.append(HP_result['results']['results_available'])
        else:
#            StaName = jsonData['Station']['Name']
#            StaName_list.append(StaName)
            StaCode = jsonData['Station']['code']
            StaCode_list.append(StaCode)
            API_Endpoint_temp = API_Endpoint+str(StaCode)
            Code_result = requests.get(API_Endpoint_temp)
            Code_result = Code_result.json()
            Code_jsonData = Code_result['ResultSet']['Point']
            longi_d = Code_jsonData['GeoPoint']["longi_d"]
            lati_d = Code_jsonData['GeoPoint']["lati_d"]
            Hot_Pepper_Endpoint = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=088ae32e84ca8e20&format=json&lat=' + lati_d + '&lng=' + longi_d + '&range=3'
            HP_result = requests.get(Hot_Pepper_Endpoint).json()
            Results_Available.append(HP_result['results']['results_available'])
        print('Pref=', Pref, 'num=', num)
        Pref_Code_list.append(Pref)
#    Rating = dict(zip(StaName_list, Results_Available))
    Rating_Code = dict(zip(StaCode_list, Results_Available))
#    Rating_list.append(Rating)
    Rating_Code_list.append(Rating_Code)

#Rating_Summary = dict(zip(list(Prefectures.keys()), Rating_list))
Rating_Code_Summary = dict(zip(Pref_Code_list, Rating_Code_list))

#with open('allPref_Rating.binaryfile', 'wb') as web:
#    pickle.dump(Rating_Summary, web)
with open('allPref_Codever_Rating.binaryfile', 'wb') as web:
    pickle.dump(Rating_Code_Summary, web)

process_time = time.time() - start
print(process_time)
