from keyword_matcher import extract_keywords


def transform_crossref_authors(authors):
    compiled_authors = []
    for author in authors:
        given = "".join([part[0] for part in author['given'].split(" ")])
        family = author['family']

        compiled_authors.append(f"'{given} {family}'")

    return ", ".join(compiled_authors)


def transform_author(author):
    author = author.strip()
    last_name = author.split(" ")[-1]

    # get the initials of the first names
    initials = "".join([name[0] for name in author.split(" ")[:-1]])

    return f"'{initials} {last_name}'"


def create_article_file(item):
    title = item['Title']
    try:
        abstract = item['Description']
    except:
        abstract = ""
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
