import json
import requests

CodeLIST_Endpoint = 'http://api.ekispert.jp//v1/json/railmap/list?key=test_yfwaB2jzcvw&stationName='
API_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=test_yfwaB2jzcvw&code='
Station = ['篠崎', '播州赤穂', '錦糸町']
StationName = []
StationCode = []
longi_d = []
lati_d = []
for Station_temp in Station:
    CodeLIST_Endpoint_temp = CodeLIST_Endpoint+Station_temp
    # API接続の実行
    Code_result = requests.get(CodeLIST_Endpoint_temp)
    Code_jsonData = Code_result.json()
    Code_Station = Code_jsonData['ResultSet']['RailMap']['Point']['Station']
    Code = Code_Station['code']
    API_Endpoint_temp = API_Endpoint+Code
    # API接続の実行
    result = requests.get(API_Endpoint_temp)
    jsonData = result.json()
    jsonData = json.dumps(jsonData, ensure_ascii=False)
    # ""をなくす（データ型を変換できるようにしたいから）。これを実行しないと'"aaa"'といった表記になる。
    jsonData = json.loads(jsonData)
    jsonData = jsonData['ResultSet']['Point']
    StationName_temp = jsonData['Station']['Name']
    StationName.append(StationName_temp)
    StationCode_temp = jsonData['Station']['code']
    StationCode.append(StationCode_temp) 
    longi_d_temp = float(jsonData['GeoPoint']["longi_d"])
    longi_d.append(longi_d_temp)
    lati_d_temp = float(jsonData['GeoPoint']["lati_d"])
    lati_d.append(lati_d_temp)

