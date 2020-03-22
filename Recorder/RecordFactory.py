from typing import Optional, List

from Recorder.AlipayRecorder import AlipayRecorder

from Recorder.ICBCRecorder import ICBCRecorder
import csv


def _read_csv(path, encoding_list=('GBK', 'UTF-8')) -> Optional[List]:
    for endcoding in encoding_list:
        try:
            with open(path, encoding=endcoding) as csv_file:

                reader = csv.reader(csv_file)
                return [row for row in reader if row]

        except UnicodeDecodeError:
            print("Not Support This File Encoding!!")
    return None


def save_to_db(file_path) -> str:
    rows = _read_csv(file_path)
    if rows:
        bill_type = rows[0][0].strip()
        if '明细查询文件下载' in bill_type:
            count = ICBCRecorder(rows).save()
            msg = "insert {} ICBC bills to database...".format(count)
        elif '支付宝交易记录明细查询' in bill_type:
            count = AlipayRecorder(rows).save()
            msg = "insert {} Alipay bills to database...".format(count)
        else:
            msg = "Insert Failed ! Not support file type: '{}'".format(bill_type)

        return msg
    else:
        return "Blank File!"
