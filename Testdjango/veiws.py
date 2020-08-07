from django import forms
from django.shortcuts imoirt render
import json
import requests
import numpy as np

def index(request):
    return render(request, 'index.html')


def plztext(request):
    try:
        input_text1=request.POST['input1']
        input_text2=request.POST['input2']
        input_text3=request.POST['input3']
        input_text4=request.POST['input4']
        input_text5=request.POST['input5']

    except:
        return render(request, 'index.html')

#ここからAPI

CodeLIST_Endpoint = 'http://api.ekispert.jp//v1/json/railmap/list?key=test_yfwaB2jzcvw&stationName='
API_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=test_yfwaB2jzcvw&code='
Station = [input_text1,input_text2,input_text3, input_text4, input_text5]
StationName = []
StationCode = []
StaCode = []
longi_d = []
lati_d = []
for Station_temp in Station:
    CodeLIST_Endpoint_temp = CodeLIST_Endpoint+Station_temp
    # API接続の実行
    Code_result = requests.get(CodeLIST_Endpoint_temp)
    Code_jsonData = Code_result.json()
    Code_Station = Code_jsonData['ResultSet']['RailMap']['Point']['Station']
    StaCode.append = Code_Station['code']



Outputnum=['output1', 'output2', 'output3', 'output4', 'output5']
Codedict = dict(zip(Outputnum, StaCode))






return render(request, 'aiueo.html', Codedict)