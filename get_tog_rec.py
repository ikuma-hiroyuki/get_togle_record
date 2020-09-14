import datetime as dt
import json
import os
from datetime import timedelta
import requests


def getTogglCsvString(startdate, worker):
    """
    toggl apiから詳細データを取得してCSV出力する。
    取得範囲は 実行日-7>= and <=実行日
    """
    endDay = startdate + timedelta(days=6)
    headers = {'content-type': 'application/json'}
    params = {
        'user_agent': worker.user_agent,
        'workspace_id': worker.workspace_id,
        'since': startdate,
        'until': endDay,
    }
    auth = requests.auth.HTTPBasicAuth(worker.api_token, 'api_token')

    api_data = requests.get('https://toggl.com/reports/api/v2/details.csv',
                            auth=auth, headers=headers, params=params)
    api_data.encoding = "UTF-8"

    # CSVファイルで出力
    me_path = os.path.dirname(os.path.abspath(__file__))
    savePath = me_path + "/" + \
        worker.name + "_" + \
        startdate.strftime("%Y%m%d") + \
        "to" + endDay.strftime("%Y%m%d") + ".csv"

    with open(savePath, mode="w", encoding='utf-8') as f:
        f.write(api_data.text)
        print(api_data.text)


class Worker():
    def __init__(self, name, mail, workspace_id, api_token):
        self.name = name
        self.user_agent = mail
        self.workspace_id = str(int(workspace_id))
        self.api_token = api_token


# 設定ファイルを参照してtogglデータを取得
dstr = input("指定日から一週間の履歴を取得します。(基本的に月曜日を指定すること)。\n")
startdate = dt.datetime.strptime(dstr, '%Y/%m/%d')

me_path = os.path.dirname(os.path.abspath(__file__))
json_open = open(me_path + r"\toggl_id.json", "r")
json_load = json.load(json_open)

for index, row in enumerate(json_load.values()):
    print(index, row['name'])
    w = Worker(
        row["name"],
        row["email"],
        row["workspace_id"],
        row["api_token"]
    )
    getTogglCsvString(startdate, w)

input("完了")
