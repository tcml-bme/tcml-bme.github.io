from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class PublicationType(Enum):
    JOURNAL_ARTICLE = "journal-article"
    CONFERENCE_PAPER = "proceedings-article"
    BOOK = "book"
    BOOK_CHAPTER = "book-chapter"
    PATENT = "patent"
    OTHER = "other"


@dataclass
class JournalArticle:
    title: str
    DOI: str
    authors: str
    publication_date: datetime
    journal: str
    description: str

    def to_file(self, destination: str):
        # strip all strings of non-unicode characters
        self.title = self.title.encode('ascii', 'ignore').decode('utf-8')
        self.authors = self.authors.encode('ascii', 'ignore').decode('utf-8')
        self.journal = self.journal.encode('ascii', 'ignore').decode('utf-8')
        self.description = self.description.encode('ascii', 'ignore').decode('utf-8')

        from keyword_matcher import extract_keywords

        jekyll_date = self.publication_date.strftime("%Y-%m-%d")
        keywords = extract_keywords(self.title,  self.description)
        keywords = "\n".join([f"  - {keyword.title()}" for keyword in keywords])

        content = f"""
---
title: "{self.title}"
date: {jekyll_date}
authors: [{self.authors}]
DOI: {self.DOI}
journal: "{self.journal}"
categories: 
{keywords}
---
{self.description}
            """

        content = content[1:]

        first_author = self.authors.split(" ")[1].split(",")[0].strip("'")
        file_title = f"{jekyll_date}-{first_author}.md"

        with open(destination + file_title, "w") as f:
            f.write(content)


@dataclass
class ConferenceAbstract:
    title: str
    authors: str
    publication_date: datetime
    conference: str
    description: str
    DOI: str

    event_start: datetime | None
    event_end: datetime | None
    event_location: str
    event_name: str

    def to_file(self, destination: str):
        # strip all strings of non-unicode characters
        self.title = self.title.encode('ascii', 'ignore').decode('utf-8')
        self.authors = self.authors.encode('ascii', 'ignore').decode('utf-8')
        self.description = self.description.encode('ascii', 'ignore').decode('utf-8')
        self.conference = self.conference.encode('ascii', 'ignore').decode('utf-8')
        self.event_location = self.event_location.encode('ascii', 'ignore').decode('utf-8')
        self.event_name = self.event_name.encode('ascii', 'ignore').decode('utf-8')

        from keyword_matcher import extract_keywords

        jekyll_date = self.publication_date.strftime("%Y-%m-%d")
        keywords = extract_keywords(self.title, self.description)
        keywords = "\n".join([f"  - {keyword.title()}" for keyword in keywords])

        if self.event_start and self.event_end:
            conference_dates = f"{self.event_start.strftime('%B %d')} - {self.event_end.strftime('%d, %Y')}"
        else:
            conference_dates = ""

        content = f"""
---
title: "{self.title}"
date: {jekyll_date}
conference_dates: {conference_dates}
conference: {self.event_name}
link: {self.DOI}
location: {self.event_location}
misc:  
categories: 
{keywords}
---
{self.description}
                    """

        content = content[1:]

        first_author = self.authors.split(" ")[1].split(",")[0].strip("'")
        file_title = f"{jekyll_date}-{first_author}.md"

        with open(destination + file_title, "w") as f:
            f.write(content)


@dataclass
class ConferencePaper:
    title: str
    DOI: str
    authors: str
    publication_date: datetime
    description: str
    journal: str
    subtitle: str

    def to_file(self, destination: str):
        # strip all strings of non-unicode characters
        self.title = self.title.encode('ascii', 'ignore').decode('utf-8')
        self.authors = self.authors.encode('ascii', 'ignore').decode('utf-8')
        self.journal = self.journal.encode('ascii', 'ignore').decode('utf-8')
        self.description = self.description.encode('ascii', 'ignore').decode('utf-8')
        self.subtitle = self.subtitle.encode('ascii', 'ignore').decode('utf-8')

        from keyword_matcher import extract_keywords

        jekyll_date = self.publication_date.strftime("%Y-%m-%d")
        keywords = extract_keywords(self.title, self.description)
        keywords = "\n".join([f"  - {keyword.title()}" for keyword in keywords])

        content = f"""
---
title: "{self.title}"
date: {jekyll_date}
authors: [{self.authors}]
conference: "{self.journal}"
categories:
{keywords}
---
{self.description}
        """

        content = content[1:]

        first_author = self.authors.split(" ")[1].split(",")[0].strip("'")
        file_title = f"{jekyll_date}-{first_author}.md"

        with open(destination + file_title, "w") as f:
            f.write(content)


@dataclass
class Book:
    publication_date: datetime
    DOI: str
    title: str
    container_title: str
    subtitle: str
    authors: str


def date_parts_to_datetime(parts):

    match len(parts):
        case 1:
            return datetime(year=parts[0], month=1, day=1)
        case 2:
            return datetime(year=parts[0], month=parts[1], day=1)
        case 3:
            return datetime(parts[0], parts[1], parts[2])
        case _:
            return None
