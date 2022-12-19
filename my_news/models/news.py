from .base import BaseModel


class NewsModel(BaseModel):
    def __init__(self):
        super().__init__('news', 'id')


    def getall(self, order=None, **kwargs):
        news = super().getall(order, **kwargs)
        return self._cut_news_body(news)


    def _cut_news_body(self, news):
        for one_news in news:
            try:
                last_index = one_news['body'].rindex('.', 0, 100)
            except ValueError or IndexError:
                last_index = 100
            one_news['body'] = one_news['body'][:last_index] + '...'
        return news


news_model = NewsModel()
