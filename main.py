import re
import time
import json
import requests


class GeetestCrack(object):
    def __init__(self):
        self.sess = requests.session()
        self.sess.headers = {
            # host 要依据请求接口，api或者www,不然请求不通
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://www.geetest.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        self.gt = ""
        self.challenge = ""
        self.token = ""

    def get_gtc(self):
        url = "https://www.geetest.com/demo/gt/register-click-official?t={}".format(int(time.time()*1000))
        resp = self.sess.get(url=url)
        # {"success":1,"challenge":"83ca2f107a331ab7294b1de01a1445a7","gt":"9dd4b398509fd4b2a2cbf2a7c0a7c605","new_captcha":true}
        self.gt = resp.json().get("gt")
        self.challenge = resp.json().get("challenge")

    
    def gettype(self):
        url = "https://api.geetest.com/gettype.php?gt={gt}&callback=geetest_{ts}".format(gt=self.gt,ts=int(time.time() * 1000))
        resp = self.sess.get(url=url)
        # geetest_1618469582477({"status": "success", "data": {"click": "/static/js/click.2.9.8.js", "static_servers": ["static.geetest.com/", "dn-staticdown.qbox.me/"], "aspect_radio": {"click": 128, "slide": 103, "voice": 128, "pencil": 128, "beeline": 50}, "voice": "/static/js/voice.1.2.0.js", "fullpage": "/static/js/fullpage.9.0.4.js", "slide": "/static/js/slide.7.7.9.js", "type": "fullpage", "pencil": "/static/js/pencil.1.0.3.js", "geetest": "/static/js/geetest.6.0.9.js", "beeline": "/static/js/beeline.1.0.1.js"}})
        # print(resp.text)

    def get_php1(self,w):
        url = "https://api.geetest.com/get.php?gt={gt}&challenge={challenge}&lang=zh-cn&pt=0&client_type=web&w={w}&callback=geetest_{ts}"
        resp = self.sess.get(url=url.format(gt=self.gt,challenge=self.challenge,w=w,ts=int(time.time() * 1000)))
        text = re.sub(r'geetest_.*?\(',"",resp.text)
        text = text.replace(")","")
        param = json.loads(text)
        data = param.get("data")
        return data.get("c"),data.get("s")

    def get_w1(self):
        url = "http://127.0.0.1:8898/get_w1"
        data = {
            "gt" : self.gt,
            "challenge" : self.challenge
        }
        res = requests.post(url,data=data)
        return res.json().get("w"),res.json().get("token_ymml")
            

    def get_ajax1(self,w):
        url = "https://api.geetest.com/ajax.php?gt={gt}&challenge={challenge}&lang=zh-cn&pt=0&client_type=web&w={w}&callback=geetest_{ts}"
        resp = self.sess.get(url=url.format(gt=self.gt,challenge=self.challenge,w=w,ts=int(time.time() * 1000)))
        # geetest_1619405391098({"status": "success", "data": {"result": "click"}})
        return resp.text

    def get_w2(self,c,s,token_ymml):
        url = "http://127.0.0.1:8898/get_w2"
        data = {
            "gt" : self.gt,
            "challenge" : self.challenge,
            "c" : c,
            "s" : s,
            "token_ymml":token_ymml
        }
        res = requests.post(url,data=data)
        return res.text


    def get_php2(self):
        url = "https://api.geetest.com/get.php?is_next=true&type={type}&gt={gt}&challenge={challenge}&lang=zh-cn&https=true&protocol=https%3A%2F%2F&offline=false&product=float&api_server=api.geetest.com&isPC=true&autoReset=true&width=100%25&callback=geetest_{ts}"
        resp = self.sess.get(url=url.format(gt=self.gt,challenge=self.challenge,type="click",ts=int(time.time() * 1000)))
        # print(resp.text)
        return resp.text




if __name__ == '__main__':
    gee = GeetestCrack()
    gee.get_gtc()
    gee.gettype()
    w1,token_ymml = gee.get_w1()
    c,s = gee.get_php1(w1)
    # print(token_ymml,c,s)
    w2 = gee.get_w2(c,s,token_ymml)
    gee.get_ajax1(w2)
    gee.get_php2()

