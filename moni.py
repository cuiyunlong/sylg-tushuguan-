
import requests
from bs4 import BeautifulSoup
import os, sys
import pytesseract
from PIL import Image


loginurl = 'http://lib.sylu.edu.cn/reader/redr_verify.php'
captchaurl = 'http://lib.sylu.edu.cn/reader/captcha.php'

headers = {
    'Referer': 'http://lib.sylu.edu.cn/reader/login.php',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
}

session = requests.Session()
##### 获取到验证码并保存
checkcodecontent = session.get(captchaurl, headers=headers)
with open('D:\checkcode\checkcode.gif', 'wb') as f:
    f.write(checkcodecontent.content)
    f.close()
print('验证码已写入到本地！', '下面开始调用tesseract-OCR引擎识别验证码！')

img = Image.open('D:\checkcode\checkcode.gif', mode='r')
result = pytesseract.image_to_string(image=img)
checkcode = result
print('验证码为：', checkcode)

# os.startfile('checkcode.jpg')
# checkcode = input('请输入验证码：')
##### 准备登陆图书馆系统
payload = {
    'number':'158212Z390',
    'passwd':'158212Z390',
    'captcha': checkcode,
    'select':'cert_no'
}

response = session.post(loginurl, headers=headers, data=payload)
print('服务器端返回码： ', response.status_code)
soup = BeautifulSoup(response.text, 'lxml')
## 打印当前用户
username = soup.find('font', {'color': 'blue'})
print(username.get_text())
## 打印积分信息
jifen = soup.find_all('span', {'class': 'bigger-170'})[3]
jifen = str(jifen.get_text())
print('当前登录用户总积分：', jifen)
