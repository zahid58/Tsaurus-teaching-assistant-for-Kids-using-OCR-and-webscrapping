from PIL import Image
import urllib
import requests
import cv2
from skimage import io
import numpy as np
from bs4 import BeautifulSoup
import imageio

while(True):
    
    x = input("type in a word : ")
    url = ""
    url = 'https://pixabay.com/en/photos/' + x + '/'
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    image_tags = soup.findAll('img')
    #for image_tag in image_tags:
        #u = image_tag.get('src')
        #if (not ('svg' in u) )and( not ('gif' in u)):
            #img_src = u
            #break
    img_src = image_tags[2].get('src')
    print(img_src)
    #img_src = "https:" + img_src 
    print(img_src)
    
    image =imageio.imread(img_src)
    print(image.shape)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    


