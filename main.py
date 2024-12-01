import sys
from src.models import NewsSource
from src.utils import get_html_content, insert_data_to_db
import unittest
# import circular error modul A n modul B
# TODO -> implement saving data, maybe onto json/ ke database -> impelement gambar grabber / downloader


def run_test():
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
        case NewsSource.polico:
            model = soup.scrape_politico()
    insert_data_to_db(model)
    print(model)


if __name__ == "__main__":
    main()
