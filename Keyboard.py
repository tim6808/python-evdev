# by Tim Hong 201811
# this project is for R-pi zero with a number keyboard, and this project will settup at a store,
# when Cashier finish checkout they can samply key the corresponding button, to record customer's age gen tpye...
 

from evdev import InputDevice, categorize, ecodes
import evdev
import pandas as pd
import pymysql
import pymysql.cursors
import datetime
import time
from sqlalchemy import create_engine


sql_tf = False

columns = ['id','GMT_TIME','AGE','GEN','TYPE']
df_ = pd.DataFrame(columns=columns)

age=""
gen=""
type=""
st=""
df_.loc[0]=[1,st,age,gen,type]

def makeList(age_,gen_,type_):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #print(st)
    df_['GMT_TIME'][0] = st
    df_['AGE'][0] = age_
    df_['GEN'][0] = gen_
    print(df_)

def setupType(type_):
    df_['TYPE'][0] = type_
    print(df_)

# put df data to mysql
def toSQL():
    print("tosql")
    
    #engine =create_engine('mysql+pymysql://root:1qaz2wsx@35.201.175.100:3306/LIVINGLAB?charset=utf8', encoding='utf-8', max_overflow=5)
    
    df_.to_sql('customer_type', engine, if_exists='append')
    print(df_)
    df_.loc[0]=[1,st,age,gen,type]
    print('tosql')
    print(df_)
    
    
dev = InputDevice('/dev/input/event0')

print(dev)
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)
    
for event in dev.read_loop():
   # print(event)
   # print(event.type)
   # print('----')
   # PLEASE check your event.code to know what key is it.
    if event.type == ecodes.EV_KEY:
      #  print(categorize(event))
        #print(type(categorize(event)))
        #print(event.code)
        if event.code == 82:
            #print('60up')
            #print(event.code)
            makeList('60up','M','')
        elif event.code == 11:
            makeList('60up','W','')
        elif event.code == 79:
            makeList('46-55','M','')
        elif event.code == 80:
            makeList('46-55','W','')
        elif event.code == 75:
            makeList('36-45','M','')
        elif event.code == 76:
            makeList('36-45','W','')
        elif event.code == 71:
            makeList('26-35','M','')
        elif event.code == 72:
            makeList('26-35','W','')      
        elif event.code == 69:
            makeList('18-25','M','')
        elif event.code == 98:
            makeList('18-25','W','')
        elif event.code == 55:
            setupType('foreign')
        elif event.code == 73:
            setupType('with_kid')
        elif event.code == 77:
            setupType('office_worker')
        elif event.code == 81:
            setupType('student')
        elif event.code == 96:
            if sql_tf == False:
                toSQL()
                sql_tf = True
            else:
                sql_tf = False
        else:
            print('other')
        
        #print(categorize(event)[0])
        
        

#import evdev
#devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

#for device in devices:
#    print(device.path, device.name, device.phys)

