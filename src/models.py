from datetime import datetime
from .exc import NewsError
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine


class NewsSource(str, Enum):
    apnews = "apnews"
    aljazeera = "aljazeera"
    middleeasteye = "middleeasteye"
    reuters = "reuters"
    bloomberg = "bloomberg"
    politico = "politico"

    @staticmethod
    def get_news(news_url: str):
        if NewsSource.apnews.value in news_url:
            return NewsSource.apnews
        elif NewsSource.aljazeera.value in news_url:
            return NewsSource.aljazeera
        elif NewsSource.middleeasteye.value in news_url:
            return NewsSource.middleeasteye
        elif NewsSource.reuters.value in news_url:
            return NewsSource.reuters
        elif NewsSource.bloomberg.value in news_url:
            return NewsSource.bloomberg
        elif NewsSource.politico.value in news_url:
            return NewsSource.politico
        else:
            raise NewsError("Invalid news source")


class NewsModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    url: str = Field(unique=True)
    writer: str
    date: datetime
    content: str
    img_url: str


engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)
