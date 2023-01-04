from .base import BaseModel
from my_news.utils.files import news_folder


class NewsModel(BaseModel):
    def __init__(self):
        super().__init__('news', 'id', folder=news_folder)
