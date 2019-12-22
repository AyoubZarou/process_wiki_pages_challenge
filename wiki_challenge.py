import urllib.request as urlreq
from urllib.parse import urljoin 
from nltk import tokenize
from bs4 import BeautifulSoup as bs
import json
import xlrd
import re
import sys
import time
from collections import defaultdict

t0=time.time()
## THE FUNCTION IS DEFINED TO DISPLAY THE PROGRESS BAR ##
# ------------------------------------------
def update_progress(job_title, progress, second_half=False):
    try : 
        length = 30 # modify this to change the length
        block = int(round(length*progress))
        msg = "\r{0} [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
        if progress >= 1: msg += " DONE\r\n"
        sys.stdout.write(msg)
        sys.stdout.flush()
    except : 
        if not second_half  : 
            print(job_title)
            
## GET THE KEYWORDS FROM THE XLSX FILE ##

wb=xlrd.open_workbook('keywords.xlsx')
s=wb.sheets()[0]
keywords=[]
for row in range(s.nrows):
    for col in range(s.ncols):
        keywords.append(s.cell(row, col).value)
        

## DEFINING THE CONSTANTS ##

# The used url for search, the keyword goes into {}        
search_url = ("https://en.wikipedia.org/w/index.php?search={}&title=Special%3ASearch"
            "&profile=advanced&fulltext=1&advancedSearch-current=%7B%22namespaces%22%3A%5B0%5D%7D&ns0=1")

# A regex pattern used to verify if a sentence contains a number 
num_pattern = re.compile(r'[(^\d)*]\d+')

# The regex to get the main part
pattern = re.compile(r'<(p|table)((.|\n)*?)\<h2\>')

# a boolean variable that contain wether the user asked to store on a json file or not 
store_json = ("storejson" in sys.argv)



## THE MAIN PART ##

s_w_numbers= defaultdict(defaultdict) # a dictionnary to store all the sentences with numbers
return_string=""
for i, keyword in enumerate(keywords): 
    return_string += "{0}\n {1}#\n{0}\n\n".format("#"*(len(keyword)+5), keyword+3*" ")
    x = "keyword {} : {}".format(i+1, keyword)
    update_progress(x+(40-len(x))*" ", 2*i/100.0)
    url = search_url.format(keyword)
    html_page = urlreq.urlopen(url).read().decode('utf-8')
    soup = bs(html_page, "html.parser") # parse the html page into a BeautifulSoup object to process it 
    # we get the first 10 links
    links_soup = soup.find_all("a", {"data-serp-pos": re.compile('^[0-9]$')}) 
    links = [element.get('href') for element in links_soup]
    for link in links:
        url = urljoin("https://en.wikipedia.org", link)
        # We get the main part that we want to process
        content = urlreq.urlopen(url).read().decode('utf-8')
        content = pattern.search(content).group()
        # parse the html page into a BeautifulSoup object 
        content = bs(content, "html.parser")
        update_progress(x+(40-len(x))*" ", (2*i+1)/100.0, second_half=True)
        # We delete scripts,styles,tables and spans
        for element in content.find_all(['script', 'style', 'table', 'span']):
            element.extract()
        # we get he text without html tags
        string=content.text
        # We get rid of the references in the text
        string = re.sub(r'(\[(.|\n)*\]|\n(\s)+)','',string)
        # We parse the body into sentences using nltk
        sentences = tokenize.sent_tokenize(string)
        sentences_with_numbers = []
        for s in sentences: 
            if num_pattern.search(s):
                sentences_with_numbers.append(s) 
        # if the user asked to store the json file, we create a dictionary structure that stores the data
        if store_json:
            s_w_numbers[keyword][url] = sentences_with_numbers 
        # We format a string so we could store it at a text file 
        all_sentences = "{0}\n{1}  |\n{0}| \n\n-\t{2}\n\n".format("_"*(len(url)+2), url, 
                                                                  '\n-\t'.join(sentences_with_numbers))
        return_string += all_sentences   
        
        
## STORING PART               
# WE STORE THE SENTENCES WITH NUMERIC VALUES ON THEM ON A TEXT FILE

with open('numeric_sentences.txt', 'w', encoding='utf-8') as f: 
    f.write(return_string)
    
# IF ASKED, WE STORE THE DATA ON A JSON TOO
if store_json: 
    with open('numeric_sentences.json', 'w') as jf:
        json.dump(s_w_numbers, jf)
update_progress("DONE"+36*" ", 100/100.0, second_half=True)


## DISPLAY THE NECESSARY TIME TO PROCESS THE SCRIPT
total_time = (time.time() - t0)
minutes = int(total_time / 60)
print("\nTook %.0f minutes and %.0f seconds"%(minutes, total_time - 60*minutes))

