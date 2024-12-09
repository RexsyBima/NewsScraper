import sys
import json
from src.models import NewsSource
from src.utils import get_html_content, download_and_convert_to_jpeg
import unittest

# TODO -> implement saving data, maybe onto json/ ke database -> impelement gambar grabber / downloader


def run_test():
    from src.testings import TestScraper
    unittest.main()


def main():
    url = sys.argv[1]  # -> CLI tool -> Command Line Interface tool
    soup = get_html_content(url)
    news_kind = NewsSource.get_news(url)
    match news_kind:
        case NewsSource.apnews:
            model = soup.scrape_associated_press()
        case NewsSource.aljazeera:
            model = soup.scrape_aljazeera()
        case NewsSource.middleeasteye:
            model = soup.scrape_middle_east_eye()
        case NewsSource.reuters:
            model = soup.scrape_reuters()
        case NewsSource.bloomberg:
            model = soup.scrape_bloomberg()
        case NewsSource.politico:
            model = soup.scrape_politico()

    # insert_data_to_db(model)
    download_and_convert_to_jpeg(model.img_url, model.title)
    with open("output.json", "w") as f:
        model.date = str(model.date)
        json.dump(model.model_dump(), f)
        print(f"news {model.title} has been saved into json and db")


if __name__ == "__main__":
    main()
