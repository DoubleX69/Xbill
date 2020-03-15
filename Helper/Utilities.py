from datetime import datetime
import csv


def str_to_datetime(str):
    t = datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    return t


def str_to_date(str):
    d = datetime.strptime(str, '%Y-%m-%d')
    return d


def date_to_str(t):
    s = datetime.strftime(t, "%m-%d %A")

    s = s.replace('Monday', '星期一')
    s = s.replace('Tuesday', '星期二')
    s = s.replace('Wednesday', '星期三')
    s = s.replace('Thursday', '星期四')
    s = s.replace('Friday', '星期五')
    s = s.replace('Saturday', '星期六')
    s = s.replace('Sunday', '星期日')
    return s
