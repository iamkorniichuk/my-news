from .base import BaseModel


class PostsModel(BaseModel):
    def __init__(self):
        super().__init__('posts', 'id')


    def getall(self, **kwargs):
        posts = super().getall(**kwargs)
        return self._cut_posts_body(posts)


    def _cut_posts_body(self, posts):
        for post in posts:
            post['body'] = post['body'][:post['body'].rindex('.', 0, 100)]+'...'
        return posts


posts_model = PostsModel()
