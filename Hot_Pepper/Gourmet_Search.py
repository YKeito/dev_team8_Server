# ライブラリのインポート
import json
import requests
########################################################################
#都道府県のコードを入手する
pre_goal_longi = str(139.906972)
pre_goal_lati = str(35.70286)
API_Endpoint = 'http://webservice.recruit.co.jp/hotpepper/large_area/v1/?key=088ae32e84ca8e20&format=json'
result = requests.get(API_Endpoint).json()
JsonData = result['results']['large_area']
Large_Area_Code = []
Large_Area_Name = []
for area in range(len(JsonData)):
    Large_Area_Code.append(JsonData[area]['code'])
    Large_Area_Name.append(JsonData[area]['name'])
Large_Area = dict(zip(Large_Area_Code, Large_Area_Name))
########################################################################
#最終目的地周辺でヒットした飲食店数を入手する
# 新宿の経度緯度を利用
pre_goal_longi = str(139.906972)
pre_goal_lati = str(35.70286)
#rangeは1:300m, 2:500m, 3:1000, 4:2000m, 5:3000m
API_Endpoint = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=088ae32e84ca8e20&format=json&lat=' + pre_goal_lati + '&lng=' + pre_goal_longi + '&range=3&order=4'
result = requests.get(API_Endpoint)
jsonData = result.json()
#集合駅の周辺にあるお店の数
NumHits = jsonData['results']['results_available']
print(NumHits, ' Hits')
########################################################################
#例) 収容人数50人以上の飲食店を入手する。
Party_Capacity = str(50)
API_Endpoint = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=088ae32e84ca8e20&format=json&lat=' + pre_goal_lati + '&lng=' + pre_goal_longi + '&range=3&order=4&party_capacity=' + Party_Capacity
result = requests.get(API_Endpoint)
jsonData = result.json()
Shop = jsonData['results']['shop']
print(Shop)
########################################################################
#予算コードを入手する
API_Endpoint = 'http://webservice.recruit.co.jp/hotpepper/budget/v1/?key=088ae32e84ca8e20&format=json'
result = requests.get(API_Endpoint)
jsonData = result.json()
Budget = jsonData['results']['budget']
#Price_Rangeにはユーザーが入力した値を入れる。
Price_Range = '～500円'
Budget_Input = filter(lambda x: Price_Range in x["name"], Budget)
Budget_Input = list(Budget_Input)
Budget_code = Budget_Input[0]['code']
#ユーザーが指定した予算範囲内の飲食店情報を入手する。
API_Endpoint = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=088ae32e84ca8e20&format=json&lat=' + pre_goal_lati + '&lng=' + pre_goal_longi + '&range=3&order=4&count=5&budget='+Budget_code
result = requests.get(API_Endpoint)
jsonData = result.json()
Shop = jsonData['results']['shop']
#print(Shop)