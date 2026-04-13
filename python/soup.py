from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By

from tqdm import tqdm


def get_soup(url, click_more=False):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(2)
    if click_more:

        while True:
            show_more_button = driver.find_element(By.ID, "gsc_bpf_more")
            show_more_button.click()
            time.sleep(5)

            if not show_more_button.is_enabled():
                print("No more content to load.")
                break

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_pubdata_from_scholar(soup):
    pub_data = []

    for publication in tqdm(soup.find_all('tr', class_='gsc_a_tr')):
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

    return pub_data


def get_detailed_pubdata(pub_data):
    detailed_pub_data = []
    for item in tqdm(pub_data):
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

                year = int(additional["Publication date"].split("-")[0])

                # if year < 2022:
                #     break
            except:
                pass

            detailed_pub_data.append(data | additional)

    return detailed_pub_data
