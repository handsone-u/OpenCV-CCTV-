import pandas as pd
import datetime
from sftp_upload import server_db
import threading


s = server_db()
'''
df1 = pd.read_csv('./csvfile/log_file.csv')
tmp = df1.loc[0,'Time']
tmp2 = df1.loc[20,'Time']
print(tmp)
print(tmp2)

tmp = datetime.datetime.strptime(tmp, '%Y-%m-%d %H-%M-%S')
tmp2 = datetime.datetime.strptime(tmp2, '%Y-%m-%d %H-%M-%S')

print(tmp)
print(tmp2)
print(tmp2-tmp)
Interval = datetime.timedelta(seconds=7)

wow = tmp2-tmp
if Interval == wow:
    print('wow')

df2 = pd.read_csv('./csvfile/log_file.csv')

condition1 = df1['face_id'] == df2['face_id']
print(condition1)'''
'''
def visualized_logs1(para): # parameter로 'face_id', 'Time' 정보 1행 를 담은 dataframe을 받는다.
                           # 이렇게 하면 안될 듯... para없애고
                           # df1 = log_file.csv에서 100개 행 불러오고,
                           # for j in range(len(visualized_df)):
                           #    tmp = df1[df1['face_id']==visualized_df.loc[j,'face_id]]
                           #    for i in range(len(tmp)):
                                    #visual_time = datetime.datetime.strptime(visualized_df.loc[j,'Time'], '%Y-%m-%d %H-%M-%S')
                                    #tmp_time = datetime.datetime.strptime(tmp.loc[i,'Time'], '%Y-%m-%d %H-%M-%S')
                                    #dif = tmp_time-visual_time
                                    #if Interval < dif:
                                        #visualized_df.loc[j,'Time'] = tmp.loc[i,'Time']

    #s.renewal_df()
    print(para)
    Interval = datetime.timedelta(minutes=3)    # 인터벌
    if len(visualized_df) == 0: # visualized_log 가 비어있을 경우
        real = visualized_df.append(para, ignore_index=True)
        real.to_csv('./csv/visualized_log.csv', mode='w',index=False)
    else:
        tmp_visual_df = visualized_df[visualized_df['face_id'] == para['face_id']]
        if len(tmp_visual_df) != 0:
            visual_time = datetime.datetime.strptime( tmp_visual_df.loc[0, 'Time'], '%Y-%m-%d %H-%M-%S')
            para_time = datetime.datetime.strptime(para.loc[0, 'Time'], '%Y-%m-%d %H-%M-%S')
            print(para_time-visual_time)
            dif = para_time-visual_time
            if Interval < dif:
                visualized_df.loc[visualized_df['face_id'] == para['face_id'], 'Time'] = para['Time']
                visualized_df.to_csv('./csv/visualized_log.csv', mode='w',index=False)
            else:
                print('아쉽네요')
'''
end = False
def execute_func(second=3.0):
    global end
    if end:
        return

    visualized_log2()

    threading.Timer(second, execute_func, [second]).start()

def visualized_log2():
    
    global s
    s.renewal_df()
    Interval = datetime.timedelta(minutes=3)    # 인터벌


    visualized_df = pd.read_csv('./csvfile/visualized_log.csv')
    #df1 = pd.read_csv('./csvfile/log_file.csv')
    #df1 = df1.tail(100)
    df1 = s.log_df.tail(100)

    for j in range(len(visualized_df)):
        tmp = df1[df1['face_id'] == visualized_df.loc[j, 'face_id']]
        tmp = tmp.reset_index(drop=True)
        print('tmp : ',tmp)
        for i in range(len(tmp)):
            visual_time = datetime.datetime.strptime(visualized_df.loc[j,'Time'], '%Y-%m-%d %H-%M-%S')
            print(tmp.loc[i,'Time'])
            tmp_time = datetime.datetime.strptime(tmp.loc[i,'Time'], '%Y-%m-%d %H-%M-%S')
            dif = tmp_time-visual_time
            if Interval < dif:
                visualized_df.loc[j,'Time'] = tmp.loc[i,'Time']
                print(visualized_df)
                print('tmp전체 :',tmp.loc[i,:])
            else:
                print('아쉽네요')
    visualized_df.to_csv('./csvfile/visualized_log.csv', mode='w', index=False)
    s.upload_file('./csvfile/','csv')

execute_func(3.0)
#2가 더 좋음

