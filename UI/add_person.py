import pandas as pd
import os
from pandas import DataFrame as df
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, \
    OperationStatusType

from sftp_upload import server_db

s = server_db()
KEY = '6b2bfbfff8314d90a59a73bc29094cae'
ENDPOINT = 'https://project-face.cognitiveservices.azure.com/'

# 프로그램을 통해 이름이랑 저장되어있는 경로를 입력받음
# 추가버튼을 눌렀다 --> API 서버와 통신해서 face_id를 받는다. (함수호출)
class addPerson():
    def __init__(self):
        print('add person')
        global s

    def add_person_to_list(self,name, directory_path):

        global KEY
        global ENDPOINT

        print('name : ', name)
        print('directory_path', directory_path)
        s.renewal_df()
        #person_list = pd.read_csv('./csvfile/personlist.csv')
        # API에 접근하기 위해 객체를 생성함. 이 객체는 프로그램 켜지면 한 번 생성하고 안없어지게 해야함! 이건 함수 작동하는거 보여주려고 넣어놓음.
        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        # 주의! 사진은 반드시 한명만 나와있는거로만 해야함
        image_path = directory_path
        try:
            image_open = open(image_path, 'rb')
            detected_faces = face_client.face.detect_with_stream(image=image_open, return_face_id=True,
                                                             recognition_model='recognition_03')
            count = 0
            if detected_faces:
                try:
                    for face in detected_faces:
                        count = count + 1
                        print(count)
                        print(face.face_id)

                    if count == 1:
                        image_open = open(image_path, 'rb')
                        face_client.face_list.add_face_from_stream(face_list_id='test_list', image=image_open)
                        face_list = face_client.face_list.get(face_list_id='test_list')

                        size = (len(face_list.persisted_faces)) - 1
                        get_face_id = face_list.persisted_faces[size].persisted_face_id
                        print('hi')
                        # 데이터 추가 하는 곳 (간단하게 loc을 이용해 추가함))
                        temp_data = df(data={'name': [name], 'face_id': [get_face_id], 'path': [directory_path]},
                                       columns=['name', 'face_id', 'path'])
                        print(s.person_df)
                        temp_person_list = s.person_df.append(temp_data, ignore_index=True)
                        print(temp_person_list)
                        temp_person_list.to_csv("./csvfile/personlist.csv", index=False)
                        s.upload_file('./csvfile/', 'csv')


                    elif count == 0:
                        print("사진에 얼굴이 자세하지 않아요. 다시 등록해주세요")

                    elif count == 2 | count > 2:
                        print("사진에 한 명이상의 얼굴이 있습니다. 한명의 얼굴만 등록해주세요.")

                except:
                    print("API 오류")

        except: print("경로 입력 오류")


    # 이 함수 활용하기 위해서는 어떤 사람을 지울껀지 선택하면 index값 return 해주는 함수 필요함.
    def delete_person_from_list(self,index):
        global KEY
        global ENDPOINT

        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        s.renewal_df()
        df1 = pd.read_csv('./csvfile/personlist.csv')
        del_face_id = df1.loc[index, "face_id"]
        print(del_face_id)
        face_client.face_list.delete_face(face_list_id='test_list',
                                          persisted_face_id=del_face_id)
        A = face_client.face_list.get(face_list_id='test_list')
        for i in range(len(A.persisted_faces)):
            print(A.persisted_faces[i].persisted_face_id)
        df2 = df1.drop(index)
        print(df2)
        df2.to_csv("./csvfile/personlist.csv", index=False)
        s.upload_file('./csvfile/', 'csv')



