from __future__ import barry_as_FLUFL
import csv
from urllib.request import Request, urlopen
import re
from googlesearch import search
from urllib.request import urlopen
import pandas as pd
from zmq import NULL

def main():
        question=["what is Data Structure","what is Algorithm","what is Source Control","what is Text Editors","what is IDEs","what is Database",
        "what is SQL","what is UNIX","what is Linux","what is Microsoft Excel","what is Programming Language","what is Networking Basics","what is Scripting Languages"]
        
        for data in question:
            #sorular da o x in
            tense_answer = list(data.split(" "))
            tense_answer.remove("what")
            tense_answer.remove("is")
        
            #source:https://stackabuse.com/using-regex-for-text-manipulation-in-python/
            data_urls=[]
            for j in search(data,tld="co.in",num=10, stop=40 , pause=2):
                data_urls.append(j)
                #source:https://www.geeksforgeeks.org/performing-google-search-using-python-code/
            counter=0
            for url in data_urls:
                    #https://itsmycode.com/python-urllib-error-httperror-http-error-403-forbidden/
                    url= Request(data_urls[counter], headers={'User-Agent': 'Mozilla/5.0'})
                    try:
                        #source:https://realpython.com/python-web-scraping-practical-introduction/
                        page=urlopen(url)
                    except:
                        print("error detected")
                    html_bytes = page.read()
                    try:
                        html = html_bytes.decode("utf-8")
                    except UnicodeDecodeError as error:
                        html="empty info"
                    
                    #html tags that may contain information
                    html_str=str(html)
                    if "<p" in html_str:
                        pattern = r"<p.*?>.*?</p.*?>"
                    elif "<i" in html_str:
                        pattern = r"<i.*?>.*?</i.*?>"

                    #Gets data that matches pattern in #html data
                    match_results = re.search(pattern, html, re.IGNORECASE)
                
                    try:
                        info = match_results.group()
                    except AttributeError as error:
                        info ="empty info"

                    info = re.sub("<.*?>", "", info)
                    different_word_arr=["á","á","â","ä","ä","ă","í","ó","æ","ß"]
                    for x in different_word_arr:
                        info = re.sub(x, "", info)
                    
                    #"importance level" is determined
                    imp_counter=0
                    res = re.findall(r'\w+', info)
                    for x in tense_answer:
                        for y in res:
                            if x.lower()==y.lower():
                                imp_counter+=1
                        
                    s=str(data_urls[counter])
                    start = s.find("www.") + len("www.")

                    try:
                        if ".com" in s:
                           end = s.find(".com") 
                        elif ".gov" in s:
                           end = s.find(".gov")
                        elif ".net" in s:
                           end = s.find(".net")
                        elif ".edu" in s:
                           end = s.find(".edu")
                        elif ".mil" in s:
                           end = s.find(".mil")
                        elif ".org" in s:
                           end = s.find(".org")
              
                        url_name = s[(start-4):(end+4)]
                    except pd.errors.ParserError as error:
                        print(error)
                
                #maybe restriction can added right here
                    if info =="" or url_name =="":
                        info="empty info"
                        url_name="empty url"
                #Does not receive "info"s longer than 450 characters
                    if len(info) >450:
                        info= info[0:450]
                     
                    rows = [data,info,imp_counter,url_name]
                    counter +=1
                    print(rows)

                    with open('output_data_whatis.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(rows)

main()





