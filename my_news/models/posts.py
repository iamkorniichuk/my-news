from .base import BaseModel
from hashlib import sha512


class PostsModel(BaseModel):
    def __init__(self):
        super().__init__('posts', 'id')


posts_model = PostsModel()
