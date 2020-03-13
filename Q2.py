import re
import glob
from natsort import natsorted


each_time_result = {'00': 0, '01': 0,'02': 0, '03': 0, '04': 0,'05': 0, '06': 0, '07': 0,'08': 0, '09': 0, '10': 0,'11': 0, '12': 0,'13': 0, '14': 0,'15': 0, '16': 0,'17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0,'23': 0} # 各時間帯毎のアクセス件数を格納するための辞書
remote_host_result = {} # リモートホスト別のアクセス件数を格納するための辞書

time_pattern = re.compile("([0-9]{1,2})/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/([0-9]{1,4}):([0-9]{2}):([0-9]{2}):([0-9]{2})")
host_pattern = re.compile("((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))")

# 各時間帯毎のアクセス件数を出力する関数
def EachTimeOut(result): 
    print("各時間帯毎のアクセス件数")
    for key, value in each_time_result.items():
        print(key, "時：", value, "件")
    print()

# リモートホスト別のアクセス件数を出力する関数
def RemoteHostOut(result):
    print("リモートホスト別のアクセス件数")
    for key, value in sorted(result.items(), key=lambda x: -x[1]):
        print(key, "：", value, "件")
    print()


log_files = glob.glob('*.log')
for i in natsorted(log_files):
    #print(i)
    for log in open(str(i), 'r'):
        #print(log)

    # 各時間帯毎のアクセス件数の計算
        time_result = time_pattern.search(log) # 日付の情報取得
        if time_result is not None:
            day, month, year, hour, minute, second = time_result.groups()
            #print(day, month, year, hour, minute, second)
            each_time_result[str(hour)] += 1

        # リモートホスト別のアクセス件数の計算
        host_result = host_pattern.search(log) # リモートホスト名の取得
        if host_result is not None:
            remote_host_name = host_result.group(0)
            #print(remote_host_name)
            if remote_host_name in remote_host_result:
                remote_host_result[remote_host_name] += 1
            else:
                remote_host_result[remote_host_name] = 1



EachTimeOut(each_time_result)
RemoteHostOut(remote_host_result)
