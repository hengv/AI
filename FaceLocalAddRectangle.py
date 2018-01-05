#!/usr/bin/python
# -*- coding: utf-8 -*-

#导入相关模块
import httplib, urllib, json
from os.path import expanduser
from PIL import Image, ImageDraw, ImageFont

def getRectangle(mydata):
    left = mydata[u'left']
    top = mydata[u'top']
    bottom = left + mydata[u'height']
    right = top + mydata[u'width']
    return ((left, top), (bottom, right))

#Face API相关的Key和Endpoint
subscription_key = '30a236e53b924f2c943892711d8d0e45'
uri_base = 'api.cognitive.azure.cn'

#定义html的header，这里Content-type决定了body中的类型，是URL还是文件类型的，这里的Json支持URL模式
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}
#定义返回的内容，包括FaceId，年龄、性别等等
params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
})
#打开本地图片
#imgfile = 'D:\\Heng\\Pictures\\C5D_3966.JPG'
#imgfile = 'D:\\Heng\\desktop\\face.JPG'
imgfile= 'D:\\Heng\\Pictures\\100EOS5D\\C5D_5895.JPG'

img = open(expanduser(imgfile), 'rb')
#Call Face API，进行人脸识别
try:
    conn = httplib.HTTPSConnection('api.cognitive.azure.cn')
    conn.request("POST", "/face/v1.0/detect?%s" % params, img, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    conn.close()

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
#新建一个文件
newimg = Image.open(imgfile)
draw = ImageDraw.Draw(newimg)
#判断其大小
size = len(str(newimg.size[0]))
#根据大小分配字体大小和字的位置
if size>= 4:
    fs = 50
    ps = 130
else:
    fs = 10
    ps = 13
#图片的字体和颜色
font = ImageFont.truetype("consola.ttf", fs)
draw.ink = 255 + 0 * 256 + 0 * 256 * 256
#给每个识别出的人脸画框、并标识年龄
for a in parsed:
    b = a[u'faceRectangle']
    c = getRectangle(b)
    draw.rectangle(c, outline='red')
    draw.text([c[0][0],c[0][1]-ps],"Age="+str(a[u'faceAttributes'][u'age']),font=font)
newimg.show()



