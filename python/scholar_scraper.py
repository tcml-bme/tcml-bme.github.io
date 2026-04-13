from habanero import Crossref

from lab_keywords import *
from soup import *
from keyword_matcher import *
from data import *
from website import *
from tqdm import tqdm
import re

main_soup = get_soup(MOTI_SCHOLAR_URL, click_more=True)
cr = Crossref()

pub_data = get_pubdata_from_scholar(main_soup)

detailed_pub_data = get_detailed_pubdata(pub_data)

preprint = []
crossref_items = []

for item in tqdm(detailed_pub_data):
    if "arxiv" in item['Journal'].lower():
        preprint.append(item)
        continue
    
    crossref_items.append(item)

low_similarity = []
items = {}

for data in crossref_items:
    x = cr.works(query=data['Title'] + data["Authors"], rows=10)
    crossref_out = x['message']['items'][0]['title'][0]
    title = data["Title"]
    doi = x['message']['items'][0]['DOI']
    pub_type = x['message']['items'][0]['type']
    container_title = x['message']['items'][0]['container-title'][0]
    description = data.get("Description", "")

    try:
        published = date_parts_to_datetime(x['message']['items'][0]['published']['date-parts'][0])
    except KeyError:
        published = date_parts_to_datetime(x['message']['items'][0]['indexed']['date-parts'][0])

    try:
        authors = x['message']['items'][0]['author']
        is_moti_paper = any([author['family'] == "Freiman" for author in authors])
        if not is_moti_paper:
            print("Not Moti paper: ", authors)
            continue

        author_list = transform_crossref_authors(authors)
    except KeyError:
        authors = data["Authors"]
        print("warning: crossref author data not found")

        author_list = ", ".join([transform_author(author) for author in authors.split(",")])

    print(title)
    crossref_title = re.sub('<[^<]+?>', '', crossref_out)
    print(crossref_title)

    similarity_score = compare_titles(title, crossref_out, lemmatize=True, remove_stopwords=False)

    enum_type = PublicationType(pub_type)

    match enum_type:
        case PublicationType.JOURNAL_ARTICLE:
            data = JournalArticle(
                title=" ".join([t.capitalize() for t in crossref_title.split(" ")]),
                DOI=doi,
                authors=author_list,
                publication_date=published,
                journal=container_title,
                description=x['message']['items'][0].get("abstract", description)
            )

        case PublicationType.CONFERENCE_PAPER:
            try:
                event_start = date_parts_to_datetime(x['message']['items'][0]['event']['start']['date-parts'][0])
                event_end = date_parts_to_datetime(x['message']['items'][0]['event']['end']['date-parts'][0])
            except KeyError:
                event_start = None
                event_end = None

            data = ConferenceAbstract(
                title=" ".join([t.capitalize() for t in crossref_title.split(" ")]),
                authors=author_list,
                publication_date=published,
                conference=container_title,
                description=x['message']['items'][0].get("abstract", description),
                event_name=x['message']['items'][0]['event']['name'],
                event_location=x['message']['items'][0]['event'].get("location", ""),
                event_start=event_start,
                event_end=event_end,
                DOI=doi
            )
        case PublicationType.BOOK:
            published = date_parts_to_datetime(x['message']['items'][0]['published-print']['date-parts'][0])

            data = Book(
                title=" ".join([t.capitalize() for t in crossref_title.split(" ")]),
                authors=author_list,
                publication_date=published,
                container_title=container_title,
                subtitle=x['message']['items'][0].get("subtitle", ""),
                DOI=doi
            )

        case PublicationType.BOOK_CHAPTER:
            published = date_parts_to_datetime(x['message']['items'][0]['published-print']['date-parts'][0])

            data = ConferencePaper(
                title=" ".join([t.capitalize() for t in crossref_title.split(" ")]),
                authors=author_list,
                publication_date=published,
                journal=container_title,
                description=x['message']['items'][0].get("abstract", description),
                DOI=doi,
                subtitle=x['message']['items'][0].get("subtitle", ""),
            )
        case _:
            breakpoint()

    if similarity_score < 0.7:
        print("Warning: low similarity score, skipping")
        print(similarity_score)
        low_similarity.append(data)
    else:
        print("Similarity score: ", similarity_score)
        items[doi] = data

    print("\n\n")

import os
os.mkdir("_abstracts/")
os.mkdir("_articles/")
os.mkdir("_conferences/")

for doi, data in items.items():
    if type(data) is ConferenceAbstract:
        data.to_file("_abstracts/")
    # elif type(data) is JournalArticle:
    #     data.to_file("_articles/")
    # elif type(data) is ConferencePaper:
    #     data.to_file("_conferences/")

breakpoint()
