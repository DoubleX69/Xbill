from typing import Optional, List

from Recorder.AlipayRecorder import AlipayRecorder
from Recorder.WeChatRecorder import WeChatRecorder
from Recorder.ICBCRecorder import ICBCRecorder
import csv


def _read_csv(path, encoding_list=('GBK', 'UTF-8', 'GB18030')) -> Optional[List]:
    for endcoding in encoding_list:
        try:
            print("encoding ", endcoding)
            with open(path, encoding=endcoding) as csv_file:

                reader = csv.reader(csv_file)
                return [row for row in reader if row]

        except UnicodeDecodeError:
            print("Not Support This File Encoding!!")
    return None


def dispatch(rows):
    bill_type = rows[0][0].strip()
    if '明细查询文件下载' in bill_type:
        return ICBCRecorder(rows)
    elif '支付宝交易记录明细查询' in bill_type:
        return AlipayRecorder(rows)
    elif '微信支付账单明细' in bill_type:
        return WeChatRecorder(rows)
    else:
        return None


def save_to_db(file_path) -> str:
    rows = _read_csv(file_path)
    if rows:
        recorder = dispatch(rows)
        if recorder is not None:
            count = recorder.save()
            msg = "insert {} {} bills to database...".format(count, recorder.get_model_name())
        else:
            msg = "Insert Failed ! Not support file type: '{}'".format(rows[0][0].strip())
        return msg
    else:
        return "Blank File!"
