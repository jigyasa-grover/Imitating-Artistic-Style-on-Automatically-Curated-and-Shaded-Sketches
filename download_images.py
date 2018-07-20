#import urllib2
import urllib
import json
import numpy as np
import cv2
import untangle
from urllib.request import urlopen

maxsize = 512

# tags = ["asu_tora","puuakachan","mankun","hammer_%28sunset_beach%29",""]

# for tag in tags:

count = 0

for i in range(10000):
    stringreturn = urlopen("http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=1girl%20solo&pid="+str(i+3000)).read().decode('utf-8')
    xmlreturn = untangle.parse(stringreturn)
    for post in xmlreturn.posts.post:
        imgurl = "http:" + post["sample_url"]
        print (imgurl)
        if ("png" in imgurl) or ("jpg" in imgurl):

            resp = urlopen(imgurl)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            height, width = image.shape[:2]
            if height > width:
                scalefactor = (maxsize*1.0) / width
                res = cv2.resize(image,(int(width * scalefactor), int(height*scalefactor)), interpolation = cv2.INTER_CUBIC)
                cropped = res[0:maxsize,0:maxsize]
                cv2.imwrite("imgs/"+str(count)+".jpg",cropped)
            if width > height:
                scalefactor = (maxsize*1.0) / height
                res = cv2.resize(image,(int(width * scalefactor), int(height*scalefactor)), interpolation = cv2.INTER_CUBIC)
                center_x = int(round(width*scalefactor*0.5))
                print (center_x)
                cropped = res[0:maxsize,center_x - int(maxsize/2):center_x + int(maxsize/2)]
                cv2.imwrite("imgs/"+str(count)+".jpg",cropped)
            # img_edge = cv2.adaptiveThreshold(cropped, 255,
            #                                  cv2.ADAPTIVE_THRESH_MEAN_C,
            #                                  cv2.THRESH_BINARY,
            #                                  blockSize=9,
            #                                  C=2)

            count += 1
            # cv2.imwrite("imgs/"+str(count)+".jpg",cropped)
            # cv2.imwrite("imgs/"+str(post["id"])+"-edge.jpg",img_edge)
