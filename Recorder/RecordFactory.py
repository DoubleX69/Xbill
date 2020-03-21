from typing import Union

from Recorder.AlipayRecorder import AlipayRecorder

from Recorder.ICBCRecorder import ICBCRecorder
import csv


def is_alipay_file(file_path) -> bool:
    is_alipay = False
    try:
        with open(file_path, encoding='GBK') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if '支付宝交易记录明细查询' in row:
                    is_alipay = True
    except UnicodeDecodeError:
        is_alipay = False
    return is_alipay


def is_icbc_file(file_path) -> bool:
    is_icbc = False
    try:
        with open(file_path, encoding='UTF-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                for val in row:
                    if '明细查询文件下载' in val:
                        is_icbc = True
    except UnicodeDecodeError:
        is_icbc = False
    return is_icbc


def get_recorder(file_path) -> Union[AlipayRecorder, ICBCRecorder, None]:
    if is_alipay_file(file_path):
        print("Read Alipay Records")
        return AlipayRecorder(file_path)
    elif is_icbc_file(file_path):
        print("Read ICBC Records")
        return ICBCRecorder(file_path)
    else:
        print("Read Unknown Records")
        return None
