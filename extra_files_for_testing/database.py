# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 00:37:49 2019

@author: HP
"""
import sqlite3
from sqlite3 import Error

from os import getcwd,path

dbcwd = getcwd()
dbsavedir = path.join(path.dirname(dbcwd) + "\\tsaurusElectron\\temp")


class  dbobject:
        def _init_(self):
            global word
            global dic_text
            dic_text=[]
            global speech_type
            global description
            global img_url
            img_url=[]
            global freq_of_srch
            freq_of_srch=0
            self.conn_url=""

        def db_init(self):
            self.conn_url= path.join(dbsavedir + "\\sqlite1.db")
            try:
                conn=sqlite3.connect(self.conn_url)
                cursor=conn.cursor()
                query="""CREATE TABLE IF NOT EXISTS word_table (
                            word text primary key,
                            dic_text  text,
                            speech_type text,
                            description text,
                            img_url1,
                            img_url2,
                            img_url3,
                            img_url4,
                            img_url5,
                            img_url6
                        );"""
                cursor.execute(query)
            except Error as e:
                print(e)
            
        def get_con(self,conn):
            try:
                 conn=sqlite3.connect(self.conn_url)
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
        
        
        def list_to_str(self,txt):
            ret=''
            for tx in txt:
                ret=ret+tx+' '
            return ret
       
        
        def set_description(self,desc):
            global description
            description=desc
        
        def set_img_url(self,url):
            #print("inside set image method/n"+url)
            img_url.append(url)
            
            
        
        def save(self):
            
            try:
                conn=0
                conn=self.get_con(conn)
                #conn=sqlite3.connect(conn_url);
                
                cur=conn.cursor()
                sql='''insert into word_table(word,dic_text,speech_type,description,img_url1,img_url2,img_url3,img_url4,img_url5,img_url6,freq_of_srch) values(?,?,?,?,?,?,?,?,?,?,?)'''
                global word
                global dic_text
                global speech_type
                global description
                attr=( word, dic_text, speech_type,description,img_url[0],img_url[1],img_url[2],img_url[3],img_url[4],img_url[5],0)
                cur.execute(sql,attr)
                conn.commit()
                conn.close()
            except Error as e:
                print(e)
            
            
                
if __name__ == '__main__':
    db=dbobject()
    db.set_word('heart')
    db.set_dic_text('lol')
    db.set_dic_partOfSpeech('noun')
    db.save()
#.open D:/tsaurus/Tsaurus-teaching-assistant-for-Kids-using-OCR-and-webscrapping/sqlitedb/sqlite1.db
#.tables
#select all