한이음 프로젝트 Git

1. Repository의 구성 
- 각각의 인원에게 Branch 할당
- 기본은 Master Branch를 기준으로함. 


2. 작업 기초 
- 코드에 수정을 가한경우 Comment로 남겨주세요. 
- Merge Request에도 Comment를 남겨주세요. 기록이 남아야함.   
  
3. 코드설명  
- sftp_upload.py 내에 server_db class  
    def __init__(self) : upload_file, download_file 작업을 위해서 필요한  
                         self.local_path (저장할 로컬파일경로) 와  
                         self.cctv_df (cctv목록, 실종자목록, log목록 type: dataframe)  
                         self.person_df  
                         self.log_df를 선언한다.  

    def upload_file(self,local_path) : 로컬파일경로를 parameter로 받아온 후, 그 경로에 있는 file(확장자 : .csv, .jpg)를 서버파일(csv는 csv_path, jpg는 img_path)에 저장한다.  
    def download_file(self,local_path) : 로컬파일경로를 parameter로 받아온 후, 서버파일(csv는 csv_path, jpg는 img_path)에서 local_path로 저장한다.  
    def renewal_df(self) : 서버에서 갱신된 csv파일들을 download_file()함수로 로컬파일에 갱신하고, dataframe에 저장한다.  
    def logging(self, persisted_face_id, ip_address) : parameter로 persisted_face_id(face API 결과값), ip_address(실종자가 발견된 cctv의 ip주소)를 받아온다.  
                                                       person_df에 등록되어있는 실종자들의 'face_id' column의 row들을 비교하고 , 일치하면 log에   
                                                       person_df에 있는 name, face_id, path, Time과 cctv_df에 있는 CCTV IP Address의 row값들을 log_file.csv에 저장한다.  
  


- main_ui.py 내에 MainUI class  

