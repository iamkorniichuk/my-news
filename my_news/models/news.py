from .base import BaseModel


class NewsModel(BaseModel):
    def __init__(self):
        super().__init__('news', 'id')


news_model = NewsModel()
