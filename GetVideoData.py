###################################################################################
#               Enter Login Detials Below in the quotations                       #
###################################################################################
username=''
passwd=''
###################################################################################
#             If you have 2fa on your account leave the below as y                #
#               If not using 2fa change the 'y' to 'n'                            #
###################################################################################

tfa_check='y'

###################################################################################
#              Enter your 2fa authenication key Below inside the quotations       #
#               NOTE: This code is used to generate the 2fa key                   #
#               Anyone with access to your system can generate a new 2fa code     #
#                   Do not run this script on a shared computer!                  #
###################################################################################

tfa=''

###################################################################################
#                   The Blow detemins if a browser window will open               #
#                    Set the value to True to hide the browser                    #
#                      Set the value to False to show the browser                 #
#                       Be sure to capitalize the first letter                    #
#                       Defualt is to hide the browser                            #
###################################################################################

hide_browser=True
###################################################################################
#               Enter The Path To The FireFox Geko Driver in the Quotes           #
###################################################################################

geko=''
###################################################################################
#               Editing Below This Point May Break The Script                     #
###################################################################################
import pyotp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta, date
import requests
import sqlite3
from sqlite3 import Error
import time
headOption = webdriver.FirefoxOptions()
headOption.headless=hide_browser
def create_connection():
    conn = None
    try:
        conn =sqlite3.connect('vid_analytics.db')
        print(sqlite3.version)
        c = conn.cursor()
        return conn,c
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def get_video_data():
    bot = webdriver.Firefox(options=headOption,executable_path=geko,service_log_path="geckodriver.log")
    site_name="Manyvids"
    url=bot.get('https://www.manyvids.com/Login/')    
    time.sleep(3)
    print('waiting for login page to load')
    email= bot.find_element(By.ID,'triggerUsername')
    password = bot.find_element(By.ID,'triggerPassword')
    email.clear()
    password.clear()
    email.send_keys(username)
    password.send_keys(passwd)
    time.sleep(1)
    password.send_keys(Keys.RETURN)
    if tfa_check == 'y':
        time.sleep(4)
        totp = pyotp.TOTP(tfa)
        bot.find_element_by_xpath('//*[@id="LoginSignupModal"]/div[5]/form/div[1]/input').send_keys(totp.now())
        bot.find_element_by_xpath('//*[@id="LoginSignupModal"]/div[5]/form/div[2]/a[2]').click()
    time.sleep(10)
    url='https://www.manyvids.com/MV-Content-Manager/'
    bot.get(url)
    time.sleep(30)
    try:
        if bot.find_element(By.CLASS_NAME,value='js-cancel-announcement'):
            bot.find_element(By.CLASS_NAME,value='js-cancel-announcement').click()
        else:
            print('No Banner Found')
    except:
        pass
    
    while url != url:
        bot.get(url)
    content_list=bot.find_elements_by_class_name('manage-content__list-item')
    i=0
    videos=[]
    titles=[]
    last_page='f'
    print('Getting video data')
    while last_page=='f':
        try:
            containers=bot.find_elements_by_class_name('manage-content__list-item')
            video_titles=bot.find_elements_by_class_name('manage-content__list-item__title')
            video_views=bot.find_elements_by_class_name('manage-content__list-item__label--views')
            video_sales=bot.find_elements_by_class_name('manage-content__list-item__label--sales-count')
            video_likes=bot.find_elements_by_class_name('manage-content__list-item__label--likes')
            video_earnings=bot.find_elements_by_class_name('manage-content__list-item__label--earned')   
            today_date=date.today()-timedelta(days=1)
            today_date=today_date.strftime("%d/%m/%Y")
            for item in containers:
                vt=video_titles[i].text
                titles.append(vt)
                insert_data=('Manyvids',today_date,video_titles[i].text,video_likes[i].text,video_views[i].text,video_sales[i].text,video_earnings[i].text)
                print(insert_data)
                videos.append(insert_data)
                i+=1
            c = 0
            try:
                time.sleep(3)
                print('looking for next button')
                bot.find_element_by_xpath('/html/body/div[3]/div/div/ul/li[5]/a').click()
                print('loading next page')
                i=0
                time.sleep(2)            
            except:
                print('on last page')
                last_page='t'
                print('there are ',len(videos),' that were scanned')
                time.sleep(10)
            
        except:
            print('error')
            break
    try:
        conn =sqlite3.connect('vid_analytics.db')
        #print(sqlite3.version)
        c = conn.cursor()
    except conn.Error as e:
        print(e)
        exit()
    total_titles=len(titles)
    ntl=[]
    for title in titles:
        rtitle = title.replace(' ','_')
        ot=rtitle.replace('-','')
        rc=ot.replace(',','_')
        nt=rc.replace("'","")
        ntl.append(nt)
        print(nt)
    completed=[]
    b=0
    bot.close()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print('sql executed')
    rows = c.fetchall()
    for vid_data in videos:
        if len(videos) > len(rows):
            try:
                c.execute("CREATE TABLE IF NOT EXISTS"+' '+ntl[b]+' '+'''([id] INTEGER PRIMARY KEY,[site_name] TEXT NOT NULL,[date] TEXT NOT NULL UNIQUE,[video_title]TEXT NOT NULL,[views] INTEGER NOT NULL,[likes] INTEGER NOT NULL,[review_score] REAL,[sold]INTEGER,[earned]INTEGER)''')
                print('table ', ntl[b], ' created')
            except error as e:
                print(e)
            completed.append(title)
            print('added ',b,' of ', len(titles))
            time.sleep(3)
            print(ntl[b])
        try:
            sql = ''' INSERT INTO'''+' '+ntl[b]+' '+'''(site_name,date,video_title,likes,views,sold,earned)
                            VALUES(?,?,?,?,?,?,?) '''
            c.execute(sql, vid_data)
            conn.commit()
            print('video written to db')
        except:
            print('Could not add data to database')
        b+=1
if __name__=='__main__':
    create_connection()
    get_video_data()