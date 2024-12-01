from curl_cffi import requests
from .soup import Soup
from .models import NewsModel, Session, engine
from sqlmodel import select
from .exc import NewsAlreadyInDBError


def insert_data_to_db(data: NewsModel):
    with Session(engine) as session:
        session.add(data)
        session.commit()


def get_html_content(url: str) -> Soup:
    # if newssource not in db, then continue, else raise Error (data already in database)
    with Session(engine) as session:
        statement = select(NewsModel).where(NewsModel.url == url)
        result = session.exec(statement).first()
        if result:
            raise NewsAlreadyInDBError
    response = requests.get(url, impersonate="edge")
    return Soup(response.content, url)
