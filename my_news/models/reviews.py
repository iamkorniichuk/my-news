from .base import BaseModel


class ReviewsModel(BaseModel):
    def __init__(self):
        super().__init__('reviews', 'id')


reviews_model = ReviewsModel()
