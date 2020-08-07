#使用するパッケージ
from django import forms
from django.shortcuts import render
from django.template import loader
import json
import requests
import pprint
import numpy as np
import itertools
#index.htmlの表示
def index(request):
    return render(request, 'inSta/index.html')
#result.htmlの表示
def plztext(request):
    #print('testooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooss')
    loader.get_template('inSta/aiueo.html')    
    try:
        input_text1=request.POST['input1']
        input_text2=request.POST['input2']
        input_text3=request.POST['input3']
        input_text4=request.POST['input4']
        input_text5=request.POST['input5']
    except:
        print('except入った')
        return render(request, 'inSta/index.html')
    #NameからCodeを出すAPI
    CodeLIST_Endpoint = 'http://api.ekispert.jp/v1/json/railmap/list?key=test_yfwaB2jzcvw&stationName='
    InputStation = [input_text1,input_text2,input_text3, input_text4, input_text5]
    InputStation = filter(lambda a: a != "", InputStation)
    InitStaCode = []
    for InputStation_temp in InputStation:
        CodeLIST_Endpoint_temp = CodeLIST_Endpoint + InputStation_temp
        # API接続の実行
        Code_result = requests.get(CodeLIST_Endpoint_temp)
        Code_jsonData = Code_result.json()
        Code_Station = Code_jsonData['ResultSet']['RailMap']['Point']['Station']
        print(Code_Station)
        InitStaCode.append(Code_Station['code'])
    #Codeから経度緯度を出すAPI
    API_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=test_yfwaB2jzcvw&code='
    InitStaName = []
    longi_d = []
    lati_d = []
    for InitStaCode_temp in InitStaCode:
        API_Endpoint_temp = API_Endpoint + InitStaCode_temp
        # API接続の実行
        result = requests.get(API_Endpoint_temp)
        jsonData = result.json()
        jsonData = jsonData['ResultSet']['Point']
        longi_d_temp = float(jsonData['GeoPoint']["longi_d"])
        longi_d.append(longi_d_temp)
        lati_d_temp = float(jsonData['GeoPoint']["lati_d"])
        lati_d.append(lati_d_temp)
    #複数の入力駅から重心を求める
    pre_goal_longi = np.mean(longi_d)
    pre_goal_lati = np.mean(lati_d)
    print(pre_goal_longi, pre_goal_lati)    
    #重心から集合駅の候補を調べるAPI
    Lng=pre_goal_lati
    Lat=pre_goal_longi    
    NeStaName = []
    NeStaCode = []
    Radius = 1000
    GetNearStation_API = 'http://api.ekispert.jp/v1/json/geo/station?key=test_yfwaB2jzcvw&geoPoint='
    GetNearStation = GetNearStation_API + str(Lng) + ','+ str(Lat) + ',tokyo,'+str(Radius)+ '&type=train'
    jDNearSta = requests.get(GetNearStation).json()
    while 'Point' not in jDNearSta['ResultSet']:
        Radius = Radius+1000
        GetNearStation = GetNearStation_API+ str(Lng) + ','+ str(Lat) + ',tokyo,'+str(Radius)+ '&type=train'
        jDNearSta = requests.get(GetNearStation).json()
    Point_temp = jDNearSta['ResultSet']['Point']
    while isinstance(Point_temp, dict) and len(Point_temp) < 6:
        Radius = Radius+1000
        GetNearStation = GetNearStation_API+ str(Lng) + ','+ str(Lat) + ',tokyo,'+str(Radius)+ '&type=train'
        jDNearSta = requests.get(GetNearStation).json()
        Point_temp = jDNearSta['ResultSet']['Point']
        if len(Point_temp) >= 6:
            for index in range(len(Point_temp)):
                NeStaName.append(Point_temp[index]['Station']['Name'])
                NeStaCode.append(Point_temp[index]['Station']['code'])
    else:
        while len(Point_temp) < 6:
            Radius = Radius+1000
            GetNearStation = GetNearStation_API+ str(Lng) + ','+ str(Lat) + ',tokyo,'+str(Radius)+ '&type=train'
            jDNearSta = requests.get(GetNearStation).json()
            Point_temp = jDNearSta['ResultSet']['Point']
            for index in range(len(Point_temp)):
                NeStaName.append(Point_temp[index]['Station']['Name'])
                NeStaCode.append(Point_temp[index]['Station']['code'])
        else:
            for index in range(len(Point_temp)):
                NeStaName.append(Point_temp[index]['Station']['Name'])
                NeStaCode.append(Point_temp[index]['Station']['code'])
    print('半径', Radius ,'m以内にヒット', len(NeStaName) ,'件')    
    #入力駅から集合候補駅までの経路調べるAPI
    API_Endpoint = 'http://api.ekispert.jp/v1/json/search/course/extreme?key=test_yfwaB2jzcvw&sort=price&viaList='
    NeStaName = NeStaName[0:5]
    NeStaCode = NeStaCode[0:5]
    diff_list=[]
    allOneway=[]
    StaCode_Time = []
    for Code_temp in NeStaCode:
        Getcourse = []
        Time_list = []
        for index in range(len(initCode)):
            API_Endpoint_temp = API_Endpoint + str(initCode[index]) +':'+ Code_temp
            jDcourse = requests.get(API_Endpoint_temp)
            jDcourse = jDcourse.json()
            jDcourse = jDcourse['ResultSet']['Course']
            if isinstance(jDcourse, list):
                Price = jDcourse[0]['Price']
                TimeOnBoard = jDcourse[0]['Route']['timeOnBoard']
                TimeOther = jDcourse[0]['Route']['timeOther']
                TimeWalk = jDcourse[0]['Route']['timeWalk']
                Time = int(TimeOnBoard)+int(TimeOther)+int(TimeWalk)
            else:
                Price = jDcourse['Price']
                TimeOnBoard = jDcourse['Route']['timeOnBoard']
                TimeOther = jDcourse['Route']['timeOther']
                TimeWalk = jDcourse['Route']['timeWalk']
                Time = int(TimeOnBoard)+int(TimeOther)+int(TimeWalk)
            OneWay = [x['Oneway'] for x in Price if x['kind'] == 'Fare']
            OneWay = int(OneWay[0]) if len(OneWay) else 'None'
            Getcourse.append(OneWay)
            Time_list.append(Time)
        #{駅コード:片道料金}というデータ
        StaCode_Time.append(dict(zip(InitStaName, Time_list)))
        Data_Summary=dict(zip(InitStaName, Getcourse))
        Data_Summary_Max = max(Data_Summary.items(), key=lambda x:x[1])
        Data_Summary_Min = min(Data_Summary.items(), key=lambda x:x[1])
        diff = Data_Summary_Max[1]-Data_Summary_Min[1]
        diff_list.append(diff)
        allOneway.append(Data_Summary)

    OneWay_Summary = dict(zip(NeStaName, diff_list))
    #片道が安い順に6駅抽出したい。だが、合計6駅になるとき、ぴったり6駅にならないことを考慮しないといけない。
    #ピッタリ6駅じゃないときは近いものを選ぶ。…と考えたがその場合でも絞り切れないこともあり、きりがない。上から6駅にしよう
    OneWay_Summary_sorted = sorted(OneWay_Summary.items(), key=lambda x:x[1])
    OneWay_Summary_sorted = OneWay_Summary_sorted[0:6]
    OneWay_Summary_sorted = dict(OneWay_Summary_sorted)
    Goal_Station = [Goal_Station[0] for Goal_Station in OneWay_Summary_sorted.items()]
    Goal_Summary = dict(zip(NeStaName, allOneway))
    Goal_Time = dict(zip(NeStaName, StaCode_Time))
    print(Goal_Time)

    #所要時間表示用のdict作成
    time_value = list()
    for p in range(0, 6):
        temp_time = list(Goal_Time.values())[p]
        time_value.append(list(temp_time.values()))
    time_value = list(itertools.chain.from_iterable(time_value))
    time_key = []
    for i in [6, 16, 26, 36, 46, 56]:
        for j in range(0, 5):
            time_key.append('data' + str(int(i)+int(j)))

    Time_dict = dict(zip(time_key, time_value))
    #運賃表示用のdict作成
    untin_value = list()
    for p in range(0, 6):
        temp_untin = list(Goal_Summary.values())[p]
        untin_value.append(list(temp_untin.values()))
    untin_value = list(itertools.chain.from_iterable(untin_value))
    untin_key = []
    for i in [1, 11, 21, 31, 41, 51]:
        for j in range(0, 5):
            untin_key.append('data' + str(int(i)+int(j)))

    Untin_dict = dict(zip(untin_key, untin_value))
    #print(Untin_dict)
    #入力駅名表示用のdict作成
    Input_dict = dict(zip(['input1', 'input2', 'input3', 'input4', 'input5'], InitStaName))
    #候補駅表示用のdict作成
    kouhonum=['kouho1','kouho2','kouho3','kouho4','kouho5','kouho6']
    Kouho_dict=dict(zip(kouhonum,Goal_Summary.keys()))
    
    #集合候補駅周辺の飲食店URLを獲得する方法
    CodeLIST_Endpoint = 'http://api.ekispert.jp//v1/json/railmap/list?key=test_yfwaB2jzcvw&stationName='
    API_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=test_yfwaB2jzcvw&code='
    URLs_list = []
    StaName = []
    for num in range(len(NeStaName)):
        URLs_list.append('https://www.hotpepper.jp/CSP/psh010/doBasic?SA=SA11&FWT='+NeStaName[num])
        StaName.append('URLs'+str(int(num)+1))
    urls_dict = dict(zip(StaName, URLs_list))

    #入力駅から集合候補駅の詳細経路のURLを獲得する方法
    Pathway_Endpoint = 'http://api.ekispert.jp/v1/json/search/course/light?key=test_yfwaB2jzcvw&from='
    ekispert_URLs = []
    Pathway_key = []
    Pathway_value = []
    i = 1
    for From in InitStaCode:
        for To in NeStaCode:
            Pathway_Endpoint_temp = Pathway_Endpoint + From + '&to=' + To
            result = requests.get(Pathway_Endpoint_temp)
            jsonData = result.json()
            Pathway_value.append(jsonData['ResultSet']['ResourceURI'])
            Pathway_key.append('Pathway' + str(i))
            i = i + 1
    Pathway_dict = dict(zip(Pathway_key, Pathway_value))

    #集合候補駅の繁華街度を出すAPI
    with open('allPref_Rating.binaryfile', 'rb') as web:
        print(os.path.getsize('allPref_Rating.binaryfile'))
        Rating = pickle.load(web)

    CodeLIST_Endpoint = 'http://api.ekispert.jp//v1/json/railmap/list?key=test_yfwaB2jzcvw&stationName='
    API_Endpoint = 'http://api.ekispert.jp/v1/json/station?key=test_yfwaB2jzcvw&code='
    StaName = []
    PrefName = []
    for Code in NeStaCode:
        #Name → 色々 API接続の実行
        API_Endpoint_temp = API_Endpoint+Code
        result = requests.get(API_Endpoint_temp)
        jsonData = result.json()
        jsonData = jsonData['ResultSet']['Point']
        PrefName.append(jsonData['Prefecture']['Name'])

    Pref_dict = dict(zip(NeStaName, PrefName))
    Score_key_BS = []
    Score_key_WS = []
    BS=[]
    WS=[]
    for p in range(len(PrefName)):
        Rating_Base = Rating[PrefName[p]]
        Rate = np.percentile(list(Rating_Base.values()), q=[0, 25, 50, 75, 100])
        Pref_value = Rating_Base.get(NeSta[p], "NotFound")
        Score_key_BS.append('Star_BS' + str(p+1))
        Score_key_WS.append('Star_WS' + str(p+1))
        if Pref_value >= Rate[0] and Pref_value < Rate[1]:
            BS.append('★')
            WS.append('☆☆☆☆')
        elif Pref_value >= Rate[1] and Pref_value < Rate[2]:
            BS.append('★★')
            WS.append('☆☆☆')
        elif Pref_value >= Rate[2] and Pref_value < Rate[3]:
            BS.append('★★★')
            WS.append('☆☆')
        elif Pref_value >= Rate[3] and Pref_value < Rate[4]:
            BS.append('★★★★')
            WS.append('☆')
        elif Pref_value >= Rate[4] and Pref_value <= Rate[5]:
            BS.append('★★★★★')
            WS.append('')

    Score_dict_BS = dict(zip(Score_key_BS, BS))
    Score_dict_WS = dict(zip(Score_key_WS, WS))

    #ひとつのdictにまとめる
    all_dict = {}
    all_dict.update(**Untin_dict, **Time_dict, **Input_dict, **Kouho_dict,**urls_dict, **Score_dict_BS,**Score_dict_WS )
    #print(all_dict)
    
    return render(request, 'inSta/result.html', all_dict)
