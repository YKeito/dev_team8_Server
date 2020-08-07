# ライブラリのインポート
import json
import requests
CodeLIST_Endpoint = 'http://api.ekispert.jp//v1/json/railmap/list?key=test_yfwaB2jzcvw&stationName='
API_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=test_yfwaB2jzcvw&code='
Station = ['篠崎', '渋谷', '錦糸町', '東京', '東陽町']
URLs_list = []
StaName = []
for num in range(len(Station)):
    CodeLIST_Endpoint_temp = CodeLIST_Endpoint+Station[num]
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
    URLs_list.append('https://www.hotpepper.jp/CSP/psh010/doBasic?SA=SA11&FWT='+jsonData['Station']['Name'])
    StaName.append('URLs'+str(int(num)+1))
print(dict(zip(StaName, URLs_list)))
urls.dict = dict(zip(StaName, URLs_list))
