# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 00:37:49 2019

@author: HP
"""
import sqlite3
from sqlite3 import Error
from os import getcwd,path

dbcwd = getcwd()
dbsavedir = path.join(path.dirname(dbcwd) + "\\temp")

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
            print("this works")
            global conn_url
            conn_url = path.join(dbsavedir + "\sqlite2.db")
            
            
           # print(conn_url)
            try:
                conn=sqlite3.connect(conn_url)
                cursor=conn.cursor()
                query="""CREATE TABLE IF NOT EXISTS word_table (
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
                #print(conn_url+'hkjhcxjk')
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
                sql='''insert into word_table (word,dic_text,speech_type,description,img_url1,img_url2,img_url3,img_url4,img_url5,img_url6,freq_of_srch) values(?,?,?,?,?,?,?,?,?,?,?)'''
                global word
                global dic_text
                global speech_type
                global description
                attr=( word, dic_text, speech_type, description ,img_url[0],img_url[1],img_url[2],img_url[3],img_url[4],img_url[5],0 )
                cur.execute(sql,attr)
                conn.commit()
                conn.close()
            except Error as e:
                print(e)
            
            
                
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