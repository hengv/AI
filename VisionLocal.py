#!/usr/bin/python
# -*- coding: utf-8 -*-

#导入相关模块
import httplib, urllib, json
from os.path import expanduser
from PIL import Image, ImageDraw, ImageFont

#Face API相关的Key和Endpoint
subscription_key = '3323373494604e7aa7fa4dc7c9d26e2a'
uri_base = 'api.cognitive.azure.cn'

#定义html的header，这里Content-type决定了body中的类型，是URL还是文件类型的，这里的Json支持URL模式
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}
# headers = {
#     # Request headers.
#     'Content-Type': 'application/json',
#     'Ocp-Apim-Subscription-Key': subscription_key,
# }
#定义返回的内容，包括FaceId，年龄、性别等等
params = urllib.urlencode({
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})
#打开本地图片

#body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg'}"
imgfile= 'D:\\h2.jpg'
#imgfile='D:\\Heng\\desktop\\face.JPG'
img = open(expanduser(imgfile), 'rb')
#Call Face API，进行人脸识别
try:
    conn = httplib.HTTPSConnection(uri_base)
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, img, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print(e)

newimg = Image.open(imgfile)
draw = ImageDraw.Draw(newimg)
#判断其大小
print (newimg.size[0],newimg.size[1])
size = len(str(newimg.size[0]))
#根据大小分配字体大小和字的位置
if size>= 4:
    fs = 100
    ps = 130
else:
    fs = 10
    ps = 13
font = ImageFont.truetype("consola.ttf", fs)
draw.ink = 255 + 0 * 256 + 0 * 256 * 256
draw.text([0,newimg.size[1]-fs],str(parsed[u'description'][u'captions'][0][u'text']),font=font)

newimg.show()

