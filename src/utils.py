from curl_cffi import requests
from .soup import Soup
from .models import NewsModel, Session, engine
from sqlmodel import select
from PIL import Image
from io import BytesIO
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


def download_and_convert_to_jpeg(image_url: str, filename: str):
    try:
        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()  # Check for HTTP errors
        # Open the image using PIL
        image = Image.open(BytesIO(response.content))
        # Convert the image to RGB (JPEG doesn't support transparency)
        if image.mode in ("RGBA", "P"):  # Convert if the image has alpha channel
            image = image.convert("RGB")
        # Save the image as JPEG
        filename = f"{filename}.jpg"
        image.save(filename, format="JPEG")
        print(f"Image saved as JPEG to {filename}")
    except Exception as e:
        print(f"Error: {e}")
