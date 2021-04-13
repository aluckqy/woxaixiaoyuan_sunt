import json
import logging
import requests, time, random
import datetime

class Xiao:
    def __init__(self):
        # Token 列表
        # 修改1
        self.tokenArray = ["c1761837-895e-4793-aca6-b391baa0af5b"] #你的token值
        # 修改2
        self.tokenName = ["Luckqy"] #你的昵称

        # 喵提醒通知
        # 修改3
        self.notifytoken = '999999' #提醒token值
        self.api = "https://student.wozaixiaoyuan.com/heat/save.json"
        self.headers = {
            "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Referer": "https://servicewechat.com/wxce6d08f781975d91/147/page-frame.html",
            "token": "",
            "Content-Length": "360",
        }
        # 修改4
        self.data = {
            "answers": '["0","0"]',
            "seq": self.get_seq(),
            "temperature": self.get_random_temprature(),
            "latitude": "33.0726212841", # 维度
            "longitude": "107.0616988312", # 经度
            "country": "中国",
            "city": "汉中市",
            "district": "汉台区",
            "province": "陕西省",
            "township": "东关街道",
            "street": "东一环路",
        }

    # 获取随机体温
    def get_random_temprature(self):
        random.seed(time.ctime())
        return "{:.1f}".format(random.uniform(36.0, 36.5))

    # seq的1,2代表着早，中
    def get_seq(self):
        current_hour = datetime.datetime.now()
        current_hour = current_hour.hour + 8
        if 0 <= current_hour <= 9:
            return "1"
        elif 12 <= current_hour < 15:
            return "2"
        else:
            return 1


    def run(self):
        num = 0
        for i in self.tokenArray:
            self.headers["token"] = i
            res = requests.post(self.api, headers=self.headers, data=self.data, ).json()
            time.sleep(1)
            mtime = datetime.datetime.now().replace(microsecond=0)  #签到时间
            msgtime= (mtime + datetime.timedelta(hours=8))
            print(res)
            print(msgtime)
            if (self.data["seq"] == 1):
                    judgment = "晨检"
            else:
                    judgment = "午检"

            if (res['code'] == 0):
                res = "成功,期待下一次成功"
            elif (res['code'] == 1):
                res = "失败,打卡时间已结束"
            elif (res['code'] == -10):
                res = "失败。当前token：" + self.headers["token"] + "失效！\n请自行手动打卡并联系管理员！！！"
            else:
                res = "失败，原因未知。\n请自行手动打卡并联系管理员！！！"

            msg = {
                "id": self.notifytoken,
                "text": "亲爱的" + self.tokenName[num] + "：\n您的" + judgment + "打卡:\n" + json.dumps(res, ensure_ascii=False) + "\n时间:" + str(msgtime),
                "type": "json"
            }
            requests.post("http://miaotixing.com/trigger", data=msg)
            num = num + 1
        return True


if __name__ == "__main__":
    Xiao().run()
