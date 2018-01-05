#!/usr/bin/python
# -*- coding: utf-8 -*-

#导入相关模块
import httplib, urllib, json
from os.path import expanduser

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
img = open(expanduser('D:\\Heng\\Pictures\\100EOS5D\\C5D_5131.JPG'), 'rb')
#Call Face API，进行人脸识别
try:
    conn = httplib.HTTPSConnection('api.cognitive.azure.cn')
    conn.request("POST", "/face/v1.0/detect?%s" % params, img, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

