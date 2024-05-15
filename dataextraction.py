from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
df = pd.read_csv('csvfiles/input.csv')
url_list = []
for i in df['URL']:
    url_list.append(i)
def get_article(url):
    page = requests.get(url)
    if page.status_code != 200:
        return 'Page not found'
    else: 
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            a = soup.find('h1')
            b = soup.find('div',class_ ='td-post-content tagdiv-type')
            return ('%s \n %s'%(a.text, b.text))
        except:
            a = soup.find('h1')
            b = soup.find('div',class_= 'td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
            c = b.find('div', class_ = 'tdb-block-inner td-fix-index')
            return ('%s \n %s'%(a.text, c.text))
sno = 1
pnf = 0
output_directory = "extracted_articles"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for y in url_list:
    url_id = df[df['URL'] == y]['URL_ID'].values[0]
    if get_article(y) == 'Page not found':
        pnf+=1
        output_file_path = os.path.join(output_directory, f"{url_id}.txt")
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write('Page not found')
        print(sno,'. ', get_article(y))
        print('---------------------',)
        sno+=1
    else:
        print('%d. %s Sucessfully extracted'%(sno ,url_id))
        output_file_path = os.path.join(output_directory, f"{url_id}.txt")
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(get_article(y))
        print('---------------------',) 
        sno+=1 

print("Total number of pages not found: ", pnf)

