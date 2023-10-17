from sqlalchemy import Column, ForeignKey, Integer, Text

from .common_model import CommonModel


class Donation(CommonModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
