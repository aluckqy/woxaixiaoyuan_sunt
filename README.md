**我在校园自动打卡-陕西理工大学**

本文写于2020.4.13，目前为止可用，原理为抓包token值模拟登录，再通过脚本将打卡数据post上传至服务器。
目前token值4天会失效一次
思路及代码参考GitHub项目：

https://github.com/178me/dailyInspectionReport/

https://github.com/Chaney1024/wozaixiaoyuan

项目根据学校不同修改了提交地址，打卡时间以及打卡问题的修订，陕西理工同学直接上手改一下token值和提醒喵token就直接可以用。

# 目录
   * [主要步骤：](#主要步骤)
      * [一、抓包获取token值](#一抓包获取token值)
         * [1、下载Fiddler](#1下载fiddler)
         * [2、安装及配置Fidder](#2安装及配置fidder)
         * [3、获取token值](#3获取token值)
      * [二、云函数部署脚本打卡](#二云函数部署脚本打卡)
         * [1、登录腾讯云](#1登录腾讯云)
         * [2、创建云函数](#2创建云函数)
         * [3、获取喵码](#3获取喵码)
         * [4、Python代码修改](#4python代码修改)
         * [5、设置定时触发](#5设置定时触发)

# 主要步骤：

- 1、抓包token值

- 2、云函数部署脚本打卡


工具：

- PC台式机一台

- 电脑端微信

- 任一浏览器

- 腾讯云账号(实名认证)


## 一、抓包获取token值

抓包教程为利用Fiddler抓包配置教程

参考文章：

https://www.cnblogs.com/liulinghua90/p/9109282.html


### 1、下载Fiddler

下载最新版fiddler ，可以在官网下载：https://www.telerik.com/download/fiddler

百度云链接：链接：https://pan.baidu.com/s/1LqqJCMlBfQgB5C0_lU4r8g 提取码：whyi 



### 2、安装及配置Fidder

① 正常安装，下一步，下一步，可以修改软件安装地址，安装完毕后，打开软件。

② 打开Fiddler，点击工具栏中的Tools—>Options

![20201202095551](http://img.chaney.top/img/20201202095551.png)

③ 点击https设置选项，勾选选择项

![20201202170213](http://img.chaney.top/img/20201202170213.png)


④ 点击Actions,点击第二项：Export Root Certificate to Desktop，这时候桌面上会出现证书FiddlerRoot.cer文件，点击OK设置成功，关闭fiddler 

![20201202170235](http://img.chaney.top/img/20201202170235.png)

⑤ PC端，在浏览器中导入证书FiddlerRoot.cer，以谷歌浏览器为例说明，在浏览器上输入: chrome://settings/  然后进入高级设置，搜索管理证书

![20201202170302](http://img.chaney.top/img/20201202170302.png)

⑥ 在受信任的根证书颁发机构，对证书进行导入

![20201202170335](http://img.chaney.top/img/20201202170335.png)

⑦ 重新打开fiddler，就可以在电脑上进行https抓包了。如果不成功请看参考文章后面解决方案

![20201202170319](http://img.chaney.top/img/20201202170319.png)

### 3、获取token值

登录电脑端微信，打开我在校园日检日报  
留意最下方出现的```student.wozaixiaoyuan.com```双击打开  

![20201202170352](http://img.chaney.top/img/20201202170352.png)

出现的这一串token字符串值就是我们需要的了，第一步任务已经实现。如果后续登录失效了，重新抓包获取这个值即可，如果不出现特殊情况这个登录能保持四天左右。

![20201202095745](http://img.chaney.top/img/20201202095745.png)

## 二、云函数部署脚本打卡

### 1、登录腾讯云

如果没有用的过话先注册，实名认证

产品中搜索云函数，点击管理控制台

![20201202095903](http://img.chaney.top/img/20201202095903.png)
![20201202095909](http://img.chaney.top/img/20201202095909.png)

### 2、创建云函数

点击左侧的函数服务

![20201202170409](http://img.chaney.top/img/20201202170409.png)

点击新建

![20201202170427](http://img.chaney.top/img/20201202170427.png)

填写函数名称autocheck，运行环境选择Python3.6，空白函数

![20201202170441](http://img.chaney.top/img/20201202170441.png)
![20201202170501](http://img.chaney.top/img/20201202170501.png)

点击下一步，直接拉到最底下点击完成

![20201202170508](http://img.chaney.top/img/20201202170508.png)

### 3、获取喵码

手机微信中搜索公众号喵提醒，注册后添加提醒，获取喵码

![20201202170525](http://img.chaney.top/img/20201202170525.png)
![20201202170542](http://img.chaney.top/img/20201202170542.png)

记住这个喵码待会代码中要用到



### 4、Python代码修改

这段代码主要需要修改的内容为注释修改1、修改2、修改3、修改4  
分别为token值、打卡人昵称、喵提醒中的喵码和打卡人地址(可从Fiddler中看到之前打卡的位置信息)  
将修改后的代码贴到index.py中  

```python
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

```


![20201202170558](http://img.chaney.top/img/20201202170558.png)

拉到下面保存，然后测试。测试成功说明代码没问题，这时你微信喵提醒应该就会给你发消息了。

![20201202170608](http://img.chaney.top/img/20201202170608.png)

这里一般会出现三种消息
```json
{“code”：0}, #表示打卡成功  
{“code”：-10}, #表示token值失效了，需要重新抓包获取token值  
{“code”：1}, #表示打卡时间已结束，不能打卡  
```


### 5、设置定时触发

点击左侧触发管理，创建触发器

![20201202170729](http://img.chaney.top/img/20201202170729.png)

起一个定时任务名称，将触发周期设置为最下面一个自定义触发周期

![20201202170739](http://img.chaney.top/img/20201202170739.png)
![20201202170747](http://img.chaney.top/img/20201202170747.png)

参数值为0 1 0,12 * * * *

分别代表着秒 分 时 日 月 星期 年

这里参数表示每天的上午0点1分、下午12点1分时触发我们的云函数

![](https://www.hualigs.cn/image/6076e616c163b.jpg)
![20201202170802](http://img.chaney.top/img/20201202170802.png)

那么到了这一步基本上我们的自动打卡也就完成了，如果有什么其他问题，可以多百度一下，享受探索的快感。
