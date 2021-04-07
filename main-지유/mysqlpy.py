import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import datetime

# Obtain connection string information from the portal
config = {
    'host': 'hanium-cctv-project.mysql.database.azure.com',
    'user': 'hongik1516@hanium-cctv-project',
    'password': '!hanium1234',
    'database': 'cctvproject'
}
class mysql_csv():
    def __init__(self):
        # Construct connection string
        try:
            self.conn = mysql.connector.connect(**config, allow_local_infile=True)
            print("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = self.conn.cursor()
            self.cctv_df = pd.read_csv("./csv_file.csv")
            self.person_df = pd.read_csv("./person_list.csv")
            self.log_df = pd.read_csv("./log_file.csv", encoding='utf-8')


    def export_cctv(self):
        cctv_insert = "INSERT INTO cctv (id, X1axis, Y1axis, CCTVIPAddress) VALUES(%s,%s,%s,%s)"
        cctv_table_drop = "DROP TABLE IF EXISTS cctv;"
        cctv_create_table = "CREATE TABLE cctv(id int(4), X1axis int(4), Y1axis int(4), CCTVIPAddress char(50), PRIMARY KEY (id));"

        self.cursor.execute(cctv_table_drop)
        self.cursor.execute(cctv_create_table)
        for i in range(len(self.cctv_df)):
            x,y,ip = self.cctv_df.iloc[i,0:3]
            print(x,y,ip)
            self.cursor.execute(cctv_insert, (int(i+1),int(x),int(y),str(ip)))
            self.conn.commit()


    def import_cctv(self):
        sql2 = "SELECT * FROM cctv"
        self.cursor.execute(sql2)
        result = self.cursor.fetchall()

        #store
        cctv_temp = pd.DataFrame(result, columns=['id','X1 axis','Y1 axis','CCTV IP Address'])
        self.cctv_df = cctv_temp.iloc[:,1:4].copy(deep=True)
        print(self.cctv_df)
        self.cctv_df.to_csv('./csv_file.csv', index=False, columns=['X1 axis','Y1 axis','CCTV IP Address'])

    def export_person(self):
        person_insert = "INSERT INTO person (name, face_id, path) VALUES(%s,%s,%s)"
        person_table_drop = "DROP TABLE IF EXISTS person;"
        person_create_table = "CREATE TABLE person(name char(20), face_id char(40), path char(40));"

        self.cursor.execute(person_table_drop)
        self.cursor.execute(person_create_table)
        for i in range(len(self.person_df)):
            na, fa, pa = self.person_df.iloc[i, 0:3]
            print(na, fa, pa)
            self.cursor.execute(person_insert, (str(na), str(fa), str(pa)))
            self.conn.commit()

    def import_person(self):
        sql2 = "SELECT * FROM person"
        self.cursor.execute(sql2)
        result = self.cursor.fetchall()

        # store
        person_temp = pd.DataFrame(result, columns=['name', 'face_id', 'path'])
        self.person_df = person_temp.iloc[:, 0:3].copy(deep=True)
        print(self.person_df)
        self.person_df.to_csv('./person_list.csv', index=False, columns=['name', 'face_id', 'path'])

    def logging(self,persisted_face_id, ip_address):
        # df1은 설정값을 읽어와야함. 안찾는 친구는 굳이 반복문 돌릴 필요 없으니까
        detected_df = self.person_df.loc[self.person_df['face_id'] == persisted_face_id]
        print(detected_df)

        if (detected_df.empty):
            print("그런사람 없어요.")
        elif (detected_df.empty == False):
            persist_cctv = self.cctv_df.loc[self.cctv_df['CCTV IP Address'] == ip_address]
            list = persist_cctv['CCTV IP Address']
            temp = detected_df.copy(deep=True)
            time = datetime.datetime.now()
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            print(now)
            temp["Time"] = now
            temp["CCTV IP Address"] = list
            print(temp)
            self.log_df = self.log_df.append(temp, ignore_index=True)
            print(self.log_df)
            print("기록")
            self.log_df.to_csv('./log_file.csv', index=False, columns=['name', 'face_id', 'path', 'Time','CCTV IP Address'])
            #person.csv는 person의 row가 추가될 때, 서버에 저장하는 방법으로 할 예정.

    def export_log(self):
        log_table_drop = "DROP TABLE IF EXISTS log;"
        log_create_table = "CREATE TABLE log (name char(20), face_id char(40), path char(40), Time  char(21),  CCTVIPAddress char(50));"
        log_insert = "INSERT INTO log (name, face_id, path, Time,  CCTVIPAddress) VALUES(%s,%s,%s,%s,%s)"

        self.cursor.execute(log_table_drop)
        self.cursor.execute(log_create_table)
        for i in range(len(self.log_df)):
            na, fa_id, pa, ti, ad = self.log_df.iloc[i,0:5]
            print(na, fa_id, pa, ti, ad)
            self.cursor.execute(log_insert, (str(na), str(fa_id), str(pa), str(ti), str(ad)))
            self.conn.commit()

    def import_log(self):
        sql2 = "SELECT * FROM log"
        self.cursor.execute(sql2)
        result = self.cursor.fetchall()
        log_temp = pd.DataFrame(result, columns=['name', 'face_id', 'path', 'Time','CCTV IP Address'])
        self.log_df = log_temp.iloc[:, 0:5].copy(deep=True)
        print(self.log_df)
        self.log_df.to_csv('./log_file.csv', index=False, columns=['name', 'face_id', 'path', 'Time','CCTV IP Address'])



m = mysql_csv()
#m.export_person()
print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
#m.import_person()

#m.export_cctv()
#m.import_cctv()

print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
m.export_log()
m.import_log()

m.logging("df674251-dede-4204-9e31-5e9d31a56cc6","255.255.255.255")