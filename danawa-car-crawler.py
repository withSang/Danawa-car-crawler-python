from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re


crawl_delay=12


codeDB = {'르노삼성 클리오':3421, '현대 i40':3243, '쉐보레 BOLT EV':3424, '기아 로체':1969} #{key:value} = {car name : car id}
carDB = {} #where the result data stores 


keyword = {'최대토크(kg.m/rpm)', '휠(후)(인치)', '굴림방식', '전장(mm)', '고속연비(km/ℓ)', '배터리종류', '친환경', '충전용량(kWh)',
          '오버행(전)(mm)', '서스펜션(후)', '변속기', '충전방식(급속)', '연료탱크(ℓ)', 'CO₂배출(g/km)', '충전시간(급속)(분)',
          '복합연비(km/ℓ)', '항속거리(km)', '고속연비(km/ℓ)', '적재함길이(mm)', '윤거(후)(mm)', '전고(mm)', '세부모델', '파워스티어링',
          '연료', '모터최고출력(ps)', '서스펜션(전)', '타이어(전)', '배기량(cc)', '전고(mm)', '브레이크(전)', '배터리전압(V)',
          '최고출력(ps/rpm)', '최고속도(km/h)', '축거(mm)', '전폭(mm)', '제로백(초)', '적재량(kg)', '휠(전)(인치)', '가격',
          '적재함넓이(mm)', '엔진형식', '승차정원', '도심연비(km/ℓ)', '모터최대토크(kg.m)', '충전시간(완속)(시간)',
          '브레이크(후)', '타이어(후)', '도심연비(전기)(km/kWh)', '배터리용량(Ah)', '고속연비(전기)(km/kWh)', '충전방식(완속)',
          '적재함높이(mm)', '공회전제한장치', '공차중량(kg)', '에너지소비효율(등급)', '도심연비(km/ℓ)', '복합연비(km/ℓ)',
          '복합연비(전기)(km/kWh)', '윤거(전)(mm)', '오버행(후)(mm)'}



new_titles = {'세부 모델':'세부모델', '가격':'가격', '엔진형식':'엔진형식', '연료':'연료', '배기량 (cc)':'배기량(cc)',
             '최고출력 (ps/rpm)':'최고출력(ps/rpm)', '최대토크 (kg.m/rpm)':'최대토크(kg.m/rpm)', '공회전 제한장치':'공회전제한장치',
             '친환경':'친환경', '배터리 종류':'배터리종류', '배터리 전압 (V)':'배터리전압(V)', '배터리 용량 (Ah)':'배터리용량(Ah)',
             '충전 용량 (kWh)':'충전용량(kWh)', '모터 최고출력 (ps)':'모터최고출력(ps)', '모터 최대토크 (kg.m)':'모터최대토크(kg.m)',
             '충전방식 (완속)':'충전방식(완속)', '충전시간 (완속) (시간)':'충전시간(완속)(시간)', '충전방식 (급속)':'충전방식(급속)', 
             '충전시간 (급속) (분)':'충전시간(급속)(분)', '굴림방식':'굴림방식', '변속기':'변속기', '서스펜션 (전)':'서스펜션(전)', 
             '서스펜션 (후)':'서스펜션(후)', '브레이크 (전)':'브레이크(전)', '브레이크 (후)':'브레이크(후)', '타이어 (전)':'타이어(전)', 
             '타이어 (후)':'타이어(후)', '휠 (전) (인치)':'휠(전)(인치)', '휠 (후) (인치)':'휠(후)(인치)', '복합연비 (km/ℓ)':'복합연비(km/ℓ)', 
             '도심연비 (km/ℓ)':'도심연비(km/ℓ)', '고속연비 (km/ℓ)':'고속연비(km/ℓ)', 'CO₂ 배출 (g/km)':'CO₂배출(g/km)', 
             '에너지소비효율 (등급)':'에너지소비효율(등급)', '복합연비 (전기) (km/kWh)':'복합연비(전기)(km/kWh)', 
             '도심연비 (전기) (km/kWh)':'도심연비(전기)(km/kWh)', '고속연비 (전기) (km/kWh)':'고속연비(전기)(km/kWh)', 
             '항속거리 (km)':'항속거리(km)', '전장 (mm)':'전장(mm)', '전폭 (mm)':'전폭(mm)', '전고 (mm)':'전고(mm)', 
             '축거 (mm)':'축거(mm)', '윤거 (전) (mm)':'윤거(전)(mm)', '윤거 (후) (mm)':'윤거(후)(mm)', 
             '오버행 (전) (mm)':'오버행(전)(mm)', '오버행 (후) (mm)':'오버행(후)(mm)', '승차정원':'승차정원', 
             '공차중량 (kg)':'공차중량(kg)', '연료탱크 (ℓ)':'연료탱크(ℓ)', '적재함 길이 (mm)':'적재함길이(mm)', 
             '적재함 넓이 (mm)':'적재함넓이(mm)', '적재함 높이 (mm)':'적재함높이(mm)', '적재량 (kg)':'적재량(kg)', 
             '제로백 (초)':'제로백(초)', '최고속도 (km/h)':'최고속도(km/h)',
             
             '전장(㎜)':'전장(mm)', '전폭(㎜)':'전폭(mm)', '전고(㎜)':'전고(mm)', '축거(㎜)':'축거(mm)' , '윤거(전)(㎜)':'윤거(전)(mm)',
             '윤거(후)(㎜)':'윤거(후)(mm)','파워스티어링':'파워스티어링',
             '변속기':'변속기', '타이어':['타이어(전)','타이어(후)'][0], '휠':['휠(전)(인치)','휠(후)(인치)'][0], 
             '서스펜션(전/후)':['서스펜션(전)','서스펜션(후)'][0], '도심연비(㎞/ℓ)':'도심연비(km/ℓ)',
             '복합연비(㎞/ℓ)':'복합연비(km/ℓ)', '고속연비(㎞/ℓ)':'고속연비(km/ℓ)', '최고출력(ps/rpm)':'최고출력(ps/rpm)',
             '최대토크(kgm/rpm)':'최대토크(kg.m/rpm)'}


