from .base import BaseModel


class CommentsModel(BaseModel):
    def __init__(self):
        super().__init__('comments', 'id')
