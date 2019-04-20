# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 00:37:49 2019

@author: HP
"""
import sqlite3
from sqlite3 import Error
from os import getcwd,path
from json import dumps as jdumps

dbcwd = getcwd()
dbsavedir = path.join(path.dirname(dbcwd) + "\\tsauruswithsqlite\\temp")

img_url = []
description = ""
speech_type=""
dic_text= ""
word= ""
freq_of_srch= 0
global conn
global conn_url

class  dbobject:
    
        def db__init__(self):
            #print("this works")
            global conn_url
            conn_url = path.join(dbsavedir + "\sqlite2.db")
            
            file = open("G:/PROJECTS/SoftDevProject/tsauruswithsqlite/errorFile.txt","w")
            file.write(conn_url)
            file.close()
            
            #print(conn_url)
            try:
                conn=sqlite3.connect(conn_url)
                cursor=conn.cursor()
                query="""CREATE TABLE IF NOT EXISTS words (
                            word text primary key,
                            dic_text  text,
                            speech_type text,
                            description text,
                            img_url1 text,
                            img_url2 text,
                            img_url3 text,
                            img_url4 text,
                            img_url5 text,
                            img_url6 text,
                            freq_of_srch number
                        );"""
                cursor.execute(query)
            except Error as e:
                print(e)
            
        def get_con(self):
            try:
                global conn_url
                conn=sqlite3.connect(conn_url)
                
                return conn
            except Error as e:
                print(e)
            
        def set_word(self,wrd):
            global word
            word=wrd
            
        def set_dic_text(self,txt):
            global dic_text
            dic_text = txt    

        def set_dic_partOfSpeech(self,sp):
            global speech_type
            speech_type=sp
        
        
        
        def set_description(self,desc):
            global description
            description=desc
        
        def set_img_url(self,url):
            #print("inside set image method/n"+url)
            img_url.append(url)
            
            
        
        def save(self):
            
            try:
                conn=0
                conn=self.get_con()
                #conn=sqlite3.connect(conn_url);
                
                cur=conn.cursor()
                sql='''insert into words (word,dic_text,speech_type,description,img_url1,img_url2,img_url3,img_url4,img_url5,img_url6,freq_of_srch) values(?,?,?,?,?,?,?,?,?,?,?)'''
                global word
                global dic_text
                global speech_type
                global description
                attr=( word, dic_text, speech_type, description ,img_url[0],img_url[1],img_url[2],img_url[3],img_url[4],img_url[5],0 )
                cur.execute(sql,attr)
                conn.commit()
                conn.close()
                dic = {}
                dic['word'] = word
                dic['dic_text'] = dic_text
                dic['speech_type'] = speech_type
                dic['description'] = description
                dic['img_url1'] = img_url[0]
                dic['img_url2'] = img_url[1]
                dic['img_url3'] = img_url[2]
                dic['img_url4'] = img_url[3]
                dic['img_url5'] = img_url[4]
                dic['img_url6'] = img_url[5]
                json = jdumps(dic)
                print(json)
                
            except:
                pass
            
        def errorNoNet(self):
            dic = {}
            global word
            dic['word'] = word
            dic['dic_text'] = "<br> check your Internet Connection !!! <br>"
            dic['description'] = "<br> Mr. Tsaurus could not get anything from the net !!! <br>"
            dic['img_url1'] = img_url[0]
            dic['img_url2'] = img_url[1]
            dic['img_url3'] = img_url[2]
            dic['img_url4'] = img_url[3]
            dic['img_url5'] = img_url[4]
            dic['img_url6'] = img_url[5]
            errorJson = jdumps(dic)
            print(errorJson)

        def errorInvalidInput(self,savedir):
            dic = {}
            global word
            dic['word'] = word
            dic['dic_text'] = "<br> You typed in an Invalid word!!! <br> Mr. Tsaurus could not find anything !!!<br>"
            dic['description'] = "<br> You typed in an Invalid word!!! <br> Mr. Tsaurus could not find anything !!! <br>"
            dic['img_url1'] = savedir + "\\errorImage.jpg"
            dic['img_url2'] = savedir + "\\errorImage.jpg"    
            dic['img_url3'] = savedir + "\\errorImage.jpg" 
            dic['img_url4'] = savedir + "\\errorImage.jpg" 
            dic['img_url5'] = savedir + "\\errorImage.jpg" 
            dic['img_url6'] = savedir + "\\errorImage.jpg" 
            errorJson = jdumps(dic)
            print(errorJson)
                
if __name__ == '__main__':
    db=dbobject()
    db.db__init__()
    db.set_word('heart2')
    db.set_description("this is description")
    db.set_dic_text('lol')
    db.set_img_url("1")   
    db.set_img_url("2")    
    db.set_img_url("3")    
    db.set_img_url("4")
    db.set_img_url("5")
    db.set_img_url("6")
    db.set_dic_partOfSpeech('noun')
    db.save()
    
#.open D:/tsaurus/Tsaurus-teaching-assistant-for-Kids-using-OCR-and-webscrapping/sqlitedb/sqlite1.db
#.tables
#select all