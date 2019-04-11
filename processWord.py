from requests import get as reqGet
from bs4 import BeautifulSoup
from os import getcwd, path 
import threading
from json import loads as jloads
from re import sub
from string import punctuation
from database import dbobject


cwd = getcwd()
savedir = path.join(path.dirname(cwd) + "\\tsaurusElectron\\temp")

a = '-'
b = '-'
c = '-'

global db
db=dbobject()
db.db__init__()

def setImage(word):        #---------------#
    try:
        img_url = "" 
        img_url = "https://www.pixabay.com/en/photos/" +word + "/"
        htmlContents = reqGet(img_url).content
        soup  =  BeautifulSoup(htmlContents,'lxml')
        image_tags = soup.find_all('img')
        count = 0
        for image_tag in image_tags:
            if count>=6:
                break
            img_src = image_tag.get('src')
            if ('svg' not in img_src) and ('gif' not in img_src):
                db.set_img_url(img_src)
                count += 1
        if count < 6:
            rem = 6 - count
            for i in range(rem):
                img_src = savedir+"\\errorImage.jpg"
                db.set_img_url(img_src)
        global a 
        a = '+'
    except:
        pass

def setDescription(word):      #--------------#
    try:
        url = ""
        url = 'https://www.britannica.com/search?query='+ word
        content = reqGet(url).content
        soup = BeautifulSoup(content,'lxml')
        div_tag = soup.find("li",class_="mb-45")
        a = div_tag.find('a')
        a['href'] = "https://www.britannica.com" + a['href']
        db.set_description(str(div_tag))
        global b
        b = '+'
    except:
        #"Oops! Mr. Taurus could not find the word in encyclopedia ! <br>  ")
        pass
        


def setDictionary(word):
    try:
        api_key = '750c98f0-f83f-4604-a78d-9065f53e5804'
        url = "https://www.dictionaryapi.com/api/v3/references/sd2/json/"+ word.lower() + "?key=" + api_key
        resp = reqGet(url)
        data = jloads(resp.text)
        defis = data[0]['def'][0]['sseq']
        count = 0
        dict_string=""
        for defi in defis:
            count += 1 
            if(count>=4):
                break
            text = defi[0][1]['dt'][0]
            text = text[1][4:]+"."
            text = text.replace("{it}", "\"")
            text = text.replace("{/it}","\"")
            text = text.replace("{bc}"," ")
            text = text.replace("{sx"," ")
            text = text.replace("|}"," ")
            text = text.replace("}"," ")
            text = sub('['+punctuation+']',' ',text)
            text = sub('[0-9]+',' ',text)
            dict_string += str("=> " + text + "<br>")
        dict_string+= str( "< " + data[0]['fl'] + " >  <br> ")
        db.set_dic_text(dict_string)
        global c 
        c = '+'
    except:
        pass





def main():

    word = "house"
    db.set_word(word)
    t1=threading.Thread(target=setImage(word),args=())
    t2=threading.Thread(target=setDictionary(word),args=())
    t3=threading.Thread(target=setDescription(word),args=())
    t1.start()
    t2.start()
    t3.start()
    db.save()
    
if __name__=="__main__":
    main()

status = a+b+c
print(status)



