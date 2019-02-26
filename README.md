# The challenge 
The challenge is as follows  : 
1. You have a list of keywords given in the xlsx file keywords.xlsx
2. You have to get to the adress : https://en.wikipedia.org/w/index.php?title=Special:Search 
then you make a search for every single keyword.
3. You get the first 10 results per keyword. 
For each result, you extract the main content of the page and, then, you store in a free format file all the sentences that contain a digit  ( not including the footnotes).
# Settig up the system and executing the script 
- First of all, you need to install BeautifulSoup if not installed. To do that, please refer to the page [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
- You need to install ntlk too. To do so, please visit their installation page [here](https://www.nltk.org/install.html)
- To use the script, you need to have had installed python 3. To execute the script, all you need to do is to make the command `python wiki_challenge.py` on the command line. In case you need to store the result on a json file too, you can use the command `python wiki_challenge.py storejson` instead.


# The suggested Solution
The solution is a script that does the job, it stores the result as follows on a text file : 
```
###########
Keyword   #
###########
_________________
url_of_subpage1  |
_________________|

- sentence with numbers n : 1
- sentence with numbers n : 1
.
.
.
_________________
url_of_subpage2  |
_________________|
.
.
.
###########
Keyword   #
###########
.
.
.

```
If you chose to store the json too, the output file has the structure : 
```
{
  keyword1 :
    {
      url_of_subpage1:
        [sentence_subpage1,sentence_subpages2,...], 
      url_of_subpage2:[...]
     ...
     },
  keyword2: 
    {
    ...
    }...
}

```

