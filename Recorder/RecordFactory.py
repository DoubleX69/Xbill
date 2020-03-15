from typing import Union

from Recorder.AlipayRecorder import AlipayRecorder
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


def get_recorder(file_path) -> Union[AlipayRecorder, None]:
    if is_alipay_file(file_path):
        print("Read Alipay Records")
        return AlipayRecorder(file_path)

    else:
        print("Read Unknown Records")
        return None
