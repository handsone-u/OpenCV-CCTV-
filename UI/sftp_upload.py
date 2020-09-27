import paramiko
import os
import glob
import pandas as pd
import datetime


# Open a transport
#host = "14.36.195.51"
host = "192.168.20.54"
port = 22
transport = paramiko.Transport((host, port))
# Auth
password = "dlaghrl0921"
username = "hogi"
transport.connect(username=username, password=password)

# Go!
sftp = paramiko.SFTPClient.from_transport(transport)

class server_db():
    def __init__(self):
        self.local_path = './csvfile/'
        self.cctv_df =  pd.DataFrame(columns=['X1 axis','Y1 axis','CCTV IP Address'])
        self.person_df = pd.DataFrame(columns=['name', 'face_id', 'path'])
        self.log_df = pd.DataFrame(columns=['name', 'face_id', 'path', 'Time','CCTV IP Address','reco_path'])
        self.persondata_df = pd.read_csv("./csvfile/persondata.csv", index_col=0)

    def upload_file(self,local_path,what):
        # Upload
        csv_path = '/home/hogi/hdd/csvfile/'
        img_path = "/home/hogi/hdd/faceimg/"
        mp4_path = "/home/hogi/hdd/test/"

        self.local_path = local_path

        if what == "csv":
            path = csv_path
        elif what == "img":
            path = img_path
        elif what == "mp4":
            path = mp4_path

        local_list = os.listdir(self.local_path)
        #print(local_list)
        if what == "csv":
            local_file_extension_list = [self.local_path+file for file in local_list if file.endswith(".csv")]
            server_file_extension_list = [path+file for file in local_list if file.endswith(".csv")]
        elif what == "img":
            local_file_extension_list = [self.local_path + file for file in local_list if file.endswith(".jpg")]
            server_file_extension_list = [path + file for file in local_list if file.endswith(".jpg")]
        elif what == "mp4":
            local_file_extension_list = [self.local_path + file for file in local_list if file.endswith(".mp4")]
            server_file_extension_list = [path + file for file in local_list if file.endswith(".mp4")]

        #print(local_file_extension_list)
        #print(server_file_extension_list)
        # Upload
        for i in range(len(local_file_extension_list)):
            sftp.put(local_file_extension_list[i], server_file_extension_list[i])

        #return server_file_extension_list

    def download_file(self,local_path,what):
        csv_path = "/home/hogi/hdd/csvfile/"
        img_path = "/home/hogi/hdd/faceimg/"
        mp4_path = "/home/hogi/hdd/test/"

        self.local_path = local_path

        if what == "csv":
            path = csv_path
        elif what == "img":
            path = img_path
        elif what == "mp4":
            path = mp4_path

        cli = paramiko.SSHClient()
        cli.set_missing_host_key_policy((paramiko.AutoAddPolicy))
        cli.connect(host, port=port, username=username, password=password)
        if what == "csv":
            stdin, stdout, stderr = cli.exec_command("cd " + path + " && ls *.csv")
        elif what == "img":
            stdin, stdout, stderr = cli.exec_command("cd " + path + " && ls *.jpg")
        elif what == "mp4":
            stdin, stdout, stderr = cli.exec_command("cd " + path + " && ls *.mp4")

        lines = stdout.readlines()
        lines = [line.rstrip() for line in lines] #"\n" 없애는 코드
        print(lines)
        server_file_extension_list = [path+file for file in lines]
        local_file_extension_list = [self.local_path+file for file in lines]
        print(server_file_extension_list)
        print(local_file_extension_list)

        for i in range(len(server_file_extension_list)):
            sftp.get(server_file_extension_list[i],local_file_extension_list[i])

        return local_file_extension_list

    def renewal_df(self):
        local_list_csv = self.download_file('./csvfile/','csv')
        self.cctv_df = pd.read_csv(local_list_csv[0])
        self.log_df = pd.read_csv(local_list_csv[1])
        #self.persondata_df = pd.read_csv(local_list_csv[2])
        self.person_df = pd.read_csv(local_list_csv[3])
        self.persondata_df = pd.read_csv("./csvfile/persondata.csv", index_col=0)

        #print(self.cctv_df)
        #print(self.log_df)
        #print(self.person_df)
        #print(self.persondata_df)


    #옷색깔 넣음

#s = server_db()
#s.upload_file('C:/Users/user/Pycharm/venv/pract/csvfile/')
#s.download_file('C:/Users/user/Pycharm/venv/pract/csvfile/')

#s.download_file('./csvfile/','csv')
#s.upload_file('./csvfile/','csv')
#print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
#s.logging("df674251-dede-4204-9e31-5e9d31a56cc6","255.255.255.255")
#s.download_file('C:/Users/user/Pycharm/venv/pract/imgfile/')
#s.found_delete("df674251-dede-4204-9e31-5e9d31a56cc6")

# Close
#sftp.close()
#transport.close()