def get_raw_car_table(car_code):
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(3) # 웹 자원이 로드되기까지의 대기 시간 지정

    driver.get('http://auto.danawa.com/auto/?Work=model&Model='+str(car_code)+'&Tab=spec')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    printTable = soup.find('div',{'id':'printTable'}) #차량 제원표만 따오기
    
    driver.close()
    
    printTable = re.sub('<.+?>','\n',str(printTable)).strip()
    printTable = [line.replace('\n',' ').replace('←','') for line in printTable.split('\n\n\n\n\n')]
    printTable = [line.split('  ') for line in printTable]
    printTable = [[j.strip() for j in i] for i in printTable][3::] #기본적인 가공만 마침(공백과 같은 불량한 데이터가 섞여있다)
    return printTable



def remove_empty_data_from(raw_car_table): #3단계로 이루어짐! 
            
    #1    
    for i in range(len(raw_car_table)): #2차원 리스트            
        for j in raw_car_table[i]:
            if j in ['','치수','엔진','구동','연비']:
                raw_car_table[i].remove(j)
    
    #2            
    for i in range(len(raw_car_table)):
        for j in range(len(raw_car_table[i])):
            if raw_car_table[i][j] == '':
                try:
                    if raw_car_table[i][j+1] == '':
                        raw_car_table[i][j] = '-'
                except:
                    raw_car_table[i][j] = '-'
        raw_car_table[i] = [j for j in raw_car_table[i] if j!='']
    
    #3
    remove_list = []
    
    for i in range(len(raw_car_table)):
        if len(raw_car_table[i]) in [0,1]:
            remove_list.append(i)
    
    new_car_table = [raw_car_table[i] for i in range(len(raw_car_table)) if i not in remove_list] 
    return new_car_table



def create_dictionary_from_table(new_car_table):
    
    zip_table = [new_row[0] for new_row in list(zip([(table_row[0], table_row[1::]) for table_row in new_car_table ]))]
    
    raw_dict = dict([(title, ['-']) for title in keyword])
    
    for row in range(len(zip_table)):
        zip_table[row] = list(zip_table[row])
        try: zip_table[row][0] = new_titles[zip_table[row][0]]
        except KeyError: print(zip_table[row][0])
        
        raw_dict[zip_table[row][0]] = zip_table[row][1]
    
    
    if raw_dict['타이어(전)']!=['-'] and raw_dict['타이어(후)']==['-']:
        raw_dict['타이어(전)'], raw_dict['타이어(후)'] = [[i] for i in raw_dict['타이어(전)']]
        
    if raw_dict['서스펜션(전)']!=['-'] and raw_dict['서스펜션(후)']==['-']:
        raw_dict['서스펜션(전)'], raw_dict['서스펜션(후)'] = [[i] for i in raw_dict['서스펜션(전)'][0].split('/')]
        
    if raw_dict['휠(전)(인치)']!=['-'] and raw_dict['휠(후)(인치)']==['-']:
        raw_dict['휠(전)(인치)'], raw_dict['휠(후)(인치)'] = [[i] for i in raw_dict['휠(전)(인치)']]
    
    return raw_dict





def remove_useless_from_dic(diction):
    
    how_many_trims = len([i for i in diction['세부모델'] if i != '-'])
    
    for key in diction:
        if len(diction[key]) == 1:
            diction[key] *= how_many_trims
            
        elif len(diction[key])>how_many_trims:
            diction[key] = diction[key][:how_many_trims]
    
    print(diction)
    
    return diction


###############################################



for name, code in codeDB.items():
    table = get_raw_car_table(code)
    table = remove_empty_data_from(table)
    carDB[name] = remove_useless_from_dic( create_dictionary_from_table(table) ) 
    time.sleep(crawl_delay)

print(carDB)