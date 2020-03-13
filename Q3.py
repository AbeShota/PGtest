import re
import glob
from natsort import natsorted
import datetime


each_time_result = {'00': 0, '01': 0,'02': 0, '03': 0, '04': 0,'05': 0, '06': 0, '07': 0,'08': 0, '09': 0, '10': 0,'11': 0, '12': 0,'13': 0, '14': 0,'15': 0, '16': 0,'17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0,'23': 0} # 各時間帯毎のアクセス件数を格納するための辞書
remote_host_result = {} # リモートホスト別のアクセス件数を格納するための辞書
month_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12} # 月を英語表記から数字表記へ変換するための辞書

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

# 日付の妥当性をチェックする関数
def CheckDate(year,month,day):
    try:
        newDataStr="%04d/%02d/%02d"%(year,month,day)
        newDate=datetime.datetime.strptime(newDataStr,"%Y/%m/%d")
        return True
    except ValueError:
        return False


# 期間指定をするかどうかの決定
while True:
    period_opt = input("期間の指定をしますか？Y/N：")
    if period_opt == 'Y' or period_opt == 'N':
        print(period_opt)
        break
    else:
        print("不適切な値です")

# 期間指定
if period_opt == 'Y':
    print("期間の指定をします")
    print("期間開始の日付を入力してください")
    # 開始年（4桁までの整数）
    while True:
        y_start = input("開始の年は？（4桁までの整数を入力）：")
        if y_start.isdigit and int(y_start) < 10000:
            #print("開始年入力完了")
            break
        else:
            print("不適切な値です")
    # 開始月（1～12の整数）
    while True:
        m_start = input("開始の月は？（1～12の整数を入力）：")
        if m_start.isdigit and 0 < int(m_start) < 13:
            #print("開始月入力完了")
            break
        else:
            print("不適切な値です")
    # 開始日（1～31の整数）
    while True:
        d_start = input("開始の日は？（1～31の整数を入力）：")
        if d_start.isdigit and 0 < int(d_start) < 32 and CheckDate(int(y_start), int(m_start), int(d_start)) == True:
            #print("開始日入力完了")
            break
        else:
            print("不適切な値です")
    print("開始の日付：", y_start, "年", m_start, "月", d_start, "日")
    print("")
    date_start = datetime.datetime(int(y_start), int(m_start), int(d_start))

    print("期間終了の日付を入力してください")
    # 終了年（4桁までの整数）
    while True:
        y_end = input("終了の年は？（4桁までの整数を入力）：")
        if y_end.isdigit and int(y_end) < 10000 and int(y_start) <= int(y_end):
            #print("終了年入力完了")
            break
        else:
            print("不適切な値です")
    # 終了月（1～12の整数）
    while True:
        m_end = input("終了の月は？（1～12の整数を入力）：")
        if m_end.isdigit and 0 < int(m_end) < 13 and 0 <= (datetime.datetime(int(y_end), int(m_end), 1) - datetime.datetime(int(y_start), int(m_start), 1)).days:
            #print("終了月入力完了")
            break
        else:
            print("不適切な値です")
    # 終了日（1～31の整数）
    while True:
        d_end = input("終了の日は？（1～31の整数を入力）：")
        if d_end.isdigit and 0 < int(d_end) < 32 and CheckDate(int(y_end), int(m_end), int(d_end)) == True and 0 <= (datetime.datetime(int(y_end), int(m_end), int(d_end)) - datetime.datetime(int(y_start), int(m_start), int(d_start))).days:
            #print("終了日入力完了")
            break
        else:
            print("不適切な値です")
    print("終了の日付：", y_end, "年", m_end, "月", d_end, "日")
    print("")
    date_end = datetime.datetime(int(y_end), int(m_end), int(d_end))



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
            if period_opt == 'Y': # 期間指定された場合実行
                if (date_start <= datetime.datetime(int(year), month_dict[month], int(day)) <= date_end) == True:
                    each_time_result[str(hour)] += 1
            else: # 期間指定されていない場合実行
                each_time_result[str(hour)] += 1

        # リモートホスト別のアクセス件数の計算
        host_result = host_pattern.search(log) # リモートホスト名の取得
        if host_result is not None:
            remote_host_name = host_result.group(0)
            #print(remote_host_name)
            if period_opt == 'Y': # 期間指定された場合実行
                if (date_start <= datetime.datetime(int(year), month_dict[month], int(day)) <= date_end) == True:
                    if remote_host_name in remote_host_result:
                        remote_host_result[remote_host_name] += 1
                    else:
                        remote_host_result[remote_host_name] = 1
            else: # 期間指定されていない場合実行
                if remote_host_name in remote_host_result:
                    remote_host_result[remote_host_name] += 1
                else:
                    remote_host_result[remote_host_name] = 1


EachTimeOut(each_time_result)
RemoteHostOut(remote_host_result)
