from bs4 import BeautifulSoup
from .models import NewsModel

import re
from datetime import datetime
# Ketika kita scrape, jenis berita gk cuman dari satu web


def process_published_date(text: str):
    pattern = r"Published date:\s*(\d{1,2} \w+ \d{4} \d{2}:\d{2} \w+)"
    match = re.search(pattern, text)
    if match:
        date_string = match.group(1)
        print("Extracted date string:", date_string)
        # Convert the extracted date string into a datetime object
        datetime_obj = datetime.strptime(
            date_string, "%d %B %Y %H:%M %Z"
        )  # TODO -> get rid of hour, minute, seconds
        return datetime_obj


class Soup(BeautifulSoup):
    def __init__(self, html: bytes, url: str):
        super().__init__(html, "html.parser")
        self.url = url

    def scrape_middle_east_eye(self) -> NewsModel:
        title = self.find("span", class_="field field-title")
        if title is not None:
            title = title.get_text()
        author = self.find("a", class_="author-name")
        if author is not None:
            author = author.get_text()
        published_date = self.find("div", class_="submitted-date")
        if published_date is not None:
            published_date = process_published_date(
                published_date.get_text().lstrip())
        content = self.find("div", class_="field field-body clearfix")
        if content is not None:
            output = ""
            text_paragraphs: list[BeautifulSoup] = content.find_all("p")
            # [p1, p2, p3, ...]
            for p in text_paragraphs:
                output += p.get_text() + "\n"
        img_url = self.find("picture").source["srcset"].replace(" 1x", "")
        img_url = f"https://www.middleeasteye.net{img_url}"
        model = NewsModel(
            title=title,
            url=self.url,
            writer=author,
            date=published_date,
            content=output,
            img_url=img_url
        )
        return model

    def scrape_aljazeera(self) -> NewsModel:
        title = self.find("header", class_="article-header").h1.get_text()
        date = self.find(
            "div", class_="date-simple").find("span", {"aria-hidden": "true"}).get_text()
        date = datetime.strptime(date, "%d %b %Y")
        content = self.find("div", {"aria-live": "polite"}).find_all("p")
        output = ""
        for p in content:
            output += p.get_text() + "\n"
        img_url = self.find("div", class_="responsive-image").img["src"]
        img_url = f"https://www.aljazeera.com{img_url}"
        return NewsModel(
            title=title,
            url=self.url,
            writer="Al Jazeera",
            date=date,
            content=output,
            img_url=img_url
        )

    def scrape_associated_press(self) -> NewsModel:
        title = self.find("h1", class_="Page-headline").get_text()
        date = self.find(
            "bsp-timestamp", {"data-timestamp": True})["data-timestamp"]
        date = int(date) / 1000
        date = datetime.fromtimestamp(date)
        writer = self.find("div", class_="Page-authors").a.get_text().title()
        content = self.find(
            "div", class_="RichTextStoryBody RichTextBody").find_all("p")
        output = ""
        for p in content:
            output += p.get_text() + "\n"
        img_url = self.find("figure", class_="Figure").find(
            "source")["srcset"].replace(" 1x", "")
        print(img_url)
# ["srcset"]
        return NewsModel(
            title=title,
            url=self.url,
            writer=writer,
            date=date,
            content=output,
            img_url=img_url
        )

    def scrape_reuters(self) -> NewsModel:
        title = self.find("span", {"headline": True})['headline']
        writer = self.find("a", rel="author").get_text()
        date = self.find("time", {"datetime": True})["datetime"]
        date = date.replace("Z", "+00:00")
        date = datetime.fromisoformat(date)
        contents = self.find("div", {"data-testid": "ArticleBody"})
        contents: list[BeautifulSoup] = self.find_all(
            "div", {"data-testid": True})
        paragraphs: list[BeautifulSoup] = []
        for c in contents:
            x = c.get("data-testid")
            if "paragraph" in x:
                paragraphs.append(c)
        paragraphs = [p.get_text() for p in paragraphs]
        paragraphs = "\n".join(paragraphs)
        img_url = self.find("div", {"data-testid": "Image"}).img["src"]
        return NewsModel(
            title=title,
            url=self.url,
            writer=writer,
            date=date,
            content=paragraphs,
            img_url=img_url
        )

    def scrape_politico(self) -> NewsModel:
        title = self.find("h1", class_="headline").get_text().lstrip()
        writer = self.find("p", class_="story-meta__authors").a.get_text()
        date = self.find("time", {"datetime": True})["datetime"]
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        contents: list[BeautifulSoup] = self.find_all(
            "p", class_="story-text__paragraph")
        contents = "\n".join([c.get_text() for c in contents])
        img_url = self.find("picture").source["srcset"].split(" 1x")[0]
        return NewsModel(title=title, writer=writer, date=date, url=self.url, content=contents, img_url=img_url)

    def scrape_bloomberg(self) -> NewsModel:
        title = self.find("div", class_="hed-and-dek").get_text()
        writer = self.find("meta", {"name": re.compile(r"author")})["content"]
        date = self.find("time", {"datetime": True})["datetime"]
        date = date.replace("Z", "+00:00")
        date = datetime.fromisoformat(date)
        contents: list[BeautifulSoup] = self.find_all(
            "p", {"data-component": "paragraph"})
        contents = [c.get_text() for c in contents]
        contents = "\n".join(contents)
        img_url = self.find("img", class_="ui-image low-res-img")["src"]
        return NewsModel(title=title, writer=writer, date=date, url=self.url, content=contents, img_url=img_url)
