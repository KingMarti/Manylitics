from datetime import datetime, timedelta, date
import sqlite3
from sqlite3 import Error
import time
from operator import itemgetter
def get_connection():
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
def get_data():
    day_select=input("How many days worth of data would you like to fetch? ")
    day_select=str(int(day_select)+1)
    output=[]
    conn =sqlite3.connect('vid_analytics.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    vid_views_list=[]
    for tables in rows:
        c.execute("SELECT * FROM "+tables[0] +" ORDER BY id DESC LIMIT "+day_select)
        table_data=c.fetchall()
        vi = 0
        old_view = 0
        v_data=[]
        for data in reversed(table_data):
            video_id=data[0]
            site_name=data[1]
            data_date=data[2]
            video_title=data[3]
            view_count=data[4]
            like_count=data[5]
            review_score=data[6]
            sale_count=data[7]
            video_earnings=data[8]
            if type(view_count) == str:
                views=view_count.replace(',','')
                views=int(views)
            else:
                views=view_count
            rtitle = video_title.replace(' ','_')
            ot=rtitle.replace('-','')
            rc=ot.replace(',','_')
            db_title=rc.replace("'","")
            if db_title == tables[0]:
                if type(view_count) == str:
                    view = view_count.replace(',','')
                    view=int(view)
                else:
                    view=view_count
                view_num=views-old_view
                if view_num ==views:
                    view_num=0
                old_view=views
                if day_select =='1':
                    new_view=views
                else:
                    new_view=old_view-views
                v_data.append(view_num)
                if video_id == data[0]:
                    conversion_rate=float(round(sale_count/views*100,3))
            else:
                print(db_title, tables[0])
        for v in v_data:
            vi=vi+v
        vid_views_list.append((video_title,vi,sale_count,conversion_rate))

    insort=input('Please Enter How You Would Like The Data Sorted\n1)By Views\n2)By Sales\n3)By Conversion Rate\n')
    if insort =='1':
        sortby=1
    elif insort =='2':
        sortby=2
    elif insort =='3':
        sortby=3
    else:print('invalid selection, please restart the script')
    inord=input('How Would you like the data output?\n1)Assending Order - Highest views viable first\n2)Decesnding Order - Lowest views viable first\n')
    if inord == '1':
        order=False
    elif inord=='2':
        order=True
    else:
        print("invalid selection")
    sorted_views=sorted(vid_views_list,key=itemgetter(sortby),reverse=order)
    print('views for the last ',int(day_select)-1,' days')
    for s in sorted_views:
        print(s[0],'New Views:',s[1],' Sold:',s[2], ' Conversion Rate:',s[3],'%\n')
        
#create_connection()
if __name__=="__main__":
    get_connection()
    get_data()