# %%
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# %%

MOTI_SCHOLAR_URL = 'https://scholar.google.com/citations?hl=en&user=8Oiqdz0AAAAJ&view_op=list_works&sortby=pubdate'

def get_soup(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

main_soup = get_soup(MOTI_SCHOLAR_URL)
# Extract data
pub_data = []
for publication in main_soup.find_all('tr', class_='gsc_a_tr'):
    title = publication.find('a', class_='gsc_a_at').text
    
    link = publication.find('a', class_='gsc_a_at')
    link_text = link['href']
    full_link = f"https://scholar.google.com{link_text}&hl=en"

    gray_text = publication.find_all('div', class_='gs_gray')

    authors, journal = gray_text
    
    pub_data.append({
        'Title': title,
        'Link': full_link,
        'Authors': authors.text,
        'Journal': journal.text
    })

# %%

detailed_pub_data = []
for item in pub_data:
    link = item['Link']
    pub_soup = get_soup(link)
    
    for info in pub_soup.find_all('div', id='gsc_oci_table'):
        field = info.find_all('div', class_='gsc_oci_field')
        value = info.find_all('div', class_='gsc_oci_value')

        data = {
                'Title': item['Title'].strip("\u200f"),
                'Authors': item['Authors'],
                'Journal': item['Journal'].strip("\u200f"),
            }
        additional = {f.text: v.text for f, v in zip(field, value)}
        additional.pop("Total citations", None)
        additional.pop("Scholar articles", None)

        try:
            additional["Publication date"] = additional["Publication date"].replace("/", "-")
            
            year = additional["Publication date"].split("-")[0]
            
            if year < 2022:
                break
        except:
            pass
            
        detailed_pub_data.append(data | additional)
        
# %%

len(detailed_pub_data)

# %%

conference = []
preprint = []
journal = []

for item in detailed_pub_data:
    if "Conference" in item.keys():
        conference.append(item)
        continue
    
    if "arxiv" in item['Journal'].lower():
        preprint.append(item)
        continue
    
    journal.append(item)
    
# %%

len(conference), len(preprint), len(journal)

# %%

from keyword_matcher import extract_keywords

DEST_ARTICLES = r"C:\Users\ang.a\Documents\GitHub\tcml-bme.github.io\_articles"
DEST_CONFERENCES = r"C:\Users\ang.a\Documents\GitHub\tcml-bme.github.io\_conferences"

def transform_author(author):
    author = author.strip()
    last_name = author.split(" ")[-1]
    
    # get the initials of the first names
    initials = "".join([name[0] for name in author.split(" ")[:-1]])
    
    return f"'{initials} {last_name}'"

def create_article_file(item):
    title = item['Title']
    abstract = item['Description']
    authors = item['Authors']
    parsed_authors = ", ".join([transform_author(author) for author in authors.split(",")])
    journal = item['Journal']
    try:
        # pad date with zeroes when applicable
        date = item['Publication date']
        date = "-".join([f"{int(part):02d}" for part in date.split("-")])
        
    except:
        date = "N/A"
    
    keywords = extract_keywords(title + "\n" + abstract)

    # transform keywords to a bulleted list
    keywords = "\n".join([f"  - {keyword.title()}" for keyword in keywords])
            
    content = f"""
---
title: "{title}"
date: {date}
authors: [{parsed_authors}]
journal: "{journal}"
categories: 
{keywords}
---
    """      
    
    # remove first newline in content
    content = content[1:]
    
    first_author = transform_author(authors.split(",")[0]).replace("'", "")
    first_author = first_author.split(" ")[1]
    file_title = f"{date}-{first_author}.md"
    
    return content, file_title

file, file_title = create_article_file(journal[1])

import os
with open(os.path.join(DEST_ARTICLES, file_title), "w") as f:
    f.write(file)
    