# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os
import io
import shutil
import pandas as pd
import numpy as np
import csv
import pandas as pd
import numpy as np
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaIoBaseDownload

new_origin_csv = 'm1.csv'
old_origin_csv = 'o1.csv'
new_edited_csv = 'm2.csv'
old_edited_csv = 'o2.csv'

origin_new_columns = ['timestamp', 'name','phone','sex','food','daystype','transportation','birthday','id','address','contact','contact-phone','email','prefessional','agent','foreign','bed','insurance','argee']
origin_old_columns = ['timestamp','name','phone','sex','food','daystype','transportation','email','bed','insurance','driver','argee']
new_columns = ['name', 'phone', 'sex','food','daystype','transportation','bed','insurance','birthday','id']
old_columns = ['name', 'phone', 'sex','food','daystype','transportation','bed','insurance','driver']

def save_dict(di):
    with open('cfg.json', 'w') as fp:
     json.dump(di, fp)
    
def load_dict():
    with open('cfg.json', 'r') as fp:
        return json.load(fp)  

def get_credentials():
    secret_dir = "/home/src/.secret"
    credential_file = 'credentials.json'
    credential_path = os.path.join(secret_dir,credential_file)
    store = Storage(credential_path)
    return store.get()

def download(credentials,remote,local):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    results = service.files().list(pageSize=100,fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        item = next(item for item in items if item['name'] == remote)
        filebytes = service.files().export(fileId=item['id'],mimeType='text/csv').execute()
        f = open(local, 'wb')
        f.write(filebytes)
        f.close()
    return local

def download_new_csv():
    cfg = load_dict()
    credentials = get_credentials()
    download(credentials,cfg['new_csv'],new_origin_csv)

def download_old_csv():
    cfg = load_dict()
    credentials = get_credentials()
    download(credentials,cfg['old_csv'],old_origin_csv)

def load_new_csv():
    tmp = pd.read_csv(new_origin_csv,header=0,names=origin_new_columns)
    return tmp 

def load_old_csv():
    tmp = pd.read_csv(old_origin_csv,header=0,names=origin_old_columns)
    return tmp

def resolve_new_members(lst):
    tmp = lst[new_columns].copy()
    tmp['phone'] = '0'+tmp['phone'].apply(str).str.replace('-','')
    tmp['transportation'] = tmp['transportation'].str.slice(0, 3).str.replace('(','').str.replace('行天','行天宮').str.replace('開','開車').str.replace('搭','前往')
    tmp['id'] = tmp['id'].str.upper()
    tmp['insurance'] = np.where(tmp['insurance']=='是','是','否')
    for index, row in tmp.iterrows():
        s = row['birthday']
        if s.find('/')==-1:
            if len(s)==6:
                row['birthday'] = s[:2] + '/' + s[2:-2] + '/' + s[-2:]
        else:
            bp = s.split('/')
            if len(bp)==3:
                bp = [x if len(x)>1 else '0'+x for x in bp]
                row['birthday'] = bp[0] + '/' + bp[1] + '/' + bp[2]
    return tmp

def resolve_old_members(lst):
    tmp = lst[old_columns].copy()
    tmp['phone'] = '0'+tmp['phone'].apply(str).str.replace('-','')
    tmp['transportation'] = tmp['transportation'].str.slice(0, 3).str.replace('(','').str.replace('行天','行天宮').str.replace('開','開車').str.replace('搭','前往')
    tmp['insurance'] = np.where(tmp['insurance']=='是','是','否')
    return tmp

def save_new_members(lst):
    lst.to_csv(new_edited_csv)

def save_old_members(lst):
    lst.to_csv(old_edited_csv)

def load_new_members():
    tmp = pd.read_csv(new_edited_csv,header=0,names=new_columns)
    return tmp

def load_old_members():
    tmp = pd.read_csv(old_edited_csv,header=0,names=old_columns)
    return tmp

def load_locations():
    tmp = pd.read_csv('locations.csv',header=None,names=['loc','loc_seq','loc_addr'])
    return tmp
    
def get_all_members(new_members,old_members):
    cfg = load_dict()
    locations = load_locations()
    new_members['isnew']=1
    lst = pd.concat([new_members,old_members])
    lst['car'] = np.where(lst['transportation']=='自行前往','',cfg['cartype'])
    lst['days'] = np.where(lst['daystype']=='二天',2,1)
    lst['bedrequired'] = np.where(lst['bed']=='否',0,1)
    lst['isnew'] = np.where(lst['isnew']==1,'*','')
    lst = lst.merge(locations, left_on='transportation', right_on='loc', how='left')
    lst = lst.sort_values(['loc_seq','daystype'])
    return lst

def get_summary_report(lst):
    cfg = load_dict()
    lst.index = np.arange(1, len(lst) + 1)
    newcnt = lst[lst.isnew=='*'].count('index')['name']
    oldcnt = lst[lst.isnew!='*'].count('index')['name']
    new1 = lst[((lst.daystype=='星期六') | (lst.daystype=='二天')) & (lst.isnew=='*')].count('index')['name']
    new2 = lst[((lst.daystype=='星期日') | (lst.daystype=='二天')) & (lst.isnew=='*')].count('index')['name']
    old1 = lst[((lst.daystype=='星期六') | (lst.daystype=='二天')) & (lst.isnew!='*')].count('index')['name']
    old2 = lst[((lst.daystype=='星期日') | (lst.daystype=='二天')) & (lst.isnew!='*')].count('index')['name']
    bed1 = lst[(lst.bedrequired==1) & (lst.sex=='男')].count('index')['name']
    bed2 = lst[(lst.bedrequired==1) & (lst.sex=='女')].count('index')['name']
    car1 = lst[(lst.transportation!='自行前往') & (lst.transportation!='自行開車')].count('index')['name']
    car2 = lst[(lst.transportation=='自行前往') | (lst.transportation=='自行開車')].count('index')['name']
    day1A = lst[((lst.daystype=='星期六') | (lst.daystype=='二天')) & (lst.food=='葷')].count('index')['name']
    day1B = lst[((lst.daystype=='星期六') | (lst.daystype=='二天')) & (lst.food=='素')].count('index')['name']
    day2A = lst[((lst.daystype=='星期日') | (lst.daystype=='二天')) & (lst.food=='葷')].count('index')['name']
    day2B = lst[((lst.daystype=='星期日') | (lst.daystype=='二天')) & (lst.food=='素')].count('index')['name']
    day1A = lst[((lst.daystype=='星期六') | (lst.daystype=='二天')) & (lst.food=='葷')].count('index')['name']
    day1B = lst[((lst.daystype=='星期六') | (lst.daystype=='二天')) & (lst.food=='素')].count('index')['name']
    day2A = lst[((lst.daystype=='星期日') | (lst.daystype=='二天')) & (lst.food=='葷')].count('index')['name']
    day2B = lst[((lst.daystype=='星期日') | (lst.daystype=='二天')) & (lst.food=='素')].count('index')['name']
    return (
        cfg['title'] + '\n' +
        '<人數資訊>\n'+
        '新義工 {0}人 舊義工 {1}人 共計{2}人\n'.format(newcnt,oldcnt,newcnt+oldcnt) +
        '<交通資訊>\n'+
        '{0} {1}人\n'.format(cfg['cartype'],car1) +
        '自行前往 {0}人\n'.format(car2) +
        '<住宿資訊>\n'+
        '男{0}人,女{1}人,共{2}人\n'.format(bed1,bed2,bed1+bed2) +
        '<餐飲資訊>\n'+
        '星期六 葷食{0}人,素食{1}人,共計{2}人\n'.format(day1A,day1B,day1A+day1B) +
        '星期日 葷食{0}人,素食{1}人,共計{2}人\n'.format(day2A,day2B,day2A+day2B)
    )

def get_avaliable_drivers(lst):
    tmp= lst[lst.driver=='是']
    tmp = tmp[['name','phone','transportation','daystype']]
    return tmp

def get_avaliable_sergeants(lst):
    tmp = lst[lst.transportation=='台電']
    tmp = tmp[['name','phone','transportation','daystype']]
    return tmp

def get_transport_locations(lst):
    cfg = load_dict()
    locs = load_locations()
    locs = locs.rename(index=str, columns={'loc':'transportation'})
    locs = locs[locs.transportation=='休息']
    locs = locs[['transportation','loc_addr','loc_seq']]
    locs['date']=cfg['source_date']
    locs['time']=cfg['source_time']
    
    target = pd.DataFrame(
        [[cfg['target'],cfg['target_addr'],cfg['target_date'],cfg['target_time'],99]],
        columns=['transportation','loc_addr','date','time','loc_seq']
    )
    
    tmp= lst[(lst.transportation!='自行前往') & (lst.transportation!='自行開車')]
    tmp = tmp[['transportation','loc_addr','loc_seq']].copy().drop_duplicates()
    tmp['date']=cfg['source_date']
    tmp['time']=cfg['source_time']
    tmp = tmp.append(locs)
    tmp = tmp.append(target)
    tmp = tmp.sort_values(by='loc_seq')
    tmp.index = np.arange(1, len(tmp) + 1)
    tmp = tmp[['transportation','loc_addr','date','time']]
    return tmp

def calcuate_fees(lst,transport_locations,drivers,sergeants):
    cfg = load_dict()
    lst['transport$'] = np.where(lst['car']==cfg['cartype'],cfg['transport_fee'],0)
    lst['food$'] = lst['days']*cfg['food_fee']
    lst['bed$'] = np.where(lst['days']==2,cfg['bed_fee']*lst['bedrequired'],0)
    lst['insurance$'] = np.where(lst['insurance']=='是',0,cfg['insurance_fee'])
    lst['total$'] = lst['transport$']+lst['food$']+lst['bed$']+lst['insurance$']
    lst = lst.merge(transport_locations, left_on='transportation', right_on='transportation', how='left')
    lst = lst[['name','phone','sex','food','daystype','transportation','time','loc_addr_x','car','days','food$','bed$','insurance$','transport$','total$','isnew','birthday','id']].copy()
    return lst

def generate_going_report(lst):
    tmp = lst[['name','phone','sex','food','daystype','transportation','car','transport$','food$','bed$','insurance$','total$','isnew']]
    tmp = tmp.rename(index=str, columns={
        'isnew': '新義工註記',
        'transportation':'站點',
        'name':'姓名',
        'phone':'電話',
        'sex':'性別',
        'daystype':'參加',
        'food':'飲食',
        'transport$':'交通費',
        'food$':'餐費',
        'bed$':'住宿費',
        'insurance$':'保險',
        'car':'備註',
        'total$':'總計'})
    #tmp.to_csv('出團名單.csv')
    return tmp

def generate_transport_report(lst):
    tmp= lst[(lst.transportation!='自行前往') & (lst.transportation!='自行開車')]
    tmp.index = np.arange(1, len(tmp) + 1)
    tmp = tmp[['isnew','time','transportation','loc_addr_x','name','phone']]
    tmp = tmp.rename(index=str, columns={
        'isnew': '新義工註記', 
        'time': '發車時間',
        'transportation':'站點',
        'loc_addr_x':'地址',
        'name':'姓名',
        'phone':'電話'})
    #tmp.to_csv('搭車名單.csv')
    return tmp
    
def generate_post_report(lst):
    cfg = load_dict()
    #tmp = lst[['time','transportation','loc_addr_x']].copy().drop_duplicates();
    print(cfg['msg1'].format(cartype=cfg['cartype']))
    for index, row in lst.iterrows():
        print("{0} {1} {2}".format(row['time'], row['transportation'],row['loc_addr']))
    print(cfg['msg2'].format(smsdate=cfg['smsdate']))

def generate_transport_locations_report(lst):
    lst = lst.rename(index=str, columns={'time': '發車時間','transportation':'站點','loc_addr':'地址'})
    #lst.to_csv('發車時刻表.csv')
    return lst

def generate_new_member_report(lst):
    tmp= lst[lst.isnew=='*']
    tmp.index = np.arange(1, len(tmp) + 1)
    tmp = tmp[['name','phone','birthday','id']]
    tmp = tmp.rename(index=str, columns={'name':'姓名','phone':'電話','birthday':'生日','id':'身分證字號'})
    #tmp.to_csv('新義工名單.csv')
    return tmp

def generate_sms_report(lst):
    cfg = load_dict()
    loc = ''
    tmp = lst[(lst.transportation!='自行前往') & (lst.transportation!='自行開車')]
    for index, row in tmp.iterrows():
        if loc != row['transportation']:
            loc = row['transportation']
            print(cfg['msg3'].format(
                time=row['time'],
                date=cfg['smsdate'],
                transportation=row['transportation'],
                loc_addr=row['loc_addr_x']))
        print(row['phone'])

